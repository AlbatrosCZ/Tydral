from sqlite3 import *
from tkinter import *

def make(root, var):
    path = "players/players.db"
    open(path, "w").close()

    connection = connect(path)
    connection.isolation_level = None

    curs = connection.cursor()
    curs.execute("""CREATE TABLE players(nickname VARCHAR PRIMARY KEY, 
                                        password VARCHAR NOT NULL, 
                                        characters VARCHAR NOT NULL)""")
    root.destroy()

    if var[0].get() == 1:
        create_player((curs, path))

def set_to_database(root, curs, var):
    if 1 == len(var[0].get().split("/")) and 1 == len(var[0].get().split(".")):
        path = "players/"+var[0].get()+".db"
        curs[0].execute("""INSERT INTO players(nickname, password, characters) 
        VALUES('{}', '{}', '{}')""".format(var[0].get(), var[1].get(), path))
        root.destroy()
        install_character(path, var[0].get(), var[1].get())
    
def install_character(path, nickname, password):
    open(path, "w").close()

    connection = connect(path)
    connection.isolation_level = None

    curs = connection.cursor()
    curs.execute("""CREATE TABLE info(
                    name VARCHAR PRIMARY KEY,
                    value VARCHAR NOT NULL)""")
    curs.execute("""CREATE TABLE character(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name VARCHAR NOT NULL,
                            maxLives INTEGER NOT NULL,
                            maxMana INTEGER NOT NULL,
                            lives INTEGER,
                            mana INTEGER,
                            class INTEGER NOT NULL,
                            race INTEGER NOT NULL,
                            special VARCHAR NOT NULL,
                            exp INTEGER NOT NULL,
                            coins INTEGER)""")
    curs.execute("""CREATE TABLE inventory(id_character INTEGER NOT NULL,
                                            item_name VARCHAR NOT NULL)""")
    curs.execute("""INSERT INTO info(name, value) VALUES('nickname', '{}')""".format(nickname))
    curs.execute("""INSERT INTO info(name, value) VALUES('password', '{}')""".format(password))
    curs.execute("""INSERT INTO info(name, value) VALUES('player_type', '{}')""".format("player"))


def create_player(cursor): 
    root = Tk()
    root.geometry("300x250+100+100")
    root.title("create player database")
    root.maxsize(300, 150)
    root.minsize(300, 150)

    Label(root, text = "Nickname:").place(x = 10, y = 10)
    Label(root, text = "Password:").place(x = 10, y = 50)

    name = StringVar()
    password = StringVar()
    Entry(root, textvariable = name).place(x = 100, y = 10)
    Entry(root, textvariable = password).place(x = 100, y = 50)

    entryes = [name, password]

    Button(root, text = "Finish", command = lambda: set_to_database(root, cursor, entryes)).place(x = 200, y = 100)
    Button(root, text = "Stop", command = lambda: root.destroy()).place(x = 165, y = 100)

    root.mainloop()


def install_players():
    root = Tk()
    root.geometry("300x250+100+100")
    root.title("create player database")
    root.maxsize(300, 100)
    root.minsize(300, 100)

    Label(root, text = "Create Player when Install:").place(x = 10, y = 10)

    add = IntVar() 
    add.set(0)
    Checkbutton(root, text="", variable = add, onvalue = 1).place(x = 200, y = 10)

    entryes = [add]

    Button(root, text = "Finish", command = lambda: make(root, entryes)).place(x = 200, y = 50)
    Button(root, text = "Stop", command = lambda: root.destroy()).place(x = 165, y = 50)

    root.mainloop()