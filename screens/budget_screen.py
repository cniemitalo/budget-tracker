import tkinter as tk
from tkinter import ttk 
from tkinter import simpledialog, messagebox 
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from app_state import app_state
from utils.file_io import save_app_state, export_budget, load_budget, BUDGET_FOLDER
from windows.expense_entry import ExpenseEntryWindow
from windows.expense_viewer import ExpenseViewerWindow 
from windows.budget_selector import BudgetSelectorDialog
from screens.previous_budget import PreviousBudgetScreen

#screen displaying pie chart and remaining totals 
#allows user to input expenses, see a previous budget, or start a new budget 
class BudgetScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller 
    
        self.fig, self.ax = plt.subplots(figsize=(4,4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack()

        self.remaining_label = tk.Label(self, text="")
        self.remaining_label.pack()

        self.cat_listbox = tk.Listbox(self, height=8, width=40)
        self.cat_listbox.pack()
        self.cat_listbox.bind("<Double-1>", self.open_category_expenses)

        ttk.Button(self, text="Add Expense", command=self.add_expense).pack()
        ttk.Button(self, text="Save", command=save_app_state).pack()
        ttk.Button(self, text="See Previous Budget", command=self.see_prev).pack()
        ttk.Button(self, text="Start New Budget", command=self.start_new_budget).pack()

    def refresh(self):
        self.ax.clear()
        self.cat_listbox.delete(0, tk.END)

        remaining = self.get_income() - sum(e["amount"] for e in app_state["expenses"])
        self.remaining_label.config(text=f"Remaining Budget: ${remaining:.2f}")

        categories = app_state["categories"]
        dollars = app_state["dollars"]
        percentages = app_state["percentages"]

        if categories and percentages: 
            self.ax.pie(percentages, labels=categories, autopct='%1.1f%%')
            self.ax.set_title("Budget Allocation")
            self.canvas.draw()

        for name, value in zip(categories, dollars):
            self.cat_listbox.insert(tk.END, f"{name}: ${value:.2f}")

    def update_display(self):
        for name, value in zip(self.categories, self.dollars): 
            self.cat_listbox.insert(tk.END, f"{name}: ${value:.2f}")

    def get_income(self):
        try: 
            return float(app_state["income"].get())
        except (ValueError, TypeError): 
            return 0.0
        
    def add_expense(self):
        ExpenseEntryWindow(self)

    def open_category_expenses(self, event):
        selection = self.cat_listbox.curselection()
        if selection:
            index = selection[0]
            category_name = app_state["categories"][index]
            ExpenseViewerWindow(self, category_name)

    def see_prev(self): 
        dialog = BudgetSelectorDialog(self)
        choice = dialog.result

        if not choice:
            messagebox.showinfo("No selection", "No budget was selected.")
            return
        
        data = load_budget(os.path.join(BUDGET_FOLDER, choice))
        self.controller.frames[PreviousBudgetScreen].load_budget_data(data)
        self.controller.show_frame(PreviousBudgetScreen)

    def start_new_budget(self):
        from screens.income_screen import IncomeScreen
        filename = simpledialog.askstring("Save Budget", "Enter filename to save:")
        export_budget(filename)
        app_state["expenses"].clear()

        #ask if user wants to edit income, period or categories? 
        changes = messagebox.askyesno(
            
            title="Changes?",
            message="Would you like to make any changes to your budget?" 
        )

        if changes:
            self.controller.show_frame(IncomeScreen)
            return
        else: 
            app_state["dollars"] = app_state["allotments"].copy()
            save_app_state()
            self.controller.show_frame(BudgetScreen)