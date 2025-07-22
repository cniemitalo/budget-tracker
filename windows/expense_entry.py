import tkinter as tk 
from tkinter import ttk 
from app_state import app_state

class ExpenseEntryWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Add Expense")

        self.date = tk.StringVar()
        self.category = tk.StringVar()
        self.amount = tk.StringVar()
        self.notes = tk.StringVar()

        tk.Label(self, text="Date:").pack()
        tk.Entry(self, textvariable=self.date).pack()

        tk.Label(self, text="Select Category:").pack()
        ttk.Combobox(self, textvariable=self.category, values=app_state["categories"]).pack()

        tk.Label(self, text="Amount:").pack()
        tk.Entry(self, textvariable=self.amount).pack()

        tk.Label(self, text="Notes (optional):").pack()
        tk.Entry(self, textvariable=self.notes).pack()

        ttk.Button(self, text="Add", command=lambda: self.save_expense(master)).pack()
    
    def save_expense(self, master):
        try: 
            date = self.date.get()
            category = self.category.get()
            amount = float(self.amount.get())
            notes = self.notes.get()

            if category not in app_state["categories"]:
                tk.messagebox.showerror("Error", "Invalid category selected")
                return 
            
            expense = {
                "date": date, 
                "amount": amount, 
                "category": category,
                "notes": notes
            }

            app_state["expenses"].append(expense)

            idx = app_state["categories"].index(category)
            app_state["dollars"][idx] -= amount 

            self.destroy()
            master.refresh()

        except ValueError:
            tk.messagebox.showerror("Error", "Please enter a valid number.")