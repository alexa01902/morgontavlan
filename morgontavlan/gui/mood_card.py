from gui.tools import create_card
from gui.colors import COLORS
import tkinter as tk
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime
import os


class MoodCard:
	def __init__(self, parent_frame, row, column, filename="mood_data.csv"):
		self.parent_frame = parent_frame
		self.row = row
		self.column = column
		self.FILE = filename
		self.column_name = ["datetime", "mood"]
					
		self.mood_card = tk.Frame(
			self.parent_frame,
			bg=COLORS["mood"],
			highlightbackground=COLORS["border"],
			highlightthickness=1
		)

		self.mood_card.grid(
			row=row,
			column=column,
			rowspan=1,
			columnspan=1,
			padx=8,
			pady=8,
			sticky="nsew"
		)

		self.title_label = tk.Label(
			self.mood_card,
			text="Morgonhumör",
			font=("Arial", 16, "bold"),
			bg=COLORS["mood"],
			fg=COLORS["text"]
		
		)

		self.title_label.pack(
			anchor="w",
			padx=20,
			pady=(18, 10)
		)

		self.mood_label = tk.Label(
			self.mood_card,
			text="Hur känner du dig?",
			font=("Arial", 12),
			bg=COLORS["mood"],
			fg=COLORS["text"]
		)

		self.mood_label.pack(pady=5)

		self.mood_options = ["Dåligt", "Okej", "Bra", "Mycket bra"]

		self.mood_combobox = tk.ttk.Combobox(
			self.mood_card,
			values=self.mood_options,
			state="readonly",
			width=12
		)

		self.mood_combobox.set("Bra")

		self.mood_combobox.pack(pady=10)

		self.mood_button = tk.Button(
			self.mood_card,
			text="Spara humör",
			command=self.log_mood,
			font=("Arial", 11),
			bg="#D8E4F2",
			relief="flat"
		)

		self.mood_button.pack(
			pady=10
		)

		self.canvas_frame = tk.Frame(
			self.mood_card,
			bg=COLORS["mood"]
		)

		self.canvas_frame.pack(
			fill="both",
			expand=True,
			padx=20,
			pady=20,

		)

		self.update_mood_plot()
	
	def log_mood(self):
		humör = self.mood_combobox.get()

		if not os.path.exists(self.FILE):
			with open(self.FILE, "a", encoding="utf-8") as f:
						f.write(f"{self.column_name[0]},{self.column_name[1]}\n")


		with open(self.FILE, "a", encoding="utf-8") as f:
			f.write(f"{datetime.now().isoformat()},{humör}\n")

		self.update_mood_plot()
	
	def skapa_stapeldiagram(self, df):
		"""Bygger ett stapeldiagram och returnerar figuren.
		"""
		
		figur = Figure(figsize=(4, 2.5), dpi=100)
		ax = figur.add_subplot(111)
		ax.bar(df[self.column_name[1]].value_counts().index, df[self.column_name[1]].value_counts().values, color="#FCE8E6"   )
		ax.set_title("Humörfördelning")
		ax.set_xlabel("Humör")
		ax.set_ylabel("Antal")
		return figur

	def update_mood_plot(self):
		try:

			df = pd.read_csv(self.FILE, sep=",")

			# Rita om diagrammet baserat på den nya datan
			figur = self.skapa_stapeldiagram(df)

			# Uppdatera canvas
			self.canvas_frame.columnconfigure(0, weight=1)
			self.canvas_frame.rowconfigure(0, weight=1)
			canvas = FigureCanvasTkAgg(figur, master=self.canvas_frame)
			tk_widget = canvas.get_tk_widget()
			tk_widget.grid(row=0, column=0,  padx=20, pady=20)

		except FileNotFoundError:
			print(f"Hittade inte filen {self.FILE}.")

