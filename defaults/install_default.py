from sqlite3 import *
from tkinter import *
import os, pickle

class plugin:
    def __init__(self, name, loadable):
        self.plugin_name = name
        self.plugin_races = []
        self.plugin_classes = []
        self.plugin_items = []
        self.plugin_champs = []
        if loadable == 1:
            self.loadable = True
        else:
            self.loadable = False

    def save(self):
        a = open("defaults/"+self.plugin_name + ".def", "wb")
        pickle.dump(self, a)

    def add(self, path):
        connection = connect(path)
        connection.isolation_level = None

        curs = connection.cursor()
        for i in self.plugin_classes:
            name, live, mana, special, can_use_id = i.save_to_database()
            curs.execute("""INSERT INTO class(name, live, mana, special, can_use_id) VALUES('{}', {}, {}, '{}', {})""".format(name, live, mana, special, can_use_id))
        for i in self.plugin_races:
            name, live, mana, special, can_use_id = i.save_to_database()
            curs.execute("""INSERT INTO race(name, live, mana, special, can_use_id) VALUES('{}', {}, {}, '{}', {})""".format(name, live, mana, special, can_use_id))
        for i in self.plugin_items:
            name, rarity, info = i.save_to_database()
            if info:
                curs.execute("""INSERT INTO item(name, rarity, info) VALUES('{}', '{}', '{}')""".format(name, rarity, info))
            else:
                curs.execute("""INSERT INTO item(name, rarity) VALUES('{}', '{}')""".format(name, rarity)) 

    def get_info(self):
        output = []
        output.append(" -----  PLUGIN INFO  ----- ")
        output.append("name: " + self.plugin_name)
        output.append("loadable: {}".format(self.loadable))
        output.append("races: {}".format(len(self.plugin_races)))
        output.append("classes: {}".format(len(self.plugin_classes)))
        output.append("items: {}".format(len(self.plugin_items)))
        output.append(" -----  RACES  ----- ")
        output.append("name, live, mana, special, can_use_id")
        for i in self.plugin_races:
            output.append("{}, {}, {}, {}, {}".format(i.name, i.live, i.mana, i.special, i.can_use_id))
        output.append(" -----  CLASSES ----- ")
        output.append("name, live, mana, special, can_use_id")
        for i in self.plugin_classes:
            output.append("{}, {}, {}, {}, {}".format(i.name, i.live, i.mana, i.special, i.can_use_id))
        output.append(" -----  ITEMS ----- ")
        output.append("name, rarity, info")
        for i in self.plugin_items:
            if i.info:
                output.append("{}, {}, {}".format(i.name, i.rarity, i.info))
            else:
                output.append("{}, {}".format(i.name, i.rarity))
        return output

    def delete_item(self, get_info_id, value):
        print(get_info_id)
        if self.get_info()[get_info_id] in [" -----  RACES  ----- ", " -----  CLASSES ----- ", " -----  ITEMS ----- ", "name, live, mana, special, can_use_id", "name, rarity, info"]:
            return False
        a = self.get_info()[get_info_id].split(",")[0]
        races, classes, items = self.get_info().index(" -----  RACES  ----- "), self.get_info().index(" -----  CLASSES ----- "), self.get_info().index(" -----  ITEMS ----- ")
        if items > get_info_id:
            if classes > get_info_id:
                if races > get_info_id:
                    return False
                else:
                    for i in range(len(self.plugin_races)):
                        if self.plugin_races[i].name == a:
                            del self.plugin_races[i]
                            value.set("New plugin")
                            return True
            else:
                for i in range(len(self.plugin_classes)):
                    if self.plugin_classes[i].name == a:
                        del self.plugin_classes[i]
                        value.set("New plugin")
                        return True
        else:
            for i in range(len(self.plugin_items)):
                if self.plugin_items[i].name == a:
                    del self.plugin_items[i]
                    value.set("New plugin")
                    return True
        return False

    def add_race(self, widgets, value):
        name = widgets["r_name_e"].get()
        live = int(widgets["r_live_s"].get())
        mana = int(widgets["r_mana_s"].get())
        special = "{}#{}#{}#{}#{}#{}#{}".format(int(widgets["r_special_s_s"].get()), int(widgets["r_special_p_s"].get()), int(widgets["r_special_e_s"].get()), int(widgets["r_special_c_s"].get()), int(widgets["r_special_i_s"].get()), int(widgets["r_special_a_s"].get()), int(widgets["r_special_l_s"].get()))
        can_use_id = widgets["r_stren_val"].get() * 8 + widgets["r_agili_val"].get() * 1 + widgets["r_relig_val"].get() * 2 + widgets["r_intel_val"].get() * 4 + 1
        self.plugin_races.append(race(name, live, mana, special, can_use_id))
        value.set("New plugin")

    def add_class(self, widgets, value):
        name = widgets["c_name_e"].get()
        live = widgets["c_live_s"].get()
        mana = widgets["c_mana_s"].get()
        special = "{}#{}#{}#{}#{}#{}#{}".format(int(widgets["c_special_s_s"].get()), int(widgets["c_special_p_s"].get()), int(widgets["c_special_e_s"].get()), int(widgets["c_special_c_s"].get()), int(widgets["c_special_i_s"].get()), int(widgets["c_special_a_s"].get()), int(widgets["c_special_l_s"].get()))
        can_use_id = widgets["c_stren_val"].get() * 8 + widgets["c_agili_val"].get() * 1 + widgets["c_relig_val"].get() * 2 + widgets["c_intel_val"].get() * 4 + 1
        self.plugin_classes.append(class_(name, live, mana, special, can_use_id))
        value.set("New plugin")

    def add_item(self, widgets, value):
        name = widgets["i_name_e"].get()
        rarity = widgets["i_rarity_zl"].cget("text")
        info = widgets["i_info_tf"].get(1.0, END)
        if info in ["", " ", "  ", "   ", "False", "None", "none", "false", "n", "f"]:
            info = False
        self.plugin_items.append(item(name, rarity, info))
        value.set("New plugin")

class race:
    def __init__(self, name, live, mana, special, can_use_id):
        self.name = name
        self.live = live
        self.mana = mana
        self.special = special
        self.can_use_id = can_use_id

    def save_to_database(self):
        return self.name, self.live, self.mana, self.special, self.can_use_id

class class_:
    def __init__(self, name, live, mana, special, can_use_id):
        self.name = name
        self.live = live
        self.mana = mana
        self.special = special
        self.can_use_id = can_use_id
    
    def save_to_database(self):
        return self.name, self.live, self.mana, self.special, self.can_use_id

class item:
    def __init__(self, name, rarity, info):
        self.name = name
        self.rarity = rarity
        self.info = info

    def save_to_database(self):
        return self.name, self.rarity, self.info

def make(root, var):
    path = "defaults/default.db"
    open(path, "w").close()

    connection = connect(path)
    connection.isolation_level = None

    curs = connection.cursor()
    curs.execute("""CREATE TABLE IF NOT EXISTS class(
                                                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                                    name VARCHAR NOT NULL, 
                                                    live INTEGER NOT NULL, 
                                                    mana INTEGER NOT NULL, 
                                                    special VARCHAR NOT NULL, 
                                                    can_use_id INTEGER NOT NULL)""")
    curs.execute("""CREATE TABLE IF NOT EXISTS race(
                                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                    name VARCHAR NOT NULL, 
                                                    live INTEGER NOT NULL, 
                                                    mana INTEGER NOT NULL, 
                                                    special VARCHAR NOT NULL, 
                                                    can_use_id INTEGER NOT NULL)""")
    curs.execute("""CREATE TABLE IF NOT EXISTS item(
                                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                    name VARCHAR NOT NULL, 
                                                    rarity INTEGER NOT NULL, 
                                                    info VARCHAR)""")
    curs.execute("""CREATE TABLE IF NOT EXISTS some_has_bonus(
                                                    some_table VARCHAR NOT NULL, 
                                                    some_id INTEGER NOT NULL, 
                                                    bounus_id INTEGER NOT NULL, 
                                                    special_value VARCHAR,
                                                    duration INTEGER)""") # 1 = use only, 2 = equip and unequip, 3 = evry round where equiped
    curs.execute("""CREATE TABLE IF NOT EXISTS bonus(
                                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                    name VARCHAR NOT NULL, 
                                                    function VARCHAR NOT NULL, 
                                                    special_value INTEGER NOT NULL)""")

    for i in var[0]:

        if i[0].get():
            load_from = open(i[1], "rb")
            plugdef = pickle.load(load_from)
            plugdef.add("defaults/default.db")

    root.destroy()

def list_dir(root, path = "defaults"):
    a = []
    y = 30
    for i in os.listdir(path):
        try:
            if i.split(".")[-1] == "def":
                Label(root, text = i).place(x = 0,y = y)
                a.append([IntVar(root), path + "/" + i])
                Checkbutton(root, variable = a[-1][0], onvalue = 1).place(x = 100, y = y)
                y += 20
        except:
            a1, y = list_dir(path + "/" + i)
            a += a1
    return a, y

def install_default():
    root = Tk()
    root.geometry("50x50+100+100")
    root.title("create default database")

    Label(root, text = "Chose default to install").place(x = 0, y = 0)

    var, y = list_dir(root)

    if y < 100:
        y = 100

    root.maxsize(150, y+50)
    root.minsize(150, y+50)

    entryes = [var]

    Button(root, text = "Finish", command = lambda: make(root, entryes)).place(x = 100, y = y + 10)
    

    root.mainloop()