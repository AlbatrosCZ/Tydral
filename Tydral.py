from app.forAll import *
from app.generator import *
from settings.settings import setting 
from players.players import players
print("\rPreloading:", 25, "%", end = "") # Other part of app
from time import *
from math import *
print("\rPreloading:", 50, "%", end = "") # Python parts

# textures from : 
# https://unsplash.com/@stephanie_moody, 
# http://www.vadreal.sk/crumpled-white-paper-texture-melemel-jpeg_260159/,
# http://www.cleanpng.com,
# https://www.uihere.com, 

try:
    settings = setting()
except:
    import settings.install_settings
    settings = setting()
try:
    player_logger = players()
except:
    import players.install_players
    player_logger = players()
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

moving = 1
move = 1

error = ""
error_time = [0,0]
error_app_step = ""

a = 0           # FPS counter
now = time()
print("\rGame start now                       ")
while True:
    draw.draw_img("textures/Wood Board.jpg", (0, 0, draw.width, draw.height))
    if eventInfo.set_(pygame.event.get()) or exit_game:
        pygame.quit()
        if app_step == "setting_setting":
            from settings import install_settings
        sys.exit()
        break

    if app_step not in ["menu", "singup/in"]:
        menu = draw.draw_button("shape", geometry = (draw.width-140,  50, 140, 50), colors = [(255,255,255), (255, 0, 0)], text = "Menu", size = 50)
        if menu:
            app_step = "menu"
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
                app_step = "menu"
                player_nickname = nickname
            else:
                error = "Wrong password or nickname"
                error_time = [time(), 30]
                error_app_step = app_step
        
        if enter:
            if player_logger.add(nickname, password):
                app_step = ""
            else:
                error = "Can't use this user name"
                error_time = [time(), 30]
                error_app_step = app_step
                
    # sing in / sing up end ---------- menu start
    if app_step == "menu":
        width, height = draw.draw_text((draw.width-250,0), "Sing up as "+nickname, size = 40, blit=False)
        draw.draw_text((draw.width-width,0), "Sing up as "+nickname, size = 40)
        player_login = draw.draw_button("shape", (draw.width-(width+125),0,125,40), colors = [(255,205,100), (0,0,0)], text = "Sing out", size = 30)
        game = draw.draw_button("image", geometry = (draw.width//2-73, 160, 146, 50, "textures/paper.png"), colors = (0, 0, 0),     text = "Game",    size = 50)
        help_ = draw.draw_button("image", geometry = (draw.width//2-60, 220, 120, 50, "textures/paper.png"), colors = (0, 0, 0),     text = "Help",    size = 50)
        edit = draw.draw_button("image", geometry = (draw.width//2-75, 280, 150, 50, "textures/paper.png"), colors = (0, 0, 0),     text = "Editor",    size = 50)
        setting = draw.draw_button("image", geometry = (draw.width//2-83, 340, 166, 50, "textures/paper.png"), colors = (0, 0, 0),     text = "Setting",    size = 50)
        exit_game = draw.draw_button("image", geometry = (draw.width//2-50, 400, 100, 50, "textures/paper.png"), colors = (255, 0, 0),     text = "Exit",    size = 50)
        draw.draw_img("textures/knight.png",  (draw.width//2-450, 80, 350, 600))
        draw.draw_img("textures/knight2.png", (draw.width//2, 80, 600, 600))
        if game:
            app_step = "game"
        elif help_:
            app_step = "help"
        elif edit:
            app_step = "editor"
        elif setting:
            app_step = "settings"
        elif player_login:
            app_step = "singup/in"
            nickname = ""
            password = ""
    # menu end ---------- settings start
    if app_step == "settings":
        window = draw.draw_button("shape", geometry = (0, 40, 200, 50), colors = [(255,255,255), (0, 255, 0)],     text = "Window",    size = 50)
        you = draw.draw_button("shape", geometry = (0, 100, 100, 50), colors = [(255,255,255), (0, 255, 0)],     text = "You",    size = 50)
        if window:
            app_step = "setting_setting"
            exit_game = True
        elif you:
            app_step = "you"
    # settings end ---------- you start
    if app_step == "you":
        pass
    


    moving += move 
    if moving > draw.width-1:
        move = -1
    elif moving < 1:
        move = 1
    escape = eventInfo.get_keys()

    if settings.get_show_fps():
        a+=1
        fpsnow = a//(time() - now)
        if fpsnow > fps:
            fpsnow = fps
        fpsnow = int(fpsnow)
        draw.draw_text((0,0), str(fpsnow))
        if time() - now > 1:
            now = time()
            a = 0

    if error_app_step != app_step:
        error_time[1] = 0

    if error_time[1]+error_time[0] > time():
        draw.draw_text((0,60), error, color = (100,0,0), size = 40)
    

    if app_step not in ["menu", "setting_setting"]:
        exit_game = draw.draw_button("shape", geometry = (draw.width-100,   0, 100, 50), colors = [(255,255,255), (255, 0, 0)], text = "Exit", size = 50)
    
    for i in escape:
        try:
            for j in i:                
                if 27 == j[0]:
                    exit_game = True
        except:
            pass
    pygame.display.update()
    clock.tick(fps)