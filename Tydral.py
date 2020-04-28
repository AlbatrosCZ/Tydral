import platform as plf
if plf.system() == "Linux":
    pass
elif plf.system == "Windows":
    pass
from app.forAll import *
from app.generator import *
from settings.settings import setting 
from players.players import *
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

error = ""
error_time = [0,0]
error_app_step = ""

editor_add = 1
editor_timer = tim.time()
editor_x = 0
editor_y = 0
editor_town_sleep = 0

a = 0           # FPS counter
now = t.time()
print("\rGame start now                       ")
while True:
    mouse = pygame.mouse.get_pos()
    if app_step not in ["editor", "full", "stay_full"]:
        draw.draw_img("textures/Wood Board.jpg", (0, 0, draw.width, draw.height))
    elif app_step != "stay_full":
        draw.display.fill((0,0,0))
    if eventInfo.set_(pygame.event.get()) or exit_game:
        pygame.quit()
        if app_step == "setting_setting":
            from settings import install_settings
            install_settings.install_settings()
        elif app_step == "setting_default":
            from defaults import install_default
            install_default.install_default()
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
        

        log = draw.draw_button("shape", (draw.width-200, 300, 180, 50), colors = [(255,205,100), (0,0,0)], text = "Sing in")
        enter = draw.draw_button("shape", (draw.width-200, 360, 180, 50), colors = [(255,205,100), (0,0,0)], text = "Sing up")
        if show_pass:
            s_h = "  Hide"
            password = draw.draw_entry("image", (draw.height-200, 200, x_wide, 50, "textures/paper.jpg"), "player_password", colors = [(0,0,0)])
        else:
            s_h = "  Show"
            password = draw.draw_entry("image", (draw.height-200, 200, x_wide, 50, "textures/paper.jpg"), "player_password", colors = [(0,0,0)], text_type = "password")
        sp = draw.draw_button("shape", (draw.width-200, 420, 180, 50), colors = [(255,205,100), (0,0,0)], text = s_h)

        if sp:
            if show_pass:
                show_pass = False
            else:
                show_pass = True

        if log:
            if player_logger.login(nickname, password):
                app_step = "menu_"
                player_nickname = nickname
            else:
                error = "Wrong password or nickname"
                error_time = [t.time(), 30]
                error_app_step = app_step
        
        if enter:
            if player_logger.add(nickname, password):
                app_step = "menu_"
                player_nickname = nickname
            else:
                error = "Can't use this user name"
                error_time = [t.time(), 30]
                error_app_step = app_step
        try:
            if (enter or log) and player_nickname == nickname:
                log_in = Player(nickname, password)
        except:
            pass
                
    # sing in / sing up end ---------- menu start
    if app_step == "menu":
        width, height = draw.draw_text((draw.width-250,0), "Sing up as "+nickname, size = 40, blit=False)
        draw.draw_text((draw.width-width,0), "Sing up as "+nickname, size = 40, color=(0, 0, 0))
        player_login = draw.draw_button("shape", (draw.width-(width+125),0,125,40), colors = [(255,205,100), (0,0,0)], text = "Sing out", size = 30)
        game = draw.draw_button("image", geometry = (draw.width//2-73, 160, 146, 50, "textures/paper.png"), colors = (0, 0, 0),     text = "Game",    size = 50)
        help_ = draw.draw_button("image", geometry = (draw.width//2-60, 220, 120, 50, "textures/paper.png"), colors = (0, 0, 0),     text = "Help",    size = 50)
        edit = draw.draw_button("image", geometry = (draw.width//2-75, 280, 150, 50, "textures/paper.png"), colors = (0, 0, 0),     text = "Editor",    size = 50)
        setting = draw.draw_button("image", geometry = (draw.width//2-83, 340, 166, 50, "textures/paper.png"), colors = (0, 0, 0),     text = "Setting",    size = 50)
        exit_game = draw.draw_button("image", geometry = (draw.width//2-50, 400, 100, 50, "textures/paper.png"), colors = (255, 0, 0),     text = "Exit",    size = 50)
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
    # menu end ---------- settings start
    if app_step == "settings":
        window = draw.draw_button("image", geometry = (draw.width//2-100, 160, 200, 50, "textures/paper.png"), colors = (0, 0, 0),     text = "Window",    size = 50)
        you = draw.draw_button("image", geometry = (draw.width//2-50, 220, 100, 50, "textures/paper.png"), colors = (0, 0, 0),     text = "You",    size = 50)
        default = draw.draw_button("image", geometry = (draw.width//2-100, 280, 200, 50, "textures/paper.png"), colors = (0, 0, 0),     text = "Plugins",    size = 50)
        if window:
            app_step = "setting_setting"
            exit_game = True
        elif you:
            app_step = "you_"
        elif default:
            app_step = "setting_default"
            exit_game = True
    # settings end ---------- you start - dokonči
    if app_step == "you":
        draw.draw_text((100, 80), "Player: "+nickname)
    # you end ---------- editor start 
    if app_step == "editor":
        if active_map != None:
            for x in range(50):
                for y in range(50):
                    x_ = x + editor_x
                    y_ = y + editor_y
                    if x * int(draw.height//50) < mouse[0] < x * int(draw.height//50) + int(draw.height//50)+2 and y * int(draw.height//50) < mouse[1] < y * int(draw.height//50) + int(draw.height//50) + 2:
                        draw.draw_shape("rect", (x*int(draw.height//50)-2, y*int(draw.height//50)-2, int(draw.height//50)+2, int(draw.height//50)+2), (255, 255, 255))
                        try:
                            if 1 in eventInfo.get_mouse()[0]:
                                if tim.time() - editor_timer > 0.1:
                                    editor_timer = tim.time()
                                    active_map.set_field(x_, y_, editor_add)
                        except:
                            pass
                    draw.draw_shape("rect", (x*int(draw.height//50), y*int(draw.height//50), int(draw.height//50)-2, int(draw.height//50)-2), get_map_color(active_map.get_field(x_, y_)))
                    text = str(active_map.get_field(x_, y_))
                    if text != "1025":
                        color_ = get_map_color(int(text))
                        color = (255 - color_[0], 255 - color_[1], 255 - color_[2])
                        text = str(int(text)-100)
                        draw.draw_text((x*int(draw.height//50), y*int(draw.height//50)), text, 13, color = color)

        add_minus = draw.draw_button("fullimage", (draw.height+100, 150, 50, 50, "textures/minus.png"))
        add_plus = draw.draw_button("fullimage", (draw.height+50, 150, 50, 50, "textures/plus.png"))

        map_up = draw.draw_button("fullimage", (draw.height+100, 300, 50, 50, "textures/up.png"))
        map_down = draw.draw_button("fullimage", (draw.height+100, 400, 50, 50, "textures/down.png"))
        map_right = draw.draw_button("fullimage", (draw.height+150, 350, 50, 50, "textures/right.png"))
        map_left = draw.draw_button("fullimage", (draw.height+50, 350, 50, 50, "textures/left.png"))

        draw.draw_text((draw.height+10, 100), "Add to field: " + str(editor_add))

        gen = draw.draw_button("image", (draw.width - 250, 100, 250, 50, "textures/paper.png"), colors = (0,0,0), text = "Generate new")
        full = draw.draw_button("image", (draw.width - 250, 150, 250, 50, "textures/paper.png"), colors = (0,0,0), text = "Show Full Map")
        if gen:
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
        
        draw.draw_shape("rect", (draw.height, 0, draw.width - draw.height, draw.height), (0,0,0))
        
        y = 50
        slep = editor_town_sleep

        for i in active_map.places_list.keys():
            if slep == 0:
                if y + 200 > draw.height:
                    break 
                draw.draw_img("textures/paper.jpg", (draw.height+10, y, draw.width - draw.height - 150, 200))
                draw.draw_text((draw.height+10, y), active_map.places_list[i].name, color = (0,0,0))
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
        back = draw.draw_button("image", (draw.width - 100, 100, 100, 50, "textures/paper.png"), colors = (0,0,0), text = "Back")
        if back:
            app_step = "editor"
    escape = eventInfo.get_keys()

    if settings.get_show_fps() and app_step not in ["stay_full"]:
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
        draw.draw_text((0,60), error, color = (100,0,0), size = 40)
    
    if app_step not in ["menu", "singup/in"]:
        menu = draw.draw_button("image", (draw.width-100, 50, 100, 50, "textures/paper.png"), colors = (0, 0, 0), text = "Menu")
        if menu:
            app_step = "menu"
    if app_step not in ["menu", "setting_setting", "setting_default"]:
        exit_game = draw.draw_button("image", (draw.width-100,   0, 100, 50, "textures/paper.png"), colors = (0, 0, 0), text = "Exit", size = 50)
    
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