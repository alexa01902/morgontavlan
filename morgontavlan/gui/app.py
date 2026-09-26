
import os
import tkinter as tk
from tkinter import ttk
from gui.colors import COLORS

from gui.clock_card import ClockCard
from gui.todo_card import TodoCard
from gui.transport_card import TransportCard
from gui.weather_card import WeatherCard
from gui.clothes_card import ClothesCard
from gui.mood_card import MoodCard

class Morgontavlan:
	def __init__(self):
		

		self.window = tk.Tk()
		self.window.title("Morgontavla")
		self.window.geometry("1500x1000")
		self.window.configure(bg="#F5F6FA")

		self.main_frame = tk.Frame(
			self.window,
			bg=COLORS["background"]
		)

		self.main_frame.pack(
			fill="both",
			expand=True,
			padx=20,
			pady=20
		)

		# Tre kolumner
		self.main_frame.columnconfigure(0, weight=1)
		self.main_frame.columnconfigure(1, weight=1)
		self.main_frame.columnconfigure(2, weight=1)

		# Två huvudrader
		self.main_frame.rowconfigure(0, weight=1)
		self.main_frame.rowconfigure(1, weight=1)

		self.clock_card = ClockCard(self.main_frame, 0, 0)
		self.todo_card = TodoCard(self.main_frame, 1, 0)
		self.transport_card = TransportCard(self.main_frame, 1 , 1)
		self.clothes_card = ClothesCard(self.main_frame, 0, 2)
		self.weather_card = WeatherCard(self.main_frame, 0, 1, self.clothes_card)
		self.mood_card = MoodCard(self.main_frame, 1, 2)


		self.window.mainloop()