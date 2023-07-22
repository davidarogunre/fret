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
    # Let's imagine this is a web API, not a range()
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
    
    names = [i[0] for i in data]     
    other_name = ["Discretionary Income"]
    final_names = names + other_name
    values = [i[2] for i in data]
    total = sum(values)
    percents = [round((i/salary)*100, 1) for i in values]
    other_percent = [100-sum(percents)]
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

def check_net_loss():
    pass

@app.command()
def main():
    intro()

@app.command()
def showb(month:str = f'{datetime.now().strftime("%B")}'):
    display_dash(month)

@app.command()
def abudget(name:str, money:int):
    try:
        conn = sqlite3.connect("fret.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO budget VALUES (?,?,?,?)",(name, datetime.now().strftime("%B"), money, date.today().year))
        conn.commit()
        conn.close()
    except sqlite3.OperationalError as e:
        print(e)

if __name__ == "__main__":
    app()

