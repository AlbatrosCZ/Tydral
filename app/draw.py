import pygame, sys, os, threading
from pygame.locals import *

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()


class drawer:
    def __init__(self, settings, event_info):
        self.event_info = event_info
        self.width, self.height = settings.get_wide()
        self.settings = settings
        if settings.get_fullscreen():
            self.display = pygame.display.set_mode([self.width, self.height], pygame.FULLSCREEN)
        else:
            self.display = pygame.display.set_mode([self.width, self.height])
        pygame.display.set_caption('Tydral')

        self.images = {}
        self.fonts = {}
        self.entrys = {}


    def draw_img(self, path: str, geometry: list, rotate = 0):
        if path not in self.images.keys():
            self.images[path] = pygame.image.load(path)
        image = self.images[path]
        image = pygame.transform.scale(image, (geometry[2], geometry[3]))
        image = pygame.transform.rotate(image, rotate)
        self.display.blit(image, geometry) 

    def draw_text(self, pozition: list, text = "", size = 50, font = "PalatinoLinoType", color = (255, 255, 255), blit = True):
        if "{},{}".format(font, size) not in self.fonts.keys():
            self.fonts["{},{}".format(font, size)] = pygame.font.SysFont(font, size)
        font = self.fonts["{},{}".format(font, size)]
        text = font.render(text, True, color)
        if blit:
            self.display.blit(text, (pozition[0], pozition[1]))
        else:
            return text.get_width(), text.get_height()

    def draw_shape(self, typ, geometry, color):
        if typ == "rect":
            pygame.draw.rect(self.display, color, geometry)
        elif typ == "poly":
            pygame.draw.polygon(self.display, color, geometry)
        elif typ == "oval":
            pygame.draw.ellipse(self.display, color, geometry)

    def draw_button(self, typ, geometry, **args):
        """typ = "shape" or "image" or "fullimage" 

        if shape -> need geometry = (x, y, longX, longY), colors = [borderColor, textColor], text, font and size
        
        if image -> need geometry = (x, y, longX, longY, path), colors = [textColor], text, font and size
        
        if fullimage -> need geometry (x, y, longX, longY, path)
        
        required arguments  =  typ, geometry, colors(not in fullimage)"""
        if typ == "shape":
            try:
                colors = args["colors"]
            except:
                raise ValueError("colors is not define")
            try:
                text = args["text"]
            except:
                text = ""
            try:
                font = args["font"]
            except:
                font = "PalatinoLinoType"
            try:
                size = args["size"]
            except:
                size = 50
            mouse = pygame.mouse.get_pos()
            if geometry[0] < mouse[0] < geometry[0] + geometry[2] and geometry[1] < mouse[1] < geometry[1] + geometry[3] and self.event_info.mouse_down[0]:
                self.draw_shape("rect", geometry, colors[0])
                self.draw_shape("rect", (geometry[0] + 1, geometry[1] + 1, geometry[2] - 2, geometry[3] - 2), colors[1])
                self.draw_text((geometry[0] + 5, geometry[1] + 5), text, size, font, colors[0])
            else:
                self.draw_shape("rect", geometry, colors[1])
                self.draw_shape("rect", (geometry[0] + 1, geometry[1] + 1, geometry[2] - 2, geometry[3] - 2), colors[0])
                self.draw_text((geometry[0] + 5, geometry[1] + 5), text, size, font, colors[1])
        elif typ == "image":
            try:
                colors = args["colors"]
            except:
                raise ValueError("colors is not define")
            try:
                text = args["text"]
            except:
                text = ""
            try:
                font = args["font"]
            except:
                font = "PalatinoLinoType"
            try:
                size = args["size"]
            except:
                size = 50
            self.draw_img(geometry[4], geometry)
            self.draw_text((geometry[0] + 5, geometry[1] + 5), text, size, font, colors[1])
        elif typ == "fullimage":
            self.draw_img(geometry[4], geometry)
        if geometry[0] < mouse[0] < geometry[0] + geometry[2] and geometry[1] < mouse[1] < geometry[1] + geometry[3]:
            try:
                equal = False
                where, when = args["equalizer"].split(",")
                if where == "up" and self.event_info.get_mouse()[1]:
                    if int(when) in self.event_info.get_mouse()[1]:
                        equal = True 
                elif where == "down" and self.event_info.get_mouse()[0]:
                    if int(when) in self.event_info.get_mouse()[0] and self.event_info.mouse_down[2][int(when)] == 0:
                        equal = True 
            except:
                equal = False
                try:
                    if 1 in self.event_info.get_mouse()[0] and self.event_info.mouse_down[2][1] == 0:
                        equal = True
                except:
                    pass
        else:
            equal = False
        return equal

    def draw_entry(self, typ, geometry, entryId, **args):
        """typ = "shape" or "image" 
        
        if shape -> need geometry = (x, y, longX, longY), colors = [borderColor, textColor], text_type, font and size
        
        if image -> need geometry = (x, y, longX, longY, path), colors = [textColor], text_type, font and size
        
        required arguments  =  typ, geometry, entryID, colors"""
        if entryId not in self.entrys.keys():
            self.entrys[entryId] = ["", 0, False] 
        text = self.entrys[entryId][0]
        show = self.entrys[entryId][1]
        write = self.entrys[entryId][2]
        if typ == "shape":
            try:
                colors = args["colors"]
            except:
                raise ValueError("colors is not define")
            try:
                font = args["font"]
            except:
                font = "PalatinoLinoType"
            try:
                size = args["size"]
            except:
                size = 50
            self.draw_shape("rect", geometry, colors[1])
            self.draw_shape("rect", (geometry[0] + 1, geometry[1] + 1, geometry[2] - 2, geometry[3] - 2), colors[0])
        elif typ == "image":
            try:
                colors = args["colors"]
            except:
                raise ValueError("colors is not define")
            try:
                font = args["font"]
            except:
                font = "PalatinoLinoType"
            try:
                size = args["size"]
            except:
                size = 50
        fps = self.settings.get_fps()
        if self.event_info.get_keys()[0] and write:
            for i in self.event_info.get_keys()[0]:
                if i[2] == 1 or i[2] > fps * 2 and i[2] % fps in [0, fps//4, fps//2, fps//2 + fps//4]:
                    if i[0] == K_BACKSPACE:
                        if len(text) > 0:
                            text = text[0:-1] 
                            if show >= len(text) and show != 0:
                                show = len(text) - 1
                    elif i[0] == K_LEFT:
                        if show > 0:
                            show -= 1
                    elif i[0] == K_RIGHT:
                        if show < len(text)-1:
                            show += 1
                    elif i[1].unicode != "":
                        text += i[1].unicode
        mouse = pygame.mouse.get_pos()
        try:
            if 1 in self.event_info.get_mouse()[0] and geometry[0] < mouse[0] < geometry[0] + geometry[2] and geometry[1] < mouse[1] < geometry[1] + geometry[3]:
                for i in self.entrys:
                    self.entrys[i][2] = False
                write = True
            elif 1 in self.event_info.get_mouse()[0]:
                write = False
        except Exception as er:
            pass
        self.entrys[entryId][0] = text
        self.entrys[entryId][1] = show
        self.entrys[entryId][2] = write
        try:
            if args["text_type"] == "password":
                text = "#"*len(text)
        except:
            pass
        try:
            maxim = len(text)  
            while self.draw_text(geometry, text[show:maxim] + "|", size, font, blit = False)[0] > geometry[2]:
                maxim -= 1
            if write:
                text = text[show:maxim] + "|"
            else:
                text = text[show:maxim]
        except LookupError as e:
            text = "|"
        
        self.draw_text((geometry[0] + 5, geometry[1] + 5), text, size, font, colors[1])
        return self.entrys[entryId][0]
        
                
            
