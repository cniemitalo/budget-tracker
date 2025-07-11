import csv
from tkinter import * 
from tkinter import ttk 

def calculate(*args):
    try:
        value = float(feet.get())
        meters.set(int(0.3048 * value * 10000.0 + 0.5) / 10000.0)
    except ValueError:
        pass 

window = Tk()
window.title("Budget Tracker")

mainframe = ttk.Frame(window, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)

feet = StringVar()
feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
feet_entry.grid(column=2, row=1, sticky=(W, E))

meters = StringVar()
ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))

ttk.Button(mainframe, text="Calculate", command=calculate).grid(column=3, row=3, sticky=W)

ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

feet_entry.focus()
window.bind("<Return>", calculate)

window.mainloop()

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
