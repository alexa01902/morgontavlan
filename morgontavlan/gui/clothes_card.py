from gui.tools import create_card
from gui.colors import COLORS
import tkinter as tk
from services.ai_advice import get_clothing_advice


class ClothesCard:
		def __init__(self, parent_frame, row, column):
			self.parent_frame = parent_frame
			self.row = row
			self.column = column
			
			self.outfit_card = tk.Frame(
				self.parent_frame,
				bg=COLORS["outfit"],
				highlightbackground=COLORS["border"],
				highlightthickness=1
			)

			self.outfit_card.grid(
				row=row,
				column=column,
				rowspan=1,
				columnspan=1,
				padx=8,
				pady=8,
				sticky="nsew"
			)

			self.title_label = tk.Label(
				self.outfit_card,
				text="Dagens klädtips",
				font=("Arial", 16, "bold"),
				bg=COLORS["outfit"],
				fg=COLORS["text"]
			
			)

			self.title_label.pack(
				anchor="w",
				padx=20,
				pady=(18, 10)
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
			#self.parent_frame.after(0, lambda: self.outfit_text.config(text=advice))
			self.outfit_text.config(text=advice)