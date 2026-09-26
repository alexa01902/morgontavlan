from gui.tools import create_card
from gui.colors import COLORS
import tkinter as tk
from services.sl_api import get_departure_mgs

class TransportCard:
	def __init__(self, parent_frame, row, column):
		self.parent_frame = parent_frame
		self.row = row
		self.column = column

		self.transport_card = create_card(
			self.parent_frame,
			"Nästa buss/tåg",
			COLORS["transport"],
			row=row,
			column=column
		)

		self.station_entry = tk.Entry(
			self.transport_card,
			font=("Arial", 12),
			width=25
		)

		self.station_entry.insert(0, "Ange station")

		self.station_entry.pack(
			padx=20,
			pady=10,
			ipady=5
		)

		self.search_transport_button = tk.Button(
			self.transport_card,
			text="Sök avgångar",
			command=self.show_departures,
			font=("Arial", 11),
			bg="#D8E4F2",
			relief="flat"
		)

		self.search_transport_button.pack(
			padx=20,
			pady=(0, 10)
		)

		self.departures_label = tk.Label(
			self.transport_card,
			text=f"",
			font=("Arial", 13),
			bg=COLORS["transport"],
			fg=COLORS["text"],
			justify="left",            # vänsterjustera raderna (standard är centrerat)
		)

		self.departures_label.pack(
			fill="x",
			padx=25,
			pady=8
		)

	def show_departures(self):

		message = get_departure_mgs(self.station_entry.get())
		self.departures_label.config(text=message)


