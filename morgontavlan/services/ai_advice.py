import os
from dotenv import load_dotenv
from google import genai

# Läs in API-nyckeln från .env-filen (se instruktioner för hur du skapar en)
load_dotenv()
client = genai.Client()  # hämtar automatiskt nyckeln från miljövariabeln GEMINI_API_KEY

def get_clothing_advice(väderdata):
    """
    Skickar väderinfo till Gemini och returnerar ett kort klädråd.

    temperatur: t.ex. 5 (grader Celsius)
    nederbörd: t.ex. "regn", "snö" eller "uppehåll"
    """
    prompt = (
        f"Det här är väderdata från SMHI: {väderdata}. "
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

if __name__ == "__main__":
        testdata = "Prognos för Stockholm:\n12:00  5 °C  3 m/s  60 % regnrisk"
        print(get_clothing_advice(testdata))


    

