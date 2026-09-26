"""
Enkel AI-integration för Morgontavlan.
Skickar väderdata till Gemini och får tillbaka ett klädråd.
"""

import os
from dotenv import load_dotenv
from google import genai

# Läs in API-nyckeln från .env-filen (se instruktioner för hur du skapar en)
load_dotenv()
client = genai.Client()  # hämtar automatiskt nyckeln från miljövariabeln GEMINI_API_KEY


def hämta_klädråd(temperatur, nederbörd):
    """
    Skickar väderinfo till Gemini och returnerar ett kort klädråd.

    temperatur: t.ex. 5 (grader Celsius)
    nederbörd: t.ex. "regn", "snö" eller "uppehåll"
    """
    prompt = (
        f"Det är {temperatur} grader Celsius och {nederbörd} ute i Stockholm. "
        "Ge ett kort klädråd på max två meningar, på svenska."
    )

    try:
        interaktion = client.interactions.create(
            model="gemini-3.8-flash",
            input=prompt
        )
        return interaktion.output_text

    except Exception as e:
        # Fångar allt som kan gå fel: fel nyckel, ingen internetuppkoppling,
        # för många anrop (rate limit) etc.
        print(f"Fel vid AI-anrop: {e}")
        return "Kunde inte hämta klädråd just nu, försök igen senare."


# Enkelt test som körs om man startar filen direkt
if __name__ == "__main__":
    rad = hämta_klädråd(temperatur=3, nederbörd="regn")
    print(rad)
	