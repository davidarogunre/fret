from os import path as p
import typer
import sqlite3
from rich import print as sprint
from rich.prompt import Prompt
from database import new_user_db_initiate
from datetime import datetime
from datetime import date
from rich.progress import track
import time
import math
import plotext as plt

PATH = 'C:/Coding/fret/fret.db'
UPATH = 'C:/Coding/fret/userinfo.txt'

app = typer.Typer()

def check_is_path_exists(path, upath):
    return p.exists(path) and p.exists(upath)

def new_user_printout():
    pass



def iterate(percent):
    for i in range(percent):
        yield i

def display_dash(month):
    data = 0
    try: 
        conn = sqlite3.connect("fret.db")
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM budget WHERE month='{month}' ")
        data = cursor.fetchall()
        conn.close()
    except:
        print("An error occured")
        return
    salary = 0
    f = open("userinfo.txt", "r")
    salary = int(f.readlines()[1])
    f.close()
    other_name = []
    other_percent = []
    names = [f'{i[0]} (\u20a6{i[2]})' for i in data]     
    values = [i[2] for i in data]
    percents = [round((i/salary)*100) for i in values]
    
    
    total = sum(values)
    if total == salary:
        other_name = []
        other_percent = []
    else:
        other_name = [f"Discretionary Income (\u20a6{salary-sum(values)})"]
        other_percent = [100-sum(percents)]
    
    
    final_names = names + other_name
    final_percents = percents + other_percent
    plt.simple_bar(final_names, final_percents, width = 75, title = f'Budget of {month} in %')
    plt.show()

def intro():
    if check_is_path_exists(PATH, UPATH):
        display_dash(datetime.now().strftime("%B"))
    else:
        sprint("[bold green]Welcome :wave:, it is has come to my attention that you are a new user")
        name= Prompt.ask("[bold magenta]What is your name ") 
        sprint(f"[bold green]Welcome once again {name}")
        income = Prompt.ask(f"[bold magenta]What is your income :moneybag: ?")
        budget = Prompt.ask("[bold cyan]To begin, enter random budget category for this month in format; {name of budget} {money set aside} then use budget command to add more")
        conn = sqlite3.connect("fret.db")
        new_user_db_initiate(conn, budget.split(" ")[0], datetime.now().strftime("%B"), budget.split(" ")[1], date.today().year)
        with open("userinfo.txt", "w") as f:
            f.writelines([f"{name}\n", f"{income}\n"])
            f.close()
        conn.close()

def check_net_loss(new_val:int, month:str = f'{datetime.now().strftime("%B")}'):
    data = 0
    try: 
        conn = sqlite3.connect("fret.db")
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM budget WHERE month='{month}' ")
        data = cursor.fetchall()
        conn.close()
        f = open("userinfo.txt", "r")
        salary = int(f.readlines()[1])
        f.close()
    except:
        print("An error occured")
        return False

    if sum([i[2] for i in data]) + new_val > salary:
        print(sum([i[2] for i in data]) + new_val)
        return False
    else:
        return True

@app.command()
def main():
    intro()

@app.command()
def showb():
    display_dash(month)

@app.command()
def abudget(name:str, money:int):
    try:
        conn = sqlite3.connect("fret.db")
        cursor = conn.cursor()
        if check_net_loss(money):
            cursor.execute("INSERT INTO budget VALUES (?,?,?,?)",(name, datetime.now().strftime("%B"), money, date.today().year))
            conn.commit()
        else:
            raise Exception("Your expenses are more than your income thereby causing net-loss, please try again or edit your other budgets")
        conn.close()
    except Exception as e:
        print(e)

@app.command()
def rbudget(title:str, month: str = f'{datetime.now().strftime("%B")}'):
    try:
        conn = sqlite3.connect("fret.db")
        cursor = conn.cursor()
        cursor.execute(f"DELETE from budget WHERE name = '{title}' AND month = '{month}'")
        conn.commit()
        conn.close()
        sprint("[bold green] Budget successfully deleted :recycle:")
    except Exception as e:
        print(e)
if __name__ == "__main__":
    app()

