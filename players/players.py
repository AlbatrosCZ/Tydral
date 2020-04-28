from sqlite3 import *
import os

class players:
    def __init__(self, path = "players/players.db"):
        
        try:
            open(path)

        except:
            raise ValueError("Need to install Players")

        self.path = path
        self.connection = connect(path)
        self.connection.isolation_level = None
        self.curs = self.connection.cursor()
        
        try:
            self.curs.execute("SELECT name FROM sqlite_master WHERE type=\'table\'")
            tryer = self.curs.fetchall()
            need_to = ["players"]
            for i in tryer:
                for j in range(len(need_to)):
                    if i[0] == need_to[j]:
                        del need_to[j]
            if len(need_to) > 0:
                raise ValueError("Need to install Players")
        except:
            raise ValueError("Need to install Players")

    def select(self, table: str, items: list = ["*"], where: str = "1"):
        try:
            self.curs.execute("SELECT {} FROM {} WHERE {}".format(", ".join(items), table, where))
            exitcode = self.curs.fetchall()
            if exitcode == []:
                raise ValueError("Nothing")
            return exitcode
        except:
            return False

    def add(self, nickname, password, typ = "player"):
        path = "players/{}.db".format(nickname)
        try:
            self.curs.execute("""INSERT INTO players(nickname, password, characters) 
        VALUES('{}', '{}', '{}')""".format(nickname, password, path))
        except:
            return False
        try:
            open(path, "w").close()
        except:
            return False

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
        curs.execute("""INSERT INTO info(name, value) VALUES('player_type', '{}')""".format(typ))
        return True

    def remove(self, nickname, password):
        path = self.select("players", ["characters"], "nickname='{}' AND password='{}'".format(nickname, password))
        while type(path) in [list, tuple]:
            path = path[0]
        os.remove(path)
        print("Succesfully remove {}".format(path))

    def get(self, nickname, password):
        data = self.select("players", ["*"], "nickname='{}' AND password='{}'".format(nickname, password))
        return data

    def login(self, nickname, password):
        if self.select("players",where = "nickname = '{}' AND password = '{}'".format(nickname, password)):
            return True
        return False

class Player:
    def __init__(self, nickname, password):
        path = "players/{}.db".format(nickname)
        try:
            open(path)

        except:
            open(path, "w")

        self.path = path
        self.connection = connect(path)
        self.connection.isolation_level = None
        self.curs = self.connection.cursor()
        
        try:
            self.curs.execute("SELECT name FROM sqlite_master WHERE type=\'table\'")
            tryer = self.curs.fetchall()
            need_to = ["characters", "info"]
            for i in tryer:
                for j in range(len(need_to)):
                    if i[0] == need_to[j]:
                        del need_to[j]
            if len(need_to) > 0:
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
        except:
            pass
    
    def add(self, name, class_, race, special):
        lives = class_.lives + race.lives
        mana = class_.lives + race.lives
        exp = 0
        class_special = class_.special
        race_special = race.special
        special_ = ""
        for i in range(7):
            special_ += str(class_special[i] + race_special[i] + special[i]) + "#"
        special = special_[:-1]
        self.curs("""INSERT INTO character(name, maxLives, maxMana, class, race, special, exp)
                                    VALUES('{}', {}, {}, '{}', '{}', '{}' {})""".format(name, lives, mana, class_.name, race.name, special, exp))

    def edit(self, value, new_value, password):
        pass

    def get(self):
        pass
