from gui.tools import create_card
from gui.colors import COLORS
import tkinter as tk
from services.weather_api import get_prognose_msg
import threading

class WeatherCard:
	def __init__(self, parent_frame, row, column,  clothes_card = "None"):
		self.parent_frame = parent_frame
		self.row = row
		self.column = column
		self.clothes_card = clothes_card

		# -------------------------
		# Väder
		# -------------------------

		self.weather_card = create_card(
			self.parent_frame,
			"Väder",
			COLORS["weather"],
			row=self.row,
			column=self.column
		)

		self.weather_label = tk.Label(
			self.weather_card,
			text="☀️   12°C",
			font=("Arial", 25, "bold"),
			bg=COLORS["weather"],
			fg=COLORS["text"]
		)

		self.weather_label.pack(pady=15)

		self.weather_info = tk.Label(
			self.weather_card,
			text="Växlande molnighet\nVind: 3 m/s\nRegn: 0%",
			font=("Arial", 13),
			bg=COLORS["weather"],
			fg=COLORS["text"],
			justify="left"
		)

		self.weather_info.pack(pady=5)

		self.location_entry = tk.Entry(
			self.weather_card,
			font=("Arial", 12),
			width=20
		)

		self.location_entry.insert(0, "Ange område")

		self.location_entry.pack(
			padx=20,
			pady=20
		)

		self.search_button = tk.Button(
			self.weather_card,
			text="Sök",
			command=self.show_prognose,
			font=("Arial", 11),
			bg="#D8E4F2",
			relief="flat"
		)	

		self.search_button.pack(
			padx=20)


	def show_prognose(self):
		
		ort = self.location_entry.get()

		message = get_prognose_msg(ort)

		if self.clothes_card is not None:
			self.clothes_card.weather_data = message

			self.clothes_card.outfit_text.config(text="Hämtar klädråd…")
			# Starta AI-anropet i en separat tråd så fönstret inte fryser
			tråd = threading.Thread(target=self.clothes_card.show_advice, args=(message,))
			tråd.daemon = True
			tråd.start()

		self.weather_info.config(text=message)