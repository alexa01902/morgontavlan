from gui.tools import create_card
from gui.colors import COLORS
import tkinter as tk

class TodoCard:
	def __init__(self, parent_frame, row, column):
		self.parent_frame = parent_frame
		self.row = row
		self.column = column

		self.todo_card = create_card(
			self.parent_frame,
			"Att göra idag",
			COLORS["todo"],
			row=self.row,
			column=self.column
		)

		self.todo_frame = tk.Frame(
			self.todo_card,
			bg=COLORS["todo"]
		)

		self.todo_frame.pack(
			fill="both",
			expand=True,
			padx=15,
			pady=15
		)

		self.task_entry = tk.Entry(
			self.todo_card,
			font=("Arial", 12)
		)

		self.task_entry.pack(
			side="left",
			padx=(20, 5),
			pady=20,
			ipady=5
		)

		self.add_button = tk.Button(
			self.todo_card,
			text="Lägg till",
			command=self.add_task,
			font=("Arial", 11),
			bg="#D8E4F2",
			relief="flat"
		)

		self.add_button.pack(
			side="left",
			padx=5,
			pady=20,
			ipady=4
		)
	
	def add_task(self):
		task = self.task_entry.get()

		if task != "":
			check = tk.Checkbutton(
				self.todo_frame,
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

			self.task_entry.delete(0, tk.END)


