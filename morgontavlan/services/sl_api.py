import requests

SL_URL = "https://transport.integration.sl.se/v1"

# Våra egna stationer. Nyckel = namn med små bokstäver, värde = SL:s site-id.
# Lägg till de stationer du själv vill kunna söka på.
STATIONER = {
    "slussen": 9192,
    "duvbo": 9324,
    "sundbyberg": 9325,
    "täby centrum": 9669,
}

def hitta_station_id(station_name):
    """Slår upp site-id för en station. Returnerar None om stationen inte finns i STATIONER."""
    stationsname = station_name.strip().lower()

    if station_name in STATIONER:
        return STATIONER[stationsname]
    else:
        return None


def hamta_avgangar(site_id, antal=5):
    """Hämtar kommande avgångar från en station och returnerar en lista med dictar.
    """
    svar = requests.get(f"{SL_URL}/sites/{site_id}/departures", timeout=10)
    svar.raise_for_status()   # Ger ett tydligt fel direkt om anropet misslyckades, istället för en krasch längre ner
    avgangar = svar.json()["departures"]

    resultat = []
    for a in avgangar[:antal]:
        resultat.append(
            {
                "linje": a["line"]["designation"],
                "slutstation": a["destination"],
                "visas": a["display"],  # T.ex. "4 min" eller "14:32", som SL själva visar det
            }
        )
    return resultat


def get_departure_msg(station):

    site_id = hitta_station_id(station)

    if site_id is None:
        message = (
            f"Jag känner inte till stationen {station}.\n"
            f"Prova: {', '.join(STATIONER)}"
        )
        return message
    else:
        try:
            avgangar = hamta_avgangar(site_id)
            if not avgangar:
                message = "Inga avgångar den närmaste timmen."
            else:
                message = f"Avgångar från {station}:\n\n"
                for a in avgangar:
                    message += f"{a['visas']:<5}  {a['linje']:<3}  {a['slutstation']}\n"
        except requests.RequestException:
            message = "Kunde inte nå SL just nu.\nKontrollera internetanslutningen."

        return message


if __name__ == "__main__":
    station = input("Vilken station vill du se avgångar för? ")
    print(get_departure_msg(station))