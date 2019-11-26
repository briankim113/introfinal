import random, os
path = os.getcwd()
item_r = 50

class Student:
    def __init__(self,x,y,r): #img #frames
        self.x = x
        self.y = y
        self.r = r
        self.vx = 5
        self.direction = RIGHT
    
    def update(self):
        if game.student.x + game.student.r >= game.w:
            self.direction = LEFT
        if game.student.x <= game.student.r:
            self.direction = RIGHT
    
    def display(self):
        circle(self.x,self.y,self.r*2)
        self.update()
        if not game.tool.down:
            if self.direction == RIGHT:
                game.student.vx = 5
            if self.direction == LEFT:
                game.student.vx = -5
        game.student.x += game.student.vx
        
class Tool:
    def __init__(self, x, y): #img
        self.x = x #left hand
        self.y = y #from the hand
        self.vy = 0
        self.y2 = self.y + item_r/2
        self.down = False

    def display(self):
        pushStyle()
        stroke(255,0,0)
        strokeWeight(3)
        line(self.x, self.y, self.x, self.y2)
        popStyle()
        #added magnet
        stroke(255,255,255)
        fill(255,255,255)
        circle(self.x, self.y2+item_r/2, item_r)
        
        #tool moves
        game.tool.x = game.student.x - game.student.r
        game.tool.y = game.student.y
        game.tool.y2 += game.tool.vy
        
        #bounces
        if game.tool.y2 + item_r == game.h:
            game.tool.vy = -5
        if game.tool.y2 == game.tool.y + item_r/2:
            game.tool.vy = 0
            game.tool.down = False

class Item:
    def __init__(self, x, y, v): #img
        self.x = x
        self.y = y
        self.v = v #value
        self.hit = False
        self.collect = True
    
    def display(self):
        stroke(0,0,0)
        fill(0,0,0)
        circle(self.x, self.y, item_r)
        
        for i in game.items:
            if not i.hit:
                if i.x - item_r <= game.tool.x and game.tool.x <= i.x + item_r:
                    if game.tool.y2+item_r > i.y: #tool's bottom hits item's top
                        i.hit = True
            if i.hit:
                #attach
                i.x = game.tool.x
                i.y = game.tool.y2+item_r
                game.tool.vy = -5
                #goes up
                if game.tool.y2 <= game.tool.y + item_r/2:
                    game.tool.vy = 0
                    game.items.remove(i)
                    game.tool.down = False

class Game:
    def __init__(self, w, h, g):
        self.w = w
        self.h = h
        self.g = g
        self.student = Student(self.w/2, self.g-50, self.g/3)
        self.tool = Tool(self.student.x - self.student.r, self.student.y)
        self.clicked = False
        
        #for item's x: divide width by 20 so each "block" is 50 px (50, 100, 150, 200)
        #for item's y: anywhere below g, no need to divide
        self.items = []
        for i in range(3): #number should change based on level?
            self.items.append(Item(random.randint(1,20)*50, random.randint(self.g*2, self.h-50), 5)) #fix value and randint to be variant
                        
    def display(self):
        stroke(0, 0, 0)
        fill(0, 0, 140)
        rect(0, 0, self.w, self.g)
        fill (150,75,0)
        rect(0, self.g, self.w, self.h)
        
        self.student.display()
        self.tool.display()
        for i in self.items:
            i.display()
 
game = Game(1200, 800, 150) 
               
def setup():
    size(game.w, game.h)
    background(255, 255, 255)
    
def draw():
    background(255, 255, 255)
    game.display()

def mouseClicked():
    global game
    #only when the tool hasn't moved
    if game.tool.y2 == (game.tool.y + item_r/2):
        game.tool.down = True
        game.student.vx = 0
        game.tool.vy = 5
