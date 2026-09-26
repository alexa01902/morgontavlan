from gui.colors import COLORS
import tkinter as tk

def create_card(parent, title, color, row, column,
                rowspan=1, columnspan=1):

    frame = tk.Frame(
        parent,
        bg=color,
        highlightbackground=COLORS["border"],
        highlightthickness=1
    )

    frame.grid(
        row=row,
        column=column,
        rowspan=rowspan,
        columnspan=columnspan,
        padx=8,
        pady=8,
        sticky="nsew"
    )

    title_label = tk.Label(
        frame,
        text=title,
        font=("Arial", 16, "bold"),
        bg=color,
        fg=COLORS["text"]
    )

    title_label.pack(
        anchor="w",
        padx=20,
        pady=(18, 10)
    )

    return frame
