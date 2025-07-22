import tkinter as tk 
from app_state import app_state
from utils.file_io import save_app_state, load_app_state, DATA_FILE
from screens.welcome_screen import WelcomeScreen
from screens.income_screen import IncomeScreen
from screens.category_screen import CategoryScreen
from screens.budget_screen import BudgetScreen
from screens.previous_budget import PreviousBudgetScreen
import atexit 
import sys

class BudgetApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Budget App")
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        app_state["name"] = tk.StringVar()
        app_state["income"] = tk.StringVar()

        self.frames = {}
        for F in (WelcomeScreen, IncomeScreen, CategoryScreen, BudgetScreen, PreviousBudgetScreen):
            frame = F(container, self)
            self.frames[F] = frame 
            frame.grid(row=0, column=0, sticky="snew")

        self.load_or_start()

    def load_or_start(self):
        if load_app_state():
            self.show_frame(BudgetScreen)
        else:
            self.show_frame(WelcomeScreen)

    def show_frame(self, page):
        frame = self.frames[page]
        if hasattr(frame, "refresh"):
            frame.refresh()

        frame.tkraise()

    def on_exit(self):
        print("on_exit called")
        save_app_state()
        self.quit()
        self.destroy()
        sys.exit(0)

if __name__ == "__main__":
    app = BudgetApp()
    app.protocol("WM_DELETE_WINDOW", app.on_exit)
    atexit.register(save_app_state)
    app.mainloop()