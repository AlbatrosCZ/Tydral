from sqlite3 import *
from app.classes import *

class default:
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
            need_to_counter = len(need_to)
            for i in tryer:
                for j in range(len(need_to)):
                    if i[0] == need_to[j]:
                        need_to_counter -= 1
            if need_to_counter > 0:
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
                                                                damage VARCHAR NOT NULL, 
                                                                rarity INTEGER NOT NULL, 
                                                                info VARCHAR,
                                                                picture VARCHAR)""")
                self.curs.execute("""CREATE TABLE IF NOT EXISTS some_has_bonus(
                                                                some_table VARCHAR NOT NULL, 
                                                                some_id INTEGER NOT NULL, 
                                                                bounus_id INTEGER NOT NULL, 
                                                                special_value VARCHAR,
                                                                duration INTEGER)""") # 1 = use only, 2 = equip and unequip, 3 = evry round where equiped, 4 = Level up
                self.curs.execute("""CREATE TABLE IF NOT EXISTS bonus(
                                                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                name VARCHAR NOT NULL, 
                                                                function VARCHAR NOT NULL, 
                                                                special_value INTEGER NOT NULL)""")
                self.curs.execute("""CREATE TABLE IF NOT EXISTS mission(
                                                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                name VARCHAR NOT NULL, 
                                                                todo VARCHAR, 
                                                                price VARCHAR NOT NULL,
                                                                open VARCHAR NOT NULL)""")
        except LookupError as error:
            raise ValueError("Need to install Defaults", error)
        self.gen_classes()
        self.gen_races()
        self.gen_items()
        self.gen_missions()


    def select(self, table: str, items: list = ["*"], where: str = "1"):
        try:
            self.curs.execute("SELECT {} FROM {} WHERE {}".format(", ".join(items), table, where))
            exitcode = self.curs.fetchall()
            if exitcode == []:
                raise ValueError("Nothing")
            return exitcode
        except:
            return False

    def gen_classes(self):
        self.classes = []
        classes = self.select("class", ["name", "live", "mana", "special", "can_use_id", "id"])
        if classes:
            for i in classes:
                self.classes.append(default_class(i[0], i[1], i[2], i[3], i[4], i[5]))

    def gen_races(self):
        self.races = []
        races = self.select("race", ["name", "live", "mana", "special", "can_use_id", "id"])
        if races:
            for i in races:
                self.races.append(default_race(i[0], i[1], i[2], i[3], i[4], i[5]))

    def gen_items(self):
        self.items = []
        items = self.select("item", ["name", "damage", "rarity", "info", "picture", "id"])
        if items:
            for i in items:
                self.items.append(default_item(i[0], i[1], i[2], i[3], i[4], i[5]))

    def gen_missions(self):
        self.missions = []
        missions = self.select("item", ["name", "price", "todo", "open"])
        if missions:
            for i in missions:
                self.missions.append(default_mission(i[0], i[1], i[2], i[3]))

    def get_class(self, identificator):
        if type(identificator) == str:
            for i in self.classes:
                if i.name == identificator:
                    return i
        elif type(identificator) == int:
            for i in self.classes:
                if i.database_id == identificator:
                    return i
        return False

    def get_race(self, identificator):
        if type(identificator) == str:
            for i in self.races:
                if i.name == identificator:
                    return i
        elif type(identificator) == int:
            for i in self.races:
                if i.database_id == identificator:
                    return i
        return False

    def get_races_names(self, classe):
        ret = []
        classe = self.get_class(classe[0])
        for i in self.races:
            if classe.try_compatibility(i):
                ret.append(i.name)
        return ret

    def get_classes_names(self):
        ret = []
        for i in self.classes:
            ret.append(i.name)
        return ret

class default_class:
    def __init__(self, name, live, mana, special, can_use_id, database_id):
        self.name = name
        self.lives = int(live)
        self.mana = int(mana)
        self.database_id = int(database_id)
        self.special_gen(special)
        self.can_use_id_gen(can_use_id)

    def can_use_id_gen(self, can_use_id):
        can_use = []
        can_use_id -= 1
        for i in range(4):
            if can_use_id%2 == 1:
                can_use.append(1)
            else:
                can_use.append(0)
            can_use_id = int(can_use_id / 2)
        self.streng = can_use[3]
        self.inteligence = can_use[2]
        self.religion = can_use[1]
        self.agility = can_use[0]

    def special_gen(self, special):
        special = special.split("#")
        self.special = []
        for i in range(7):
            self.special.append(int(special[i]))

    def try_compatibility(self, race):
        if self.streng:
            if not race.streng:
                return False
        if self.inteligence:
            if not race.inteligence:
                return False
        if self.religion:
            if not race.religion:
                return False
        if self.agility:
            if not race.agility:
                return False
        return True

class default_race:
    def __init__(self, name, live, mana, special, can_use_id, database_id):
        self.name = name
        self.lives = int(live)
        self.mana = int(mana)
        self.database_id = int(database_id)
        self.special_gen(special)
        self.can_use_id_gen(can_use_id)

    def can_use_id_gen(self, can_use_id):
        can_use = []
        can_use_id -= 1
        for i in range(4):
            if can_use_id%2 == 1:
                can_use.append(1)
            else:
                can_use.append(0)
            can_use_id = int(can_use_id / 2)
        self.streng = can_use[3]
        self.inteligence = can_use[2]
        self.religion = can_use[1]
        self.agility = can_use[0]

    def special_gen(self, special):
        special = special.split("#")
        self.special = []
        for i in range(7):
            self.special.append(int(special[i]))

class default_item:
    def __init__(self, name, damage, rarity, info, picture, database_id):
        self.name = name
        self.damage = damage
        self.rarity = int(rarity)
        self.info = info
        self.picture = picture
        self.database_id = int(database_id)

    def get_rarity_name(self):
        raritis = {0:"Normal", 1:"Rare", 2:"Special", 3:"Ledendary", 4:"Divinaly", 5:"Tydralable"}
        return raritis[self.rarity]

    def gen_damage(self):
        damage = self.damage.split("/")
        self.damage = []
        for i in damage:
            self.damage.append(int(i))

class default_mission:
    def __init__(self, name, price, to_do, mopen = None):
        self.name = name
        try:
            self.price = int(price)
        except:
            self.pricer(price)
        self.maker(to_do)
        if mopen != None:
            self.mopen = mopen
        else:
            self.mopen = None
    
    def get(self, character):
        self.character = character
        for i in self.to_do:
            if i[0] == "goto":
                if i[1] == "now":
                    i[1] = character.pozition[0]
                if i[2] == "now":
                    i[2] = character.pozition[1]

    def maker(self, to_do):
        self.to_do = []
        to_do = to_do.split("|")
        for i in to_do:
            i = i.split(" ")
            if i[0] == "goto":
                if i[1] == "#":
                    x = rand.randint(0,1024)
                    y = rand.randint(0,1024)
                else:
                    x, y = i[1].split(",")
                    try:
                        x = x.split("-")
                        x = rand.randint(int(x[0]), int(x[1]))
                    except:
                        x = int(x)
                    try:
                        y = y.split("-")
                        y = rand.randint(int(y[0]), int(y[1]))
                    except:
                        y = int(y)
                self.to_do.append(["goto", x, y, False])
            
            elif i[0] == "fightwith":
                name= i[1]
                lives = [int(i[2]), int(i[3])]
                mana = [int(i[4]), int(i[5])] 
                attacks = i[6::]
                self.to_do.append(["fight", name, lives, mana, attacks, False])
            
            elif i[0] == "goback":
                self.to_do.append(["goto", "now", "now", False])
            
            elif i[0] == "takeprice":
                self.to_do.append(["take", False])

            elif i[0] == "giveme":
                self.to_do.append(["give", i[1], False])
                
    def tryer(self, fight="no"):
        for i in range(len(self.to_do)):
            if not self.to_do[i][-1]:
                if self.to_do[i-1][0] == "goto":
                    if not self.to_do[i-1][1] == self.character.pozition[0] or not self.to_do[i-1][2] == self.character.pozition[1]:
                        self.to_do[i-1][-1] = False
                        return self.to_do[i-1]
                if self.to_do[i][0] == "goto":
                    if self.to_do[i][1] == self.character.pozition[0] and self.to_do[i][2] == self.character.pozition[1]:
                        self.to_do[i][-1] = True
                        return self.tryer()
                if self.to_do[i][0] == "fight":
                    if fight == "no":
                        return self.to_do[i]
                    elif fight == "win":
                        self.to_do[i][-1] = True 
                        return self.tryer()         
                if self.to_do[i][0] == "give":
                    if self.to_do[i][1] in self.character.inventory:
                        del self.character.inventory[self.character.inventory.index(self.to_do[i][1])]
                        self.to_do[i][-1] = True
                        return self.tryer()
                    else:
                        return self.to_do[i]
                if self.to_do == "take":
                    self.take(self.character)
                    self.to_do == True 
                    return True
        return True
        
    def pricer(self, price):
        self.price = []
        price = price.split["|"]
        for i in price:
            i = i.split[" "]
            num = int(i[0])
            if i[1] == "coins":
                self.price.append(["coins", num])
            elif i[1] == "maxlives":
                self.price.append(["maxlives", num])
            elif i[1] == "maxmana":
                self.price.append(["maxmana", num])
            elif i[1] == "exp":
                self.price.append("exp", num)
    
    def take(self, character):
        for i in self.price:
            if i[0] == "coins":
                character.money += i[1]
            elif i[0] == "maxlives":
                character.lives[1] += i[1]
                character.lives[0] += i[1]
            elif i[0] == "manalives":
                character.mana[1] += i[1]
                character.mana[0] += i[1]
            elif i[0] == "exp":
                character.exp += i[1]
        if self.mopen != None:
            self.mopen = self.mopen.split(",")
