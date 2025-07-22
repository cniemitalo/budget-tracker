import tkinter as tk 
from app_state import app_state

class ExpenseViewerWindow(tk.Toplevel):
    def __init__(self, master, category_name):
        super().__init__(master)
        self.title(f"Expenses for {category_name}")
        tk.Label(self, text=f"Expenses for {category_name}").pack()
        listbox = tk.Listbox(self, width=60)
        listbox.pack()

        for expense in app_state["expenses"]:
            if expense["category"] == category_name:
                display = f"{expense['date']} - {expense['amount']:.2f} - {expense['notes']}"
                listbox.insert(tk.END, display)
        