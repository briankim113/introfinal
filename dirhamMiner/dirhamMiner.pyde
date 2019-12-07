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
                game.student.vx = 7
            if self.direction == LEFT:
                game.student.vx = -7
        game.student.x += game.student.vx
        
        
class Tool:
    def __init__(self, x, y): #?img?
        self.x = x
        self.y = y
        self.vy = 0
        self.y2 = self.y + item_r/2
        self.down = False

    def move(self):
        if game.student.direction == LEFT:
            game.tool.x = game.student.x - game.student.r
        if game.student.direction == RIGHT:
            game.tool.x = game.student.x + game.student.r
        game.tool.y = game.student.y
        game.tool.y2 += game.tool.vy
        
        #bounces
        if game.tool.y2 + item_r == game.h:
            game.tool.vy = -5
        if game.tool.y2 == game.tool.y + item_r/2:
            game.tool.vy = 0
            game.tool.down = False
    
    def display(self):
        #string
        pushStyle()
        stroke(255,0,0)
        strokeWeight(3)
        line(self.x, self.y, self.x, self.y2)
        popStyle()
        
        #magnet
        stroke(255,255,255)
        fill(255,255,255)
        circle(self.x, self.y2+item_r/2, item_r)
        
        self.move()
    
    
class Item:
    def __init__(self, x, y, type, subtype): #?img?
        self.x = x
        self.y = y
        self.type = type #type 0 will be rocks, 1 for dirhams, and 2 for mystery bag
        self.subtype = subtype #for mystery bag
        self.hit = False

            
    def display(self):
        if self.type == 0:
            stroke(0,0,0) #black for rocks
            fill(0,0,0)
        elif self.type == 1:
            stroke(52,73,40) #green for dirhams
            fill(52,73,40)
        elif self.type ==2:
            stroke(128,0,0) #red for mystery bag
            fill(128,0,0)
        circle(self.x, self.y, item_r)
                
        for i in game.items:
            if not i.hit:
                if i.x - item_r <= game.tool.x and game.tool.x <= i.x + item_r:
                    if game.tool.y2+item_r > i.y: #tool's bottom hits item's top
                        i.hit = True
            else:
                #attach to magnet
                i.x = game.tool.x
                i.y = game.tool.y2+item_r
                game.tool.vy = -5
                
                #goes up
                if game.tool.y2 <= game.tool.y + item_r/2:
                    game.tool.vy = 0
                    if i.type == 0 or i.subtype == 0:
                        game.score -= 5
                    elif i.type == 1:
                        game.score += 10
                    elif i.subtype == 1:
                        game.score += 20
                    game.items.remove(i)
                    game.tool.down = False
        
        
class Cat:
    def __init__(self,x,y,r): #img
        self.x = x
        self.y = y
        self.r = r 
        self.vx = 2
        self.vy = 2
        self.direction_list = [RIGHT, LEFT, UP, DOWN]
        self.direction = self.direction_list[random.randint(0,3)]
    
    def move(self):
        
        #so it bounces off the boundaries 
        if game.cat.y > game.h - item_r or game.cat.y < item_r + game.g:
            game.cat.vy *= -1
        if game.cat.x > game.w - item_r or game.cat.x < item_r:
            game.cat.vx *= -1
            
        game.cat.x += game.cat.vx
        game.cat.y += game.cat.vy
    
    def kill(self):
        if game.cat.x <= game.tool.x + item_r and game.cat.x >= game.tool.x - item_r and game.cat.y <= game.tool.y2 + item_r and game.cat.y >= game.tool.y2 - item_r:
            game.screen = 2
    
    def display(self):
        stroke(75,0,130)
        fill (75,0,130) 
        circle(self.x,self.y,self.r)
        self.move()
        self.kill()        
        
        
class Game:
    def __init__(self, w, h, g):
        self.w = w
        self.h = h
        self.g = g
        self.t = millis()
        
        self.student = Student(self.w/2, self.g-50, self.g/3)
        self.tool = Tool(self.student.x - self.student.r, self.student.y)
        #fix Cat's starting position?
        self.cat = Cat(random.randint(1,20)*50, random.randint(self.g*2, self.h-50), item_r)
        self.items = []

        self.level = 1
        self.goal = 0
        self.food = ""
        self.score = 0
        self.screen = -1
        
        self.create_items()    
        
    def create_items(self):
        if self.level == 1:
            num_rocks = 4
            num_dirhams = 5 
            num_bags = 1
        elif self.level == 2:
            num_rocks = 4
            num_dirhams = 5 
            num_bags = 2
        elif self.level == 3:
            num_rocks = 5
            num_dirhams = 5 
            num_bags = 2
        elif self.level == 4:
            num_rocks = 5
            num_dirhams = 6 
            num_bags = 2
        elif self.level == 5:
            num_rocks = 0
            num_dirhams = 0
            num_bags = 10
        
        for num in range(num_rocks): #rocks
            x = random.randrange(0 + item_r, self.w - item_r, 60)
            y = random.randrange(self.g + item_r, self.h - item_r, 60)
    
            for item in self.items:
                if x == item.x:
                    x = random.randrange(0 + item_r, self.w - item_r, 60)
            
            self.items.append(Item(x,y,0,2))
       
        for num in range(num_dirhams): #dirhams
            x = random.randrange(0 + item_r, self.w - item_r, 60)
            y = random.randrange(self.g + item_r, self.h - item_r, 60)
    
            for item in self.items:
                if x == item.x:
                    x = random.randrange(0 + item_r, self.w - item_r, 60)
            
            self.items.append(Item(x,y,1,2)) 
            
        for num in range(num_bags): #mysterybags
            subtype = random.randint(0,1)
            
            x = random.randrange(0 + item_r, self.w - item_r, 60)
            y = random.randrange(self.g + item_r, self.h - item_r, 60)
    
            for item in self.items:
                if x == item.x:
                    x = random.randrange(0 + item_r, self.w - item_r, 60)
            
            self.items.append(Item(x,y,2,subtype))

            
    def display(self):
        left = 350
        right = 500
        
        if self.screen == -1:
            fill(0,0,0)
            textSize(40)
            text("DIRHAM MINER", left, 75, right, self.h)
            
            textSize(20)            
            text("You are hungry and want to eat a hearty breakfast. But you ran out of dirhams, so let's go mine some.", left, 175, right, self.h)
            text("Objective: Reach the goal amount of dirhams within 60 seconds and pass all five levels!", left, 275, right, self.h)
            text("Scoring", left, 435, right, self.h)

            textSize(17)
            text("Warning: Beware of the Campus Cat...", left, 370, right, self.h)
            text("Dirham = 10", left, 475, right, self.h)
            text("Rock = -5", left, 500, right, self.h)
            text("Mystery Bag = -5 OR 20 (test your luck!)", left, 525, right, self.h)
            text("Created by: Sarah Al-Yahya & Brian Kim", left, 700, right, self.h)
            
            textSize(25)
            text("Click to begin!", left, 625, right, self.h)
        
        if self.screen == 0:
            stroke(255,255,255)
            fill(135,206,235)
            rect(0, 0, self.w, self.g)
            fill(245,245,220)
            rect(0, self.g, self.w, self.h)
            
            self.student.display()
            self.tool.display()
            self.cat.display()
            for i in self.items:
                i.display()
            
            self.board()
            
            if self.level == 1:
                self.goal = 15
                self.food = "Banana"
            elif self.level == 2:
                self.goal = 20
                self.food = "Bread"
            elif self.level == 3:
                self.goal = 25
                self.food = "Milk"
            elif self.level == 4:
                self.goal = 30
                self.food = "Cereal"
            elif self.level == 5:
                self.goal = 40
                self.food = "Nutella"
            
            if self.score >= self.goal:
                self.level += 1
                if self.level < 6: #next level pass
                    self.score = 0
                    self.screen = 4
                    self.items = []
                    self.create_items()
                else: #pass all five screens = win
                    self.screen = 3
                        
        if self.screen == 1:
            text("Time is up - GAME OVER", 0, 400, self.w, self.h)
            text("Click to play again!", 0, 450, self.w, self.h)
        if self.screen == 2:
            text("You were KILLED by a campus cat!", 0, 400, self.w, self.h)
            text("Click to play again!", 0, 450, self.w, self.h)
        if self.screen == 3:
            text("You WON! Congrats on your breakfast :)", 0, 400, self.w, self.h)
            text("Click to play again!", 0, 450, self.w, self.h)
        if self.screen == 4:
            text("Level " + str(self.level - 1) + " complete!", 0, 400, self.w, self.h)
            text("Click to move to the next level!", 0, 450, self.w, self.h)
        textAlign(CENTER)

    def board(self):
        #FIX BOARD textAlign works weird?
        textSize(20)
        fill(0,0,0)
        text("LEVEL " + str(self.level), 20, 40)
        text("FOOD: " + self.food, 20, 65)
        text("GOAL: " + str(self.goal) + " aed", 1050, 40)
        text("BALANCE: " + str(self.score) + " aed", 1050, 65)
        self.timer()

    def timer(self):
        #fix time to start not in the beginning but when the level starts
        begin = 100
        if self.t > 0:
            self.t = begin - (millis() / 1000) 
            text("TIME: " + str(self.t), 1050, 115)
            if self.t == 0:
                self.screen = 1

game = Game(1200, 800, 150) 
               
def setup():
    size(game.w, game.h)
    background(255, 255, 255)
    
def draw():
    background(255, 255, 255)
    game.display()

def mouseClicked():
    global game
    if game.screen == 0:
        if game.tool.y2 == (game.tool.y + item_r/2):
            game.tool.down = True
            game.student.vx = 0
            game.tool.vy = 5
    if game.screen == -1 or game.screen == 4:
        game.screen = 0
    elif game.screen != 0:
        game = Game(1200, 800, 150)
