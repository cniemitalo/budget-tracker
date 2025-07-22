import tkinter as tk 
from tkinter import simpledialog 
import os 
from utils.file_io import BUDGET_FOLDER

class BudgetSelectorDialog(simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="Select a saved budget:").pack(pady=5)
        
        self.budget_files= [f for f in os.listdir(BUDGET_FOLDER) if f.endswith(".json")]
        self.listbox = tk.Listbox(master, width=40, height=10)
        self.listbox.pack(padx=10)

        for f in self.budget_files:
            self.listbox.insert(tk.END, f)

        return self.listbox
    
    def apply(self):
        selection = self.listbox.curselection()
        if selection:
            self.result = self.budget_files[selection[0]]
        else:
            self.result = None
