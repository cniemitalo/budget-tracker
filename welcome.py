import tkinter as tk 
from tkinter import ttk 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
import numpy as np 
import csv 

#global variable
#will eventually be saved to a csv or other format to save data between uses 
app_state = {
    "name": None,
    "income": 0, 
    "categories": [], 
    "dollars": [],
    "percentages": [], 
    "period": None 
} 

#overarching budget app class that allows for display of individual frames
class BudgetApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Budget App")

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        app_state["name"] = tk.StringVar()
        app_state["income"] = tk.StringVar()

        self.frames = {}

        for F in (WelcomeScreen, IncomeScreen, CategoryScreen, BudgetScreen): 
            frame = F(container, self)
            self.frames[F] = frame 
            frame.grid(row=0, column=0, sticky="snew")
        
        self.show_frame(WelcomeScreen)
    
    def show_frame(self, page):
        frame = self.frames[page]
        if hasattr(frame, "refresh"):
            frame.refresh()
        frame.tkraise()

#welcome screen is displayed upon first start up, will be disregarded once first budget is created 
class WelcomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        tk.Label(self, text="Welcome!").pack()
        tk.Label(self, text="Name: ").pack()
        tk.Entry(self, width=15, textvariable=app_state["name"]).pack()
        tk.Button(self, text="Let's get started...", command=lambda: controller.show_frame(IncomeScreen)).pack()

#info screen asks for period of budget and user's income for selected period 
class IncomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        tk.Label(self, text="Select period for budget: ").pack()
        self.color_cb = ttk.Combobox(self, values=["weekly", "bi-weekly", "monthly"])
        self.color_cb.pack()

        def save():
            app_state["period"] = self.color_cb.get()
            print(app_state["name"].get())
            print(app_state["income"].get())
            print(app_state["period"])

        tk.Label(self, text="Enter income for selected period: ").pack()
        tk.Entry(self, width=15, textvariable=app_state["income"]).pack()

        ttk.Button(self, text="Save", command=save).pack()
        tk.Button(self, text="Continue", command=lambda: controller.show_frame(CategoryScreen)).pack()

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
        for c in self.categories: 
            name, amount = c
            app_state["categories"].append(name)
            app_state["dollars"].append(amount)
            app_state["percentages"].append((amount / self.get_income()) * 100)

        print(app_state["categories"])
        print(app_state["dollars"])
        print(app_state["percentages"])


    def update_display(self):
        remaining = self.get_income() - self.total_allocated 
        self.remaining_label.config(text=f"Remaining Budget: ${remaining:.2f}")
        
#screen displaying pie chart and remaining totals 
#allows user to input expenses, see a previous budget, or start a new budget 
class BudgetScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
    
        self.fig, self.ax = plt.subplots(figsize=(4,4))

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack()

        self.cat_listbox = tk.Listbox(self, height=8, width=40)
        self.cat_listbox.pack()

        #ttk.Button(self, text="Add Expense", command=lambda: controller.show_frame(ExpenseScreen)).pack()
        ttk.Button(self, text="See Previous Budget", command=self.see_prev).pack()
        #ttk.Button(self, text="Start New Budget", command=lambda: controller.show_frame(StartNewScreen)).pack()
    
    #def add_expense(self):

    def refresh(self):
        self.ax.clear()
        self.cat_listbox.delete(0, tk.END)

        categories = app_state["categories"]
        dollars = app_state["dollars"]
        percentages = app_state["percentages"]

        if categories and percentages: 
            self.ax.pie(percentages, labels=categories, autopct='%1.1f%%')
            self.ax.set_title("Budget Allocation")
            self.canvas.draw()

        for name, value in zip(categories, dollars):
            self.cat_listbox.insert(tk.END, f"{name}: ${value:.2f}")
        

    def see_prev(self): 
        ttk.Button(self, text="See Previous...").pack()

    def update_display(self):
        for name, value in zip(self.categories, self.dollars): 
            self.cat_listbox.insert(tk.END, f"{name}: ${value:.2f}")


#lass StartNewScreen(tk.Frame): 

        

if __name__ == "__main__":
    app = BudgetApp()
    app.mainloop()