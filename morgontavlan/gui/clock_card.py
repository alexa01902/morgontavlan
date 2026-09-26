
from gui.tools import create_card
from gui.colors import COLORS
import tkinter as tk
from datetime import datetime

class ClockCard:
	def __init__(self, parent_frame, row, column):

		self.parent_frame = parent_frame
		self.row = row
		self.column = column

		"""Skapar klockkortet i GUI:t."""
		self.clock_card = create_card(
			self.parent_frame,
			"☀  Morgontavla",
			COLORS["clock"],
			row=self.row,
			column=self.column
		)

		self.clock_label = tk.Label(
			self.clock_card,
			text="",
			font=("Arial", 42, "bold"),
			bg=COLORS["clock"],
			fg=COLORS["text"]
		)
		self.clock_label.pack(pady=(40, 10))

		self.date_label = tk.Label(
			self.clock_card,
			text="",
			font=("Arial", 14),
			bg=COLORS["clock"],
			fg=COLORS["text"]
		)
		self.date_label.pack(pady=(0, 30))

		self.uppdatera_klocka()

	def uppdatera_klocka(self):
		nu = datetime.now() # Hämtar den aktuella tiden
		text_time = nu.strftime("%H:%M") # Formaterar tiden till en sträng
		text_date = nu.strftime("%A %d %B %Y")
		self.clock_label.config(text=text_time)
		self.date_label.config(text=text_date)
		self.clock_card.after(60000, self.uppdatera_klocka) # Uppdaterar klockan varje sekund

