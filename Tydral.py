from app.draw import *
from app.forAll import *
from settings.settings import setting
from players.players import players
print("\rPreloading:", 25, "%", end = "") # Other part of app
from time import *
from math import *
print("\rPreloading:", 50, "%", end = "") # Python parts



try:
    settings = setting()
except:
    import settings.install_settings as install
    settings = setting()
try:
    player_logger = players()
except:
    import players.install_players as install
    player_logger = players()
print("\rPreloading", 70, "%", end = "") # Database

eventInfo = forAll() 
clock = pygame.time.Clock()
draw = drawer(settings, eventInfo)
print("\rPreloading:", 100, "%", end = "") # Create Window
print("\rLoading start in few secunds", end = "")

exit_game = False # Exit window

fps = settings.get_fps() # Load max Fps

app_step = "singin" # Set step of game

rsing = "up" # reverse step of sing in/un
sing = "in" # step of sing up/in

moving = 1
move = 1

error = ""
error_time = [0,0]

a = 0           # FPS counter
now = time()
print("\rGame start now                       ")
while True:
    draw.display.fill((0, 0, 0))
    if eventInfo.set_(pygame.event.get()) or exit_game:
        pygame.quit()
        sys.exit()
        break

    if app_step not in ["menu", "singin", "singup"]:
        menu = draw.draw_button("shape", geometry = (draw.width-100,  50, 100, 50), colors = [(0, 0, 0), (255, 0, 0)], text = "Menu", size = 50)
    
    if app_step in ["singup", "singin"]:
        draw.draw_img("textures/Game_Logo.png", (0,100, draw.height-200, draw.height-200))
        
        draw.draw_text((draw.height-200, 60), "Nickname", color=(0,255,0))
        draw.draw_text((draw.height-200, 160), "Password", color=(0,255,0))
        x_wide = draw.width - (draw.height-200) - 50
        nickname = draw.draw_entry("shape", (draw.height-200, 100, x_wide, 50), "player_nickname", colors = [(0,0,0), (0,255,0)])
        password = draw.draw_entry("shape", (draw.height-200, 200, x_wide, 50), "player_password", colors = [(0,0,0), (0,255,0)], text_type = "password")

        log = draw.draw_button("shape", (draw.height-200, 300, 180, 50), colors = [(0,0,0), (0,255,0)], text = "Sing "+rsing)
        enter = draw.draw_button("shape", (draw.height, 300, 180, 50), colors = [(0,0,0), (0,255,0)], text = "Sing "+sing)

        if log:
            if sing == "up":
                sing = "in"
                rsing = "up"
            else:
                sing = "up"
                rsing = "in"
        
        if enter:
            if sing == "up":
                if player_logger.add(nickname, password):
                    app_step = "menu"
                else:
                    error = "Nickname is already used"
                    error_time = [time(), 30]
            elif sing == "in":
                if player_logger.login(nickname, password):
                    app_step = "menu"
                else:
                    error = "Wrong password or nickname"
                    error_time = [time(), 30]

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

    if error_time[1]+error_time[0] > time():
        draw.draw_text((0,60), error, color = (255,0,0))
    


    exit_game = draw.draw_button("shape", geometry = (draw.width-100,   0, 100, 50), colors = [(0, 0, 0), (255, 0, 0)], text = "Exit", size = 50)
    for i in escape:
        try:
            for j in i:                
                if 27 == j[0]:
                    exit_game = True
        except:
            pass
    pygame.display.update()
    clock.tick(fps)