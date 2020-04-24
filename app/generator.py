from random import randint, random, choice
from app.draw import *

class generator:
    def __init__(self, drawer):
        self.have = 0
        self.need = 1026 * 1025
        self.list = []
        self.drawer = drawer
        self.generating = False

    def left_middle(self, tlc, brc):
        if self.list[(tlc[0]+brc[0])//2][tlc[1]] == -1:
            self.list[(tlc[0]+brc[0])//2][tlc[1]] = (self.list[tlc[0]][tlc[1]] + self.list[brc[0]][tlc[1]]) // 2 
            + randint(-(brc[0] - tlc[0]), (brc[0] - tlc[0]))
            
            if self.list[(tlc[0]+brc[0])//2][tlc[1]] > 1025:
                self.list[(tlc[0]+brc[0])//2][tlc[1]] = 1025
            
            elif self.list[(tlc[0]+brc[0])//2][tlc[1]] < 0:
                self.list[(tlc[0]+brc[0])//2][tlc[1]] = 0

            self.have += 1

    def right_middle(self, tlc, brc):
        if self.list[(tlc[0]+brc[0])//2][brc[1]] == -1:
            self.list[(tlc[0]+brc[0])//2][brc[1]] = (self.list[tlc[0]][brc[1]] + self.list[brc[0]][brc[1]]) // 2 
            + randint(-(brc[0] - tlc[0]), (brc[0] - tlc[0]))
            
            if self.list[(tlc[0]+brc[0])//2][brc[1]] > 1025:
                self.list[(tlc[0]+brc[0])//2][brc[1]] = 1025
            
            elif self.list[(tlc[0]+brc[0])//2][brc[1]] < 0:
                self.list[(tlc[0]+brc[0])//2][brc[1]] = 0

            self.have += 1

    def top_middle(self, tlc, brc):
        if self.list[tlc[0]][(tlc[1]+brc[1])//2] == -1:
            self.list[tlc[0]][(tlc[1]+brc[1])//2] = (self.list[tlc[0]][tlc[1]] + self.list[tlc[0]][brc[1]]) // 2 
            + randint(-(brc[0] - tlc[0]), (brc[0] - tlc[0]))
            
            if self.list[tlc[0]][(tlc[1]+brc[1])//2] > 1025:
                self.list[tlc[0]][(tlc[1]+brc[1])//2] = 1025
            
            elif self.list[tlc[0]][(tlc[1]+brc[1])//2] < 0:
                self.list[tlc[0]][(tlc[1]+brc[1])//2] = 0

            self.have += 1

    def bottom_middle(self, tlc, brc):
        if self.list[brc[0]][(tlc[1]+brc[1])//2] == -1:
            self.list[brc[0]][(tlc[1]+brc[1])//2] = (self.list[brc[0]][tlc[1]] + self.list[brc[0]][brc[1]]) // 2 
            + randint(-(brc[0] - tlc[0]), (brc[0] - tlc[0]))
            
            if self.list[brc[0]][(tlc[1]+brc[1])//2] > 1025:
                self.list[brc[0]][(tlc[1]+brc[1])//2] = 1025
            
            elif self.list[brc[0]][(tlc[1]+brc[1])//2] < 0:
                self.list[brc[0]][(tlc[1]+brc[1])//2] = 0

            self.have += 1

    def middle_of_middles(self, tlc, brc):
        if self.list[(tlc[0]+brc[0])//2][(tlc[1]+brc[1])//2] == -1:
            self.list[(tlc[0]+brc[0])//2][(tlc[1]+brc[1])//2] = (self.list[brc[0]][(tlc[1]+brc[1])//2] + self.list[tlc[0]][(tlc[1]+brc[1])//2] + self.list[(tlc[0]+brc[0])//2][brc[1]] + self.list[(tlc[0]+brc[0])//2][tlc[1]]) // 4
            + randint(-(brc[0] - tlc[0]), (brc[0] - tlc[0]))
            
            if self.list[(tlc[0]+brc[0])//2][(tlc[1]+brc[1])//2] > 1025:
                self.list[(tlc[0]+brc[0])//2][(tlc[1]+brc[1])//2] = 1025
            
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
        self.list[0][0] = randint(0,1025)
        self.list[-1][0] = randint(0,1025)
        self.list[0][-1] = randint(0,1025)
        self.list[-1][-1] = randint(0,1025)

    def generate(self):
        self.generate_free()
        self.random_corns()
        self.loop([0,0], [len(self.list)-1, len(self.list)-1])

        return self.list

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

            self.drawer.draw_shape("rect", (100, self.drawer.height//2 - 25, self.drawer.width-200, 50), (255, 255, 255))
            self.drawer.draw_shape("rect", (100, self.drawer.height//2 - 25, int((self.drawer.width-200)*(self.have/self.need)), 50), (50, 150, 50))

            pygame.display.update()

            self.loop(tlc, center)
            self.loop(up, right)
            self.loop(center, brc)
            self.loop(left, down)

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