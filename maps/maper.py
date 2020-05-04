from threading import Thread
from app.classes import *
import os, pickle, time

class saver(Thread):
    def __init__(self):
        super().__init__()
        self.maps = []
        self.maps_to_save = []
        self.running = True
        self.nothing_to_do = 0
        self.load_all()

    def save(self, mapa):
        if mapa not in self.maps:
            self.maps.append(mapa)
        if mapa.name:
            self.maps_to_save.append([mapa, "maps/"+mapa.name])
        else:
            map_name = "map"
            num = 1
            need = True
            while need:
                need = False
                for i in self.maps:
                    if i.name == map_name+str(num):
                        need = True
                        break
            mapa.name = map_name + str(num)
            self.maps_to_save.append([mapa, "maps/"+map_name+str(num)])
                
    def list_dir(self, directory = "maps/"):
        maps = []
        for i in os.listdir(directory):
            try:
                if i.split(".")[-1] == "tmap":
                    maps.append(directory + "/" + i)
                else:
                    try:
                        maps += self.list_dir(directory + "/" + i)
                    except:
                        pass
            except:
                try:
                    maps += self.list_dir(directory + "/" + i)
                except:
                    pass
        return maps

    def load(self, name):
        for i in self.maps:
            if i.name == name:
                return i
        maps_directory = self.list_dir()
        for i in maps_directory:
            if ".".join(i.split("/")[-1].split(".")[0:-1]) == name:
                return self.load_from(i)
        return False

    def load_from(self, directory):
        directory = open(directory, "rb")
        return pickle.load(directory)

    def run(self):
        while self.running:
            if len(self.maps_to_save) > 0:
                pickle.dump(self.maps_to_save[0][0], open(self.maps_to_save[0][1]+".tmap", "wb"))
                del self.maps_to_save[0]
                self.nothing_to_do = 0
            else:
                time.sleep(0.1)
                self.nothing_to_do += 1 
            if self.nothing_to_do == 50:
                self.nothing_to_do = 0
                self.load_all()

    def load_all(self):
        maps_directory = self.list_dir()
        for i in maps_directory:
            a = self.load_from(i)
            can = True
            for i in self.maps:
                if a.name == i.name:
                    can = False
            if can:
                self.maps.append(a)
        return self.maps

  