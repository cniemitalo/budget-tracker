import csv

name = input("Enter name: ")
print(f"Hello, {name}! Let's set up your budget tracker!")

#store default user values 
time = input("Would you like to calculate your budget weekly, bi-weekly, or monthly? ")
income = input(f"Please input your {time} antipated income: ")
categories = []
limit = input("How many categories would you like to budget for? ")

for c in range(limit): 
    category = input("Enter category: ")
    categories.append(category)

#ask user for expenses  
expenses = []
for e in range(5): 
    expense = input(f"Enter expense #{e+1}: ")
    expenses.append(expense)

print("Your expenses are:", expenses)

#write expenses to a csv file
with open('expenses.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(expenses)