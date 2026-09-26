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

		self.mood_card = create_card(
			self.parent_frame,
			"Morgonhumör",
			COLORS["mood"],
			row=self.row,
			column=self.column
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
			pady=20
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

	
	def las_data(self, filnamn):
		"""Läser csv-filen.
	
		Excel på svenska sparar csv med semikolon som avgränsare och decimalkomma,
		därför sep=";" och decimal=",". Om åäö blir konstiga tecken, prova
		encoding="cp1252" (Windows) i stället för standardvärdet utf-8.
		"""
		return pd.read_csv(filnamn, sep=",")
	
	
	def skapa_stapeldiagram(self, df):
		"""Bygger ett stapeldiagram och returnerar figuren.
	
	
		Vi använder Figure direkt och inte plt.subplots(). Då hamnar diagrammet
		bara i vårt tkinter-fönster och matplotlib försöker inte öppna ett eget.
		"""
		
		figur = Figure(figsize=(7, 4), dpi=100)
		ax = figur.add_subplot(111)
		ax.bar(df[self.column_name[1]].value_counts().index, df[self.column_name[1]].value_counts().values, color="#FCE8E6"   )
	
		ax.set_title("Humörfördelning")
		ax.set_xlabel("Humör")
		ax.set_ylabel("Antal")
		figur.tight_layout()
		return figur

	def update_mood_plot(self):
		try:

			df = self.las_data(self.FILE)

			# Rita om diagrammet baserat på den nya datan
			figur = self.skapa_stapeldiagram(df)

			# Uppdatera canvas
			canvas = FigureCanvasTkAgg(figur, master=self.canvas_frame)
			tk_widget = canvas.get_tk_widget()
			tk_widget.grid(row=0, column=0,  padx=20, pady=20, sticky="nsew")

		except FileNotFoundError:
			print(f"Hittade inte filen {self.FILE}.")

