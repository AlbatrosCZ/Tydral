from sqlite3 import *
from app.classes import *

class setting:
    def __init__(self, path = "defaults/default.db"):
        
        try:
            open(path)

        except:
            open(path, "w").close()

            connection = connect(path)
            connection.isolation_level = None

        self.path = path
        self.connection = connect(path)
        self.connection.isolation_level = None
        self.curs = self.connection.cursor()
        
        try:
            self.curs.execute(
            "SELECT name FROM sqlite_master WHERE type=\'table\'")
            tryer = self.curs.fetchall()
            need_to = ["class", "race", "item", "some_has_bonus", "bonus"]
            for i in tryer:
                for j in range(len(need_to)):
                    if i[0] == need_to[j]:
                        del need_to[j]
            if len(need_to) > 0:
                self.curs.execute("""CREATE TABLE IF NOT EXISTS class(
                                                                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                                                name VARCHAR NOT NULL, 
                                                                live INTEGER NOT NULL, 
                                                                mana INTEGER NOT NULL, 
                                                                special VARCHAR NOT NULL, 
                                                                can_use_id INTEGER NOT NULL)""")
                self.curs.execute("""CREATE TABLE IF NOT EXISTS race(
                                                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                name VARCHAR NOT NULL, 
                                                                live INTEGER NOT NULL, 
                                                                mana INTEGER NOT NULL, 
                                                                special VARCHAR NOT NULL, 
                                                                can_use_id INTEGER NOT NULL)""")
                self.curs.execute("""CREATE TABLE IF NOT EXISTS item(
                                                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                name VARCHAR NOT NULL, 
                                                                rarity INTEGER NOT NULL, 
                                                                info VARCHAR)""")
                self.curs.execute("""CREATE TABLE IF NOT EXISTS some_has_bonus(
                                                                some_table VARCHAR NOT NULL, 
                                                                some_id INTEGER NOT NULL, 
                                                                bounus_id INTEGER NOT NULL, 
                                                                special_value VARCHAR,
                                                                duration INTEGER)""") # 1 = use only, 2 = equip and unequip, 3 = evry round where equiped
                self.curs.execute("""CREATE TABLE IF NOT EXISTS bonus(
                                                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                name VARCHAR NOT NULL, 
                                                                function VARCHAR NOT NULL, 
                                                                special_value INTEGER NOT NULL)""")
        except:
            raise ValueError("Need to install Defaults")


    def select(self, table: str, items: list = ["*"], where: str = "1"):
        try:
            self.curs.execute("SELECT {} FROM {} WHERE {}".format(", ".join(items), table, where))
            exitcode = self.curs.fetchall()
            if exitcode == []:
                raise ValueError("Nothing")
            return exitcode
        except:
            return False

    def 