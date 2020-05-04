import pygame, sys, os, threading
from pygame.locals import *
import string

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

        self.abc = []
        for i in list(string.printable):
            if i not in list(string.whitespace):
                self.abc.append(i)

        self.images = {}
        self.fonts = {}
        self.entrys = {}
        self.switches = {}


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
        elif typ == "line":
            pygame.draw.line(self.display, color, geometry[0], geometry[1])

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
            self.draw_img(geometry[4], (geometry[0], geometry[1], geometry[2], geometry[3]))
            self.draw_text((geometry[0] + 5, geometry[1] + 5), text, size, font, colors)
        elif typ == "fullimage":
            self.draw_img(geometry[4], (geometry[0], geometry[1], geometry[2], geometry[3]))
        mouse = pygame.mouse.get_pos()
        if geometry[0] < mouse[0] < geometry[0] + geometry[2] and geometry[1] < mouse[1] < geometry[1] + geometry[3]:
            try:
                equal = False
                if 1 in self.event_info.mouse_down[1] and self.event_info.mouse_down[2][1] in [0]:
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
                if len(colors) < 2:
                    colors = [0, colors[0]]
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
            self.draw_img(geometry[4], (geometry[0], geometry[1], geometry[2], geometry[3]))
            
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
                    elif i[1].unicode in self.abc:
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
        
    def draw_switch(self, typ, geometry, switchID, buttons, horizontal = False, **args):
        """typ = "shape" or "image" 
        
if shape -> need geometry = (x, y, long), colors = [borderColor, textColor], switchID, buttons = {"buttonText": value}, horizontal = bool, setifnot = value, font and size

if image -> need geometry = (x, y, long, path), colors = [textColor], switchID, buttons = {"buttonText": value}, horizontal = bool, setifnot = value, font and size

required arguments  =  typ, geometry, switchID, colors, buttons"""
        if switchID not in self.switches.keys():
            try:
                self.switches[switchID] = args["setifnot"]
            except:
                self.switches[switchID] = None
        if typ == "shape":
            try:
                colors = args["colors"]
            except:
                raise ValueError("colors is not define")
        elif typ == "image":
            try:
                colors = args["colors"]
                if len(colors) > 1 and type(colors[0]) in [list, tuple]:
                    colors = colors[0]
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

        lenghts = []
        for i in buttons.keys():
            width, height = self.draw_text((0,0), i, blit = False)
            if horizontal:
                lenghts.append(height - 2)
            else:
                lenghts.append(width + 10)
        try:
            x, y, height = geometry
        except:
            x, y, height, path = geometry
        mouse = pygame.mouse.get_pos()
        for i in range(len(buttons.keys())):
            if x < mouse[0] < x + lenghts[i] + 8 and y < mouse[1] < y + 50:
                    try:
                        if 1 in self.event_info.get_mouse()[0]:
                            if 1 <= self.event_info.mouse_down[2][1]:
                                self.switches[switchID] = buttons[list(buttons.keys())[i]]
                    except TypeError as er:
                        pass
            if typ == "shape" and not horizontal:
                self.draw_shape("rect", (x, y, lenghts[i] + 10, height), colors[1])
                self.draw_shape("rect", (x+1, y+1, lenghts[i] + 8, height - 2), colors[0])
                self.draw_text((x+5,y), list(buttons.keys())[i], size, font, colors[1])
                if self.switches[switchID] == buttons[list(buttons.keys())[i]]:
                    self.draw_shape("line", [(x + 5, y + size - 5), (x + 5 + lenghts[i], y + size - 5)], colors[1])
                    self.draw_shape("line", [(x + 5, y + size - 6), (x + 5 + lenghts[i], y + size - 6)], colors[1])
                    self.draw_shape("line", [(x + 5, y + size - 7), (x + 5 + lenghts[i], y + size - 7)], colors[1])
                x += lenghts[i] + 8
            if typ == "image" and not horizontal:
                self.draw_img(path, (x, y, lenghts[i] + 10, height))
                self.draw_text((x+5,y), list(buttons.keys())[i], size, font, colors)
                if self.switches[switchID] == buttons[list(buttons.keys())[i]]:
                    self.draw_shape("line", [(x + 5, y + size - 5), (x + 5 + lenghts[i], y + size - 5)], colors)
                    self.draw_shape("line", [(x + 5, y + size - 6), (x + 5 + lenghts[i], y + size - 6)], colors)
                    self.draw_shape("line", [(x + 5, y + size - 7), (x + 5 + lenghts[i], y + size - 7)], colors)
                x += lenghts[i] + 10
            if typ == "shape" and horizontal:
                self.draw_shape("rect", (x, y, height, lenghts[i]), colors[1])
                self.draw_shape("rect", (x+1, y+1, height-2, lenghts[i]-2), colors[0])
                self.draw_text((x+5,y), list(buttons.keys())[i], size, font, colors[1])
                if self.switches[switchID] == buttons[list(buttons.keys())[i]]:
                    self.draw_shape("line", [(x + 5, y + size - 5), (x + 5 + lenghts[i], y + size - 5)], colors[1])
                    self.draw_shape("line", [(x + 5, y + size - 6), (x + 5 + lenghts[i], y + size - 6)], colors[1])
                    self.draw_shape("line", [(x + 5, y + size - 7), (x + 5 + lenghts[i], y + size - 7)], colors[1])
                y += lenghts[i]
            if typ == "image" and horizontal:
                self.draw_img(path, (x, y, height, lenghts[i]))
                self.draw_text((x+5,y), list(buttons.keys())[i], size, font, colors)
                if self.switches[switchID] == buttons[list(buttons.keys())[i]]:
                    self.draw_shape("line", [(x + 5, y + size - 5), (x + 5 + lenghts[i], y + size - 5)], colors)
                    self.draw_shape("line", [(x + 5, y + size - 6), (x + 5 + lenghts[i], y + size - 6)], colors)
                    self.draw_shape("line", [(x + 5, y + size - 7), (x + 5 + lenghts[i], y + size - 7)], colors)
                y += lenghts[i]
            
        return self.switches[switchID]
            
            
