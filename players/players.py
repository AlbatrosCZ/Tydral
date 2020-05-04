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
        self.nickname = nickname
        self.password = password
        self.characters = []
        

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
                self.curs.execute("""CREATE TABLE info(
                                name VARCHAR PRIMARY KEY,
                                value VARCHAR NOT NULL)""")
                self.curs.execute("""CREATE TABLE character(
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
                                        coins INTEGER NOT NULL)""")
                self.curs.execute("""CREATE TABLE inventory(id_character INTEGER NOT NULL,
                                                       item_name VARCHAR NOT NULL)""")
                self.curs.execute("""CREATE TABLE bonuses(id_character INTEGER NOT NULL,
                                                       bonus_var VARCHAR NOT NULL,
                                                       bonus_value VARCHAR)""")
                self.curs.execute("""INSERT INTO info(name, value) VALUES('nickname', '{}')""".format(nickname))
                self.curs.execute("""INSERT INTO info(name, value) VALUES('password', '{}')""".format(password))
                self.curs.execute("""INSERT INTO info(name, value) VALUES('player_type', '{}')""".format("player"))
        except:
            pass
        self.gen_characters()
    
    def add(self, name, class_, race, special):
        self.curs.execute("SELECT * FROM character WHERE name = '{}'")
        if self.curs.fetchall() != []:
            return False
        lives = class_.lives + race.lives
        mana = class_.lives + race.lives
        exp = 0
        class_special = class_.special
        race_special = race.special
        special_ = ""
        for i in range(7):
            special_ += str(class_special[i] + race_special[i] + special[i]) + "#"
        special = special_[:-1]
        self.curs.execute("""INSERT INTO character(name, maxLives, maxMana, class, race, special, exp, money)
                                    VALUES('{}', {}, {}, '{}', '{}', '{}', {}, {})""".format(name, lives, mana, class_.name, race.name, special, exp, 0))
        return True

    def edit(self, value, new_value, char_name):
        if value != "special":
            self.curs.execute("UPDATE character SET {}={} WHERE name='{}'".format(value, new_value, char_name))
        else:
            self.curs.execute("UPDATE character SET {}='{}' WHERE name='{}'".format(value, new_value, char_name))

    def gen_characters(self):
        self.curs.execute("SELECT name, maxLives, maxMana, class, race, special, exp, money FROM character")
        ret = self.curs.fetchall()
        for i in ret:
            self.characters.append(Character(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]))

    def get_character_by_name(self, name):
        for i in self.characters:
            if i.name == name:
                return i
        return None

    def get_character_from_database(self, name):
        self.curs.execute("SELECT name, maxLives, maxMana, class, race, special, exp, money FROM character WHERE name='{}'".format(name))
        ret = self.curs.fetchall()
        if ret == []:
            return None
        for i in ret:
            self.characters.append(Character(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]))
            return self.characters[-1]

    def get_characters_names(self):
        self.curs.execute("SELECT name FROM character")
        ret = self.curs.fetchall()
        retu = []
        for i in ret:
            retu.append(i[0])
        return retu

class Character:
    def __init__(self, name, maxLives, maxMana, class_, race, special, exp, money):
        self.over_water = [0]
        self.name = name
        self.lives = [int(maxLives), int(maxLives)]
        self.mana = [int(maxMana), int(maxMana)]
        self.class_ = class_
        self.race = race
        self.special = special
        self.exp = int(exp)
        self.special_gen(special)
        self.pozition = []
        self.money = int(money)
        self.actions = [10, 10]
        self.bonuses = []

    def add_bonus(self, bonus):
        self.bonuses.append(bonus)
        if bonus[1] in [1, 2, 4]:
            self.use_bonus(bonus)

    def remove_bonus(self, bonus):
        try:
            if bonus[1] in [2]:
                self.unuse_bonus(bonus)
            self.bonuses.remove(bonus)
        except:
            pass

    def special_gen(self, special):
        special = special.split("#")
        self.special = []
        for i in range(7):
            self.special.append(int(special[i]))
        
    def get_to_save(self):
        ret = ["{}, {}, {}, {}, {}, {}, {}", self.name]
        ret[0].format(self.name, self.lives[1], self.mana[1], self.class_, self.race, "#".join(self.special), self.exp) 
        return

    def pozition_set(self, pozition):
        for i in range(2):
            self.pozition.append(0)
        self.pozition[0] = int(pozition[0]) 
        self.pozition[1] = int(pozition[1])
    
    def up(self, mapa):
        if self.actions[0] <= 0:
            return False
        field = mapa.get_field(self.pozition[0], self.pozition[1]-1)
        if max(self.over_water) ==0:
            if field >= 100:
                self.pozition[1] -= 1
            else:
                return False
        if max(self.over_water) ==1:
            if field >= 50:
                self.pozition[1] -= 1
            else:
                return False
        if max(self.over_water) ==2:
            if field >= 0:
                self.pozition[1] -= 1
            else:
                return False
        if field < 50:
            self.actions[0] -= 2
        elif field < 300:
            pass
        elif field < 410:
            self.actions[0] -= 1
        elif field < 480:
            self.actions[0] -= 2
        elif field <= 500:
            self.actions[0] -= 3
        self.actions[0] -= 1
        

    def down(self, mapa):
        if self.actions[0] <= 0:
            return False
        field = mapa.get_field(self.pozition[0], self.pozition[1]+1)
        if max(self.over_water) ==0:
            if field >= 100:
                self.pozition[1] += 1
            else:
                return False
        if max(self.over_water) ==1:
            if field >= 50:
                self.pozition[1] += 1
            else:
                return False
        if max(self.over_water) ==2:
            if field >= 0:
                self.pozition[1] += 1
            else:
                return False
        if field < 50:
            self.actions[0] -= 2
        elif field < 300:
            pass
        elif field < 410:
            self.actions[0] -= 1
        elif field < 480:
            self.actions[0] -= 2
        elif field <= 500:
            self.actions[0] -= 3
        self.actions[0] -= 1

    def left(self, mapa):
        if self.actions[0] <= 0:
            return False
        field = mapa.get_field(self.pozition[0]-1, self.pozition[1])
        if max(self.over_water) ==0:
            if field >= 100:
                self.pozition[0] -= 1
            else:
                return False
        if max(self.over_water) ==1:
            if field >= 50:
                self.pozition[0] -= 1
            else:
                return False
        if max(self.over_water) ==2:
            if field >= 0:
                self.pozition[0] -= 1
            else:
                return False
        if field < 50:
            self.actions[0] -= 2
        elif field < 300:
            pass
        elif field < 410:
            self.actions[0] -= 1
        elif field < 480:
            self.actions[0] -= 2
        elif field <= 500:
            self.actions[0] -= 3
        self.actions[0] -= 1

    def right(self, mapa):
        if self.actions[0] <= 0:
            return False
        field = mapa.get_field(self.pozition[0]+1, self.pozition[1])
        if max(self.over_water) ==0:
            if field >= 100:
                self.pozition[0] += 1
            else:
                return False
        if max(self.over_water) ==1:
            if field >= 50:
                self.pozition[0] += 1
            else:
                return False
        if max(self.over_water) ==2:
            if field >= 0:
                self.pozition[0] += 1
            else:
                return False
        if field < 50:
            self.actions[0] -= 2
        elif field < 300:
            pass
        elif field < 410:
            self.actions[0] -= 1
        elif field < 480:
            self.actions[0] -= 2
        elif field <= 500:
            self.actions[0] -= 3
        self.actions[0] -= 1
    
    def next_move(self):
        self.actions[0] = self.actions[1]
        for i in self.bonuses:
            if i[1] in [3]:
                self.use_bonus(i)

    def use_bonus(self, bonus):
        if bonus not in self.bonuses:
            return False
        else:
            bonus_pozition = self.bonuses.index(bonus)
        when = bonus[1]
        bonus = bonus[0].split("|")
        get_back = [bonus[0], ]
        for i in bonus[1::]:
            add = True
            i = i.split(" ")

            if i[0] == "add":
                action = +1
            elif i[0] == "remove":
                action = -1
            elif i[0] == "set":
                action = 0

            if i[1] == "mana":
                do_on = [self.mana, 0]
            elif i[1] == "lives":
                do_on = [self.lives, 0]
            elif i[1] == "maxmana":
                do_on = [self.mana, 1]
            elif i[1] == "maxlives":
                do_on = [self.lives, 1]
            elif i[1] == "actions":
                do_on = [self.actions, 1]
            elif i[1] == "waterwalk":
                do_on = ["waterwalk"]
            elif i[1].find("special") != -1:
                do_on = [self.special, i[1][i[1].find("special")+7::]]
                if do_on[1] == "s":
                    do_on[1] = 0 
                elif do_on[1] == "p":
                    do_on[1] = 1
                elif do_on[1] == "e":
                    do_on[1] = 2
                elif do_on[1] == "c":
                    do_on[1] = 3
                elif do_on[1] == "i":
                    do_on[1] = 4
                elif do_on[1] == "a":
                    do_on[1] = 5
                elif do_on[1] == "l":
                    do_on[1] = 6
            elif i[1] == "exp":
                do_on = ["exp"]
            elif i[1] == "money":
                do_on == ["money"]
            elif i[1].find("bonus") != -1:
                do_on = ["self", i[1]]

            try:
                num = int(i[2])
                if len(i) > 3:
                    if i[3] == "+#":
                        num += self.get_level()
                    if i[3] == "*#":
                        num *= self.get_level()
                    if i[3] == "-#":
                        num -= self.get_level()
            except:
                if len(i) < 3:
                    num = "full"
            i = " ".join(i)

            if action != 0 and type(num) == int:
                if action == 1 and num < 0:
                    add = False
                elif action == -1 and num > 0:
                    add = False
                elif type(do_on[0]) != str:
                    do_on[0][do_on[1]] += num
                elif do_on[0] == "exp":
                    self.exp += num
                elif do_on[0] == "money":
                    self.money += num
                elif do_on[0] == "self":
                    res = [i for i in get_back if do_on[1] in i.split(" ")] 
                    if len(res) < 1:
                        add = False
                    else:
                        index = get_back.index(res[0])
                        edit = get_back[index].split(" ")
                        edit[2] = str(int(edit[2]) + num)
                        get_back[index] = " ".join(edit)

            elif action == 0 and type(num) == int:
                if do_on[0] == "waterwalk":
                    if self.over_water < num:
                        self.over_water.append(num)

            elif type(num) == str:
                if action == 0:
                    if do_on[0] == "waterwalk":
                        self.over_water.append(2) 
                elif action == -1:
                    if do_on[0] == "self":
                        res = [i for i in get_back if do_on[1] in i.split(" ")] 
                        if len(res) < 1:
                            add = False
                        else:
                            index = get_back.index(res[0])
                            del get_back[index]

            if add:
                get_back.append(i)
        self.bonuses[bonus_pozition] = ["|".join(get_back), when]

    def unuse_bonus(self, bonus):
        if bonus not in self.bonuses:
            return False
        else:
            bonus_pozition = self.bonuses.index(bonus)
        when = bonus[1]
        bonus = bonus[0].split("|")
        get_back = [bonus[0], ]
        for i in bonus[1::]:
            add = True
            i = i.split(" ")

            if i[0] == "add":
                action = +1
            elif i[0] == "remove":
                action = -1
            elif i[0] == "set":
                action = 0

            if i[1] == "mana":
                do_on = [self.mana, 0]
            elif i[1] == "lives":
                do_on = [self.lives, 0]
            elif i[1] == "maxmana":
                do_on = [self.mana, 1]
            elif i[1] == "maxlives":
                do_on = [self.lives, 1]
            elif i[1] == "actions":
                do_on = [self.actions, 1]
            elif i[1] == "waterwalk":
                do_on = ["waterwalk"]
            elif i[1].find("special") != -1:
                do_on = [self.special, i[1][i[1].find("special")+7::]]
                if do_on[1] == "s":
                    do_on[1] = 0 
                elif do_on[1] == "p":
                    do_on[1] = 1
                elif do_on[1] == "e":
                    do_on[1] = 2
                elif do_on[1] == "c":
                    do_on[1] = 3
                elif do_on[1] == "i":
                    do_on[1] = 4
                elif do_on[1] == "a":
                    do_on[1] = 5
                elif do_on[1] == "l":
                    do_on[1] = 6

            try:
                num = int(i[2])
                if len(i) > 3:
                    if i[3] == "+#":
                        num += self.get_level()
                    if i[3] == "*#":
                        num *= self.get_level()
                    if i[3] == "-#":
                        num -= self.get_level()
            except:
                if len(i) < 3:
                    num = "full"

            if action != 0 and type(num) == int:
                if action == 1 and num < 0:
                    add = False
                elif action == -1 and num > 0:
                    add = False
                elif type(do_on[0]) != str:
                    do_on[0][do_on[1]] -= num

            elif action == 0 and type(num) == int:
                if do_on[0] == "waterwalk":
                    if self.over_water < num:
                        self.over_water.remove(num)

            elif type(num) == str:
                if action == 0:
                    if do_on[0] == "waterwalk":
                        self.over_water.remove(2) 
                



    def can_walk_over_water(self): # 0 = can't over water 1 = low water (light blue) 2 = deep water (dark blue)
        return max(self.over_water)

    def remove_money(self, money):
        if self.money >= money:
            self.money -= money
            return True
        else:
            return False

    def get_level(self):
        if self.exp < 100:
            return 1
        else:
            for i in range(18):
                if self.exp < (2**i)*100:
                    return i + 2
        return 20
