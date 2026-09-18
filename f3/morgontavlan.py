
import tkinter as tk
from tkinter import ttk


# -------------------------
# Fönster
# -------------------------

window = tk.Tk()
window.title("Morgontavla")
window.geometry("1100x700")
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

tasks = [
    "Träna",
    "Plugga",
    "Handla",
    "Skicka mejl"
]

for task in tasks:

    check = tk.Checkbutton(
        todo_card,
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

departures = [
    ("Buss 43", "08:32"),
    ("Buss 43", "08:47"),
    ("Buss 52", "09:02")
]

for bus, time in departures:

    departure_label = tk.Label(
        transport_card,
        text=f"{bus:<15}{time}",
        font=("Arial", 13),
        bg=COLORS["transport"],
        fg=COLORS["text"],
        anchor="w"
    )

    departure_label.pack(
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