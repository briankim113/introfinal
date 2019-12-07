import random, os, time
path = os.getcwd()
item_r = 50

class Student:
    def __init__(self,x,y,r): #?img and frames?
        self.x = x
        self.y = y
        self.r = r
        self.vx = 5
        self.direction = RIGHT
        self.alive = True
    
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
                game.student.vx = 8
            if self.direction == LEFT:
                game.student.vx = -8
        game.student.x += game.student.vx
        
class Tool:
    def __init__(self, x, y): #?img?
        self.x = x
        self.y = y
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
    def __init__(self, x, y, v,type,subtype): #?img?
        self.x = x
        self.y = y
        self.v = v #?value?
        self.hit = False
        self.type = type #type 0 will be rocks, 1 for dirhams, and 2 for mystery bag
        self.subtype = subtype #for mystery bag
    
    def display(self):
        if self.type == 0: #?later on the load image could be under these if conditions?
            stroke(0,0,0) #black for rocks
            fill(0,0,0)
        elif self.type == 1:
            stroke(52,73,40) #green for dirhams
            fill(52,73,40)
        elif self.type ==2:
            stroke(128,0,0) #red for mystery bag
            fill(128,0,0)
        
        circle(self.x, self.y, item_r)
        #cat kill condition
        if game.cat.x <= game.tool.x + item_r and game.cat.x >= game.tool.x - item_r and game.cat.y < game.tool.y2:
            game.cat.attack = True
            game.over = True 
        
        for i in game.items:
            if not i.hit:
                if i.x - item_r <= game.tool.x and game.tool.x <= i.x + item_r:
                    if game.tool.y2+item_r > i.y: #tool's bottom hits item's top
                        i.hit = True

            if i.hit:
                #attach to magnet
                i.x = game.tool.x
                i.y = game.tool.y2+item_r
                game.tool.vy = -5
                #goes up
                if game.tool.y2 <= game.tool.y + item_r/2:
                    game.tool.vy = 0
                    if i.type == 0:
                        game.score -= 5
                    elif i.type == 1:
                        game.score += 15
                    elif i.type == 2 and i.subtype == 0:
                        game.score -= 5
                    elif i.type == 2 and i.subtype == 1:
                       game.score += 10 
                    game.items.remove(i)
                    game.tool.down = False
                    
        
class Cat:
    def __init__(self,x,y,r): #?img?
        self.x = x
        self.y = y
        self.r = r 
        self.vx = 8
        self.vy = 8
        self.direction_list = [RIGHT,LEFT, UP,DOWN]
        self.direction = self.direction_list[random.randint(0,3)]
        self.attack = False
        
    def display(self):
        stroke(75,0,130)
        fill (75,0,130) 
        circle(self.x,self.y,self.r)
        if not game.over:
            #so it bounces off the boundaries 
            if game.cat.y > game.h - item_r or game.cat.y < item_r + game.g:
                game.cat.vy *= -1
            if game.cat.x > game.w - item_r or game.cat.x < item_r:
                game.cat.vx *= -1
        #movement        
        game.cat.x += game.cat.vx
        game.cat.y += game.cat.vy
class Game:
    def __init__(self, w, h, g):
        self.w = w
        self.h = h
        self.g = g
        self.student = Student(self.w/2, self.g-50, self.g/3)
        self.tool = Tool(self.student.x - self.student.r, self.student.y)
        self.cat = Cat(random.randint(1,20)*50, random.randint(self.g*2, self.h-50), item_r)
        self.clicked = False
        self.score = 0
        self.t = millis()
        self.items = []
        self.over = False
        
        valid_position = False
        for i in range(6): #rocks
            #for item's x: divide width by 20 so each "block" is 50 px (50, 100, 150, 200)
            #for item's y: anywhere below g, no need to divide
            #?the same randint for x coordinate should not be used again?
            rockX = random.randint(1,20)*50 #saving the random position in the var to be able to check  
            rockY = random.randint(self.g*2, self.h-50)
            if len(self.items) ==0:
                    if len(self.items) == 0:
                        self.items.append(Item(rockX, rockY, -5,0,0))
            while valid_position == False:
                for i in range (len(self.items)):
                    rockX = random.randint(1,20)*50
                    rockY = random.randint(self.g*2, self.h-50)
                    if self.items[i].x != rockX and self.items[i].y != rockY: 
                        valid_position = True 
            self.items.append(Item(rockX, rockY, -5,0,0))
            valid_position = False
        for j in range(6): #dirhams
            dirhamX = random.randint(1,20)*50
            dirhamY = random.randint(self.g*2, self.h-50)
            while valid_position == False:
                for i in range (len(self.items)):
                    rockX = random.randint(1,20)*50
                    rockY = random.randint(self.g*2, self.h-50)
                    if self.items[i].x != dirhamX and self.items[i].y != dirhamY: 
                        valid_position = True 
            self.items.append(Item(dirhamX, dirhamY, 10,1,1))
            valid_position = False
        for k in range(2): #mysterybags
            subtype= random.randint(0,1)
            if subtype == 0:
                value= -5
            elif subtype == 1:
                value = 15
            bagX = random.randint(1,20)*50
            bagY = random.randint(self.g*2, self.h-50)
            while valid_position == False:
                for i in range (len(self.items)):
                    bagX = random.randint(1,20)*50
                    bagY = random.randint(self.g*2, self.h-50)
                    if self.items[i].x != bagX and self.items[i].y != bagY: 
                        valid_position = True 
            self.items.append(Item(bagX, bagY, value,2,subtype))
            valid_position = False
            
            
            
    def display(self):
        #game screen
        if not self.over:
            stroke(0, 0, 0)
            fill(0, 0, 140)
            rect(0, 0, self.w, self.g)
            fill (150,75,0)
            rect(0, self.g, self.w, self.h)
            stroke(0)
            textSize(20)
            text("Score: " + str(self.score), 20, 65)
            self.timer()
            self.student.display()
            self.tool.display()
            self.cat.display()
            for i in self.items:
                i.display()
                
        #between levels / game over
        #levels counter, if level finish, then count += 1
        if self.over and self.t == 0:
            text("Time is up!", 400, 400)
            #different end game messages
        elif self.over and self.cat.attack == True:
            text("you were KILLED by a campus cat!", 400,400)


    def timer(self):
        begin = 60
        if self.t > 0:
            self.t = begin - (millis() / 1000) 
            text("Timer: " + str(self.t), 1000, 65)
            if self.t == 0:
                self.over = True

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
