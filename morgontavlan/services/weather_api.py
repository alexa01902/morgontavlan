"""Väderdelen av Morgontavlan: från ortnamn till prognos.

Steg 1: ortnamn -> koordinater (geokodning, Open-Meteo, ingen nyckel behövs)
Steg 2: koordinater -> prognos (SMHI:s öppna data, ingen nyckel behövs)
"""

from datetime import datetime
from zoneinfo import ZoneInfo  # På Windows: pip install tzdata

import requests

GEOKODNING_URL = "https://geocoding-api.open-meteo.com/v1/search"
SMHI_URL = (
    "https://opendata-download-metfcst.smhi.se/api/category/snow1g/version/1"
    "/geotype/point/lon/{lon}/lat/{lat}/data.json"
)


# SMHI anger tider i UTC, vi vill visa svensk tid
SVENSK_TID = ZoneInfo("Europe/Stockholm")

def hitta_plats(ortnamn):
    """Slår upp en ort och returnerar (namn, lat, lon), eller None om orten saknas."""
    svar = requests.get(
        GEOKODNING_URL,
        params={
            "name": ortnamn,
            "count": 1,
        },
        timeout=10,
    )
    svar.raise_for_status()

    # Om inget hittas saknas nyckeln "results" helt i svaret
    traffar = svar.json().get("results")
    if not traffar:
        return None

    plats = traffar[0]
    return plats["name"], plats["latitude"], plats["longitude"]


def hamta_prognos(lat, lon, antal_timmar=6):
    """Hämtar prognosen för en punkt och returnerar en lista med en dict per tidpunkt."""
    url = SMHI_URL.format(lat=lat, lon=lon)
    svar = requests.get(url, timeout=10)
    svar.raise_for_status()

    tidsserie = svar.json()["timeSeries"]

    prognos = []
    for punkt in tidsserie[:antal_timmar]:
        data = punkt["data"]
        tid_utc = datetime.fromisoformat(punkt["time"])
        prognos.append(
            {
                "tid": tid_utc.astimezone(SVENSK_TID),
                "temperatur": data["air_temperature"],
                "vind": data["wind_speed"],
                "nederbordsrisk": data["probability_of_precipitation"],
            }
        )
    return prognos

def get_prognose_msg(ort):

    try:
        plats = hitta_plats(ort)
        if plats is None:
            message = f"Hittade ingen ort som heter {ort}."
        else:
            namn, lat, lon = plats
            message = f"Prognos för {namn}:\n"
            for rad in hamta_prognos(lat, lon):
                tid_text = rad['tid'].strftime("%H:%M")
                message += (
                    f"{tid_text}  {round(rad['temperatur'])} °C  "
                    f"{rad['vind']} m/s  {rad['nederbordsrisk']} % regnrisk\n"
                )
    except requests.RequestException:
        print("Kunde inte nå tjänsten just nu. Kontrollera internetanslutningen.")

    return message
