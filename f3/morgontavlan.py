
import tkinter as tk
from tkinter import ttk

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

# Väderkoder (Wsymb2) från SMHI, översatta till svenska
VADERSYMBOLER = {
    1: "Klart",
    2: "Mestadels klart",
    3: "Växlande molnighet",
    4: "Halvklart",
    5: "Molnigt",
    6: "Mulet",
    7: "Dimma",
    8: "Lätta regnskurar",
    9: "Måttliga regnskurar",
    10: "Kraftiga regnskurar",
    11: "Åskväder",
    12: "Lätta byar av snöblandat regn",
    13: "Måttliga byar av snöblandat regn",
    14: "Kraftiga byar av snöblandat regn",
    15: "Lätta snöbyar",
    16: "Måttliga snöbyar",
    17: "Kraftiga snöbyar",
    18: "Lätt regn",
    19: "Måttligt regn",
    20: "Kraftigt regn",
    21: "Åska",
    22: "Lätt snöblandat regn",
    23: "Måttligt snöblandat regn",
    24: "Kraftigt snöblandat regn",
    25: "Lätt snöfall",
    26: "Måttligt snöfall",
    27: "Kraftigt snöfall",
}

SL_URL = "https://transport.integration.sl.se/v1"

# Våra egna stationer. Nyckel = namn med små bokstäver, värde = SL:s site-id.
# Lägg till de stationer du själv vill kunna söka på.
STATIONER = {
    "slussen": 9192,
    "duvbo": 9324,
    "sundbyberg": 9325,
    "täby centrum": 9669,
}


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


def visa_avgangar():
    station = station_entry.get()
    site_id = hitta_station_id(station)

    if site_id is None:
        message = (
            f"Jag känner inte till stationen {station}.\n"
            f"Prova: {', '.join(STATIONER)}"
        )
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

    departures_label.config(text=message)


def hitta_plats(ortnamn):
    """Slår upp en ort och returnerar (namn, lat, lon), eller None om orten saknas."""
    svar = requests.get(
        GEOKODNING_URL,
        params={
            "name": ortnamn,
            "count": 1,
            "language": "sv",
            "countryCode": "SE",  # Ta bort raden för att även hitta t.ex. Oslo
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
        tid_utc = datetime.fromisoformat(punkt["time"].replace("Z", "+00:00"))
        prognos.append(
            {
                "tid": tid_utc.astimezone(SVENSK_TID),
                "temperatur": data["air_temperature"],
                "vind": data["wind_speed"],
                "nederbordsrisk": data["probability_of_precipitation"],
                "beskrivning": VADERSYMBOLER.get(data["symbol_code"], "Okänt väder"),
            }
        )
    return prognos

def visa_prognos():
    ort = location_entry.get()

    try:
        plats = hitta_plats(ort)
        if plats is None:
            print(f"Hittade ingen ort som heter {ort}.")
        else:
            namn, lat, lon = plats
            message = f"Prognos för {namn}:\n"
            for rad in hamta_prognos(lat, lon):
                message += (
                    f"{rad['tid']:%H:%M}  {round(rad['temperatur'])} °C  "
                    f"{rad['vind']} m/s  {rad['nederbordsrisk']} % regnrisk  "
                    f"{rad['beskrivning']} \n"
                )
        weather_info.config(text=message)
    except requests.RequestException:
        print("Kunde inte nå tjänsten just nu. Kontrollera internetanslutningen.")


# -------------------------
# Fönster
# -------------------------

window = tk.Tk()
window.title("Morgontavla")
window.geometry("1500x1000")
window.configure(bg="#F5F6FA")


# -------------------------
# Färger
# -------------------------

COLORS = {
    "background": "#F5F6FA",
    "clock": "#E5F1FC",
    "weather": "#E5F1FC",
    "outfit": "#EEE9FC",
    "todo": "#E7F4E5",
    "transport": "#FFF3D9",
    "sleep": "#EDEBFA",
    "mood": "#FCE8E6",
    "bottom": "#E5EEF7",
    "text": "#172033",
    "border": "#D5DCE5"
}


# -------------------------
# Hjälpfunktion
# -------------------------

def create_card(parent, title, color, row, column,
                rowspan=1, columnspan=1):

    frame = tk.Frame(
        parent,
        bg=color,
        highlightbackground=COLORS["border"],
        highlightthickness=1
    )

    frame.grid(
        row=row,
        column=column,
        rowspan=rowspan,
        columnspan=columnspan,
        padx=8,
        pady=8,
        sticky="nsew"
    )

    title_label = tk.Label(
        frame,
        text=title,
        font=("Arial", 16, "bold"),
        bg=color,
        fg=COLORS["text"]
    )

    title_label.pack(
        anchor="w",
        padx=20,
        pady=(18, 10)
    )

    return frame

def add_task():
    task = task_entry.get()

    if task != "":
        check = tk.Checkbutton(
            todo_frame,
            text=task,
            font=("Arial", 13),
            bg=COLORS["todo"],
            fg=COLORS["text"],
            anchor="w",
            padx=15,
            pady=4
        )

        check.pack(
            fill="x",
            padx=15
        )

        task_entry.delete(0, tk.END)


# -------------------------
# Huvudlayout
# -------------------------

main_frame = tk.Frame(
    window,
    bg=COLORS["background"]
)

main_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=20
)


# Tre kolumner
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)
main_frame.columnconfigure(2, weight=1)

# Två huvudrader
main_frame.rowconfigure(0, weight=1)
main_frame.rowconfigure(1, weight=1)


# -------------------------
# 1. Klocka
# -------------------------

clock_card = create_card(
    main_frame,
    "☀  Morgontavla",
    COLORS["clock"],
    row=0,
    column=0
)

clock_label = tk.Label(
    clock_card,
    text="08:24",
    font=("Arial", 42, "bold"),
    bg=COLORS["clock"],
    fg=COLORS["text"]
)

clock_label.pack(pady=(40, 10))

date_label = tk.Label(
    clock_card,
    text="Måndag 22 september 2025",
    font=("Arial", 14),
    bg=COLORS["clock"],
    fg=COLORS["text"]
)

date_label.pack(pady=(0, 30))


# -------------------------
# 2. Väder
# -------------------------

weather_card = create_card(
    main_frame,
    "Väder",
    COLORS["weather"],
    row=0,
    column=1
)

weather_label = tk.Label(
    weather_card,
    text="☀️   12°C",
    font=("Arial", 25, "bold"),
    bg=COLORS["weather"],
    fg=COLORS["text"]
)

weather_label.pack(pady=15)

weather_info = tk.Label(
    weather_card,
    text="Växlande molnighet\nVind: 3 m/s\nRegn: 0%",
    font=("Arial", 13),
    bg=COLORS["weather"],
    fg=COLORS["text"],
    justify="left"
)

weather_info.pack(pady=5)

location_entry = tk.Entry(
    weather_card,
    font=("Arial", 12),
    width=20
)

location_entry.insert(0, "Ange område")

location_entry.pack(
    padx=20,
    pady=20
)

search_button = tk.Button(
    weather_card,
	text="Sök",
    command=visa_prognos,
	font=("Arial", 11),
	bg="#D8E4F2",
	relief="flat"
)	

search_button.pack(
	padx=20)


# -------------------------
# 3. Klädtips
# -------------------------

outfit_card = create_card(
    main_frame,
    "Dagens klädtips",
    COLORS["outfit"],
    row=0,
    column=2
)

outfit_icon = tk.Label(
    outfit_card,
    text="🧥",
    font=("Arial", 45),
    bg=COLORS["outfit"]
)

outfit_icon.pack(pady=10)

outfit_text = tk.Label(
    outfit_card,
    text="Det blir lite kyligt idag,\n"
         "så en tunn jacka och\n"
         "långbyxor passar bra.",
    font=("Arial", 13),
    bg=COLORS["outfit"],
    fg=COLORS["text"],
    justify="left"
)

outfit_text.pack(pady=10)


# -------------------------
# 4. To-do-lista
# -------------------------

todo_card = create_card(
    main_frame,
    "Att göra idag",
    COLORS["todo"],
    row=1,
    column=0
)

todo_frame = tk.Frame(
	todo_card,
	bg=COLORS["todo"]
)

todo_frame.pack(
	fill="both",
	expand=True,
	padx=15,
	pady=15
)

task_entry = tk.Entry(
    todo_card,
    font=("Arial", 12)
)

task_entry.pack(
    side="left",
    padx=(20, 5),
    pady=20,
    ipady=5
)

add_button = tk.Button(
    todo_card,
    text="Lägg till",
    command=add_task,
    font=("Arial", 11),
    bg="#D8E4F2",
    relief="flat"
)

add_button.pack(
    side="left",
    padx=5,
    pady=20,
    ipady=4
)


# -------------------------
# 5. Kollektivtrafik
# -------------------------

transport_card = create_card(
    main_frame,
    "Nästa buss/tåg",
    COLORS["transport"],
    row=1,
    column=1
)

station_entry = tk.Entry(
    transport_card,
    font=("Arial", 12),
    width=25
)

station_entry.insert(0, "Ange station")

station_entry.pack(
    padx=20,
    pady=10,
    ipady=5
)

search_transport_button = tk.Button(
    transport_card,
    text="Sök avgångar",
    command=visa_avgangar,
    font=("Arial", 11),
    bg="#D8E4F2",
    relief="flat"
)
search_transport_button.pack(
    padx=20,
    pady=(0, 10)
)

departures_label = tk.Label(
    transport_card,
    text=f"",
    font=("Arial", 13),
    bg=COLORS["transport"],
    fg=COLORS["text"],
    justify="left",            # vänsterjustera raderna (standard är centrerat)
)

departures_label.pack(
    fill="x",
    padx=25,
    pady=8
)
# -------------------------
# Hälsa
# -------------------------

bottom_right_frame = tk.Frame(
    main_frame,
    bg=COLORS["background"]
)

bottom_right_frame.grid(
    row=1,
    column=2,
    padx=8,
    pady=8,
    sticky="nsew"
)

# Två kolumner inuti behållaren
bottom_right_frame.columnconfigure(0, weight=1)
bottom_right_frame.columnconfigure(1, weight=1)

bottom_right_frame.rowconfigure(0, weight=1)

# -------------------------
# 6. Sömn
# -------------------------

sleep_card = create_card(
    bottom_right_frame,
    "Sömn",
    COLORS["sleep"],
    row=0,
    column=0
)

sleep_icon = tk.Label(
    sleep_card,
    text="☾",
    font=("Arial", 30),
    bg=COLORS["sleep"]
)

sleep_icon.pack(pady=5)

sleep_label = tk.Label(
    sleep_card,
    text="Hur många timmar sov du?",
    font=("Arial", 12),
    bg=COLORS["sleep"],
    fg=COLORS["text"]
)

sleep_label.pack(pady=5)

sleep_options = ["4 h", "5 h", "6 h", "7 h", "8 h", "9 h"]

sleep_combobox = ttk.Combobox(
    sleep_card,
    values=sleep_options,
    state="readonly",
    width=10
)

sleep_combobox.set("7 h")

sleep_combobox.pack(pady=10)

# -------------------------
# 7. Morgonhumör
# -------------------------

mood_card = create_card(
    bottom_right_frame,
    "Morgonhumör",
    COLORS["mood"],
    row=0,
    column=1
)

mood_label = tk.Label(
    mood_card,
    text="Hur känner du dig?",
    font=("Arial", 12),
    bg=COLORS["mood"],
    fg=COLORS["text"]
)

mood_label.pack(pady=5)

mood_options = ["Dåligt", "Okej", "Bra", "Mycket bra"]

mood_combobox = ttk.Combobox(
    mood_card,
    values=mood_options,
    state="readonly",
    width=12
)

mood_combobox.set("Bra")

mood_combobox.pack(pady=10)


# -------------------------
# 8. Starta appen
# -------------------------

window.mainloop()