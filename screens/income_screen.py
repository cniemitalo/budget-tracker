import tkinter as tk 
from tkinter import ttk
from app_state import app_state
from screens.category_screen import CategoryScreen 

#info screen asks for period of budget and user's income for selected period 
class IncomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        tk.Label(self, text="Select period for budget: ").pack()
        self.color_cb = ttk.Combobox(self, values=["weekly", "bi-weekly", "monthly"])
        self.color_cb.pack()

        def save():
            app_state["period"] = self.color_cb.get()

        tk.Label(self, text="Enter income for selected period: ").pack()
        tk.Entry(self, width=15, textvariable=app_state["income"]).pack()

        ttk.Button(self, text="Save", command=save).pack()
        tk.Button(self, text="Continue", command=lambda: controller.show_frame(CategoryScreen)).pack()