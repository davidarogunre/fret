import sqlite3



def new_user_db_initiate(conn, name, month, money,  year):
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE budget (name TEXT, month TEXT, money INTEGER, year INTEGER)")
#     create_table = '''CREATE TABLE budget(
#     NAME CHAR(200) NOT NULL,
#    MONTH CHAR(9),
#    MONEY INT,
#    YEAR INT
# )''' 
#     params =  (name, month, int(money), int(year))
#     cursor.execute(create_table)
    cursor.execute("INSERT INTO budget VALUES (?,?,?,?)",(name, month, money, year))
    conn.commit()

   
# def get_dashboard_info():
#     pass

