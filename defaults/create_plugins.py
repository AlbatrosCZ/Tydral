import pickle
from sqlite3 import *
from tkinter import *

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

def delete_item(widget, value):
    global default 
    default.delete_item(widget.curselection()[0], value)

def create_plugin(widgets, value):
    global default
    default = plugin(widgets["name_e"].get(), widgets["loadable_v"].get())
    value.set("New plugin")

def widget_set_text(widget1, widget2, widget3, text = {}, minimal = None, maximal = None):
    widget_set(widget1, widget2, minimal, maximal)
    widget3.config(text = text[widget1.get()])

def widget_set(widget1, widget2, minimal = None, maximal = None):
    value = widget1.get()
    if minimal != None and maximal != None:
        if minimal > value:
            value = minimal
        elif maximal < value:
            value = maximal 
    elif minimal == None:
        if maximal < value:
            value = maximal 
    elif maximal == None:
        if minimal > value:
            value = minimal 
    widget2.set(value)
    widget1.set(value)

def load_def(widgets, value):
    global default
    path = "defaults/" + widgets["load_e"].get() + ".def"
    load_from = open(path, "rb")
    default = pickle.load(load_from)
    value.set("New plugin")

def change(value, root, widgets = {}):
    global default
    step = value.get()
    for i in widgets.keys():
        try:
            widgets[i].place_forget()
        except:
            try:
                widgets[i][0].place_forget()
                widgets[i][1].pack_forget()
                widgets[i][2].pack_forget()
            except:
                pass 

    if step == "Program Info":
        if "info" not in widgets.keys():
            widgets["info"] = Text(root, state=NORMAL)
            widgets["info"].insert(END, """Version 1.0.0 Beta
This Version have:
New Plugin
New Race
New Class
New Item
Load Old Loadabel Plugin""")
            widgets["info"].config(state=DISABLED) 

        widgets["info"].place(x = 5, y = 50)


    elif step == "New plugin":
        if "name_e" not in widgets.keys():
            widgets["name_e"] = Entry(root)
        if "name_l" not in widgets.keys():
            widgets["name_l"] = Label(root, text = "Plugin name:")
        if "loadable_l" not in widgets.keys():
            widgets["loadable_l"] = Label(root, text = "Loadable:")
            widgets["loadable_v"] = IntVar(root)
            widgets["loadable_c"] = Checkbutton(root, variable = widgets["loadable_v"], onvalue = 1, offvalue = 0)
            widgets["loadable_v"].set(1)
        if "create_p" not in widgets.keys():
            widgets["create_p"] = Button(root, command = lambda: create_plugin(widgets, value), text = "Create")
        if "info_frame" not in widgets.keys():
            widgets["info_frame"] = [Frame(root, width = 20, height = 20), Scrollbar(root, orient=VERTICAL)]
            widgets["info_frame"].append(Listbox(root, height = 20, width = 50, yscrollcommand=widgets["info_frame"][1].set))

            widgets["info_frame"][1].config(command = widgets["info_frame"][2].yview)
            widgets["info_frame"][2].bind("<Double-Button-1>", lambda a = "": delete_item(widgets["info_frame"][2], value))
        if "save" not in widgets.keys():
            widgets["save"] = Button(root, text = "Save")
            
        if default != None:
            widgets["info_frame"][2].delete(0, END)
            for i in default.get_info():
                widgets["info_frame"][2].insert(END, i)
            widgets["save"].config(command = default.save)
            widgets["save"].place(x = 0, y = 110)

        widgets["info_frame"][1].pack(side = "right", fill="y")
        widgets["info_frame"][2].pack(side = "left", fill="x")
        widgets["info_frame"][0].pack(fill=None, expand=False)
        widgets["create_p"].place(x = 250, y = 50)
        widgets["name_l"].place(x = 0, y = 50)
        widgets["name_e"].place(x = 100, y = 50)
        widgets["loadable_l"].place(x = 0, y = 80)
        widgets["loadable_c"].place(x = 100, y = 80)


    elif step == "New race":
        if "r_name_l" not in widgets.keys():
            widgets["r_name_l"] = Label(root, text = "Race name:")
            widgets["r_name_e"] = Entry(root)
        if "r_live_l" not in widgets.keys():
            widgets["r_live_l"] = Label(root, text = "Race Lives:")
            widgets["r_live_s"] = Spinbox(root, from_ = 0, to = 500)
        if "r_mana_l" not in widgets.keys():
            widgets["r_mana_l"] = Label(root, text = "Race Mana:")
            widgets["r_mana_s"] = Spinbox(root, from_ = 0, to = 500)
        if "r_special_s_l" not in widgets.keys():
            widgets["r_special_s_l"] = Label(root, text = "Stenght:")
            widgets["r_special_p_l"] = Label(root, text = "Perception:")
            widgets["r_special_e_l"] = Label(root, text = "Endurence:")
            widgets["r_special_c_l"] = Label(root, text = "Charism:")
            widgets["r_special_i_l"] = Label(root, text = "Inteligence:")
            widgets["r_special_a_l"] = Label(root, text = "Agility:")
            widgets["r_special_l_l"] = Label(root, text = "Luck:")
            widgets["r_special_s_s"] = Spinbox(root, from_ = 0, to = 3)
            widgets["r_special_p_s"] = Spinbox(root, from_ = 0, to = 3)
            widgets["r_special_e_s"] = Spinbox(root, from_ = 0, to = 3)
            widgets["r_special_c_s"] = Spinbox(root, from_ = 0, to = 3)
            widgets["r_special_i_s"] = Spinbox(root, from_ = 0, to = 3)
            widgets["r_special_a_s"] = Spinbox(root, from_ = 0, to = 3)
            widgets["r_special_l_s"] = Spinbox(root, from_ = 0, to = 3)
        if "r_stren_l" not in widgets.keys():
            widgets["r_stren_l"] = Label(root, text = "Can use class with streng:")
            widgets["r_stren_val"] = IntVar(root)
            widgets["r_stren_c"] = Checkbutton(root, variable = widgets["r_stren_val"], offvalue = 0, onvalue = 1)
        if "r_agili_l" not in widgets.keys():
            widgets["r_agili_l"] = Label(root, text = "Can use class with agility:")
            widgets["r_agili_val"] = IntVar(root)
            widgets["r_agili_c"] = Checkbutton(root, variable = widgets["r_agili_val"], offvalue = 0, onvalue = 1)
        if "r_relig_l" not in widgets.keys():
            widgets["r_relig_l"] = Label(root, text = "Can use class with religion:")
            widgets["r_relig_val"] = IntVar(root)
            widgets["r_relig_c"] = Checkbutton(root, variable = widgets["r_relig_val"], offvalue = 0, onvalue = 1)
        if "r_intel_l" not in widgets.keys():
            widgets["r_intel_l"] = Label(root, text = "Can use class with inteligence:")
            widgets["r_intel_val"] = IntVar(root)
            widgets["r_intel_c"] = Checkbutton(root, variable = widgets["r_intel_val"], offvalue = 0, onvalue = 1)
        if "r_add" not in widgets.keys():
            widgets["r_add"] = Button(root, text = "Add", command = lambda: default.add_race(widgets, value))


        widgets["r_stren_val"].set(1)
        widgets["r_agili_val"].set(1)
        widgets["r_relig_val"].set(1)
        widgets["r_intel_val"].set(1)


        widgets["r_name_l"].place(x = 0, y = 50)
        widgets["r_name_e"].place(x = 100, y = 50)
        widgets["r_live_l"].place(x = 0, y = 80)
        widgets["r_live_s"].place(x = 100, y = 80)
        widgets["r_mana_l"].place(x = 0, y = 110)
        widgets["r_mana_s"].place(x = 100, y = 110)
        widgets["r_special_s_l"].place(x = 0, y = 140)
        widgets["r_special_p_l"].place(x = 0, y = 170)
        widgets["r_special_e_l"].place(x = 0, y = 200)
        widgets["r_special_c_l"].place(x = 0, y = 230)
        widgets["r_special_i_l"].place(x = 0, y = 260)
        widgets["r_special_a_l"].place(x = 0, y = 290)
        widgets["r_special_l_l"].place(x = 0, y = 320)
        widgets["r_special_s_s"].place(x = 120, y = 140)
        widgets["r_special_p_s"].place(x = 120, y = 170)
        widgets["r_special_e_s"].place(x = 120, y = 200)
        widgets["r_special_c_s"].place(x = 120, y = 230)
        widgets["r_special_i_s"].place(x = 120, y = 260)
        widgets["r_special_a_s"].place(x = 120, y = 290)
        widgets["r_special_l_s"].place(x = 120, y = 320)
        widgets["r_stren_l"].place(x = 0, y = 350)
        widgets["r_stren_c"].place(x = 250, y = 350)
        widgets["r_agili_l"].place(x = 0, y = 380)
        widgets["r_agili_c"].place(x = 250, y = 380)
        widgets["r_relig_l"].place(x = 0, y = 410)
        widgets["r_relig_c"].place(x = 250, y = 410)
        widgets["r_intel_l"].place(x = 0, y = 440)
        widgets["r_intel_c"].place(x = 250, y = 440)
        widgets["r_add"].place(x = 200, y = 470)


    elif step == "New class":
        if "c_name_l" not in widgets.keys():
            widgets["c_name_l"] = Label(root, text = "Class name:")
            widgets["c_name_e"] = Entry(root)
        if "c_live_l" not in widgets.keys():
            widgets["c_live_l"] = Label(root, text = "Class Lives:")
            widgets["c_live_s"] = Spinbox(root, from_ = 0, to = 100)
        if "c_mana_l" not in widgets.keys():
            widgets["c_mana_l"] = Label(root, text = "Class Mana:")
            widgets["c_mana_s"] = Spinbox(root, from_ = 0, to = 100)
        if "c_special_s_l" not in widgets.keys():
            widgets["c_special_s_l"] = Label(root, text = "Stenght:")
            widgets["c_special_p_l"] = Label(root, text = "Perception:")
            widgets["c_special_e_l"] = Label(root, text = "Endurence:")
            widgets["c_special_c_l"] = Label(root, text = "Charism:")
            widgets["c_special_i_l"] = Label(root, text = "Inteligence:")
            widgets["c_special_a_l"] = Label(root, text = "Agility:")
            widgets["c_special_l_l"] = Label(root, text = "Luck:")
            widgets["c_special_s_s"] = Spinbox(root, from_ = 0, to = 1)
            widgets["c_special_p_s"] = Spinbox(root, from_ = 0, to = 1)
            widgets["c_special_e_s"] = Spinbox(root, from_ = 0, to = 1)
            widgets["c_special_c_s"] = Spinbox(root, from_ = 0, to = 1)
            widgets["c_special_i_s"] = Spinbox(root, from_ = 0, to = 1)
            widgets["c_special_a_s"] = Spinbox(root, from_ = 0, to = 1)
            widgets["c_special_l_s"] = Spinbox(root, from_ = 0, to = 1)
        if "c_stren_l" not in widgets.keys():
            widgets["c_stren_l"] = Label(root, text = "Can use class with streng:")
            widgets["c_stren_val"] = IntVar(root)
            widgets["c_stren_c"] = Checkbutton(root, variable = widgets["c_stren_val"], offvalue = 0, onvalue = 1)
        if "c_agili_l" not in widgets.keys():
            widgets["c_agili_l"] = Label(root, text = "Can use class with agility:")
            widgets["c_agili_val"] = IntVar(root)
            widgets["c_agili_c"] = Checkbutton(root, variable = widgets["c_agili_val"], offvalue = 0, onvalue = 1)
        if "c_relig_l" not in widgets.keys():
            widgets["c_relig_l"] = Label(root, text = "Can use class with religion:")
            widgets["c_relig_val"] = IntVar(root)
            widgets["c_relig_c"] = Checkbutton(root, variable = widgets["c_relig_val"], offvalue = 0, onvalue = 1)
        if "c_intel_l" not in widgets.keys():
            widgets["c_intel_l"] = Label(root, text = "Can use class with inteligence:")
            widgets["c_intel_val"] = IntVar(root)
            widgets["c_intel_c"] = Checkbutton(root, variable = widgets["c_intel_val"], offvalue = 0, onvalue = 1)
        if "c_add" not in widgets.keys():
            widgets["c_add"] = Button(root, text = "Add", command = lambda: default.add_class(widgets, value))


        widgets["c_stren_val"].set(1)
        widgets["c_agili_val"].set(1)
        widgets["c_relig_val"].set(1)
        widgets["c_intel_val"].set(1)


        widgets["c_name_l"].place(x = 0, y = 50)
        widgets["c_name_e"].place(x = 100, y = 50)
        widgets["c_live_l"].place(x = 0, y = 80)
        widgets["c_live_s"].place(x = 100, y = 80)
        widgets["c_mana_l"].place(x = 0, y = 110)
        widgets["c_mana_s"].place(x = 100, y = 110)
        widgets["c_special_s_l"].place(x = 0, y = 140)
        widgets["c_special_p_l"].place(x = 0, y = 170)
        widgets["c_special_e_l"].place(x = 0, y = 200)
        widgets["c_special_c_l"].place(x = 0, y = 230)
        widgets["c_special_i_l"].place(x = 0, y = 260)
        widgets["c_special_a_l"].place(x = 0, y = 290)
        widgets["c_special_l_l"].place(x = 0, y = 320)
        widgets["c_special_s_s"].place(x = 120, y = 140)
        widgets["c_special_p_s"].place(x = 120, y = 170)
        widgets["c_special_e_s"].place(x = 120, y = 200)
        widgets["c_special_c_s"].place(x = 120, y = 230)
        widgets["c_special_i_s"].place(x = 120, y = 260)
        widgets["c_special_a_s"].place(x = 120, y = 290)
        widgets["c_special_l_s"].place(x = 120, y = 320)
        widgets["c_stren_l"].place(x = 0, y = 350)
        widgets["c_stren_c"].place(x = 250, y = 350)
        widgets["c_agili_l"].place(x = 0, y = 380)
        widgets["c_agili_c"].place(x = 250, y = 380)
        widgets["c_relig_l"].place(x = 0, y = 410)
        widgets["c_relig_c"].place(x = 250, y = 410)
        widgets["c_intel_l"].place(x = 0, y = 440)
        widgets["c_intel_c"].place(x = 250, y = 440)
        widgets["c_add"].place(x = 200, y = 470)


    elif step == "New item":
        if "i_name_l" not in widgets.keys():
            widgets["i_name_l"] = Label(root, text = "Item Name:")
            widgets["i_name_e"] = Entry(root)
        if "i_rarity_l" not in widgets.keys():
            to_text = {1:"Normal", 2:"Rare", 3:"Legendary", 4:"Special", 5:"Tydralable"}
            widgets["i_rarity_l"] = Label(root, text = "Item Rarity:")
            widgets["i_rarity_zl"] = Label(root, text = "")
            widgets["i_rarity_s"] = Scale(root, from_ = 1, to = 5, orient = HORIZONTAL)
            widgets["i_rarity_v"] = DoubleVar()
            widgets["i_rarity_v"].trace("w", lambda a = "", b = "", c = "": widget_set_text(widgets["i_rarity_v"], widgets["i_rarity_s"], widgets["i_rarity_zl"], to_text, 1, 5))
            widgets["i_rarity_s"].config(command = lambda a = "", b = "", c = "": widget_set_text(widgets["i_rarity_s"], widgets["i_rarity_v"], widgets["i_rarity_zl"], to_text, 1, 5))
            widgets["i_rarity_v"].set(1)
        if "i_info_l" not in widgets.keys():
            widgets["i_info_l"] = Label(root, text = "Description:")
            widgets["i_info_tf"] = Text(root, width = 35)
        if "i_add" not in widgets.keys():
            widgets["i_add"] = Button(root, text = "Add", command = lambda: default.add_item(widgets, value))

        widgets["i_name_l"].place(x = 10, y = 50)
        widgets["i_name_e"].place(x = 150, y = 50)
        widgets["i_rarity_l"].place(x = 10, y = 80)
        widgets["i_rarity_zl"].place(x = 220, y = 100)
        widgets["i_rarity_s"].place(x = 100, y = 80)
        widgets["i_info_l"].place(x = 10, y = 140)
        widgets["i_info_tf"].place(x = 80, y = 140)
        widgets["i_add"].place(x = 300, y = 550)

    elif step == "Load plugin":
        if "load_l" not in widgets.keys():
            widgets["load_l"] = Label(root, text = "Path:")
            widgets["load_e"] = Entry(root)
        if "load_add" not in widgets.keys():
            widgets["load_add"] = Button(root, text = "Load", command = lambda: load_def(widgets, value))

        widgets["load_l"].place(x = 0, y = 50)
        widgets["load_e"].place(x = 100, y = 50)
        widgets["load_add"].place(x = 150, y = 80)
        


default = None

root = Tk()
root.title("Default Editor Defaults")
root.minsize(400, 600)
root.maxsize(400, 600)

items = [
    "Program Info",
    "New plugin",
    "New race",
    "New class",
    "New item",
    "Load plugin"
]

value = StringVar(root)
value.trace("w", lambda a = "", b = "", c = "": change(value, root))
value.set(items[0]) 

w = OptionMenu(root, value, *items)
w.place(x = 0, y = 0)

root.mainloop()