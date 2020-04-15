import pygame, sys, os, threading
from pygame.locals import *

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()


class drawer:
    def __init__(self, settings, event_info):
        self.event_info = event_info
        self.width, self.height = settings.get_wide()
        if settings.fullscreen():
            self.display = pygame.display.set_mode([self.width, self.height], pygame.FULLSCREEN)
        else:
            self.display = pygame.display.set_mode([self.width, self.height])
        pygame.display.set_caption('Tydral')

        self.images = {}
        self.fonts = {}


    def draw_img(self, path: str, geometry: list, rotate = 0):
        if path not in self.images.keys():
            self.images[path] = pygame.image.load(path)
        image = self.images[path]
        image = pygame.transform.rotate(image, rotate)
        self.display.blit(image) 

    def draw_text(self, pozition: list, text = "", size = 50, font = "PalatinoLinoType", color = (255, 255, 255), blit = True):
        if "{},{}".format(font, size) not in self.fonts.keys():
            self.fonts["{},{}".format(font, size)] = pygame.font.SysFont(font, size)
        font = self.fonts["{},{}".format(font, size)]
        self.display.blit(font.render(text, True, color), (pozition[0], pozition[1]))

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
        
        if fullimage -> need geometry (x, y, longX, longY, path)"""
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
        try:
            equal = False
            where, when = args["equalizer"].split(",")
            if where == "up" and self.event_info.get_mouse()[1]:
                if int(when) in self.event_info.get_mouse()[1]:
                    equal = True 
            elif where == "down" and self.event_info.get_mouse()[0]:
                if int(when) in self.event_info.get_mouse()[0]:
                    equal = True 
        except:
            equal = False
        return equal
            
