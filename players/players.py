from sqlite3 import *

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

    def add(self, nickname, password):
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
                                exp INTEGER NOT NULL)""")
        return True

    def remove(self):
        pass

    def get(self):
        pass

    def edit(self):
        pass

    def login(self, nickname, password):
        if self.select("players",where = "nickname = '{}' AND password = '{}'".format(nickname, password)):
            return True
        return False

class Player:
    def __init__(self, path):
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
            need_to = ["characters"]
            for i in tryer:
                for j in range(len(need_to)):
                    if i[0] == need_to[j]:
                        del need_to[j]
            if len(need_to) > 0:
                self.curs.execute("""CREATE TABLE character(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name VARCHAR NOT NULL,
                                maxLives INTEGER NOT NULL,
                                maxMana INTEGER NOT NULL,
                                lives INTEGER,
                                mana INTEGER,
                                class VARCHAR NOT NULL,
                                race VARCHAR NOT NULL,
                                special VARCHAR NOT NULL,
                                exp INTEGER NOT NULL,
                                map INTEGER)""")
        except:
            pass
    
    def add(self, name, class_, race, special):
        lives = 0
        mana = 0
        exp = 0
        special = "0#0#0#0#0#0#0"
        self.curs("""INSERT INTO character(name, maxLives, maxMana, class, race, special, exp)
                                    VALUES('{}', {}, {}, '{}', '{}', '{}' {})""".format(name, lives, mana, class_.name, race.name, special, exp))

    def edit(self):
        pass

    def get(self):
        pass
