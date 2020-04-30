class race:
    def __init__(self, name, live, mana, special, can_use_id):
        self.name = name
        self.live = live
        self.mana = mana
        self.special = special
        self.can_use_id = can_use_id

class class_:
    def __init__(self, name, live, mana, special, can_use_id):
        self.name = name
        self.live = live
        self.mana = mana
        self.special = special
        self.can_use_id = can_use_id

class item:
    def __init__(self, name, rarity, info):
        self.name = name
        self.rarity = rarity
        self.info = info

class map_:
    def __init__(self, name, map_list, places_list):
        self.name = name
        self.map_list = map_list
        self.places_list = places_list

    def get_field(self, x, y):
        if "{},{}".format(x,y) in self.places_list.keys():
            return 1025
        else:
            return self.map_list[y][x]

    def set_field(self, x, y, add):
        if "{},{}".format(x,y) not in self.places_list.keys():
            self.map_list[y][x] += add
            if self.map_list[y][x] > 500:
                self.map_list[y][x] = 500
            elif self.map_list[y][x] < 0:
                self.map_list[y][x] = 0

class town:
    def __init__(self, name, town_map, come_price, lead_race, buildings):
        self.name = name
        self.town_map = town_map
        self.come_price = come_price
        self.lead_race = lead_race
        self.buildings = buildings

class village(town):
    def __init__(self, name, village_map, lead_race, buildings):
        super().__init__(name, village_map, 0, lead_race, buildings)
        self.village_map = village_map

class building:
    def __init__(self, name, typ, **args):
        self.name = name
        self.typ = typ
        if "build" in args.keys():
            self.build = args["build"]
        self.other = args

    def door(self):
        try:
            return self.build[-2], self.build[-1]
        except:
            return False