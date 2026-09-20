"""SL-delen av Morgontavlan: från stationsnamn till kommande avgångar.

Steg 1: stationsnamn -> site-id (vi söker i SL:s lista över alla stationer)
Steg 2: site-id -> avgångar (SL Transport API, ingen nyckel behövs)
"""

from functools import cache

import requests

SL_URL = "https://transport.integration.sl.se/v1"


@cache
def hamta_alla_stationer():
    """Hämtar SL:s lista över alla stationer (sites).

    @cache gör att listan bara hämtas första gången funktionen anropas.
    Därefter återanvänds resultatet tills programmet stängs.
    """
    svar = requests.get(f"{SL_URL}/sites", params={"expand": "true"}, timeout=20)
    svar.raise_for_status()
    return svar.json()


def visningsnamn(station):
    """Namn som passar i en lista, t.ex. 'Tegnérgatan (på Sveavägen)'.

    Flera stationer kan heta samma sak, och då är 'note' det som skiljer dem åt.
    """
    if station.get("note"):
        return f"{station['name']} ({station['note']})"
    return station["name"]


def hitta_stationer(sokord, max_antal=8):
    """Söker efter stationer vars namn matchar sökordet.

    Returnerar en lista med stationer, bästa träffen först:
    exakt träff, sedan namn som börjar med sökordet, sedan namn som innehåller det.
    """
    sokord = sokord.strip().casefold()
    if not sokord:
        return []

    traffar = []
    for station in hamta_alla_stationer():
        # Vissa stationer har alias, t.ex. "Stockholm" för "Stockholm City"
        namn = [n.casefold() for n in [station["name"]] + station.get("alias", [])]

        if sokord in namn:
            poang = 0
        elif any(n.startswith(sokord) for n in namn):
            poang = 1
        elif any(sokord in n for n in namn):
            poang = 2
        else:
            continue

        traffar.append((poang, station["name"], station))

    # Lägre poäng först, därefter alfabetiskt på namn
    traffar.sort(key=lambda t: (t[0], t[1]))
    return [station for _, _, station in traffar[:max_antal]]


def hamta_avgangar(site_id, antal=5, transportslag=None):
    """Hämtar kommande avgångar från en station.

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


def valj_station(stationer):
    """Används bara i terminaltestet: låter användaren välja om det finns flera träffar."""
    if len(stationer) == 1:
        return stationer[0]

    print("Flera träffar:")
    for nummer, station in enumerate(stationer, start=1):
        print(f"  {nummer}. {visningsnamn(station)}")

    val = input("Välj nummer (Enter för 1): ").strip()
    try:
        return stationer[int(val) - 1] if val else stationer[0]
    except (ValueError, IndexError):
        print("Ogiltigt val, tar första träffen.")
        return stationer[0]


if __name__ == "__main__":
    sokord = input("Vilken station? ")

    try:
        stationer = hitta_stationer(sokord)
        if not stationer:
            print(f"Hittade ingen station som heter {sokord}.")
        else:
            station = valj_station(stationer)
            print(f"\nAvgångar från {visningsnamn(station)}:")
            avgangar = hamta_avgangar(station["id"])
            if not avgangar:
                print("Inga avgångar den närmaste timmen.")
            for a in avgangar:
                print(f"{a['visas']:>8}  {a['linje']:>4}  {a['slutstation']}")
    except requests.RequestException:
        print("Kunde inte nå SL just nu. Kontrollera internetanslutningen.")