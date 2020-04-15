from app.draw import *
from app.forAll import *
from settings.settings import setting

clock = pygame.time.Clock()

eventInfo = forAll() 
try:
    settings = setting()
except:
    import install_settings as install
    settings = setting()
draw = drawer(settings, eventInfo)

x = [2,0]
y = [2,0]

s = pygame.Surface((1000,750))
s.set_alpha(20)
s.fill((0,0,0))
show = True
exit_game = False
screen_size = {"width":settings.get_wide()[0],"height":settings.get_wide()[1]}
fps = settings.get_fps()

while True:
    if eventInfo.set_(pygame.event.get()) or exit_game:
        pygame.quit()
        sys.exit()

    exit_game = draw.draw_button("shape", geometry = (screen_size["width"]-100, 0, 100, 50), colors = [(0, 0, 0), (255, 0, 0)], text = "Exit", size = 50, equalizer = "down,1")

    escape = eventInfo.get_keys()
    for i in escape:
        try:
            for j in i:                
                if 27 in j:
                    exit_game = True
        except:
            pass
    pygame.display.update()
    clock.tick(fps)