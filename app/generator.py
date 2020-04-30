from random import randint, random, choice
from app.draw import *
from app.classes import *
import time as tim

class generator:
    def __init__(self, drawer):
        self.have = 0
        self.need = 1026 * 1025 + 5000000
        self.list = []
        self.drawer = drawer
        self.generating = False

    def left_middle(self, tlc, brc):
        if self.list[(tlc[0]+brc[0])//2][tlc[1]] == -1:
            self.list[(tlc[0]+brc[0])//2][tlc[1]] = (self.list[tlc[0]][tlc[1]] + self.list[brc[0]][tlc[1]]) // 2 + randint(-(brc[0] - tlc[0]), (brc[0] - tlc[0]))
            
            if self.list[(tlc[0]+brc[0])//2][tlc[1]] > 500:
                self.list[(tlc[0]+brc[0])//2][tlc[1]] = 500
            
            elif self.list[(tlc[0]+brc[0])//2][tlc[1]] < 0:
                self.list[(tlc[0]+brc[0])//2][tlc[1]] = 0

            self.have += 1

    def right_middle(self, tlc, brc):
        if self.list[(tlc[0]+brc[0])//2][brc[1]] == -1:
            self.list[(tlc[0]+brc[0])//2][brc[1]] = (self.list[tlc[0]][brc[1]] + self.list[brc[0]][brc[1]]) // 2 + randint(-(brc[0] - tlc[0]), (brc[0] - tlc[0]))
            
            if self.list[(tlc[0]+brc[0])//2][brc[1]] > 500:
                self.list[(tlc[0]+brc[0])//2][brc[1]] = 500
            
            elif self.list[(tlc[0]+brc[0])//2][brc[1]] < 0:
                self.list[(tlc[0]+brc[0])//2][brc[1]] = 0

            self.have += 1

    def top_middle(self, tlc, brc):
        if self.list[tlc[0]][(tlc[1]+brc[1])//2] == -1:
            self.list[tlc[0]][(tlc[1]+brc[1])//2] = (self.list[tlc[0]][tlc[1]] + self.list[tlc[0]][brc[1]]) // 2 + randint(-(brc[0] - tlc[0]), (brc[0] - tlc[0]))
            
            if self.list[tlc[0]][(tlc[1]+brc[1])//2] > 500:
                self.list[tlc[0]][(tlc[1]+brc[1])//2] = 500
            
            elif self.list[tlc[0]][(tlc[1]+brc[1])//2] < 0:
                self.list[tlc[0]][(tlc[1]+brc[1])//2] = 0

            self.have += 1

    def bottom_middle(self, tlc, brc):
        if self.list[brc[0]][(tlc[1]+brc[1])//2] == -1:
            self.list[brc[0]][(tlc[1]+brc[1])//2] = (self.list[brc[0]][tlc[1]] + self.list[brc[0]][brc[1]]) // 2 + randint(-(brc[0] - tlc[0]), (brc[0] - tlc[0]))
            
            if self.list[brc[0]][(tlc[1]+brc[1])//2] > 500:
                self.list[brc[0]][(tlc[1]+brc[1])//2] = 500
            
            elif self.list[brc[0]][(tlc[1]+brc[1])//2] < 0:
                self.list[brc[0]][(tlc[1]+brc[1])//2] = 0

            self.have += 1

    def middle_of_middles(self, tlc, brc):
        if self.list[(tlc[0]+brc[0])//2][(tlc[1]+brc[1])//2] == -1:
            self.list[(tlc[0]+brc[0])//2][(tlc[1]+brc[1])//2] = (self.list[brc[0]][(tlc[1]+brc[1])//2] + self.list[tlc[0]][(tlc[1]+brc[1])//2] + self.list[(tlc[0]+brc[0])//2][brc[1]] + self.list[(tlc[0]+brc[0])//2][tlc[1]]) // 4 + randint(-(brc[0] - tlc[0]), (brc[0] - tlc[0]))
            
            if self.list[(tlc[0]+brc[0])//2][(tlc[1]+brc[1])//2] > 500:
                self.list[(tlc[0]+brc[0])//2][(tlc[1]+brc[1])//2] = 500
            
            elif self.list[(tlc[0]+brc[0])//2][(tlc[1]+brc[1])//2] < 0:
                self.list[(tlc[0]+brc[0])//2][(tlc[1]+brc[1])//2] = 0

            self.have += 1
    
    def generate_free(self):
        self.list = []
        a = []
        for i in range(2**10+1):
            self.have += 1
            a.append(-1)
        for i in range(2**10+1):
            self.list.append(a.copy())

    def random_corns(self):
        self.list[0][0] = randint(0,500)
        self.list[-1][0] = randint(0,500)
        self.list[0][-1] = randint(0,500)
        self.list[-1][-1] = randint(0,500)

    def generate(self):
        self.have = 0
        self.generate_free()
        self.random_corns()
        self.loop([0,0], [len(self.list)-1, len(self.list)-1])

        self.drawer.draw_shape("rect", (100, self.drawer.height//2 - 25, self.drawer.width-200, 50), (255, 255, 255))
        self.drawer.draw_shape("rect", (100, self.drawer.height//2 - 25, int((self.drawer.width-200)*(self.have/self.need)), 50), (50, 150, 50))
        pygame.display.update()

        places = self.generate_map_places()

        self.drawer.draw_shape("rect", (100, self.drawer.height//2 - 25, self.drawer.width-200, 50), (255, 255, 255))
        self.drawer.draw_shape("rect", (100, self.drawer.height//2 - 25, int((self.drawer.width-200)*(self.have/self.need)), 50), (50, 150, 50))
        pygame.display.update()

        return map_("", self.list, places)
        
    def loop(self, tlc, brc):
        if brc[0]-tlc[0] >= 2 and brc[1]-tlc[1] >= 2:
            self.bottom_middle(tlc, brc)
            self.top_middle(tlc, brc)
            self.left_middle(tlc, brc)
            self.right_middle(tlc, brc)
            self.middle_of_middles(tlc, brc)

            up = [tlc[0], (tlc[1]+brc[1])//2]
            down = [brc[0], (tlc[1]+brc[1])//2]
            left = [(tlc[0]+brc[0])//2, tlc[1]]
            right = [(tlc[0]+brc[0])//2, brc[1]]
            center = [(tlc[0]+brc[0])//2, (tlc[1]+brc[1])//2]
            
            if self.have%1025 == 0 or self.have == self.need:
                self.drawer.draw_shape("rect", (100, self.drawer.height//2 - 25, self.drawer.width-200, 50), (255, 255, 255))
                self.drawer.draw_shape("rect", (100, self.drawer.height//2 - 25, int((self.drawer.width-200)*(self.have/self.need)), 50), (50, 150, 50))

                pygame.display.update()

            self.loop(tlc, center)
            self.loop(up, right)
            self.loop(center, brc)
            self.loop(left, down)

    def generate_town_map(self, typ):
        # 0 = grass
        # 1 = road
        # 2 = house wall
        # 3 = hause inside
        # 4 = house door
        # 5 = defend wall
        # 6 = gate
        if typ == "town":
            map_list = []
            map_list1 = [1]*(randint(8,14)*5+5)
            for i in range(randint(8,14)*5+5):
                map_list.append(map_list1.copy())

            for i in range(0, len(map_list[1])):
                map_list[0][i] = 0
                map_list[-1][i] = 0
            for i in range(0, len(map_list)):
                map_list[i][0] = 0
                map_list[i][-1] = 0

            for i in range(1, len(map_list[1])-1):
                map_list[1][i] = 5
                map_list[-2][i] = 5
            for i in range(1, len(map_list)-1):
                map_list[i][1] = 5
                map_list[i][-2] = 5

            min_buildings = 0
            start_in = tim.time()
            buildings = {}
            while min_buildings < 40 and tim.time() - start_in < 0.2:
                no_space = False
                x = randint(3, len(map_list[0])-8)
                y = randint(3, len(map_list)-8)
                x_ = randint(4, 6)
                y_ = randint(4, 6)
                for i in range(x-1, x+x_+2):
                    for j in range(y-1, y+y_+2):
                        if map_list[j][i] not in [1]:
                            no_space = True
                if not no_space:
                    for i in range(x, x+x_+1):
                        map_list[y][i] = 2
                        map_list[y+y_][i] = 2
                    for j in range(y, y+y_+1):
                        map_list[j][x] = 2
                        map_list[j][x+x_] = 2

                    side = randint(0,1)
                    tops = [x, x+x_]
                    sides = [y, y+y_]
                    if side == 0:
                        xx = tops[randint(0,1)]
                        yy = randint(y, y+y_)
                    if side == 1:
                        yy = sides[randint(0,1)]
                        xx = randint(x, x+x_)
                    map_list[yy][xx] = 4
                    buildings[min_buildings] = "{},{},{},{},{},{}".format(x, y, x_, y_, xx, yy)

                    for i in range(x+1, x+x_):
                        for j in range(y+1, y+y_):
                            map_list[j][i] = 3
                    min_buildings += 1
            gate = 0
            need_gate = randint(3,6)
            while gate != need_gate:
                no_space = False
                side = randint(0,3)
                sides = {0: 1, 1: len(map_list)-2, 2:1, 3:len(map_list[0])-2}
                if side in [0,1]:
                    x = randint(3, len(map_list[1])-4)
                    y = sides[side]
                    for i in range(-2,3):
                        if map_list[y][x+i] != 5:
                            no_space = True
                elif side in [2,3]:
                    y = randint(3, len(map_list)-4)
                    x = sides[side]
                    for i in range(-2,3):
                        if map_list[y+i][x] != 5:
                            no_space = True
                if not no_space:
                    if side in [0, 1]:
                        for i in range(-1,2):
                            map_list[y][x+i] = 6
                    elif side in [2, 3]:
                        for i in range(-1,2):
                            map_list[y+i][x] = 6
                    gate += 1

        elif typ == "village":
            map_list = []
            map_list1 = [1]*(randint(7,10)*5+5)
            for i in range(randint(7,10)*5+5):
                map_list.append(map_list1.copy())
            for i in range(0, len(map_list[1])):
                map_list[0][i] = 0
                map_list[-1][i] = 0
            for i in range(0, len(map_list)):
                map_list[i][0] = 0
                map_list[i][-1] = 0

            for i in range(1, len(map_list[1])-1):
                map_list[1][i] = 5
                map_list[-2][i] = 5
            for i in range(1, len(map_list)-1):
                map_list[i][1] = 5
                map_list[i][-2] = 5
            min_buildings = 0
            start_in = tim.time()
            buildings = {}
            while min_buildings < 20 and tim.time() - start_in < 0.2:
                no_space = False
                x = randint(3, len(map_list[0])-8)
                y = randint(3, len(map_list)-8)
                x_ = randint(4, 6)
                y_ = randint(4, 6)
                for i in range(x-1, x+x_+2):
                    for j in range(y-1, y+y_+2):
                        if map_list[j][i] not in [1]:
                            no_space = True
                if not no_space:
                    
                    for i in range(x, x+x_+1):
                        map_list[y][i] = 2
                        map_list[y+y_][i] = 2
                    for j in range(y, y+y_+1):
                        map_list[j][x] = 2
                        map_list[j][x+x_] = 2

                    side = randint(0,1)
                    tops = [x, x+x_]
                    sides = [y, y+y_]
                    if side == 0:
                        xx = tops[randint(0,1)]
                        yy = randint(y, y+y_)
                    if side == 1:
                        yy = sides[randint(0,1)]
                        xx = randint(x, x+x_)
                    map_list[yy][xx] = 4
                    buildings[min_buildings] = "{},{},{},{},{},{}".format(x, y, x_, y_, xx, yy)

                    for i in range(x+1, x+x_):
                        for j in range(y+1, y+y_):
                            map_list[j][i] = 3
                    min_buildings += 1
            gate = 0
            need_gate = randint(1,4)
            while gate != need_gate:
                no_space = False
                side = randint(0,3)
                sides = {0: 1, 1: len(map_list)-2, 2:1, 3:len(map_list[0])-2}
                if side in [0,1]:
                    x = randint(3, len(map_list[1])-4)
                    y = sides[side]
                    for i in range(-2,3):
                        if map_list[y][x+i] != 5:
                            no_space = True
                elif side in [2,3]:
                    y = randint(3, len(map_list)-4)
                    x = sides[side]
                    for i in range(-2,3):
                        if map_list[y+i][x] != 5:
                            no_space = True
                if not no_space:
                    if side in [0, 1]:
                        for i in range(-1,2):
                            map_list[y][x+i] = 6
                    elif side in [2, 3]:
                        for i in range(-1,2):
                            map_list[y+i][x] = 6
                    gate += 1

        else:
            raise ValueError("typ is wrong need 'village' or 'town' but take '{}'".format(typ))
        return map_list, buildings
            

    def generate_town(self):
        map_list, buildings = self.generate_town_map("town")
        try:
            buildings = self.generate_building(buildings, randint(8, max(buildings.keys()) - 8), "town")
        except:
            buildings = self.generate_building(buildings, randint(8, max(buildings.keys())), "town")
        return town(doname(), map_list, randint(0,150), None, buildings)

    def generate_village(self):
        map_list, buildings = self.generate_town_map("village")
        try:
            buildings = self.generate_building(buildings, randint(4, max(buildings.keys()) - 8), "village")
        except:
            buildings = self.generate_building(buildings, randint(4, max(buildings.keys())), "village")
        return village(doname(), map_list, None, buildings)

    def generate_building(self, buildings_pozitions, buildings_max, typ):
        buildings = {}
        buildings_def = {0:("Casel"), 1:("Town Hall"), 2:("Cathedral", "Church", "Chapel"), 3:("Tavern"), 4:("Shop", "Marketplace"), 5:("Wizzard", "School")}
        to_build = 3
        while buildings_max != 0:
            build_ = randint(0, max(buildings_pozitions.keys()))
            try:
                build = buildings_pozitions[build_]
                build = build.split(",")
                for i in range(len(build)):
                    build[i] = int(build[i])
                if to_build == 3:
                    buildings[buildings_max] = building(buildings_def[3], buildings_def[3], build = build)
                elif to_build == 2:
                    if typ == "town" and random() > 0.8:
                        buildings[buildings_max] = building(buildings_def[0], buildings_def[0], build = build)
                    else:
                        buildings[buildings_max] = building(buildings_def[1], buildings_def[1])
                elif to_build == 1:
                    build_typ = randint(0,2)
                    buildings[buildings_max] = building(buildings_def[2][build_typ], buildings_def[2][build_typ], build = build)
                else:
                    if random() >= 0.5:
                        build_typ = randint(0,1)
                        buildings[buildings_max] = building(buildings_def[4][build_typ], buildings_def[4][build_typ], build = build)
                    else:
                        build_typ = randint(0,1)
                        buildings[buildings_max] = building(buildings_def[5][build_typ], buildings_def[5][build_typ], build = build)
                del buildings_pozitions[build_]
                del build_
                to_build -= 1
                buildings_max -= 1
            except LookupError as er:
                pass
        return buildings

    def generate_map_places(self, minimal = 50, maximal = 150, village_to_town = 3):
        places = {}
        to_generate = int(randint(minimal, maximal)/village_to_town)*village_to_town
        add = 5000000/to_generate
        while to_generate > 0:
            x = randint(1,1023)
            y = randint(1,1023)
            i = to_generate%4
            if 400 > self.list[y][x] > 150:
                if i == 3:
                    places["{},{}".format(x,y)] = self.generate_town()
                else:
                    places["{},{}".format(x,y)] = self.generate_village()
                to_generate -= 1
                self.have += add
            self.drawer.draw_shape("rect", (100, self.drawer.height//2 - 25, self.drawer.width-200, 50), (255, 255, 255))
            self.drawer.draw_shape("rect", (100, self.drawer.height//2 - 25, int((self.drawer.width-200)*(self.have/self.need)), 50), (50, 150, 50))
            pygame.display.update()
        return places

    def add_place(self, t_v, map_class):
        to_generate = 1
        use = 15
        while to_generate > 0 and use:
            x = randint(1,1023)
            y = randint(1,1023)
            i = to_generate%4
            if 400 > map_class.get_field(x, y) > 150:
                if t_v == "town":
                    map_class.places_list["{},{}".format(x,y)] = self.generate_town()
                else:
                    map_class.places_list["{},{}".format(x,y)] = self.generate_village()
                to_generate -= 1
            use -= 1
            

def doname():
    first = ["Chelm", "Elm", "El", "Bur", "En", "Eg", "Pem", "Pen", "Edg", "Sud", "Sod", "Hors", "Dur", "Sun", "Nort", "Brad", "Farn", "Barn", "Dart", "Hart", "South", "Shaft", "Blan", "Rock", "Alf", "Wy", "Marl", "Staf", "Wet", "Cas", "Stain", "Whit", "Stap", "Brom", "Wych", "Watch", "Win", "Horn", "Mel", "Cook", "Hurst", "Ald", "Shriv", "Kings", "Clere", "Maiden", "Leather", "Brack","Brain", "Walt", "Prest", "Wen", "Flit", "Ash"]
    doubles = ["Bass", "Chipp", "Sodd", "Sudd", "Ell", "Burr", "Egg", "Emm", "Hamm", "Hann", "Cann", "Camm", "Camb", "Sund", "Pend", "End", "Warr", "Worr", "Hamp", "Roth", "Both", "Sir", "Cir", "Redd", "Wolv", "Mill", "Kett", "Ribb", "Dribb", "Fald", "Skell", "Chedd", "Chill", "Tipp", "Full", "Todd", "Abb", "Booth"]
    postdoubles = ["ing", "en", "er"]
    mid = ["bas", "ber", "stan", "ring", "den", "-under-", " on ", "en", "re", "rens", "comp", "mer", "sey", "mans"]
    last = ["ford", "stoke", "ley", "ney",  "don", "den", "ton", "bury", "well", "beck", "ham", "borough", "side", "wick", "hampton", "wich", "cester", "chester", "ling", "moor", "wood", "brook", "port", "wold", "mere", "castle", "hall", "bridge", "combe", "smith", "field", "ditch", "wang", "over", "worth", "by", "brough", "low", "grove", "avon", "sted", "bourne", "borne", "thorne", "lake", "shot", "bage", "head", "ey", "nell", "tree", "down"]

    finished_name = ""
    pd = 0
    if(random()  > 0.4):
        finished_name = finished_name + choice(doubles)
        if(random()  > 0.6):
            finished_name = finished_name + choice(postdoubles)
            pd = 1
        else:
            finished_name = finished_name[0:len(finished_name) - 1]
    else:
        finished_name = finished_name + choice(first)

    if(random()  > 0.5 and not pd):
        if(finished_name.endswith("r") or finished_name.endswith("b")):
            if(random()  > 0.4):
                finished_name = finished_name + "ble"
            else:
                finished_name = finished_name + "gle"
        elif(finished_name.endswith("n") or finished_name.endswith("d")):
            finished_name = finished_name + "dle"
        elif(finished_name.endswith("s")):
            finished_name = finished_name + "tle"

    if(random()  > 0.7 and finished_name.endswith("le")):
        finished_name = finished_name + "s"

    elif(random()  > 0.5):
        if(finished_name.endswith("n")):
            if(random()  > 0.5):
                finished_name = finished_name + "s"
            else:
                finished_name = finished_name + "d"
        elif(finished_name.endswith("m")):
            finished_name = finished_name + "s"

    if(random()  > 0.7):
        finished_name = finished_name + choice(mid)
    finished_name = finished_name + choice(last)

    fix = finished_name.rpartition(' ')
    if(fix[1] == ' '):
        finished_name = fix[0] + ' ' + fix[2].capitalize()

    fix = finished_name.rpartition('-')
    if(fix[1] == '-'):
        finished_name = fix[0] + '-' + fix[2].capitalize()

    return finished_name