from tkinter import *
from tkinter import ttk
import threading
import time

def OnRecord():
    global record
    if record:
        buttontext.set("Record")
    else:
        buttontext.set("Stop")
    record = not record    


def ToggleFull(event):
    global fullscreen
    fullscreen = not fullscreen
    root.attributes("-fullscreen", fullscreen)

def RecordThread():
    global record
    while True:
        #do record here
        if record:
            print("recording")  
        else:
            print("not recording")
        time.sleep(1)        

 
root = Tk() 
root.minsize(400,400)
#fullscreen = True
fullscreen = False
# root.attributes("-fullscreen", True)
root.bind("<Escape>",ToggleFull)

bottomframe = Frame(root)
bottomframe.pack(side = BOTTOM)
exitbutton = Button(bottomframe,text = "Quit",command = quit)
exitbutton.pack(side = RIGHT, padx=20, pady=20)
record = False
buttontext = StringVar()
recordbutton = Button(bottomframe,textvariable = buttontext,command = OnRecord)
buttontext.set("Record")
recordbutton.pack(side = RIGHT, padx=20, pady=20)

leftframe = Frame(root)
leftframe.pack( side = LEFT)
test_string = ["January", "February", "March", "April"]
leftcombo = ttk.Combobox(leftframe,values = test_string)
leftcombo.grid(column=0, row=1)
leftcombo.current(0)
leftcombo.pack(side = TOP)
lefttext = Label(leftframe,text = " this is a text this is a text this is a text this is a text this is a text this is a text this is a text this is a text",width = 30,wraplength = 150)
lefttext.pack(side = TOP)

rightframe = Frame(root)
rightframe.pack(side = RIGHT)
rightcombo = ttk.Combobox(rightframe,values = test_string)
rightcombo.grid(column=0, row=1)
rightcombo.current(0)
rightcombo.pack(side = TOP)
righttext = Label(rightframe,text = " this is a text this is a text this is a text this is a text this is a text this is a text this is a text this is a text",width = 30,wraplength = 150)
righttext.pack(side = TOP)

x = threading.Thread(target = RecordThread)
x.daemon = True
x.start()

root.mainloop()