import tkinter as tk 
from tkinter import ttk 
from app_state import app_state 
from screens.income_screen import IncomeScreen 

#welcome screen is displayed upon first start up, will be disregarded once first budget is created 
class WelcomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        tk.Label(self, text="Welcome!").pack()
        tk.Label(self, text="Name: ").pack()
        tk.Entry(self, width=15, textvariable=app_state["name"]).pack()
        tk.Button(self, text="Let's get started...", command=lambda: controller.show_frame(IncomeScreen)).pack()