from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from versatel_availability_ranked import (
    AddressInput,
    LoginRequired,
    VersatelAvailabilityBot,
    VERSATEL_USERNAME,
    VERSATEL_PASSWORD,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://versatel.can-lead.de",
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:8000",
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/versatel/debug-ping")
def versatel_debug_ping():
    return {
        "ok": True,
        "source": "fastapi",
        "message": "debug-ping-aus-versatel_api.py"
    }


@app.get("/api/versatel/debug-ping")
def versatel_debug_ping():
    return {
        "ok": True,
        "source": "fastapi",
        "message": "debug-ping-aus-versatel_api.py"
    }


class VersatelCheckRequest(BaseModel):
    street: str
    houseNumber: str
    postalCode: str
    city: str
    externalId: str = ""


@app.post("/api/versatel/login")
def versatel_login():
    username = (VERSATEL_USERNAME or "").strip()
    password = (VERSATEL_PASSWORD or "").strip()

    if not username:
        raise HTTPException(status_code=500, detail="VERSATEL_USERNAME fehlt.")
    if not password:
        raise HTTPException(status_code=500, detail="VERSATEL_PASSWORD fehlt.")

    bot = VersatelAvailabilityBot(
        headless=False,
        load_state=False,
    )

    try:
        bot.start()
        result = bot.login_with_credentials(
            username=username,
            password=password,
            wait_seconds=60,
        )

        return result
    except LoginRequired as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        bot.stop()


@app.post("/api/versatel/check")
def versatel_check(payload: VersatelCheckRequest):
    street = (payload.street or "").strip()
    house_number = (payload.houseNumber or "").strip()
    postal_code = (payload.postalCode or "").strip()
    city = (payload.city or "").strip()
    external_id = (payload.externalId or "").strip()

    if not street:
        raise HTTPException(status_code=400, detail="Straße fehlt.")
    if not house_number:
        raise HTTPException(status_code=400, detail="Hausnummer fehlt.")
    if not postal_code:
        raise HTTPException(status_code=400, detail="PLZ fehlt.")
    if not city:
        raise HTTPException(status_code=400, detail="Ort fehlt.")

    bot = VersatelAvailabilityBot(
        headless=False,
        load_state=True,
    )

    try:
        print("[VERSATEL API] check gestartet")
        print(f"[VERSATEL API] Adresse: {street} {house_number}, {postal_code} {city}")

        try:
            bot.start()
            print("[VERSATEL API] Browser erfolgreich gestartet")
        except Exception as e:
            print(f"[VERSATEL API] Browserstart fehlgeschlagen: {e}")
            raise HTTPException(status_code=500, detail=f"Browserstart fehlgeschlagen: {e}")

        try:
            bot.ensure_logged_in()
            print("[VERSATEL API] Bestehende Session gültig")
        except LoginRequired:
            print("[VERSATEL API] Keine gültige Session, starte Auto-Login")
            login_result = bot.login_with_credentials(
                username=VERSATEL_USERNAME,
                password=VERSATEL_PASSWORD,
                wait_seconds=60,
            )
            print(f"[VERSATEL API] Login-Ergebnis: {login_result}")

            if not login_result or login_result.get("status") != "ok":
                raise HTTPException(status_code=401, detail="Versatel-Login konnte nicht aufgebaut werden.")

            bot.ensure_logged_in()
            print("[VERSATEL API] Session nach Login gültig")

        row = AddressInput(
            row_index=0,
            original_row={},
            street=street,
            house_number=house_number,
            postal_code=postal_code,
            city=city,
            external_id=external_id,
        )

        result = bot.check_address(row)
        print(f"[VERSATEL API] Check-Ergebnis: status={result.status} error={result.error}")

        return {
            "debug_source": "versatel_api_check_current_build",
            "status": result.status,
            "error": result.error,
            "matches": result.matches,
            "detail_type": result.detail_type,
            "availability_text": result.availability_text,
            "source_url": result.source_url,
            "checked_at": result.checked_at,
        }
    except HTTPException:
        raise
    except LoginRequired as e:
        print(f"[VERSATEL API] LoginRequired: {e}")
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        print(f"[VERSATEL API] Unerwarteter Fehler: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        bot.stop()
