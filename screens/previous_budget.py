import tkinter as tk 
from tkinter import ttk
from app_state import app_state
from windows.expense_viewer import ExpenseViewerWindow

class PreviousBudgetScreen(tk.Frame):
    def __init__(self, parent, controller):
        from screens.budget_screen import BudgetScreen
        super().__init__(parent)
        self.controller = controller 

        self.period_label = tk.Label(self, text="")
        self.income_label = tk.Label(self, text="")
        self.expense_label = tk.Label(self, text="")
        self.remaining_label = tk.Label(self, text="")
        self.income_label.pack()
        self.expense_label.pack()
        self.remaining_label.pack()

        tk.Label(self, text="All Categories").pack()
        self.cat_listbox = tk.Listbox(self, width=50)
        self.cat_listbox.pack()
        self.cat_listbox.bind("<<ListboxSelect>>", self.view_expenses)

        tk.Label(self, text="Overspent Categories").pack()
        self.overspent_listbox = tk.Listbox(self, width=50)
        self.overspent_listbox.pack()
        
        tk.Label(self, text="Underspent Categories").pack()
        self.underspent_listbox = tk.Listbox(self, width=50)
        self.underspent_listbox.pack()

        ttk.Button(self, text="Back", command=lambda: controller.show_frame(BudgetScreen)).pack()

    def load_budget_data(self, data):
        period = data.get("period", "")
        income = float(data.get("income", 0))
        categories = data.get("categories", [])
        allotments = data.get("allotments", [])
        expenses = data.get("expenses", [])

        total_expenses = sum(e["amount"] for e in expenses if e["category"] in categories)
        remaining = income - total_expenses 

        self.period_label.config(text=f"Period: {period}")
        self.income_label.config(text=f"Income: ${income:.2f}")
        self.expense_label.config(text=f"Total expenses: ${total_expenses:.2f}")
        self.remaining_label.config(text=f"Remaining budget: ${remaining:.2f}")

        self.cat_listbox.delete(0, tk.END)
        self.overspent_listbox.delete(0, tk.END)
        self.underspent_listbox.delete(0, tk.END)

        for i, cat in enumerate(categories):
            allot = allotments[i]
            spent = sum(e["amount"] for e in expenses if e["category"] == cat)
            
            self.cat_listbox.insert(tk.END, f"{cat}: ${spent:.2f}")

            if spent > allot:
                self.overspent_listbox.insert(tk.END, f"{cat}: ${spent - allot:.2f}")
            elif allot > spent:
                self.underspent_listbox.insert(tk.END, f"{cat}: ${allot - spent:.2f}")
        
    def view_expenses(self, event):
        selection = self.cat_listbox.curselection()
        if not selection:
            return 
        
        index = selection[0]
        category = app_state["categories"][index]

        ExpenseViewerWindow(self, category)


