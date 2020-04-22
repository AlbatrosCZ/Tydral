from sqlite3 import *

class setting:
    def __init__(self, path = "settings/settings.db"):
        
        try:
            open(path)

        except:
            raise ValueError("Need to install Settings")

        self.path = path
        self.connection = connect(path)
        self.connection.isolation_level = None
        self.curs = self.connection.cursor()
        
        try:
            self.curs.execute(
            "SELECT name FROM sqlite_master WHERE type=\'table\'")
            tryer = self.curs.fetchall()
            need_to = ["Window"]
            for i in tryer:
                for j in range(len(need_to)):
                    if i[0] == need_to[j]:
                        del need_to[j]
            if len(need_to) > 0:
                raise ValueError("Need to install Settings")
        except:
            raise ValueError("Need to install Settings")
        try:
            self.get_fullscreen()
            self.get_wide()
            self.get_fps()
            self.get_show_fps()
        except:
            raise ValueError("Need to install Settings")


    def select(self, table: str, items: list = ["*"], where: str = "1"):
        try:
            self.curs.execute("SELECT {} FROM {} WHERE {}".format(", ".join(items), table, where))
            exitcode = self.curs.fetchall()
            if exitcode == []:
                raise ValueError("Nothing")
            return exitcode
        except:
            return False

    # Get Function
    def get_fullscreen(self):
        try:
            if self.select("window", where="name='fullscreen'")[0][1] == "True":
                return True
            else:
                return False
        except:
            raise ValueError("Need to install Settings")
    def get_wide(self):
        try:
            x = int(self.select("window", where="name='x'")[0][1])
            y = int(self.select("window", where="name='y'")[0][1])
        except:
            raise ValueError("Need to install Settings")
        return x, y
    def get_fps(self):
        try:
            fps = int(self.select("window", where="name='fps'")[0][1])
        except:
            raise ValueError("Nedd to install Settings")
        return fps
    def get_show_fps(self):
        try:
            if self.select("window", where="name='showfps'")[0][1] == "True":
                return True
            else:
                return False
        except:
            raise ValueError("Need to install Settings")
