import os
path = os.getcwd() 

class Student:
    def __init__(self,x,y,r): #img #frames
        self.x = x
        self.y = y
        self.r = r
        self.vx = 5
    
    def display(self):
        circle(self.x,self.y,self.r*2)
        
class Tool:
    def __init__(self, x, y): #img
        self.x = x #left hand
        self.y = y #from the hand
        self.vy = 0
        self.y2 = self.y + 30

    def display(self):
        stroke(255,0,0)
        line(self.x, self.y, self.x, self.y2)

class Game:
    def __init__(self, w, h, g):
        self.w = w
        self.h = h
        self.g = g
        self.student = Student(self.w/2, self.g-50, self.g/3)
        self.tool = Tool(self.student.x - self.student.r, self.student.y)
    
    def update(self):
        if self.student.x + self.student.r >= self.w:
            self.student.vx = -5
        if self.student.x <= self.student.r:
            self.student.vx = 5
        self.student.x += self.student.vx
        
        self.tool.x = self.student.x - self.student.r
        self.tool.y = self.student.y
        self.tool.y2 += self.tool.vy
    
    def display(self):
        stroke(0, 0, 0)
        fill(0, 0, 140)
        rect(0, 0, self.w, self.g)
        fill (150,75,0)
        rect(0, self.g, self.w, self.h)
        
        self.update()
        self.student.display()
        self.tool.display()
 
game = Game(1024, 768, 150) 
               
def setup():
    size(game.w, game.h)
    background(255, 255, 255)
    
def draw():
    background(255, 255, 255)
    game.display()

def mouseClicked():
    global game
    game.student.vx = 0
    game.tool.vy = 5
