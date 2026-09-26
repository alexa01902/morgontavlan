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

tk_widget = None  # Variabel för att hålla referensen till det nuvarande diagrammet

def hitta_station_id(stationsnamn):
    """Slår upp site-id för en station. Returnerar None om stationen inte finns i STATIONER."""
    return STATIONER.get(stationsnamn.strip().lower())


def hamta_avgangar(site_id, antal=5, transportslag=None):
    """Hämtar kommande avgångar från en station och returnerar en lista med dictar.

    transportslag kan vara t.ex. "METRO", "BUS", "TRAIN" eller "TRAM".
    Utan transportslag får du alla sorter blandat.
    """
    svar = requests.get(f"{SL_URL}/sites/{site_id}/departures", timeout=10)
    svar.raise_for_status()
    avgangar = svar.json()["departures"]

    if transportslag:
        avgangar = [a for a in avgangar if a["line"]["transport_mode"] == transportslag]

    # Sortera på förväntad tid, och på planerad tid om ingen förväntad finns
    avgangar.sort(key=lambda a: a.get("expected") or a.get("scheduled", ""))

    resultat = []
    for a in avgangar[:antal]:
        resultat.append(
            {
                "linje": a["line"]["designation"],
                "slutstation": a["destination"],
                "visas": a["display"],  # T.ex. "4 min" eller "14:32", som SL själva visar det
                "transportslag": a["line"]["transport_mode"],
            }
        )
    return resultat


def get_departure_mgs(station):

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
                    message += f"{a['visas']:>8}  {a['linje']:>4}  {a['slutstation']}\n"
        except requests.RequestException:
            message = "Kunde inte nå SL just nu.\nKontrollera internetanslutningen."

        return message
    