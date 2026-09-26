
import os
import tkinter as tk
from tkinter import ttk
from datetime import datetime

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
    text="",
    font=("Arial", 42, "bold"),
    bg=COLORS["clock"],
    fg=COLORS["text"]
)

clock_label.pack(pady=(40, 10))

date_label = tk.Label(
    clock_card,
    text="",
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
    text="Sök på vädret i en ort för att få klädtips.",
    font=("Arial", 13),
    bg=COLORS["outfit"],
    fg=COLORS["text"],
    justify="left",
    wraplength=300
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
# 7. Morgonhumör
# -------------------------

mood_card = create_card(
    main_frame,
    "Morgonhumör",
    COLORS["mood"],
    row=1,
    column=2
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

mood_button = tk.Button(
    mood_card,
    text="Spara humör",
    command=log_mood,
    font=("Arial", 11),
    bg="#D8E4F2",
    relief="flat"
)

mood_button.pack(
    pady=10
)

canvas_frame = tk.Frame(
    mood_card,
    bg=COLORS["mood"]
)

canvas_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=20
)

# -------------------------
# 8. Starta appen
# -------------------------

window.mainloop()