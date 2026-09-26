
from gui.colors import COLORS
import tkinter as tk
from datetime import datetime

class ClockCard:
	def __init__(self, parent_frame, row, column):

		self.parent_frame = parent_frame
		self.row = row
		self.column = column


		self.clock_card = tk.Frame(
			self.parent_frame,
			bg=COLORS["clock"],
			highlightbackground=COLORS["border"],
			highlightthickness=1
    	)

		self.clock_card .grid(
			row=row,
			column=column,
			rowspan=1,
			columnspan=1,
			padx=8,
			pady=8,
			sticky="nsew"
		)

		self.title_label = tk.Label(
			self.clock_card ,
			text="Klockan",
			font=("Arial", 16, "bold"),
			bg=COLORS["clock"],
			fg=COLORS["text"]
		
		)

		self.title_label.pack(
			anchor="w",
			padx=20,
			pady=(18, 10)
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
		self.clock_card.after(60000, self.uppdatera_klocka) # Uppdaterar klockan varje minut

