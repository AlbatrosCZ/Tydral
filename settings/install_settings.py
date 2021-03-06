from sqlite3 import * 
from tkinter import *

def make(root, entryes):
    # entryes = [size, full, fps]
    size = entryes[0].get()
    fullscreen = entryes[1].get()
    if fullscreen != "":
        fullscreen = "False"
    else:
        fullscreen = "True"
    showFPS = entryes[3].get()
    if showFPS != "":
        showFPS = "False"
    else:
        showFPS = "True"
    fps = int(entryes[2].get())
    if size == 0:
        x = root.winfo_screenwidth()
        y = root.winfo_screenheight()
        if x >= 1366:
            maxim = 3
        elif x >= 1360:
            maxim = 2
        elif x >= 1280:
            maxim = 1
        sizes = {3:"1366x768", 2: "1360x768", 1: "1280x768"}
        x, y = sizes[maxim].split("x")
        x = int(x)
        y = int(y)
    else:
        sizes = {3:"1366x768", 2: "1360x768", 1: "1280x768"}
        x, y = sizes[size].split("x")
        x = int(x)
        y = int(y)

    path = "settings/settings.db"
    open(path, "w").close()

    connection = connect(path)
    connection.isolation_level = None

    curs = connection.cursor()
    curs.execute("CREATE TABLE Window(name VARCHAR Primary Key, value VARCHAR NOT NULL)")
    curs.execute("INSERT INTO Window(name, value) VALUES('x', {})".format(x))
    curs.execute("INSERT INTO Window(name, value) VALUES('y', {})".format(y))
    curs.execute("INSERT INTO Window(name, value) VALUES('fullscreen', '{}')".format(fullscreen))
    curs.execute("INSERT INTO Window(name, value) VALUES('fps', {})".format(fps))
    curs.execute("INSERT INTO Window(name, value) VALUES('showfps', '{}')".format(showFPS))
    root.destroy()


def sizer(var, label):
    sizes = {0:"auto", 3:"1366x768", 2: "1360x768", 1: "1280x768"}
    a = var.get()
    label.config(text = sizes[a])

def faster(var, scale):
    try:
        if int(var.get()) > 2000:
            var.set(2000)
        elif int(var.get()) < 20:
            var.set(20)
    except:
        var.set(20)
    scale.set(int(var.get()))

def reverse_faster(var, scale):
    var.set(int(scale.get()))
    
def install_settings():
    root = Tk()
    root.geometry("300x250+100+100")
    root.title("window settings")

    Label(root, text = "Screen Size").place(x = 10, y = 50)
    Label(root, text = "Max Fps").place(x = 10, y = 100)
    Label(root, text = "Full Screen").place(x = 10, y = 150)
    Label(root, text = "Show FPS").place(x = 10, y = 200)

    a = Label(root, text = "")
    a.place(x = 210, y = 50)

    fps  = Scale(root, from_ = 20, to = 2000, orient = HORIZONTAL)
    b_var = DoubleVar()
    b_var.trace("w", lambda p0="", p1="", p2="": faster(b_var, fps))
    b = Spinbox(root, textvariable = b_var, width = 30)
    b_var.set(200)
    fps.config(command = lambda p0="", p1="", p2="": reverse_faster(b_var, fps))
    b.place(x = 210, y = 100)
    fps.place(x = 100 , y = 100)

    x = root.winfo_screenwidth()
    if x >= 1366:
        maxim = 3
    elif x >= 1360:
        maxim = 2
    elif x >= 1280:
        maxim = 1
    elif x < 1024:
        raise ValueError("Your Monitor is too tiny")

    size = Scale(root, from_ = 0, to = maxim, orient = HORIZONTAL)
    size.config(command = lambda p0="", p1="", p2="": sizer(size, a))
    size.set(0)
    sizer(size, a)
    size.place(x = 100, y = 50)

    full = StringVar() 
    Checkbutton(root, text="", variable = full, onvalue = "True").place(x = 100, y = 150)

    showfps = StringVar() 
    Checkbutton(root, text="", variable = showfps, onvalue = "True").place(x = 100, y = 200)

    entryes = [size, full, fps, showfps]

    Button(root, text = "Finish", command = lambda: make(root, entryes)).place(x = 150, y = 200)

    root.mainloop()