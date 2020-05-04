import random as rand
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
        self.sort_place_by_type_x()

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

    def sort_place_by_type_x(self):
        towns = {}
        villages = {}
        place_list = {}
        for i in self.places_list.keys():
            if type(self.places_list[i]) == town:
                towns[i] = self.places_list[i]
            elif type(self.places_list[i]) == village:
                villages[i] = self.places_list[i]
        keys = list(towns.keys()).copy()
        next_keys = []
        while len(keys) > 0:
            next_keys.append(min(keys))
            del keys[keys.index(min(keys))]
        for i in next_keys:
            place_list[i] = towns[i]
        keys = list(villages.keys()).copy()
        next_keys = []
        while len(keys) > 0:
            next_keys.append(min(keys))
            del keys[keys.index(min(keys))]
        for i in next_keys:
            place_list[i] = villages[i]
        self.places_list = place_list



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
    def __init__(self, name, typ):
        self.name = name
        self.typ = typ
        if self.typ in ["Town Hall", "Casel"]:
            self.generate_missions()
        elif self.typ in ["Shop"]:
            self.generate_common(10)
        elif self.typ in ["Marketplace"]:
            self.generate_common(5)
            self.generate_rare(5)

    def generate_missions(self):
        self.missions = []

    def generate_common(self, up_to):
        self.items_to_sell = []

    def generate_rare(self, up_to):
        self.items_to_sell = []

    def __str__(self):
        return self.name

    def come_in(self):
        if self.typ in ["Town Hall", "Casel"]:
            return self.missions
        elif self.typ in ["Chapel"]:
            return "+5 mana"
        elif self.typ in ["Church"]:
            return "+10 mana"
        elif self.typ in ["Cathedral"]:
            return "+15 mana"
        elif self.typ in ["Tavern"]:
            return "-10 coins|+10 lives"
        elif self.typ in ["Shop"]:
            return self.items_to_sell
        elif self.typ in ["Marketplace"]:
            return self.items_to_sell
        elif self.typ in ["Wizzard"]:
            return "! maxmana < 100 *#|-10 coins|+10 maxmana"
        elif self.typ in ["School"]:
            return "! maxlives < 150 *#|-10 coins|+10 maxlives"

    def gen_to_draw_text(self):
        if self.typ in ["Town Hall", "Casel"]:
            return str(len(self.missions))+" missions to do"
        elif self.typ in ["Chapel"]:
            return "add 5 mana"
        elif self.typ in ["Church"]:
            return "add 10 mana"
        elif self.typ in ["Cathedral"]:
            return "add 15 mana"
        elif self.typ in ["Tavern"]:
            return "add 10 lives per 10 coins"
        elif self.typ in ["Shop"]:
            return str(len(self.items_to_sell))+" items to sell now"
        elif self.typ in ["Marketplace"]:
            return str(len(self.items_to_sell))+" items to sell now"
        elif self.typ in ["Wizzard"]:
            return "add 10 max mana per 10 coins"
        elif self.typ in ["School"]:
            return "add 10 max lives per 10 coins"

# 0:("Casel")
# 1:("Town Hall")
# 2:("Cathedral", "Church", "Chapel")
# 3:("Tavern")
# 4:("Shop", "Marketplace")
# 5:("Wizzard", "School")
    