from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from versatel_availability_ranked import (
    AddressInput,
    LoginRequired,
    VersatelAvailabilityBot,
)

app = FastAPI()


class VersatelLoginRequest(BaseModel):
    username: str
    password: str


class VersatelCheckRequest(BaseModel):
    street: str
    houseNumber: str
    postalCode: str
    city: str
    externalId: str = ""


@app.post("/api/versatel/login")
def versatel_login(payload: VersatelLoginRequest):
    username = (payload.username or "").strip()
    password = (payload.password or "").strip()

    if not username:
        raise HTTPException(status_code=400, detail="Benutzername fehlt.")
    if not password:
        raise HTTPException(status_code=400, detail="Passwort fehlt.")

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
        bot.start()
        bot.ensure_logged_in()

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

        return {
            "status": result.status,
            "error": result.error,
            "matches": result.matches,
            "detail_type": result.detail_type,
            "availability_text": result.availability_text,
            "source_url": result.source_url,
            "checked_at": result.checked_at,
        }
    except LoginRequired as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        bot.stop()
