from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from versatel_availability_ranked import (
    AddressInput,
    LoginRequired,
    VersatelAvailabilityBot,
)

app = FastAPI()


class CheckAddressWithLoginRequest(BaseModel):
    street: str
    houseNumber: str
    postalCode: str
    city: str
    externalId: str = ""


@app.post("/api/versatel/check-address-with-login")
def check_address_with_login(payload: CheckAddressWithLoginRequest):
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

        row = AddressInput(
            row_index=0,
            original_row={},
            street=street,
            house_number=house_number,
            postal_code=postal_code,
            city=city,
            external_id=external_id,
        )

        result = bot.login_and_check_address(
            row=row,
            login_wait_seconds=60,
            post_login_delay_seconds=3.0,
        )

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
