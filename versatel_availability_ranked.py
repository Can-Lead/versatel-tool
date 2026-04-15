from __future__ import annotations

import csv
import json
import sqlite3
import time
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Any, Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import re

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

from datacentermap_scraper import (
    request_cancel,
    reset_cancel,
    is_cancel_requested,
    raise_if_cancel_requested,
    ScrapeCancelled,
    sleep_with_cancel,
    clean,
    safe_text,
)

BASE_URL = "https://preview.versatel.psp.infrafin.net/map"
DEFAULT_STATE_FILE = "versatel_state.json"
DEFAULT_DB_FILE = "versatel_availability.sqlite"

HEADLESS = False
SLOW_MO_MS = 00
PAGE_TIMEOUT_MS = 15000
REQUEST_DELAY_MS = 1200


class LoginRequired(Exception):
    pass


@dataclass
class AddressInput:
    row_index: int
    original_row: Dict[str, Any]
    street: str
    house_number: str
    postal_code: str
    city: str
    external_id: str = ""


@dataclass
class AvailabilityMatch:
    rank: int
    type: str
    label: str


@dataclass
class AvailabilityResult:
    row_index: int
    external_id: str
    street: str
    house_number: str
    postal_code: str
    city: str
    status: str
    detail_type: str
    availability_text: str
    source_url: str
    checked_at: str
    error: str = ""
    raw_payload: str = ""
    matches: List[Dict[str, Any]] = field(default_factory=list)


class AvailabilityStorage:
    def __init__(self, db_path: str = DEFAULT_DB_FILE):
        self.db_path = str(db_path)
        self._init_db()

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        return conn

    def _init_db(self):
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS availability_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    row_index INTEGER,
                    external_id TEXT,
                    street TEXT,
                    house_number TEXT,
                    postal_code TEXT,
                    city TEXT,
                    status TEXT,
                    detail_type TEXT,
                    availability_text TEXT,
                    source_url TEXT,
                    checked_at TEXT,
                    error TEXT,
                    raw_payload TEXT,
                    matches_json TEXT DEFAULT '[]'
                )
                """
            )
            conn.commit()

            columns = [row[1] for row in conn.execute("PRAGMA table_info(availability_results)").fetchall()]
            if "detail_type" not in columns:
                conn.execute("ALTER TABLE availability_results ADD COLUMN detail_type TEXT DEFAULT ''")
                conn.commit()
            if "matches_json" not in columns:
                conn.execute("ALTER TABLE availability_results ADD COLUMN matches_json TEXT DEFAULT '[]'")
                conn.commit()

    def save_result(self, result: AvailabilityResult):
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO availability_results (
                    row_index, external_id, street, house_number, postal_code, city,
                    status, detail_type, availability_text, source_url, checked_at, error, raw_payload, matches_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    result.row_index,
                    result.external_id,
                    result.street,
                    result.house_number,
                    result.postal_code,
                    result.city,
                    result.status,
                    result.detail_type,
                    result.availability_text,
                    result.source_url,
                    result.checked_at,
                    result.error,
                    result.raw_payload,
                    json.dumps(result.matches, ensure_ascii=False),
                ),
            )
            conn.commit()

    def export_csv(self, outfile: str):
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT row_index, external_id, street, house_number, postal_code, city,
                       status, detail_type, availability_text, source_url, checked_at, error, raw_payload, matches_json
                FROM availability_results
                ORDER BY id
                """
            ).fetchall()

        headers = [
            "row_index",
            "external_id",
            "street",
            "house_number",
            "postal_code",
            "city",
            "status",
            "detail_type",
            "availability_text",
            "source_url",
            "checked_at",
            "error",
            "raw_payload",
            "matches_json",
        ]

        with open(outfile, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(headers)
            writer.writerows(rows)


class VersatelAvailabilityBot:
    MATCH_PRIORITY = {
        "onnet": 1,
        "buildings_passed": 2,
        "telekom_vorleistung": 3,
        "nearnet": 4,
        "offnet": 5,
        "other": 6,
    }

    MATCH_LABELS = {
        "onnet": "Onnet",
        "buildings_passed": "Buildings Passed",
        "telekom_vorleistung": "Telekom Vorleistung",
        "nearnet": "Nearnet",
        "offnet": "Offnet",
        "other": "Sonstiges",
    }

    def __init__(
        self,
        state_file: str = DEFAULT_STATE_FILE,
        headless: bool = HEADLESS,
        timeout_ms: int = PAGE_TIMEOUT_MS,
        load_state: bool = True,
    ):
        self.state_file = str(state_file)
        self.headless = headless
        self.timeout_ms = timeout_ms
        self.load_state = load_state

        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def start(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            slow_mo=SLOW_MO_MS,
            args=[
                "--deny-permission-prompts",
            ],
        )

        state_path = Path(self.state_file).resolve()
        self.state_file = str(state_path)

        context_kwargs = {
            "ignore_https_errors": True,
            "locale": "de-DE",
        }

        if self.load_state and state_path.exists():
            context_kwargs["storage_state"] = str(state_path)
            print(f"[VERSATEL] Lade storage_state aus: {state_path}")
        else:
            print(f"[VERSATEL] Kein storage_state geladen: {state_path}")

        self.context = self.browser.new_context(**context_kwargs)

        self.context.add_init_script("""
            Object.defineProperty(navigator, 'geolocation', {
                value: {
                    getCurrentPosition: function(success, error) {
                        if (error) {
                            error({
                                code: 1,
                                message: 'Geolocation blocked by automation'
                            });
                        }
                    },
                    watchPosition: function(success, error) {
                        if (error) {
                            error({
                                code: 1,
                                message: 'Geolocation blocked by automation'
                            });
                        }
                        return 0;
                    },
                    clearWatch: function() {}
                },
                configurable: true
            });
        """)

        self.page = self.context.new_page()
        self.page.set_default_timeout(self.timeout_ms)

    def stop(self):
        try:
            if self.context:
                self.context.close()
        except Exception:
            pass

        try:
            if self.browser:
                self.browser.close()
        except Exception:
            pass

        try:
            if self.playwright:
                self.playwright.stop()
        except Exception:
            pass

    def save_state(self):
        if not self.context:
            return

        state_path = Path(self.state_file).resolve()
        state_path.parent.mkdir(parents=True, exist_ok=True)
        self.context.storage_state(path=str(state_path))
        self.state_file = str(state_path)

    def open_map(self):
        raise_if_cancel_requested()
        self.page.goto(BASE_URL, wait_until="domcontentloaded", timeout=self.timeout_ms)
        sleep_with_cancel(self.page, 600)
        self._dismiss_location_prompt()
        sleep_with_cancel(self.page, 200)

    def _has_session_data(self) -> bool:
        try:
            cookies = self.context.cookies([BASE_URL]) if self.context else []
            if cookies:
                return True
        except Exception:
            pass

        try:
            state = self.context.storage_state() if self.context else {}
            if state.get("cookies"):
                return True
            origins = state.get("origins", [])
            if origins:
                return True
        except Exception:
            pass

        return False

    def _dismiss_location_prompt(self):
        if not self.page:
            return

        try:
            sleep_with_cancel(self.page, 200)
        except Exception:
            pass

    def ensure_logged_in(self):
        message = (
            "Keine gültige Versatel-Session gefunden. "
            "Bitte /api/versatel/login ausführen und im sichtbaren Browser manuell einloggen."
        )

        if not self.page or self.page.is_closed():
            raise LoginRequired(message)

        state_path = Path(self.state_file).resolve()
        if not state_path.exists():
            raise LoginRequired(f"{message} State-Datei fehlt: {state_path}")

        if not self._has_session_data():
            raise LoginRequired(f"{message} Es wurden keine Session-Daten geladen.")

        try:
            self.open_map()
        except Exception as e:
            raise LoginRequired(f"{message} Map konnte nicht geöffnet werden: {e}")

        for _ in range(5):
            try:
                current_url = (self.page.url or "").lower()
            except Exception:
                current_url = ""

            if any(x in current_url for x in ["login", "oauth", "sso", "signin", "auth"]):
                raise LoginRequired(f"{message} Versatel hat auf die Login-Seite umgeleitet.")

            if self._is_logged_in():
                return

            sleep_with_cancel(self.page, 1000)

        raise LoginRequired(f"{message} Session-Datei vorhanden, aber UI wurde nicht als eingeloggt erkannt.")

    def login_with_credentials(self, username: str, password: str, wait_seconds: int = 60):
        if not self.page or self.page.is_closed():
            raise LoginRequired("Browser-Seite für Versatel-Login ist nicht verfügbar.")

        self.open_map()

        deadline = time.time() + wait_seconds
        last_error = ""

        user_selectors = [
            "input[name='username']",
            "input[type='email']",
            "input[name='email']",
            "input[id*='user']",
            "input[id*='email']",
            "input[placeholder*='E-Mail']",
            "input[placeholder*='Benutzer']",
        ]

        pass_selectors = [
            "input[name='password']",
            "input[type='password']",
            "input[id*='pass']",
            "input[placeholder*='Passwort']",
        ]

        submit_selectors = [
            "button[type='submit']",
            "input[type='submit']",
            "button:has-text('Anmelden')",
            "button:has-text('Login')",
            "button:has-text('Weiter')",
        ]

        while time.time() < deadline:
            raise_if_cancel_requested()

            try:
                if self._is_logged_in():
                    self.save_state()
                    return {
                        "status": "ok",
                        "state_file": self.state_file,
                        "message": f"Versatel-Session erfolgreich gespeichert: {self.state_file}"
                    }
            except Exception:
                pass

            try:
                user_field = None
                for selector in user_selectors:
                    loc = self.page.locator(selector).first
                    if loc.count() > 0:
                        user_field = loc
                        break

                pass_field = None
                for selector in pass_selectors:
                    loc = self.page.locator(selector).first
                    if loc.count() > 0:
                        pass_field = loc
                        break

                if user_field and pass_field:
                    user_field.fill("")
                    user_field.fill(username)
                    sleep_with_cancel(self.page, 150)

                    pass_field.fill("")
                    pass_field.fill(password)
                    sleep_with_cancel(self.page, 150)

                    clicked = False
                    for selector in submit_selectors:
                        btn = self.page.locator(selector).first
                        if btn.count() > 0:
                            btn.click(timeout=2000)
                            clicked = True
                            break

                    if not clicked:
                        pass_field.press("Enter")

                    sleep_with_cancel(self.page, 1500)

                    if self._is_logged_in():
                        self.save_state()
                        return {
                            "status": "ok",
                            "state_file": self.state_file,
                            "message": f"Versatel-Session erfolgreich gespeichert: {self.state_file}"
                        }
            except Exception as e:
                last_error = str(e)

            sleep_with_cancel(self.page, 1000)

        raise LoginRequired(f"Automatischer Login fehlgeschlagen. Letzter Fehler: {last_error or 'Login-Formular nicht erkannt'}")

    def interactive_login(self, wait_seconds: int = 180):
        print("[VERSATEL] Bitte jetzt manuell im geöffneten Browser einloggen ...")

        deadline = time.time() + wait_seconds
        while time.time() < deadline:
            raise_if_cancel_requested()

            if not self.page:
                raise ScrapeCancelled("Login abgebrochen: Seite nicht mehr verfügbar")

            try:
                if self.page.is_closed():
                    raise ScrapeCancelled("Login abgebrochen: Browser/Fenster wurde geschlossen")
            except Exception:
                raise ScrapeCancelled("Login abgebrochen: Browser/Fenster wurde geschlossen")

            try:
                current_url = self.page.url or ""
            except Exception:
                current_url = ""

            print(f"[VERSATEL LOGIN] aktuelle URL: {current_url}")

            try:
                if self._is_logged_in():
                    self.save_state()
                    print(f"[VERSATEL] Session gespeichert in {self.state_file}")
                    return {
                        "status": "ok",
                        "state_file": self.state_file,
                        "message": f"Versatel-Session erfolgreich gespeichert: {self.state_file}"
                    }
            except ScrapeCancelled:
                raise
            except Exception as e:
                print(f"[VERSATEL LOGIN] _is_logged_in Fehler: {e}")

            try:
                sleep_with_cancel(self.page, 1000)
            except ScrapeCancelled:
                raise
            except Exception:
                raise ScrapeCancelled("Login abgebrochen: Browser/Fenster wurde geschlossen")

        raise LoginRequired("Login wurde nicht innerhalb des Zeitfensters abgeschlossen.")

    def _is_logged_in(self) -> bool:
        if not self.page:
            return False

        try:
            current_url = (self.page.url or "").lower()
        except Exception:
            current_url = ""

        blocked_markers = ["login", "oauth", "sso", "signin", "auth"]
        if any(marker in current_url for marker in blocked_markers):
            return False

        if not self._has_session_data():
            return False

        positive_checks = [
            lambda: "versatel.psp.infrafin.net/map" in current_url,
            lambda: self.page.locator("input[placeholder*='Adresse']").count() > 0,
            lambda: self.page.locator("text=Adresse").count() > 0,
            lambda: self.page.locator("button:has-text('Verfügbarkeit')").count() > 0,
        ]

        hits = 0
        for check in positive_checks:
            try:
                if check():
                    hits += 1
            except Exception:
                continue

        return hits >= 1

    def _normalize_street_for_search(self, street: str) -> str:
        text = clean(street)

        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"\bstr\.\b", "straße", text, flags=re.IGNORECASE)
        text = re.sub(r"\bstr\b", "straße", text, flags=re.IGNORECASE)

        text = re.sub(r",?\s*\b(büro|büro-nr\.?|treppenhaus)\b.*$", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s*/\s*\d+\s*\.?\s*(og|obergeschoss)\b.*$", "", text, flags=re.IGNORECASE)
        text = re.sub(r",?\s*\d+\s*\.?\s*(og|obergeschoss)\b.*$", "", text, flags=re.IGNORECASE)
        text = re.sub(r",?\s*\b\d+\s*\.?\s*etage\b.*$", "", text, flags=re.IGNORECASE)

        text = re.sub(r"(\d)\s+([A-Za-z])\b", r"\1\2", text)

        return clean(text)

    def _normalize_postal_code_for_search(self, postal_code: str) -> str:
        digits = re.sub(r"\D", "", str(postal_code or ""))
        if len(digits) == 4:
            return digits.zfill(5)
        return digits[:5] if len(digits) >= 5 else digits

    def _normalize_city_for_search(self, city: str) -> str:
        return clean(re.sub(r"\s+", " ", str(city or "")))

    def _build_search_variants(self, row: AddressInput) -> List[str]:
        street = self._normalize_street_for_search(row.street)
        house_number = clean(str(row.house_number or ""))
        postal_code = self._normalize_postal_code_for_search(row.postal_code)
        city = self._normalize_city_for_search(row.city)

        left = clean(f"{street} {house_number}")
        right = clean(f"{postal_code} {city}")

        variants = []

        full_main = clean(f"{left}, {right}")
        if full_main:
            variants.append(full_main)

        if street and postal_code and city:
            variants.append(clean(f"{street}, {postal_code} {city}"))

        if left and city:
            variants.append(clean(f"{left}, {city}"))

        if street and city:
            variants.append(clean(f"{street}, {city}"))

        deduped = []
        seen = set()
        for item in variants:
            key = item.lower()
            if item and key not in seen:
                deduped.append(item)
                seen.add(key)

        return deduped

    def _full_address(self, row: AddressInput) -> str:
        variants = self._build_search_variants(row)
        return variants[0] if variants else ""

    def _find_address_field(self):
        candidates = [
            lambda: self.page.get_by_label("Adresse", exact=False),
            lambda: self.page.get_by_placeholder("Adresse", exact=False),
            lambda: self.page.locator("input[placeholder*='Adresse']").first,
            lambda: self.page.locator("input[type='text']").first,
        ]

        for factory in candidates:
            try:
                locator = factory()
                locator.wait_for(timeout=1500)
                return locator
            except Exception:
                continue
        return None

    def _fill_address(self, full_address: str) -> str:
        field = self._find_address_field()
        if field is None:
            try:
                self.open_map()
            except Exception:
                pass

            field = self._find_address_field()
            if field is None:
                return "failed"

        try:
            self._dismiss_location_prompt()
            sleep_with_cancel(self.page, 120)

            field.click(timeout=2000)
            try:
                field.fill("")
            except Exception:
                pass

            try:
                field.press("Control+A")
                field.press("Delete")
            except Exception:
                pass

            field.fill(full_address)
            sleep_with_cancel(self.page, 350)

            suggestion_selectors = [
                "[role='listbox'] [role='option']",
                "[role='option']",
                ".autocomplete-option",
                ".suggestion",
                ".pac-item",
            ]

            def _popup_with_pruefen_visible() -> bool:
                selectors = [
                    "button:has-text('PRÜFEN')",
                    "button:has-text('Prüfen')",
                    "[role='button']:has-text('PRÜFEN')",
                    "[role='button']:has-text('Prüfen')",
                ]

                for sel in selectors:
                    try:
                        loc = self.page.locator(sel)
                        if loc.count() > 0 and loc.first.is_visible():
                            return True
                    except Exception:
                        continue

                return False

            for selector in suggestion_selectors:
                try:
                    loc = self.page.locator(selector)
                    count = min(loc.count(), 5)

                    for i in range(count):
                        try:
                            item = loc.nth(i)
                            if not item.is_visible():
                                continue

                            txt = clean(item.inner_text())
                            if not txt:
                                continue

                            print(f"[VERSATEL] Autocomplete-Kandidat {i+1}: {txt}")

                            item.click(timeout=1200)
                            sleep_with_cancel(self.page, 1200)

                            try:
                                current_value = field.input_value()
                            except Exception:
                                current_value = ""

                            print(f"[VERSATEL] Vorschlag per Klick gewählt. Feldwert jetzt: {current_value!r}")

                            if clean(current_value):
                                return "selected_suggestion"

                            if _popup_with_pruefen_visible():
                                print("[VERSATEL] Prüf-Popup ist sichtbar -> Auswahl als erfolgreich gewertet.")
                                return "selected_suggestion"
                        except Exception:
                            continue
                except Exception:
                    continue

            try:
                self.page.keyboard.press("ArrowDown")
                sleep_with_cancel(self.page, 350)
                self.page.keyboard.press("Enter")
                sleep_with_cancel(self.page, 1200)

                try:
                    current_value = field.input_value()
                except Exception:
                    current_value = ""

                print(f"[VERSATEL] Ersten Vorschlag per Tastatur gewählt. Feldwert jetzt: {current_value!r}")

                if clean(current_value):
                    return "selected_suggestion"

                if _popup_with_pruefen_visible():
                    print("[VERSATEL] Prüf-Popup ist nach Tastaturauswahl sichtbar -> Auswahl als erfolgreich gewertet.")
                    return "selected_suggestion"
            except Exception:
                pass

            try:
                current_value = field.input_value()
            except Exception:
                current_value = ""

            print(f"[VERSATEL] Kein Vorschlag gewählt. Feldwert bleibt: {current_value!r}")
            if not clean(current_value) and not _popup_with_pruefen_visible():
                return "failed"
            return "filled_only"
        except Exception:
            return "failed"

    def _trigger_search(self) -> bool:
        self._dismiss_location_prompt()

        selectors = [
            "button:has-text('PRÜFEN')",
            "button:has-text('Prüfen')",
            "[role='button']:has-text('PRÜFEN')",
            "[role='button']:has-text('Prüfen')",
            "button:has-text('Suchen')",
            "[role='button']:has-text('Suchen')",
            "button:has-text('Verfügbarkeit prüfen')",
            "[role='button']:has-text('Verfügbarkeit prüfen')",
            "button[type='submit']",
        ]

        end_time = time.time() + 8
        while time.time() < end_time:
            for selector in selectors:
                try:
                    loc = self.page.locator(selector)
                    count = min(loc.count(), 5)

                    for i in range(count):
                        try:
                            btn = loc.nth(i)
                            if not btn.is_visible():
                                continue

                            txt = clean(btn.inner_text())
                            print(f"[VERSATEL] Prüf-Button Kandidat: selector={selector} text={txt}")

                            try:
                                if btn.is_disabled():
                                    continue
                            except Exception:
                                pass

                            try:
                                btn.scroll_into_view_if_needed(timeout=1000)
                            except Exception:
                                pass

                            try:
                                print(f"[VERSATEL] Klicke jetzt auf Prüf-Button: {txt}")
                                btn.click(timeout=1500)
                                sleep_with_cancel(self.page, 300)
                                return True
                            except Exception:
                                pass

                            try:
                                print(f"[VERSATEL] Klicke jetzt per force auf Prüf-Button: {txt}")
                                btn.click(timeout=1500, force=True)
                                sleep_with_cancel(self.page, 300)
                                return True
                            except Exception:
                                pass

                            try:
                                print(f"[VERSATEL] Klicke jetzt per JS auf Prüf-Button: {txt}")
                                btn.evaluate("(node) => node.click()")
                                sleep_with_cancel(self.page, 300)
                                return True
                            except Exception:
                                pass

                        except Exception:
                            continue
                except Exception:
                    continue

            sleep_with_cancel(self.page, 100)

        return False

    def _open_availability_result(self) -> bool:
        search_selectors = [
            "button:has-text('Verfügbarkeit')",
            "[role='button']:has-text('Verfügbarkeit')",
            "a:has-text('Verfügbarkeit')",
            "[role='tab']:has-text('Verfügbarkeit')",
            "button:has-text('Verfügbarkeit prüfen')",
            "[role='button']:has-text('Verfügbarkeit prüfen')",
            "text=/.*Verfügbarkeit.*/i",
        ]

        result_indicators = [
            "text=/.*Telekom.*/i",
            "text=/.*Vorleistung.*/i",
            "text=/.*onnet.*/i",
            "text=/.*on-net.*/i",
            "text=/.*nearnet.*/i",
            "text=/.*near-net.*/i",
            "text=/.*nicht verfügbar.*/i",
            "text=/.*verfügbar.*/i",
            "text=/.*Glasfaser.*/i",
            "text=/.*FTTH.*/i",
            "text=/.*FTTB.*/i",
            "text=/.*VDSL.*/i",
            "text=/.*ADSL.*/i",
            "text=/.*SDSL.*/i",
        ]

        end_time = time.time() + 12.0

        while time.time() < end_time:
            raise_if_cancel_requested()

            for selector in result_indicators:
                try:
                    loc = self.page.locator(selector)
                    if loc.count() > 0 and loc.first.is_visible():
                        print(f"[VERSATEL] Ergebnis bereits sichtbar: {selector}")
                        return True
                except Exception:
                    continue

            for selector in search_selectors:
                try:
                    loc = self.page.locator(selector)
                    count = min(loc.count(), 8)

                    for i in range(count):
                        try:
                            el = loc.nth(i)

                            if not el.is_visible():
                                continue

                            txt = clean(el.inner_text())
                            print(f"[VERSATEL] Kandidat gefunden: selector={selector} text={txt}")

                            try:
                                el.click(timeout=1500)
                                sleep_with_cancel(self.page, 800)
                                return True
                            except Exception:
                                pass

                            try:
                                el.click(timeout=1500, force=True)
                                sleep_with_cancel(self.page, 800)
                                return True
                            except Exception:
                                pass

                            try:
                                el.evaluate("(node) => node.click()")
                                sleep_with_cancel(self.page, 800)
                                return True
                            except Exception:
                                pass

                        except Exception:
                            continue
                except Exception:
                    continue

            try:
                snapshot = self._debug_visible_text_snapshot().lower()
                if any(x in snapshot for x in [
                    "telekom",
                    "vorleistung",
                    "onnet",
                    "on-net",
                    "nearnet",
                    "near-net",
                    "nicht verfügbar",
                    "verfügbar",
                    "glasfaser",
                    "ftth",
                    "fttb",
                    "vdsl",
                    "adsl",
                    "sdsl",
                ]):
                    print("[VERSATEL] Ergebnis über Snapshot erkannt, ohne zusätzlichen Klick.")
                    return True
            except Exception:
                pass

            sleep_with_cancel(self.page, 300)

        return False

    def _debug_visible_text_snapshot(self) -> str:
        try:
            body = self.page.locator("body").inner_text()
            lines = [clean(x) for x in str(body).splitlines() if clean(x)]
            return " | ".join(lines[:80])
        except Exception:
            return ""

    def _close_result_panel(self) -> bool:
        if not self.page:
            return False

        selectors = [
            "button[aria-label='Close']",
            "button[aria-label='Schließen']",
            ".gm-ui-hover-effect",
            "[role='dialog'] button",
            "button:has-text('Schließen')",
            "text='×'",
            "text='✕'",
        ]

        for selector in selectors:
            try:
                loc = self.page.locator(selector)
                count = min(loc.count(), 10)

                for i in range(count):
                    try:
                        el = loc.nth(i)
                        if not el.is_visible():
                            continue

                        txt = clean(el.inner_text())
                        aria = (el.get_attribute("aria-label") or "").strip().lower()
                        cls = (el.get_attribute("class") or "").strip().lower()

                        is_close_candidate = (
                            txt in ["", "×", "✕"]
                            or "close" in aria
                            or "schließen" in aria
                            or "gm-ui-hover-effect" in cls
                        )

                        if not is_close_candidate:
                            continue

                        try:
                            el.click(timeout=1200)
                            sleep_with_cancel(self.page, 300)
                            return True
                        except Exception:
                            pass

                        try:
                            el.click(timeout=1200, force=True)
                            sleep_with_cancel(self.page, 300)
                            return True
                        except Exception:
                            pass

                        try:
                            el.evaluate("(node) => node.click()")
                            sleep_with_cancel(self.page, 300)
                            return True
                        except Exception:
                            pass

                    except Exception:
                        continue
            except Exception:
                continue

        try:
            self.page.keyboard.press("Escape")
            sleep_with_cancel(self.page, 300)
            return True
        except Exception:
            return False

    def _looks_like_availability_result(self, text: str) -> bool:
        low = (text or "").lower()

        if not low.strip():
            return False

        return any(x in low for x in [
            "telekom",
            "vorleistung",
            "onnet",
            "on-net",
            "nearnet",
            "near-net",
            "offnet",
            "off-net",
            "nicht verfügbar",
            "verfügbar",
            "glasfaser",
            "ftth",
            "fttb",
            "business",
            "anschluss",
            "bandbreite",
            "produkt",
            "building passed",
            "buildings passed",
        ])

    def _classify_detail_type(self, availability_text: str, raw_payload_obj: Dict[str, Any]) -> str:
        low = (availability_text or "").lower()

        payload_text = ""
        try:
            payload_text = json.dumps(raw_payload_obj, ensure_ascii=False).lower()
        except Exception:
            payload_text = ""

        combined = f"{low} | {payload_text}"

        if any(x in combined for x in ["buildings passed", "building passed", "passed home", "homes passed"]):
            return "buildings_passed"

        if any(x in combined for x in [
            "telekom vorleistung",
            "vorleistung telekom",
            "telekom-wholesale",
            "telekom wholesale",
            "telekom vorleistung: regio",
            "regio",
            "bitstrom",
            "bsa",
            "layer 2",
            "l2-bsa",
        ]):
            return "telekom_vorleistung"

        if any(x in combined for x in [
            "onnet",
            "on-net",
            "on net",
            "onnet eigen",
            "im versatel netz",
            "eigenes netz",
            "eigene infrastruktur",
        ]):
            return "onnet"

        if any(x in combined for x in [
            "nearnet",
            "near-net",
            "near net",
            "netznah",
            "nahe am netz",
        ]):
            return "nearnet"

        if any(x in combined for x in ["offnet", "off-net", "off net"]):
            return "offnet"

        return ""

    def _extract_result_text(self) -> str:
        selectors = [
            "[role='dialog']",
            "[class*='dialog']",
            "[class*='modal']",
            "[class*='popover']",
            "[class*='drawer']",
            "[class*='sheet']",
            "[class*='result']",
            "[class*='availability']",
            "[class*='detail']",
            "[data-testid*='availability']",
            "[data-testid*='result']",
        ]

        collected = []

        for selector in selectors:
            try:
                loc = self.page.locator(selector)
                count = min(loc.count(), 10)

                for i in range(count):
                    try:
                        el = loc.nth(i)
                        if not el.is_visible():
                            continue

                        text = clean(el.inner_text())
                        if not text:
                            continue

                        if text not in collected:
                            collected.append(text)
                    except Exception:
                        continue
            except Exception:
                continue

        if collected:
            collected = sorted(collected, key=len, reverse=True)
            return " | ".join(collected[:10])

        try:
            body_text = self.page.locator("body").inner_text()
            lines = [clean(line) for line in str(body_text).splitlines() if clean(line)]
            if lines:
                return " | ".join(lines[:50])
        except Exception:
            pass

        return ""

    def _collect_match_types(self, availability_text: str, raw_payload_obj: Dict[str, Any]) -> List[str]:
        combined_parts = [availability_text or ""]

        try:
            combined_parts.append(json.dumps(raw_payload_obj, ensure_ascii=False))
        except Exception:
            pass

        combined = " | ".join(combined_parts).lower()

        found: List[str] = []

        def add(match_type: str):
            if match_type not in found:
                found.append(match_type)

        if any(x in combined for x in [
            "onnet",
            "on-net",
            "on net",
            "onnet eigen",
            "im versatel netz",
            "eigenes netz",
            "eigene infrastruktur",
        ]):
            add("onnet")

        if any(x in combined for x in [
            "buildings passed",
            "building passed",
            "passed home",
            "homes passed",
        ]):
            add("buildings_passed")

        if any(x in combined for x in [
            "telekom vorleistung",
            "vorleistung telekom",
            "telekom-wholesale",
            "telekom wholesale",
            "telekom vorleistung: regio",
            "regio",
            "bitstrom",
            "bsa",
            "layer 2",
            "l2-bsa",
        ]):
            add("telekom_vorleistung")

        if any(x in combined for x in [
            "nearnet",
            "near-net",
            "near net",
            "netznah",
            "nahe am netz",
        ]):
            add("nearnet")

        if any(x in combined for x in [
            "offnet",
            "off-net",
            "off net",
        ]):
            add("offnet")

        if not found and clean(combined):
            add("other")

        return found

    def _build_ranked_matches(self, availability_text: str, raw_payload_obj: Dict[str, Any]) -> List[Dict[str, Any]]:
        match_types = self._collect_match_types(availability_text, raw_payload_obj)

        sorted_types = sorted(
            match_types,
            key=lambda item: self.MATCH_PRIORITY.get(item, self.MATCH_PRIORITY["other"])
        )

        result: List[Dict[str, Any]] = []
        for idx, match_type in enumerate(sorted_types[:3], start=1):
            result.append({
                "rank": idx,
                "type": match_type,
                "label": self.MATCH_LABELS.get(match_type, self.MATCH_LABELS["other"]),
            })

        return result

    def login_and_check_address(
        self,
        row: AddressInput,
        username: str,
        password: str,
        login_wait_seconds: int = 60,
        post_login_delay_seconds: float = 3.0,
    ) -> AvailabilityResult:
        try:
            self.ensure_logged_in()
        except LoginRequired:
            self.login_with_credentials(
                username=username,
                password=password,
                wait_seconds=login_wait_seconds,
            )
            if post_login_delay_seconds > 0:
                time.sleep(post_login_delay_seconds)
            self.ensure_logged_in()

        return self.check_address(row)

    def check_address(self, row: AddressInput) -> AvailabilityResult:
        raise_if_cancel_requested()

        try:
            self._close_result_panel()
        except Exception:
            pass

        captured_json: List[Dict[str, Any]] = []

        def handle_response(response):
            try:
                content_type = (response.headers.get("content-type") or "").lower()
                if "application/json" not in content_type:
                    return

                url = (response.url or "").lower()
                if not any(key in url for key in ["address", "search", "availability", "coverage", "map"]):
                    return

                payload = response.json()
                captured_json.append({
                    "url": response.url,
                    "status": response.status,
                    "payload": payload,
                })
            except Exception:
                pass

        self.page.on("response", handle_response)

        try:
            full_address = self._full_address(row)
            print(f"[VERSATEL] Adresse: {full_address}")

            fill_result = self._fill_address(full_address)
            print(f"[VERSATEL] fill_result={fill_result}")

            if fill_result not in ["selected_suggestion", "filled_only"]:
                return AvailabilityResult(
                    row_index=row.row_index,
                    external_id=row.external_id,
                    street=row.street,
                    house_number=row.house_number,
                    postal_code=row.postal_code,
                    city=row.city,
                    status="ui_changed",
                    detail_type="",
                    availability_text="",
                    source_url=self.page.url,
                    checked_at=time.strftime("%Y-%m-%d %H:%M:%S"),
                    error="Adresse konnte nicht sicher übernommen werden",
                    raw_payload="",
                    matches=[],
                )

            print("[VERSATEL] Adressvorschlag gewählt, warte auf Button 'Prüfen' ...")
            sleep_with_cancel(self.page, 300)

            try:
                field = self._find_address_field()
                current_value = field.input_value() if field else ""
            except Exception:
                current_value = ""

            print(f"[VERSATEL] Feldwert vor _trigger_search: {current_value!r}")
            print("[VERSATEL] Starte _trigger_search unabhängig vom Feldwert ...")

            if not self._trigger_search():
                return AvailabilityResult(
                    row_index=row.row_index,
                    external_id=row.external_id,
                    street=row.street,
                    house_number=row.house_number,
                    postal_code=row.postal_code,
                    city=row.city,
                    status="ui_changed",
                    detail_type="",
                    availability_text="",
                    source_url=self.page.url,
                    checked_at=time.strftime("%Y-%m-%d %H:%M:%S"),
                    error="Button 'Prüfen' konnte nicht ausgelöst werden",
                    raw_payload="",
                    matches=[],
                )

            sleep_with_cancel(self.page, REQUEST_DELAY_MS)

            result_wait_end = time.time() + 15.0
            availability_text = ""
            debug_snapshot = ""

            while time.time() < result_wait_end:
                raise_if_cancel_requested()

                candidate_text = self._extract_result_text()
                if self._looks_like_availability_result(candidate_text):
                    availability_text = candidate_text[:4000]
                    break

                debug_snapshot = self._debug_visible_text_snapshot()
                if self._looks_like_availability_result(debug_snapshot):
                    availability_text = debug_snapshot[:4000]
                    break

                sleep_with_cancel(self.page, 400)

            if not availability_text:
                availability_opened = self._open_availability_result()

                if availability_opened:
                    second_wait_end = time.time() + 8.0
                    while time.time() < second_wait_end:
                        raise_if_cancel_requested()

                        candidate_text = self._extract_result_text()
                        if self._looks_like_availability_result(candidate_text):
                            availability_text = candidate_text[:4000]
                            break

                        debug_snapshot = self._debug_visible_text_snapshot()
                        if self._looks_like_availability_result(debug_snapshot):
                            availability_text = debug_snapshot[:4000]
                            break

                        sleep_with_cancel(self.page, 400)

            if not availability_text:
                debug_snapshot = self._debug_visible_text_snapshot()
                print("[VERSATEL] Kein Ergebnistext erkannt.")
                print("[VERSATEL] URL:", self.page.url)
                print("[VERSATEL] Sichtbarer Inhalt:", debug_snapshot[:1500] if debug_snapshot else "<leer>")

            raw_payload_obj = {
                "page_url": self.page.url,
                "captured_json": captured_json[-1] if captured_json else None,
            }

            if not availability_text:
                debug_snapshot = self._debug_visible_text_snapshot()
                raw_payload_obj["debug_snapshot"] = debug_snapshot
                if debug_snapshot:
                    availability_text = debug_snapshot[:4000]

            raw_payload = json.dumps(raw_payload_obj, ensure_ascii=False)

            low = (availability_text or "").lower()
            detail_type = self._classify_detail_type(availability_text, raw_payload_obj)
            matches = self._build_ranked_matches(availability_text, raw_payload_obj)

            if not availability_text:
                status = "no_result"
            elif detail_type in ["buildings_passed", "telekom_vorleistung", "onnet", "nearnet", "offnet"]:
                status = "available"
            elif "nicht verfügbar" in low:
                status = "not_available"
            elif (
                "verfügbar" in low
                or "ftth" in low
                or "fttb" in low
                or "glasfaser" in low
            ):
                status = "available"
            else:
                status = "ok"

            print("[VERSATEL] Adresse:", full_address)
            print("[VERSATEL] URL nach Klick:", self.page.url)
            print("[VERSATEL] Ergebnistext:", availability_text[:1000] if availability_text else "<leer>")
            print("[VERSATEL] Matches:", matches)

            panel_closed = self._close_result_panel()
            if not panel_closed:
                try:
                    print("[VERSATEL] Ergebnisfenster konnte nicht sauber geschlossen werden, öffne Map neu.")
                    self.open_map()
                except Exception as e:
                    print(f"[VERSATEL] Map-Neuaufbau nach Ergebnis fehlgeschlagen: {e}")

            return AvailabilityResult(
                row_index=row.row_index,
                external_id=row.external_id,
                street=row.street,
                house_number=row.house_number,
                postal_code=row.postal_code,
                city=row.city,
                status=status,
                detail_type=detail_type,
                availability_text=availability_text,
                source_url=self.page.url,
                checked_at=time.strftime("%Y-%m-%d %H:%M:%S"),
                error="",
                raw_payload=raw_payload,
                matches=matches,
            )

        except PlaywrightTimeoutError as e:
            return AvailabilityResult(
                row_index=row.row_index,
                external_id=row.external_id,
                street=row.street,
                house_number=row.house_number,
                postal_code=row.postal_code,
                city=row.city,
                status="timeout",
                detail_type="",
                availability_text="",
                source_url=self.page.url if self.page else BASE_URL,
                checked_at=time.strftime("%Y-%m-%d %H:%M:%S"),
                error=str(e),
                raw_payload="",
                matches=[],
            )
        finally:
            try:
                self.page.remove_listener("response", handle_response)
            except Exception:
                try:
                    self.page.off("response", handle_response)
                except Exception:
                    pass


def _process_address_chunk_worker(
    rows: List[AddressInput],
    state_file: str,
    headless: bool,
    result_callback=None,
    username: str = "",
    password: str = "",
    auto_login: bool = False,
    login_wait_seconds: int = 60,
    post_login_delay_seconds: float = 3.0,
) -> List[Dict[str, Any]]:
    bot = VersatelAvailabilityBot(
        state_file=state_file,
        headless=headless,
        timeout_ms=PAGE_TIMEOUT_MS,
    )

    payloads: List[Dict[str, Any]] = []

    try:
        bot.start()

        if auto_login:
            if not str(username or "").strip():
                raise LoginRequired("Automatischer Login angefordert, aber Benutzername fehlt.")
            if not str(password or "").strip():
                raise LoginRequired("Automatischer Login angefordert, aber Passwort fehlt.")
        else:
            bot.ensure_logged_in()

        for row in rows:
            if is_cancel_requested():
                raise ScrapeCancelled("Abbruch angefordert")

            try:
                if auto_login:
                    result = bot.login_and_check_address(
                        row=row,
                        username=username,
                        password=password,
                        login_wait_seconds=login_wait_seconds,
                        post_login_delay_seconds=post_login_delay_seconds,
                    )
                else:
                    result = bot.check_address(row)

                payload = asdict(result)
            except Exception as e:
                payload = asdict(
                    AvailabilityResult(
                        row_index=row.row_index,
                        external_id=row.external_id,
                        street=row.street,
                        house_number=row.house_number,
                        postal_code=row.postal_code,
                        city=row.city,
                        status="error",
                        detail_type="",
                        availability_text="",
                        source_url=bot.page.url if bot.page else BASE_URL,
                        checked_at=time.strftime("%Y-%m-%d %H:%M:%S"),
                        error=str(e),
                        raw_payload="",
                        matches=[],
                    )
                )

            payloads.append(payload)

            if result_callback:
                result_callback(payload)

        return payloads
    finally:
        bot.stop()


def process_address_batch(
    rows: List[AddressInput],
    state_file: str = DEFAULT_STATE_FILE,
    db_path: str = DEFAULT_DB_FILE,
    headless: bool = False,
    progress_callback=None,
    max_workers: int = 1,
    username: str = "",
    password: str = "",
    auto_login: bool = False,
    login_wait_seconds: int = 60,
    post_login_delay_seconds: float = 3.0,
) -> List[Dict[str, Any]]:
    storage = AvailabilityStorage(db_path=db_path)
    total = len(rows)

    if total == 0:
        return []

    max_workers = max(1, min(max_workers, total))
    results: List[Dict[str, Any]] = []
    results_lock = threading.Lock()
    completed = 0

    def handle_result(payload: Dict[str, Any]):
        nonlocal completed

        result_obj = AvailabilityResult(
            row_index=payload.get("row_index", -1),
            external_id=payload.get("external_id", ""),
            street=payload.get("street", ""),
            house_number=payload.get("house_number", ""),
            postal_code=payload.get("postal_code", ""),
            city=payload.get("city", ""),
            status=payload.get("status", ""),
            detail_type=payload.get("detail_type", ""),
            availability_text=payload.get("availability_text", ""),
            source_url=payload.get("source_url", ""),
            checked_at=payload.get("checked_at", ""),
            error=payload.get("error", ""),
            raw_payload=payload.get("raw_payload", ""),
            matches=payload.get("matches", []) or [],
        )

        with results_lock:
            storage.save_result(result_obj)
            results.append(payload)
            completed += 1
            current_completed = completed

        if progress_callback:
            progress_callback(current_completed, total, payload)

    executor = ThreadPoolExecutor(max_workers=max_workers)
    future_map = {}
    cancelled = False

    chunks: List[List[AddressInput]] = [rows[i::max_workers] for i in range(max_workers)]

    try:
        future_map = {
            executor.submit(
                _process_address_chunk_worker,
                chunk,
                state_file,
                headless,
                handle_result,
                username,
                password,
                auto_login,
                login_wait_seconds,
                post_login_delay_seconds,
            ): chunk
            for chunk in chunks if chunk
        }

        for future in as_completed(future_map):
            if is_cancel_requested():
                cancelled = True
                break

            chunk = future_map[future]

            try:
                payloads = future.result()
            except ScrapeCancelled:
                cancelled = True
                break
            except LoginRequired:
                raise
            except Exception as e:
                payloads = [
                    asdict(
                        AvailabilityResult(
                            row_index=row.row_index,
                            external_id=row.external_id,
                            street=row.street,
                            house_number=row.house_number,
                            postal_code=row.postal_code,
                            city=row.city,
                            status="error",
                            detail_type="",
                            availability_text="",
                            source_url=BASE_URL,
                            checked_at=time.strftime("%Y-%m-%d %H:%M:%S"),
                            error=str(e),
                            raw_payload="",
                            matches=[],
                        )
                    )
                    for row in chunk
                ]

                for payload in payloads:
                    handle_result(payload)

        if cancelled or is_cancel_requested():
            for future in future_map:
                try:
                    future.cancel()
                except Exception:
                    pass
            executor.shutdown(wait=False, cancel_futures=True)
            raise ScrapeCancelled("Abbruch angefordert")
    finally:
        try:
            executor.shutdown(wait=False, cancel_futures=True)
        except TypeError:
            executor.shutdown(wait=False)

    results.sort(key=lambda x: int(x.get("row_index", 0)))
    return results
