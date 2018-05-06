import tkinter as tk
import random
import time
win = tk.Tk()
win.title("Beaver Game")
win.wm_attributes("-topmost", 1)#Makes it stay on top of other windows
canvas = tk.Canvas(win, width=300, height=300, bg='#97FEFF', bd = 0, highlightthickness = 0)   
canvas.pack()
canvas.create_rectangle(0, 270,300, 300, fill = "brown")
win.update()

class Beaver:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = self.canvas.create_rectangle(150,150, 100, 100, fill = color)
        self.y = 0
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Up>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Down>', self.turn_right)
        self.sticks = 0
    def draw(self):
        self.canvas.move(self.id, 0, self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = 0
        if pos[3] >= self.canvas_height:
            self.y = 0
    def turn_left(self, evt):
        self.y = -3
    def turn_right(self,evt):
        self.y = 3
class Stick:
    def __init__(self, canvas, color, x, y):
        self.canvas = canvas
        self.color = color
        self.x = x
        self.y = y        
    def draw(self):
        canvas.create_rectangle(self.x, self.y, 5, 40, fill = self.color)
beaver = Beaver(canvas, "pink")

grassXs = []
for i in range(25):
     grassXs.append(i * 25)

sticks = []
for i in range(40): 
    sticks.append(Stick(canvas, "black", i * 4 + 100, random.randint(20, 26)))

while 1:
   for i in range(len(grassXs)):
      canvas.create_rectangle(grassXs[i], 250, 270, 270, fill = "green")
      grassXs[i] -= 1
      if (grassXs[i] <= -20):
         grassXs[i] = canvas.winfo_width()
   for i in range(len(sticks)):
       sticks[i].draw()
       sticks[i].x -= 1
   beaver.draw()
   win.update_idletasks()
   win.update()