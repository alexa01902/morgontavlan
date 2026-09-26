from gui.tools import create_card
from gui.colors import COLORS
import tkinter as tk
from services.ai_advice import get_clothing_advice


class ClothesCard:
		def __init__(self, parent_fram, row, column):
			self.parent_fram = parent_fram
			self.row = row
			self.column = column
			self.weather_data = None

			self.outfit_card = create_card(
				self.parent_fram,
				"Dagens klädtips",
				COLORS["outfit"],
				row=0,
				column=2
			)

			self.outfit_icon = tk.Label(
				self.outfit_card,
				text="🧥",
				font=("Arial", 45),
				bg=COLORS["outfit"]
			)

			self.outfit_icon.pack(pady=10)

			self.outfit_text = tk.Label(
				self.outfit_card,
				text="Sök på vädret i en ort för att få klädtips.",
				font=("Arial", 13),
				bg=COLORS["outfit"],
				fg=COLORS["text"],
				justify="left",
				wraplength=300
			)

			self.outfit_text.pack(pady=10)


		def show_advice(self, weather_data):
			advice = get_clothing_advice(weather_data)
			self.parent_fram.after(0, lambda: self.outfit_text.config(text=advice))