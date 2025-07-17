import matplotlib.pyplot as plt
import numpy as np 
import csv
from tkinter import * 
from tkinter import ttk 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root = Tk()
root.title("Budget Tracker")

mainframe = ttk.Frame(root, padding="10")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Variables
name = StringVar()
income = StringVar()
category = []
percentage = []
categories = []
percentages = [] 

fig, ax = plt.subplots(figsize=(4,4))
canvas = FigureCanvasTkAgg(fig, master=mainframe)
canvas.get_tk_widget().grid(column=4, row=1, rowspan=10, padx=10, pady=10)

def add_category(): 
    row = len(category) + 3 
    cat = StringVar()
    perc = StringVar()
    category.append(cat)
    percentage.append(perc)

    cat_entry = ttk.Entry(mainframe, width=15, textvariable=cat)
    perc_entry = ttk.Entry(mainframe, width=15, textvariable=perc)
    cat_entry.grid(column=1, row=row, sticky=W)
    perc_entry.grid(column=2, row=row, sticky=W)

    categories.append(cat_entry)
    percentages.append(perc_entry)

def submit_budget():
    categories = [var.get() for var in category]
    percentages = [] 
    try:
        for var in percentage:
            percentages.append(float(var.get()))
    except ValueError:
        print("Invalid percentage point")
        return
    
    ax.clear()

    ax.pie(percentages, labels=categories, autopct='%1.1f%%')
    canvas.draw()

ttk.Label(mainframe, text="Name: ").grid(column=1, row=1, sticky=E)
ttk.Entry(mainframe, width=20, textvariable=name).grid(column=2, row=1, sticky=(W, E))

ttk.Label(mainframe, text="Income: ").grid(column=1, row=2, sticky=E)
ttk.Entry(mainframe, width=20, textvariable=income).grid(column=2, row=2, sticky=(W, E))

ttk.Button(mainframe, text="Add category", command=add_category).grid(column=1, row=20, sticky=W)
ttk.Button(mainframe, text="Submit budget", command=submit_budget).grid(column=2, row=20, sticky=W)

add_category()
add_category()

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.mainloop()


# run upon intial opening of the budget tracker, or upon editing information 
def set_up(): 
    name = input("Enter name: ")
    print(f"Hello, {name}! Let's set up your budget tracker!")

    #store default user values 
    time = input("Would you like to calculate your budget weekly, bi-weekly, or monthly? ")
    income = input(f"Please input your {time} antipated income: ")
    categories = []
    limit = input("How many categories would you like to budget for? ")

    for c in range(int(limit)): 
        category = input("Enter category: ")
        categories.append(category)

    percentages = [] 
    remain_percent = 100
    for c in categories:
        percentage = input(f"Enter budget percentage for {c} ({remain_percent}% remaining): ")
        remain_percent = remain_percent - int(percentage) 
        percentages.append(int(percentage))

    y = np.array(percentages)
    ax.pie(y, labels=categories)
    canvas.draw()

# create a function that asks a user to input their expense
# amount | date | description | category 
def add_expense(): 
    with open('data/expenses.csv', 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        
        amount = input("Amount: ")
        date = input("Date: ")
        description = input("Description: ")
        category = input("Category: ")

        spamwriter.writerow([amount, date, description, category])

# function reading all expenses stored in data/expenses.csv
def read_expenses(): 
    try: 
        with open('data/expenses.csv', 'r', newline='') as file: 
            reader = csv.reader(file)
            print("\nTransactions:\n")
            for row in reader: 
                print(row)
    except FileNotFoundError: 
        print("No transactions yet.")

def clear_expenses(): 
    with open('data/expenses.csv', 'w') as f: 
        pass 
