import platform as plf
if plf.system() == "Linux":
    pass
elif plf.system() == "Windows":
    pass
from app.forAll import *
from app.generator import *
from settings.settings import setting 
from players.players import *
from defaults.default import *
from maps.maper import saver
print("\rPreloading:", 25, "%", end = "") # Other part of app
import time as t
from math import *
print("\rPreloading:", 50, "%", end = "") # Python parts

# textures from : 
# https://unsplash.com/@stephanie_moody, 
# http://www.vadreal.sk/crumpled-white-paper-texture-melemel-jpeg_260159/,
# http://www.cleanpng.com,
# https://www.uihere.com, 

try:
    settings = setting()
    instal = [False]
except:
    instal = [True]
try:
    player_logger = players()
    instal.append(False)
except:
    instal.append(True)
if True in instal:
    instal.append(True)
    from instaler import *
    instaler(instal[0], instal[1], instal[2])
player_logger = players()
settings = setting()
defaults = default()
maper = saver()
maper.start()
print("\rPreloading", 70, "%", end = "") # Database

eventInfo = forAll() 
clock = pygame.time.Clock()
draw = drawer(settings, eventInfo)
gener = generator(draw)
print("\rPreloading:", 100, "%", end = "") # Create Window and generator
print("\rLoading start in few secunds", end = "")

exit_game = False # Exit window

fps = settings.get_fps() # Load max Fps

app_step = "singup/in" # Set step of game
show_pass = False

try:
    active_map = maper.load_from("maps/default_map.tmap")
    if not active_map:
        active_map = gener.generate()
except:
    active_map = gener.generate()

def get_map_color(height): # map colors
    if height < 50:
        return (0,0,100) # deep water
    elif height < 100:
        return (0,0,255) # water
    elif height < 150:
        return (200,200,0) # sand
    elif height < 300:
        return (0,250,0) # grass
    elif height < 410:
        return (150,100,20) # hills
    elif height < 480:
        return (100,100,100) # rock hills
    elif height <= 500:
        return (255,255,255) # mountines
    else:
        return (255,0,0) # Towns / villages

def get_place_color(number):
    if number == 0:
        return (0, 255, 0) # 0 = grass
    elif number == 1:
        return (200, 180, 170) # 1 = road
    elif number == 2:
        return (160, 80, 60) # 2 = house wall
    elif number == 3:
        return (0, 0, 0) # 3 = hause inside
    elif number == 4:
        return (198, 144, 135) # 4 = house door
    elif number == 5:
        return (150, 150, 150) # 5 = defend wall
    elif number == 6:
        return (200, 150, 140) # 6 = gate

error = ""
error_time = [0,0]
error_app_step = ""
error_pozition = (0,0)

editor_add = 1
editor_timer = tim.time()
editor_x = 0
editor_y = 0
editor_town_sleep = 0

active_character = None

you_character_sleep = 0

editing_character = None

chose_map_sleep = 0

adding = []

a = 0           # FPS counter
now = t.time()
print("\rGame start now                       ")
while True:
    if app_step != "add_char_name":
        rolls = [4, [0,0,0,0,0,0,0]]
        move_to = [-1,-1,-1,-1,-1,-1,-1, -1]
        set_to = [3,3,3,3,3,3,3,53]
        
    mouse = pygame.mouse.get_pos()
    if app_step != "stay_full":
        draw.display.fill((0,0,0))
    if eventInfo.set_(pygame.event.get()) or exit_game:
        pygame.quit()
        if app_step == "setting_setting":
            from settings import install_settings
            install_settings.install_settings()
        elif app_step == "setting_default":
            from defaults import install_default
            install_default.install_default()
        maper.running = False
        sys.exit()
        break
    if app_step[-1] == "_":
        app_step = app_step[:-1]

    
     # sing up / sing in start 
    if app_step in ["singup/in"]:
        draw.draw_img("textures/Game_Logo.png", (0,100, draw.height-200, draw.height-200))
        
        draw.draw_text((draw.height-200, 60), "Nickname", color=(0,100,0))
        draw.draw_text((draw.height-200, 160), "Password", color=(0,100,0))
        x_wide = draw.width - (draw.height-200) - 50
        nickname = draw.draw_entry("image", (draw.height-200, 100, x_wide, 50, "textures/paper.jpg"), "player_nickname", colors = [(0,0,0)])
        

        log = draw.draw_button("shape", (draw.width-200, 300, 180, 50), colors = [(0,0,0), (255,205,100)], text = "Sing in")
        enter = draw.draw_button("shape", (draw.width-200, 360, 180, 50), colors = [(0,0,0), (255,205,100)], text = "Sing up")
        if show_pass:
            s_h = "  Hide"
            password = draw.draw_entry("image", (draw.height-200, 200, x_wide, 50, "textures/paper.jpg"), "player_password", colors = [(0,0,0)])
        else:
            s_h = "  Show"
            password = draw.draw_entry("image", (draw.height-200, 200, x_wide, 50, "textures/paper.jpg"), "player_password", colors = [(0,0,0)], text_type = "password")
        sp = draw.draw_button("shape", (draw.width-200, 420, 180, 50), colors = [(0,0,0), (255,205,100)], text = s_h)

        if sp:
            if show_pass:
                show_pass = False
            else:
                show_pass = True

        if log:
            if player_logger.login(nickname, password):
                player_nickname = nickname
            else:
                error = "Wrong password or nickname"
                error_time = [t.time(), 30]
                error_app_step = app_step
                error_pozition = (0,60)
        
        if enter:
            if player_logger.add(nickname, password):
                player_nickname = nickname
            else:
                error = "Can't use this user name"
                error_time = [t.time(), 30]
                error_app_step = app_step
                error_pozition = (0,60)
        try:
            if (enter or log) and player_nickname == nickname:
                log_in = Player(nickname, password)
                app_step = "menu_"
        except Exception as er:
            print(er)
                
    # sing in / sing up end ---------- menu start
    if app_step == "menu":
        width, height = draw.draw_text((draw.width-250,0), "Sing up as "+nickname, size = 40, blit=False)
        draw.draw_text((draw.width-width-125,0), "Sing up as "+nickname, size = 40, color = (255,255,255))
        player_login = draw.draw_button("image", (draw.width-125,0,125,40, "textures/paper.png"), colors = (0, 0, 0), text = "Sing out", size = 30)
        game = draw.draw_button("image", geometry = (draw.width//2-73, 160, 146, 50, "textures/paper.png"), colors = (0, 0, 0),     text = "Game",    size = 50)
        help_ = draw.draw_button("image", geometry = (draw.width//2-60, 220, 120, 50, "textures/paper.png"), colors = (0, 0, 0),     text = "Help",    size = 50)
        edit = draw.draw_button("image", geometry = (draw.width//2-75, 280, 150, 50, "textures/paper.png"), colors = (0, 0, 0),     text = "Editor",    size = 50)
        width, height = draw.draw_text((0,0), "Chose Map", blit = False)
        map_chose = draw.draw_button("image", geometry = (draw.width//2-int((width+10)/2), 340, width+10, 50, "textures/paper.png"), colors = (0, 0, 0),     text = "Chose Map",    size = 50)
        setting = draw.draw_button("image", geometry = (draw.width//2-83, 400, 166, 50, "textures/paper.png"), colors = (0, 0, 0),     text = "Setting",    size = 50)
        exit_game = draw.draw_button("image", geometry = (draw.width//2-50, 460, 100, 50, "textures/paper.png"), colors = (255, 0, 0),     text = "Exit",    size = 50)
        draw.draw_img("textures/knight.png",  (draw.width//2-450, 80, 350, 600))
        draw.draw_img("textures/knight2.png", (draw.width//2, 80, 600, 600))
        if game:
            app_step = "game_"
        elif help_:
            app_step = "help_"
        elif edit:
            app_step = "editor_"
        elif setting:
            app_step = "settings_"
        elif player_login:
            app_step = "singup/in_"
            del log_in
            nickname = ""
            password = ""
        elif map_chose:
            app_step = "chose_map"
    # menu end ---------- settings start
    if app_step == "settings":
        window = draw.draw_button("image", geometry = (draw.width//2-100, 160, 200, 50, "textures/paper.png"), colors = (0, 0, 0),     text = "Window",    size = 50)
        you = draw.draw_button("image", geometry = (draw.width//2-50, 220, 100, 50, "textures/paper.png"), colors = (0, 0, 0),     text = "You",    size = 50)
        default = draw.draw_button("image", geometry = (draw.width//2-100, 280, 200, 50, "textures/paper.png"), colors = (0, 0, 0),     text = "Plugins",    size = 50)
        if window:
            app_step = "setting_setting"
            exit_game = True
        elif you:
            app_step = "you"
        elif default:
            app_step = "setting_default"
            exit_game = True
    # settings end ---------- you start - dokonči
    if app_step == "add_char_class":
        draw.draw_text((50, 50), "Select class:")
        y = 150
        x = 10
        for i in defaults.get_classes_names():
            width, height = draw.draw_text((0,0), i, blit = False)
            if x + width + 10 > draw.width - 20:
                y += 60
                x = 10 
            if y + 50 > draw.height:
                break
            this = draw.draw_button("image", (x, y, width+10, 50, "textures/paper.png"), text = i, colors = (0, 0, 0))
            if this:
                adding.append(i)
                app_step = "add_char_race_"
                break
            x += width + 15
        width, whight = draw.draw_text((0,0), "Back", blit = False)
        back = draw.draw_button("image", (draw.width - width - 10, 100, width + 10, 50, "textures/paper.png"), text = "Back", colors = (0,0,0))
        if back:
            app_step = "you"
    if app_step == "add_char_race": 
        y = 150
        x = 10
        draw.draw_text((150, 0), "You class: {}".format(adding[0]))
        draw.draw_text((50, 50), "Select race:")
        for i in defaults.get_races_names(adding):
            width, height = draw.draw_text((0,0), i, blit = False)
            if x + width + 10 > draw.width - 20:
                y += 60
                x = 10 
            if y + 50 > draw.height:
                break
            this = draw.draw_button("image", (x, y, width+10, 50, "textures/paper.png"), text = i, colors = (0, 0, 0))
            if this:
                adding.append(i)
                app_step = "add_char_name_"
                break
            x += width + 15
        width, whight = draw.draw_text((0,0), "Back", blit = False)
        back = draw.draw_button("image", (draw.width - width - 10, 100, width + 10, 50, "textures/paper.png"), text = "Back", colors = (0,0,0))
        if back:
            del adding[-1]
            app_step = "add_char_class"
    if app_step == "add_char_name":
        draw.draw_text((0, 50), "Character name:", color = (255,255,255))
        name = draw.draw_entry("image", (400, 50, draw.width - 800, 50, "textures/paper.jpg"), "character_nickname", colors = [(0,0,0)])
        
        width, height = draw.draw_text((0,0),"Add Character", blit=False)
        
        items = {"Normal":0, "Moving":1, "Adding":2}
        value = draw.draw_switch("image", (250, 110, 50, "textures/paper.png"), "set_special", items, colors = (0,0,0), setifnot = 0)
        items = {y:x for x,y in items.items()}
        if value == 0:
            if rolls[0] == 4:
                all_ = 0
                rolls[0] -= 1
                for i in range(7):
                    rolls[1][i] = randint(1,6) + randint(1,6) + randint(1,6)
                    all_ += rolls[1][i]
                if all_ < 21:
                    raise ValueError("Stats is to low")
                rolls[1].sort()
                while all_ > 80:
                    i = randint(0,6)
                    if rolls[1][i] > 3:
                        rolls[1][i] -= 1
                        all_ -= 1
                rolls[1].sort()
            if rolls[0] > 0:
                width, height = draw.draw_text((0,0), "Roll", blit = False)
                roll = draw.draw_button("image", (250, 170, width + 10, 50, "textures/paper.png"), colors = (0,0,0), text = "Roll")
                draw.draw_text((250 + width + 30, 174), "{} Rolls remaining".format(rolls[0]), color = (255,255,255))
                if roll:
                    all_ = 0
                    rolls[0] -= 1
                    for i in range(7):
                        rolls[1][i] = randint(1,6) + randint(1,6) + randint(1,6)
                        all_ += rolls[1][i]
                    if all_ < 21:
                        raise ValueError("Stats is too low")
                    rolls[1].sort()
                    while all_ > 80:
                        i = randint(0,6)
                        if rolls[1][i] > 3:
                            rolls[1][i] -= 1
                            all_ -= 1
                    rolls[1].sort()
            suma = 0
            for x in rolls[1]:
                suma += x 
            if 81 > suma >= 21:
                draw.draw_text((10, 230), "Streng:", color = (255,255,255))
                draw.draw_text((10, 290), "Perception:", color = (255,255,255))
                draw.draw_text((10, 350), "Endurance:", color = (255,255,255))
                draw.draw_text((10, 410), "Charisma:", color = (255,255,255))
                draw.draw_text((10, 470), "Inteligence:", color = (255,255,255))
                draw.draw_text((10, 530), "Agility:", color = (255,255,255))
                draw.draw_text((10, 590), "Luck:", color = (255,255,255))
                draw.draw_text((300, 230), "{}".format(rolls[1][0]), color = (255,255,255))
                draw.draw_text((300, 290), "{}".format(rolls[1][1]), color = (255,255,255))
                draw.draw_text((300, 350), "{}".format(rolls[1][2]), color = (255,255,255))
                draw.draw_text((300, 410), "{}".format(rolls[1][3]), color = (255,255,255))
                draw.draw_text((300, 470), "{}".format(rolls[1][4]), color = (255,255,255))
                draw.draw_text((300, 530), "{}".format(rolls[1][5]), color = (255,255,255))
                draw.draw_text((300, 590), "{}".format(rolls[1][6]), color = (255,255,255))
                change1 = draw.draw_switch("image", (500, 230, 50, "textures/paper.png"), "change_special_1",{"S":0, "P":1, "E":2, "C":3, "I":4, "A":5, "L":6}, horizontal = True, setifnot = 0, colors = (0,0,0))
                change2 = draw.draw_switch("image", (630, 230, 50, "textures/paper.png"), "change_special_2",{"S":0, "P":1, "E":2, "C":3, "I":4, "A":5, "L":6}, horizontal = True, setifnot = 0, colors = (0,0,0))
                changing = draw.draw_button("image", (500, 580, 180, 50, "textures/paper.png"), colors = (0, 0, 0), text = "Change")
                draw.draw_img("textures/left.png", (565, 300, 50, 50))
                draw.draw_img("textures/right.png", (565, 400, 50, 50))
                if changing:
                    some = rolls[1][change1]
                    rolls[1][change1] = rolls[1][change2]
                    rolls[1][change2] = some
        elif value == 1:
            if rolls[0] == 4:
                all_ = 0
                rolls[0] -= 1
                for i in range(7):
                    rolls[1][i] = randint(1,6) + randint(1,6) + randint(1,6)
                    all_ += rolls[1][i]
                if all_ < 21:
                    raise ValueError("Stats is to low")
                rolls[1].sort()
                while all_ > 80:
                    i = randint(0,6)
                    if rolls[1][i] > 3:
                        rolls[1][i] -= 1
                        all_ -= 1
                rolls[1].sort()
            if rolls[0] > 0:
                width, height = draw.draw_text((0,0), "Roll", blit = False)
                roll = draw.draw_button("image", (250, 170, width + 10, 50, "textures/paper.png"), colors = (0,0,0), text = "Roll")
                draw.draw_text((250 + width + 30, 174), "{} Rolls remaining".format(rolls[0]), color = (255,255,255))
                if roll:
                    move_to = [-1,-1,-1,-1,-1,-1,-1, -1]
                    all_ = 0
                    rolls[0] -= 1
                    for i in range(7):
                        rolls[1][i] = randint(1,6) + randint(1,6) + randint(1,6)
                        all_ += rolls[1][i]
                    if all_ < 21:
                        raise ValueError("Stats is too low")
                    rolls[1].sort()
                    while all_ > 80:
                        i = randint(0,6)
                        if rolls[1][i] > 3:
                            rolls[1][i] -= 1
                            all_ -= 1
                    rolls[1].sort()
            suma = 0
            for x in rolls[1]:
                suma += x 
            if 81 > suma >= 21:
                draw.draw_text((10, 230), "Streng:", color = (255,255,255))
                draw.draw_text((10, 290), "Perception:", color = (255,255,255))
                draw.draw_text((10, 350), "Endurance:", color = (255,255,255))
                draw.draw_text((10, 410), "Charisma:", color = (255,255,255))
                draw.draw_text((10, 470), "Inteligence:", color = (255,255,255))
                draw.draw_text((10, 530), "Agility:", color = (255,255,255))
                draw.draw_text((10, 590), "Luck:", color = (255,255,255))
                y = 230
                clear_button = []
                for i in range(7):
                    if move_to[i] != -1:
                        clear_button.append(draw.draw_button("shape", (300, y, 50, 50), text = "{}".format(rolls[1][move_to[i]]), colors = [(0,0,0),(255,255,255)]))
                    else:
                        clear_button.append(draw.draw_button("shape", (300, y, 50, 50), text = "", colors = [(0,0,0),(255,255,255)]))
                    y+=60
                if move_to[7] != -1:
                    some = draw.draw_button("shape", (mouse[0]-25, mouse[1]-25, 50, 50), text = "{}".format(rolls[1][move_to[7]]), colors = [(0,0,0),(255,255,255)])
                    if some:
                        if True in clear_button:
                            move_to[clear_button.index(True)] = move_to[7]
                            clear_button[clear_button.index(True)] = False
                        move_to[7] = -1
                y = 230
                for i in range(7):
                    if i not in move_to:
                        some = draw.draw_button("shape", (500, y, 50, 50), text = "{}".format(rolls[1][i]), colors = [(0,0,0),(255,255,255)])
                        if some:
                            move_to[7] = i
                        y += 60
                if True in clear_button:
                    move_to[clear_button.index(True)] = -1

        elif value == 2:
            suma = 0
            for x in set_to:
                suma += x 
            if 81 > suma >= 21:
                draw.draw_text((10, 230), "Streng:", color = (255,255,255))
                draw.draw_text((10, 290), "Perception:", color = (255,255,255))
                draw.draw_text((10, 350), "Endurance:", color = (255,255,255))
                draw.draw_text((10, 410), "Charisma:", color = (255,255,255))
                draw.draw_text((10, 470), "Inteligence:", color = (255,255,255))
                draw.draw_text((10, 530), "Agility:", color = (255,255,255))
                draw.draw_text((10, 590), "Luck:", color = (255,255,255))
                draw.draw_text((500, 650), str(set_to[7]))
                y = 230
                for i in range(7):
                    draw.draw_text((300, y), "{}".format(set_to[i]), color = (255,255,255))
                    minus = draw.draw_button("fullimage", (500, y, 50, 50, "textures/minus.png"))
                    plus = draw.draw_button("fullimage", (560, y, 50, 50, "textures/plus.png"))
                    y += 60
                    if minus and set_to[i] > 3:
                        set_to[i] -= 1
                        set_to[7] += 1
                    if plus and set_to[i] < 18 and set_to[7] > 0:
                        set_to[i] += 1
                        set_to[7] -= 1
        if 81 > suma >= 21:
            class_special = defaults.get_class(adding[0]).special
            race_special = defaults.get_race(adding[1]).special
        y = 230
        for i in range(7):
            if class_special[i]:
                draw.draw_text((360, y), "+{}".format(class_special[i]))
            if race_special[i]:
                draw.draw_text((420, y), "+{}".format(race_special[i]))
            y += 60
        width, whight = draw.draw_text((0,0), "Back", blit = False)
        draw.draw_text((700, 300), "You class: {}".format(adding[0]))
        draw.draw_text((700, 400), "You race: {}".format(adding[1]))
        back = draw.draw_button("image", (draw.width - width - 10, 100, width + 10, 50, "textures/paper.png"), text = "Back", colors = (0,0,0))
        if back:
            del adding[-1]
            app_step = "add_char_race"
        add = draw.draw_button("image", (draw.width - width - 60, draw.height - 100, width + 10, 50, "textures/paper.png"), text = "Add Character", colors = (0,0,0))
        if add:
            if value == 0:
                adding.append(rolls[1])
            elif value == 1:
                adding.append([rolls[1][move_to[i]] for i in range(7)])
            elif value == 2:
                adding.append([set_to[i] for i in range(7)])
            if 31 > len(name) > 2:
                log_in.add(name, defaults.get_class(adding[0]), defaults.get_race(adding[1]), adding[2])
                app_step = "you"
            else:
                error = "Nickname need from 3 to 30"
                error_time = [t.time(), 30]
                error_app_step = app_step
                error_pozition = (draw.width - 510, 180)
    if app_step == "you_edit_char":
        if editing_character == None:
            app_step = "you"
        else:
            draw.draw_text((0,50), "Nickname:  {}".format(editing_character.name))
            draw.draw_text((0,100), "Class:  {}".format(editing_character.class_))
            draw.draw_text((0,150), "Race:  {}".format(editing_character.race))
            draw.draw_text((0,200), "Exp:  {}".format(editing_character.exp))
            draw.draw_text((0,250), "S:  {}".format(editing_character.special[0]))
            draw.draw_text((0,300), "P:  {}".format(editing_character.special[1]))
            draw.draw_text((0,350), "E:  {}".format(editing_character.special[2]))
            draw.draw_text((0,400), "C:  {}".format(editing_character.special[3]))
            draw.draw_text((0,450), "I:  {}".format(editing_character.special[4]))
            draw.draw_text((0,500), "A:  {}".format(editing_character.special[5]))
            draw.draw_text((0,550), "L:  {}".format(editing_character.special[6]))

            width, height = draw.draw_text((0,0), "Activate", blit = False)
            activ = draw.draw_button("image", (0, 600, width + 10, 50, "textures/paper.png"), text = "Activate", colors = (0,0,0))
            if activ:
                active_character = editing_character
                app_step = "you_"

            width, height = draw.draw_text((0,0), "Back", blit = False)
            back = draw.draw_button("image", (draw.width - width - 10, 100, width + 10, 50, "textures/paper.png"), text = "Back", colors = (0,0,0))
            if back:
                app_step = "you"
    if app_step == "you":
        draw.draw_text((10, 80), "Player: "+nickname, color = (255,255,255))
        draw.draw_text((10, 140), "Characters:", color = (255,255,255))
        y = 200
        sleeper = 0
        for i in log_in.get_characters_names():
            if sleeper < you_character_sleep:
                sleeper += 1
            else:
                width, height = draw.draw_text((0, 0), i, blit = False)
                char = draw.draw_button("image", (60, y, width+10, 50, "textures/paper.png"), colors = (0,0,0), text = i)
                if char:
                    editing_character = log_in.get_character_by_name(i)
                    app_step = "you_edit_char"
                    break
                if y + 55 > draw.height:
                    break
                else:
                    y += 55
        you_up = draw.draw_button("fullimage", (5, 200, 50, 50, "textures/up.png"))
        you_down = draw.draw_button("fullimage", (5, 300, 50, 50, "textures/down.png"))
        if you_up:
            if you_character_sleep < len(log_in.get_characters_names()) - 1:
                you_character_sleep += 1
        if you_down:
            if you_character_sleep > 0:
                you_character_sleep -= 1
        width, height = draw.draw_text((0,0), " + Add Character + ", blit = False)
        add_char = draw.draw_button("image", (300, 140, width + 10, 50, "textures/paper.png"), text = " + Add Character + ", colors = (0, 0, 0))
        if add_char:
            app_step = "add_char_class"
    # you end ---------- chose_map start
    if app_step == "chose_map":
        y = 100
        to_drow = False
        draw.draw_text((60, y-50), "Active map:")
        width, height = draw.draw_text((60, y), active_map.name, blit = False)
        this = draw.draw_button("image", (60, y, width+10, 50, "textures/paper.png"), text = active_map.name, colors = (0,0,0))
        if 60 < mouse[0] < 70 + width and y < mouse[1] < y + 50: 
                to_drow = active_map
        if this:
            app_step = "menu_"
        y+=105
        draw.draw_text((60, y-50), "Other Maps:")
        slep = chose_map_sleep
        for i in maper.maps:
            if slep > 0:
                slep -= 1
            else:
                width, height = draw.draw_text((60, y), i.name, blit = False)
                this = draw.draw_button("image", (60, y, width+10, 50, "textures/paper.png"), text = i.name, colors = (0,0,0))
                if 60 < mouse[0] < 70 + width and y < mouse[1] < y + 50:
                    to_drow = i
                if this:
                    active_map = i
                    app_step = "menu_"
                y += 55
                if y + 50 >= draw.height:
                    break
        up = draw.draw_button("fullimage", (0, 210, 50, 50, "textures/up.png"))
        down = draw.draw_button("fullimage", (0, draw.height - 60, 50, 50, "textures/down.png"))
        if up:
            if chose_map_sleep > 0:
                chose_map_sleep -= 1
        if down:
            if chose_map_sleep < len(maper.maps) - 1:
                chose_map_sleep += 1
        if to_drow:
            for x in range(0,1025, 8):
                for y in range(0,1025, 8):
                    draw.draw_shape("rect", (int(x/8)*2+draw.height, int(y/8)*2+200, 2, 2), color = get_map_color(to_drow.get_field(x, y)))
    # chose_map end ---------- editor start 
    if app_step == "save_map":
        draw.draw_text((0, 50), "Map name:", color = (255,255,255))
        try:
            draw.entrys["save_map_name"][0] = active_map.name
            text = draw.draw_entry("image", (250, 50, 500, 50, "textures/paper.jpg"), "save_map_name", colors = [(0, 0, 0)])
        except:
            text = draw.draw_entry("image", (250, 50, 500, 50, "textures/paper.jpg"), "save_map_name", colors = [(0, 0, 0)])
            text = active_map.name
        width, height = draw.draw_text((0,0), "Save", blit = False)
        save = draw.draw_button("image", (10, 180, width + 10, 50, "textures/paper.png"), text = "Save", colors = (0,0,0))
        width2, height = draw.draw_text((0,0), "Save as Default map", blit = False) 
        save_as_def = draw.draw_button("image", (25 + width, 180, width2 + 10, 50, "textures/paper.png"), colors = (0,0,0), text = "Save as Default map")
        active_map.name = text
        if save_as_def:
            active_map.name = "default_map"
            maper.save(active_map)
            app_step = "editor_"
        if save:
            maper.save(active_map)
            app_step = "editor_"
        width, height = draw.draw_text((0,0), "Back", blit = False)
        back = draw.draw_button("image", (draw.width - (width + 10), 100, width+10, 50, "textures/paper.png"), text = "Back", colors = (0,0,0))
        if back:
            app_step = "editor_"
        
    if app_step == "editor":
        if active_map != None:
            for x in range(40):
                for y in range(40):
                    x_ = x + editor_x
                    y_ = y + editor_y
                    if x * int(draw.height//40) < mouse[0] < x * int(draw.height//40) + int(draw.height//40)+2 and y * int(draw.height//40) < mouse[1] < y * int(draw.height//40) + int(draw.height//40) + 2:
                        draw.draw_shape("rect", (x*int(draw.height//40)-2, y*int(draw.height//40)-2, int(draw.height//40)+2, int(draw.height//40)+2), (255, 255, 255))
                        try:
                            if 1 in eventInfo.get_mouse()[0]:
                                if tim.time() - editor_timer > 0.1:
                                    editor_timer = tim.time()
                                    active_map.set_field(x_, y_, editor_add)
                        except:
                            pass
                    draw.draw_shape("rect", (x*int(draw.height//40), y*int(draw.height//40), int(draw.height//40)-2, int(draw.height//40)-2), get_map_color(active_map.get_field(x_, y_)))
                    text = str(active_map.get_field(x_, y_))
                    if text != "1025":
                        color_ = get_map_color(int(text))
                        color = (255 - color_[0], 255 - color_[1], 255 - color_[2])
                        text = str(int(text)-100)
                        draw.draw_text((x*int(draw.height//40), y*int(draw.height//40)), text, 13, color = color)

        add_minus = draw.draw_button("fullimage", (draw.height+100, 400, 50, 50, "textures/minus.png"))
        add_plus = draw.draw_button("fullimage", (draw.height+50, 400, 50, 50, "textures/plus.png"))

        map_up = draw.draw_button("fullimage", (draw.height+100, 500, 50, 50, "textures/up.png"))
        map_down = draw.draw_button("fullimage", (draw.height+100, 600, 50, 50, "textures/down.png"))
        map_right = draw.draw_button("fullimage", (draw.height+150, 550, 50, 50, "textures/right.png"))
        map_left = draw.draw_button("fullimage", (draw.height+50, 550, 50, 50, "textures/left.png"))

        draw.draw_text((draw.height+10, 350), "Add to field: " + str(editor_add))

        gen = draw.draw_button("image", (draw.width - 340, 100, 340, 50, "textures/paper.png"), colors = (0,0,0), text = "Generate New")
        full = draw.draw_button("image", (draw.width - 350, 150, 350, 50, "textures/paper.png"), colors = (0,0,0), text = "Show Full Map")
        save = draw.draw_button("image", (draw.width - 340, 200, 340, 50, "textures/paper.png"), colors = (0,0,0), text = "Save This Map" )
        if gen:
            draw.display.fill((0,0,0))
            pygame.display.update()
            active_map = gener.generate()
        if full:
            app_step = "full"
        if add_minus:
            if editor_add > -50 and editor_add != 1:
                editor_add -= 1
            elif editor_add == 1:
                editor_add -= 2
        if add_plus:
            if editor_add < 50 and editor_add != -1:
                editor_add += 1
            elif editor_add == -1:
                editor_add += 2
        if map_up and editor_y > 0:
            editor_y -= 10
        if map_down:
            editor_y += 10
        if editor_y + 50 > len(active_map.map_list)-1:
            editor_y = len(active_map.map_list) - 51
        if editor_y < 0:
            editor_y = 0
        if map_left and editor_y > 0:
            editor_x -= 10
        if map_right:
            editor_x += 10
        if editor_x + 50 > len(active_map.map_list[0])-1:
            editor_x = len(active_map.map_list[0]) - 51
        if editor_x < 0:
            editor_x = 0
        if save:
            app_step = "save_map"
            
    if app_step == "full":
        draw.display.fill((0,0,0))
        if active_map != None:
            a = 0
            y_ = 0
            for y in range(1025):
                if a < 1:
                    a += (1025-768)/768 
                    y_ += 1
                    b = 0
                    x_ = 0
                    for x in range(1025):
                        if b < 1:
                            b += (1025-768)/768 
                            x_ += 1
                            color = get_map_color(active_map.get_field(x, y))
                            if color != (255, 0, 0):
                                draw.draw_shape("rect", (x_, y_, 1, 1), color)
                            else:
                                draw.draw_shape("rect", (x_-2, y_-2, 3, 3), color)
                        else:
                            b -= 1
                else:
                    a -= 1
        app_step = "stay_full"
    elif app_step == "stay_full":

        active_map.sort_place_by_type_x()
        
        draw.draw_shape("rect", (draw.height, 0, draw.width - draw.height, draw.height), (0,0,0))
        
        y = 120
        slep = editor_town_sleep

        for i in active_map.places_list.keys():
            if slep == 0:
                if y + 200 > draw.height:
                    break 
                draw.draw_img("textures/paper.jpg", (draw.height+10, y, draw.width - draw.height - 150, 200))
                if type(active_map.places_list[i]) == town:
                    draw.draw_text((draw.height+10, y), "Town: "+active_map.places_list[i].name, color = (0,0,0))
                if type(active_map.places_list[i]) == village:
                    draw.draw_text((draw.height+10, y), "Village: "+active_map.places_list[i].name, color = (0,0,0))
                draw.draw_text((draw.height+10, y+50), "X:" + i.split(",")[0] + "   Y:" + i.split(",")[1], color = (0,0,0))
                rem = draw.draw_button("image", (draw.height+10, y+100, 250, 50, "textures/paper.png"), colors = (0,0,0), text = "Remove")
                if rem:
                    del active_map.places_list[i]
                    app_step = "full"
                    draw.display.fill((0,0,0))
                    if editor_town_sleep >= len(active_map.places_list.keys())-1:
                        editor_town_sleep = len(active_map.places_list.keys())-2
                    if editor_town_sleep < 0:
                        editro_town_sleep = 0
                    break
                y += 220
            else:
                slep -= 1
        if editor_town_sleep > 0:
            place_up = draw.draw_button("fullimage", (draw.width-100, 300, 50, 50, "textures/up.png"))
            if place_up:
                editor_town_sleep -= 1
        if editor_town_sleep < len(active_map.places_list.keys())-1:
            place_down = draw.draw_button("fullimage", (draw.width-100, 400, 50, 50, "textures/down.png")) 
            if place_down:
                editor_town_sleep += 1
        add_t = draw.draw_button("image", (draw.height+35, 10, 260, 50, "textures/paper.png"), colors = (0,0,0), text = "Add Town")
        add_v = draw.draw_button("image", (draw.height+20, 60, 290, 50, "textures/paper.png"), colors = (0,0,0), text = "Add Village")
        back = draw.draw_button("image", (draw.width - 120, 100, 120, 50, "textures/paper.png"), colors = (0,0,0), text = "Back")
        if add_t:
            gener.add_place("town", active_map)
            app_step = "full"
        if add_v:
            gener.add_place("village", active_map)
            app_step = "full"
        if back:
            app_step = "editor"
    # end editor ---------- start game
    if app_step == "game":
        if active_character != None:
            map_type = draw.draw_switch("image", (0, 50, 50, "textures/paper.png"), "map_type", {"Map":0, "Minimap":1}, colors = (0,0,0), setifnot = 0)
            if map_type == 0:
                if active_character.pozition == []:
                    active_character.pozition_set(list(active_map.places_list.keys())[randint(0, len(active_map.places_list.keys())-1)].split(","))
                player_x = active_character.pozition[0]
                player_y = active_character.pozition[1]
                for x in range(0,7):
                    for y in range(0,7):
                        x_ = x
                        y_ = y
                        if len(active_map.map_list)-4 > player_x > 3:
                            x_ = x + player_x - 3
                        elif len(active_map.map_list)-4 <= player_x:
                            x_ = x + 1018
                        if len(active_map.map_list)-4 > player_y > 3:
                            y_ = y + player_y - 3
                        elif len(active_map.map_list)-4 <= player_y:
                            y_ = y + 1018
                        draw.draw_shape("rect", (x*int(draw.height//14), y*int(draw.height//14) + 100, int(draw.height//14)-1, int(draw.height//14)-1), get_map_color(active_map.get_field(x_, y_)))
                if len(active_map.map_list) - 3 > player_x > 2:
                    x = 3
                elif player_x <= 2:
                    x = player_x
                else:
                    x = 6 - (len(active_map.map_list) - 1 - player_x)
                if len(active_map.map_list) - 3 > player_y > 2:
                    y = 3
                elif player_y <= 2:
                    y = player_y
                else:
                    y = 6 - (len(active_map.map_list) - 1 - player_y)
                draw.draw_img("textures/Character.png", (x*(int(draw.height//14)), y*(int(draw.height//14)) + 100, (int(draw.height//14)), (int(draw.height//14))))
            elif map_type == 1:
                player_x = active_character.pozition[0]
                player_y = active_character.pozition[1]
                for x in range(51):
                    for y in range(51):
                        x_ = x
                        y_ = y
                        if len(active_map.map_list)-26 > player_x > 25:
                            x_ = x + player_x - 25
                        elif len(active_map.map_list)-26 <= player_x:
                            x_ = x + 974
                        if len(active_map.map_list)-26 > player_y > 25:
                            y_ = y + player_y - 25
                        elif len(active_map.map_list)-26 <= player_y:
                            y_ = y + 974
                        draw.draw_shape("rect", (x*int(draw.height//100), y*int(draw.height//100) + 100, int(draw.height//100)-1, int(draw.height//100)-1), get_map_color(active_map.get_field(x_, y_)))
                if len(active_map.map_list) - 25 > player_x > 24:
                    x = 25
                elif player_x <= 24:
                    x = player_x
                else:
                    x = 50 - (len(active_map.map_list) - 1 - player_x)
                if len(active_map.map_list) - 25 > player_y > 24:
                    y = 25
                elif player_y <= 24:
                    y = player_y
                else:
                    y = 6 - (len(active_map.map_list) - 1 - player_y)
                draw.draw_img("textures/Character.png", (x*int(draw.height//100), y*int(draw.height//100) + 100, int(draw.height//100)-1, int(draw.height//100)-1))
            up = eventInfo.is_in(273)
            down = eventInfo.is_in(274)
            right = eventInfo.is_in(275)
            left = eventInfo.is_in(276)
            if up[0] and up[1] == 1:
                if active_character.pozition[1] > 0:
                    active_character.up(active_map)
            if down[0] and down[1] == 1:
                if active_character.pozition[1] < len(active_map.map_list) - 1:
                    active_character.down(active_map)
            if right[0] and right[1] == 1:
                if active_character.pozition[0] < len(active_map.map_list) - 1:
                    active_character.right(active_map)
            if left[0] and left[1] == 1:
                if active_character.pozition[0] > 0:
                    active_character.left(active_map)
            draw.draw_text((draw.height//2,  50), "Nickname: {}".format(active_character.name))
            draw.draw_text((draw.height//2, 100), "X: {}".format(player_x))
            draw.draw_text((draw.height//2, 150), "Y: {}".format(player_y))
            draw.draw_text((draw.height//2, 200), "Lives: {}/{}".format(active_character.lives[0], active_character.lives[1]))
            draw.draw_text((draw.height//2, 250), "Mana: {}/{}".format(active_character.mana[0], active_character.mana[1]))
            if 1025 == active_map.get_field(active_character.pozition[0], active_character.pozition[1]):
                if type(active_map.places_list["{},{}".format(active_character.pozition[0], active_character.pozition[1])]) == town:
                    width, height = draw.draw_text((0,0), "Town", blit = False)
                    tow = draw.draw_button("image", (draw.height//2 + 200, 150, width + 10, 50, "textures/paper.png"), colors = (0,0,0), text = "Town")
                    if tow:
                        in_place = active_map.places_list["{},{}".format(active_character.pozition[0], active_character.pozition[1])]
                        app_step = "game_in_place_"
                elif type(active_map.places_list["{},{}".format(active_character.pozition[0], active_character.pozition[1])]) == village:
                    width, height = draw.draw_text((0,0), "Village", blit = False)
                    vil = draw.draw_button("image", (draw.height//2 + 200, 150, width + 10, 50, "textures/paper.png"), colors = (0,0,0), text = "Village")
                    if vil:
                        in_place = active_map.places_list["{},{}".format(active_character.pozition[0], active_character.pozition[1])]
                        app_step = "game_in_place_"
        else:
            app_step = "you"
    if app_step == "game_in_place":
        to_draw = ""
        if type(in_place) == village:
            map_list = in_place.village_map
        elif type(in_place) == town:
            map_list = in_place.town_map
        for y in range(len(map_list)):
            for x in range(len(map_list[y])):
                draw.draw_shape("rect", (x*10, y*10, 9, 9), get_place_color(map_list[y][x]))
        y = 50
        x = len(map_list[0]) * 10 + 15
        for i in in_place.buildings.keys():
            width, height = draw.draw_text((0, 0),  text = str(in_place.buildings[i]), blit = False)
            if x + width + 15 > draw.width - 200:
                x = len(map_list[0]) * 10 + 15
                y += 60
            some = draw.draw_button("image", (x, y, width+10, 50, "textures/paper.png"), text = str(in_place.buildings[i]), colors = (0,0,0))
            if x < mouse[0] < x + width+10 and y < mouse[1] < y + 50:
                to_draw = in_place.buildings[i].gen_to_draw_text()
            if some:
                use = in_place.buildings[i].come_in()
                if type(use) != str:
                    app_step = "come_to"
                    building = in_place.buildings[i]
                    break
                use = use.split("|")
                for i in use:
                    i = i.split(" ")
                    try:
                        num = int(i[0])
                        if i[1] == "coins":
                            if not active_character.remove_money(num):
                                break
                            else:
                                remove_coins = num
                        if i[1] == "lives":
                            if active_character.lives[0] + num <= active_character.lives[1]:
                                active_character.lives[0] += num
                                if active_character.lives[0] + num > active_character.lives[1]:
                                     active_character.lives[0] = active_character.lives[1]
                            else:
                                try:
                                    active_character.money += remove_coins
                                except:
                                    pass
                        if i[1] == "mana":
                            if active_character.mana[0] + num <= active_character.mana[1]:
                                active_character.mana[0] += num
                                if active_character.mana[0] + num > active_character.mana[1]:
                                     active_character.mana[0] = active_character.mana[1]
                            else:
                                try:
                                    active_character.money += remove_coins
                                except:
                                    pass
                        if i[1] == "maxlives":
                            active_character.lives[0] += num
                            active_character.lives[1] += num
                        if i[1] == "maxmana":
                            active_character.mana[0] += num
                            active_character.mana[1] += num
                    except:
                        if i[0] == "!":
                            try:
                                if i[4] == "*#":
                                    need = active_character.get_level()*int(i[3])
                                elif i[4] == "+#":
                                    need = active_character.get_level()+int(i[3])
                            except:
                                need = int(i[3])
                            if i[1] == "maxlives":
                                equalizer = active_character.lives[1]
                            elif i[1] == "maxmana":
                                equalizer = active_character.mana[1]
                            if i[2] == "<":
                                if equalizer >= need:
                                    break
                            elif i[2] == ">":
                                if equalizer <= need:
                                    break
                            elif i[2] == "=":
                                if equalizer != need:
                                    break
                            elif i[2] == "<=":
                                if equalizer > need:
                                    break
                            elif i[2] == ">=":
                                if equalizer < need:
                                    break

            x += width + 15
        draw.draw_text((len(map_list[0])*10+15, y + 60), to_draw)
        width, height = draw.draw_text((0,0), "Back", blit = False)
        back = draw.draw_button("image", (draw.width - (width + 10), 100, width+10, 50, "textures/paper.png"), text = "Back", colors = (0,0,0))
        if back:
            app_step = "game_"
    if app_step == "come_to":
        if building.typ in ["Shop", "Marketplace"]:
            if building.come_in() == []:
                app_step = "game_in_place"
                error = "There's Nothing to buy"
                error_time = [t.time(), 30]
                error_app_step = app_step
                error_pozition = (len(map_list[0]) * 10 + 15, 0)
        elif building.typ in ["Town Hall", "Casel"]:
            if building.come_in() == []:
                app_step = "game_in_place"
                error = "There's Nothing to do"
                error_time = [t.time(), 30]
                error_app_step = app_step
                error_pozition = (len(map_list[0]) * 10 + 15, 0)
        width, height = draw.draw_text((0,0), "Back", blit = False)
        back = draw.draw_button("image", (draw.width - (width + 10), 100, width+10, 50, "textures/paper.png"), text = "Back", colors = (0,0,0))
        if back:
            app_step = "game_in_place"


    # game end

    escape = eventInfo.get_keys()

    if settings.get_show_fps() and app_step not in ["stay_full", "full"]:
        a+=1
        fpsnow = a//(t.time() - now)
        if fpsnow > fps:
            fpsnow = fps
        fpsnow = int(fpsnow)
        draw.draw_text((0,0), str(fpsnow))
        if t.time() - now > 1:
            now = t.time()
            a = 0

    if error_app_step != app_step:
        error_time[1] = 0

    if error_time[1]+error_time[0] > t.time():
        draw.draw_text(error_pozition, error, color = (255,0,0), size = 40)
    
    if app_step not in ["menu", "menu_", "singup/in", "singup/in_"]:
        menu = draw.draw_button("image", (draw.width-140, 50, 140, 50, "textures/paper.png"), colors = (0, 0, 0), text = "Menu")
        if menu:
            app_step = "menu"

    if app_step not in ["menu", "singup/in_", "menu_", "setting_setting", "setting_default"]:
        exit_game = draw.draw_button("image", (draw.width-100,   0, 100, 50, "textures/paper.png"), colors = (0, 0, 0), text = "Exit", size = 50)
        if exit_game and not (eventInfo.mouse_down[2][1] < 1):
            exit_game = False
    for i in escape:
        try:
            for j in i:                
                if 27 == j[0]:
                    exit_game = True
        except:
            pass
    pygame.display.update()
    clock.tick(fps)
"""
Na Dodělání:
You 
Game
Help

Na předělání:
Settings"""