from gui.tools import create_card
from gui.colors import COLORS
import tkinter as tk

class TodoCard:
	def __init__(self, parent_frame, row, column):
		self.parent_frame = parent_frame
		self.row = row
		self.column = column

		self.todo_card = tk.Frame(
			parent_frame,
			bg=COLORS["todo"],
			highlightbackground=COLORS["border"],
			highlightthickness=1
    	)

		self.todo_card .grid(
			row=row,
			column=column,
			rowspan=1,
			columnspan=1,
			padx=8,
			pady=8,
			sticky="nsew"
		)

		self.title_label = tk.Label(
			self.todo_card ,
			text="Att göra idag",
			font=("Arial", 16, "bold"),
			bg=COLORS["todo"],
			fg=COLORS["text"]
		
		)

		self.title_label.pack(
			anchor="w",
			padx=20,
			pady=(18, 10)
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
		task = self.task_entry.get() # Få ut texten som står i entry

		if task != "": # kolla så att texten inte är tom
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
				anchor="w",
				padx=15
			)

			self.task_entry.delete(0, tk.END) #töm entry


