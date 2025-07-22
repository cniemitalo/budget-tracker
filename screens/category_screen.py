import tkinter as tk 
from tkinter import ttk
from app_state import app_state
from screens.budget_screen import BudgetScreen 


#category screen allows user to input categories and their allocated amounts 
#either through a percentage of the user's income or specific dollar amount 
class CategoryScreen(tk.Frame): 
    def __init__(self, parent, controller): 
        super().__init__(parent)
        self.controller = controller 

        self.mode = tk.StringVar(value="percentage")
        self.category_var = tk.StringVar()
        self.value_var = tk.StringVar()
        self.del_category_var = tk.StringVar() 
        self.del_value_var = tk.StringVar()

        self.total_allocated = 0.0
        self.categories = []

        tk.Label(self, text="Enter budget categories:").pack()

        mode_frame = tk.Frame(self)
        tk.Radiobutton(mode_frame, text="Percentage", variable=self.mode, value="percentage", command=self.update_display).pack(side="left")
        tk.Radiobutton(mode_frame, text="Dollar Amount", variable=self.mode, value="dollar", command=self.update_display).pack(side="left")
        mode_frame.pack()

        tk.Label(self, text="Category Name:").pack()
        tk.Entry(self, textvariable=self.category_var).pack()

        tk.Label(self, text="Amount (as % or $):").pack()
        tk.Entry(self, textvariable=self.value_var).pack()

        ttk.Button(self, text="Add Category", command=self.add_category).pack()

        self.remaining_label = tk.Label(self, text="")
        self.remaining_label.pack()

        self.cat_listbox = tk.Listbox(self, height=8, width=40)
        self.cat_listbox.pack()

        ttk.Button(self, text="Delete Category", command=self.delete_category).pack()
        ttk.Button(self, text="Save", command=self.save_categories).pack()

        self.update_display()
        tk.Button(self, text="Continue", command=lambda: controller.show_frame(BudgetScreen)).pack()

    def get_income(self):
        try: 
            return float(app_state["income"].get())
        except (ValueError, TypeError): 
            return 0.0
 
    def add_category(self):
        try: 
            name = self.category_var.get()
            value = float(self.value_var.get())

            if self.mode.get() == "percentage":
                dollar_value = self.get_income() * value / 100
            else: 
                dollar_value = value 

            if self.total_allocated + dollar_value > self.get_income():
                tk.messagebox.showerror("Error", "You've exceeded your income.")
                return 
        
            self.categories.append((name, dollar_value))
            self.total_allocated += dollar_value 

            self.cat_listbox.insert(tk.END, f"{name}: ${dollar_value:.2f}")
            self.category_var.set("")
            self.value_var.set("")
            self.update_display()

        except ValueError:
            tk.messagebox.showerror("Invalid input", "Please enter a valid number.")
    
    def delete_category(self):
        selected = self.cat_listbox.curselection()
        if not selected:
            return 
        
        index = selected[0]

        _, amount = self.categories[index]
        self.total_allocated -= amount 

        self.categories.pop(index)
        self.cat_listbox.delete(index)

        self.update_display()

    def save_categories(self): 
        app_state["categories"].clear()
        app_state["dollars"].clear()
        app_state["allotments"].clear()
        app_state["percentages"].clear()

        for c in self.categories: 
            name, amount = c
            app_state["categories"].append(name)
            app_state["dollars"].append(amount)
            app_state["allotments"].append(amount)
            app_state["percentages"].append((amount / self.get_income()) * 100)


    def update_display(self):
        remaining = self.get_income() - self.total_allocated 
        self.remaining_label.config(text=f"Remaining Budget: ${remaining:.2f}")

    def refresh(self):
        self.cat_listbox.delete(0, tk.END)
        self.categories = []
        self.total_allocated = 0.0

        if app_state["categories"] and app_state["allotments"]:
            for name, allotment in zip(app_state["categories"], app_state["allotments"]):
                self.categories.append((name, allotment))
                self.cat_listbox.insert(tk.END, f"{name}: ${allotment:.2f}")
                self.total_allocated += allotment 

        self.update_display()