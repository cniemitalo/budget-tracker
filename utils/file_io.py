import tkinter as tk 
import json 
import os 
from datetime import datetime 
from app_state import app_state 

DATA_FILE = "data/budget_data.json"
DATA_FOLDER = os.path.dirname(DATA_FILE)
BUDGET_FOLDER = os.path.dirname("data/budgets")

if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

if not os.path.exists(BUDGET_FOLDER):
    os.makedirs(BUDGET_FOLDER)

def get_app_state():
    data = {
        "name": app_state["name"].get() if isinstance(app_state["name"], tk.StringVar) else app_state["name"],
        "period": app_state["period"], 
        "income": app_state["income"].get() if isinstance(app_state["income"], tk.StringVar) else app_state["income"],
        "categories": app_state["categories"],
        "dollars": app_state["dollars"],
        "allotments": app_state["allotments"],
        "percentages": app_state["percentages"],
        "expenses": app_state["expenses"]   
    }
    return data

def save_app_state():
    state_copy = get_app_state()

    with open(DATA_FILE, "w") as f:
        json.dump(state_copy, f)

def load_app_state():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            loaded = json.load(f)
            app_state["name"].set(loaded.get("name", ""))
            app_state["period"] = loaded.get("period", "")
            app_state["income"].set(loaded.get("income", 0))
            app_state["categories"] = loaded.get("categories", [])
            app_state["dollars"] = loaded.get("dollars", [])
            app_state["allotments"] = loaded.get("allotments", [])
            app_state["percentages"] = loaded.get("percentages", [])
            app_state["expenses"] = loaded.get("expenses", [])
        return True
    else:
        return False

def export_budget(filename):
    data = get_app_state()

    file_name = os.path.join(BUDGET_FOLDER, f"{filename}.json")

    with open(file_name, "w") as f:
        json.dump(data, f, indent=4)

def load_budget(path):
    with open(path, "r") as f:
        data = json.load(f)
    return data