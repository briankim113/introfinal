add_library('minim')
import random, os
path = os.getcwd()
item_r = 50
player = Minim(this)

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
                game.student.vx = 6
            if self.direction == LEFT:
                game.student.vx = -6
        game.student.x += game.student.vx
        
        
class Tool:
    def __init__(self, x, y): 
        self.x = x
        self.y = y
        self.vy = 0
        self.y2 = self.y + item_r/2
        self.down = False
        
        self.img = loadImage(path + "/images/" + "tool.png")
        self.sound = player.loadFile(path + "/sounds/rock.mp3")

    def move(self):
        if game.student.direction == LEFT:
            self.x = game.student.x - game.student.r
        if game.student.direction == RIGHT:
            self.x = game.student.x + game.student.r
        self.y = game.student.y
        self.y2 += game.tool.vy
        
        #bounces
        if self.y2 + item_r == game.h:
            # self.sound.rewind()
            self.vy = -5
            # self.sound.play()
        if self.y2 == game.tool.y + item_r/2:
            self.vy = 0
            self.down = False
    
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
        image(self.img, self.x-item_r/2, self.y2, item_r, item_r)

        # circle(self.x, self.y2+item_r/2, item_r)
        
        self.move()
    
    
class Item:
    def __init__(self, x, y, type, subtype): #?img?
        self.x = x
        self.y = y
        self.type = type #type 0 will be rocks, 1 for dirhams, and 2 for mystery bag
        self.subtype = subtype #for mystery bag
        self.hit = False
        
        self.img0 = loadImage(path + "/images/" + "rock2.png")
        self.img1 = loadImage(path + "/images/" + "dirham.png")
        self.img2 = loadImage(path + "/images/" + "mysterybag2.png")
        
        self.sound = 0
        self.rock_sound = player.loadFile(path + "/sounds/rock.mp3")
        self.dirham_sound = player.loadFile(path + "/sounds/dirham.mp3")
        
    def display(self):
        if self.type == 0:
            img = self.img0
        elif self.type == 1:
            img = self.img1
        elif self.type == 2:
            img = self.img2
                        
        image(img, self.x-item_r/2, self.y-item_r/2, item_r, item_r)
                        
        for i in game.items:
            if not i.hit:
                if i.x - (item_r/1.3) <= game.tool.x and game.tool.x <= i.x + (item_r/1.3):
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
                        self.sound = player.loadFile(path + "/sounds/rock.mp3")
                        self.sound.play()
                        game.score -= 5
                    elif i.type == 1:
                        self.sound = player.loadFile(path + "/sounds/dirham.mp3")
                        self.sound.play()
                        game.score += 10
                    elif i.subtype == 1:
                        self.sound = player.loadFile(path + "/sounds/dirham.mp3")
                        self.sound.play()
                        game.score += 20
                    game.items.remove(i)
                    game.tool.down = False
        
        if game.items == []:
            game.screen = 5
        
class Cat:
    def __init__(self,x,y,r): #img
        self.x = x
        self.y = y
        self.r = r 
        self.vx = 2
        self.vy = 2
        self.direction_list = [RIGHT, LEFT, UP, DOWN]
        self.direction = self.direction_list[random.randint(0,3)]
        self.cat_sound = player.loadFile(path + "/sounds/cat.mp3")
    
    def move(self):
        #so it bounces off the boundaries 
        if self.y > game.h - item_r or self.y < item_r + game.g:
            self.vy *= -1
        if self.x > game.w - item_r or self.x < item_r:
            self.vx *= -1
            
        self.x += self.vx
        self.y += self.vy
    
    def kill(self):
        if self.x <= game.tool.x + (item_r/1.3) and self.x >= game.tool.x - (item_r/1.3) and self.y <= game.tool.y2 + (item_r/1.5) and self.y >= game.tool.y2 - (item_r/1.5):
            self.cat_sound.rewind()
            self.cat_sound.play()
            game.screen = 2
    
    def display(self):
        stroke(75,0,130)
        fill(75,0,130) 
        circle(self.x,self.y,self.r)
        self.move()
        self.kill()        
        
        
class Game:
    def __init__(self, w, h, g):
        self.w = w
        self.h = h
        self.g = g
        self.t = 30
        
        self.bg = loadImage(path + "/images/" + "background.png")
        self.background_sound = player.loadFile(path + "/sounds/background.mp3")        
        
        self.student = Student(self.w/2, self.g-50, item_r)
        self.tool = Tool(self.student.x - self.student.r, self.student.y)

        self.cat = Cat(random.randint(1,20)*50, random.randint(self.g*2, self.h-50), item_r)
        self.items = []

        self.level = 1
        self.goal = 0
        self.food = ""
        self.score = 0
        self.screen = -1
        
        self.create_items()  
            
    def update_cat(self):
        if self.level == 1:
            self.cat.vx = 1
            self.cat.vy = 1
            
        elif self.level == 2:
            self.cat.vx = 2
            self.cat.vy = 2
        
        elif game.level == 3:
            self.cat.vx = 3
            self.cat.vy = 3
            
        elif game.level == 4:
            self.cat.vx = 4
            self.cat.vy = 4
            
        elif game.level == 5:
            self.cat.vx = 5
            self.cat.vy = 5
    
    def create_items(self):
        if self.level == 1:
            num_rocks = 3
            num_dirhams = 4
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
            num_bags = 3
        elif self.level == 5:
            num_rocks = 0
            num_dirhams = 0
            num_bags = 15
                                    
        for num in range(num_rocks):
            y = random.randrange(self.g + item_r, self.h - item_r, 60)
            valid = False
            while not valid:
                x = random.randrange(0 + item_r, self.w - item_r, 60)
                valid = True
                for item in self.items:
                    if x == item.x:
                        valid = False
                        break
    
            self.items.append(Item(x,y,0,2))
        
        for num in range(num_dirhams):
            y = random.randrange(self.g + item_r, self.h - item_r, 60)
            valid = False
            while not valid:
                x = random.randrange(0 + item_r, self.w - item_r, 60)
                valid = True
                for item in self.items:
                    if x == item.x:
                        valid = False
                        break
    
            self.items.append(Item(x,y,1,2))                                                                                                                                                                                                                           
        
            
        for num in range(num_bags): #mysterybags
            subtype = random.randint(0,1)
            y = random.randrange(self.g + item_r, self.h - item_r, 60)
            valid = False
            while not valid:
                x = random.randrange(0 + item_r, self.w - item_r, 60)
                valid = True
                for item in self.items:
                    if x == item.x:
                        valid = False
                        break
    
            self.items.append(Item(x,y,2,subtype))
            
    def display(self):
        image(self.bg, 0, -400)
        
        left = 200
        right = 800
              
        #instructions
        if self.screen == -1:
            fill(0,0,0)
            textSize(40)
            text("DIRHAM MINER", left, 75, self.w, self.h)
            
            textSize(20)            
            text("You are hungry and want to eat a hearty breakfast. But you ran out of campus dirhams, so let's go mine some in the sand!", left, 250, right, self.h)
            text("Instructions: Reach the goal dirhams within 30 seconds for each level. Pass all five to have good breakfast!", left, 325, right, self.h)
            text("Left-Click = Magnet Down", left, 400, right, self.h)
            text("Scoring", left, 490, self.w, self.h)

            textSize(17)
            text("Created by: Sarah Al-Yahya & Brian Kim", left, 140, right, self.h)
            text("Dirham = 10", left, 525, right, self.h)
            text("Rock = -5", left, 550, right, self.h)
            text("Mystery Bag = -5 OR 20 (test your luck!)", left, 575, right, self.h)
            text("Warning: Beware of the Campus Cat...", left, 750, right, self.h)
            
            textSize(25)
            text("Click to begin!", left, 650, self.w, self.h)
        
        #game screen
        if self.screen == 0:
            stroke(255,255,255)
            #fill(135,206,235)
            #rect(0, 0, self.w, self.g)
            #fill(245,245,220)
            #rect(0, self.g, self.w, self.h)
            
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
                self.goal = 25
                self.food = "Bread"
            elif self.level == 3:
                self.goal = 35
                self.food = "Milk"
            elif self.level == 4:
                self.goal = 45
                self.food = "Cereal"
            elif self.level == 5:
                self.goal = 60
                self.food = "Nutella"
            
            if self.score >= self.goal:
                self.level += 1
                if self.level < 6: #next level pass
                    self.screen = 4
                    self.update_cat()  
                    self.score = 0
                    self.items = []
                    self.create_items()
                else: #pass all five screens = win
                    self.screen = 3
        
        #game over screens - need images! - is laggy?
        x = 400
        y = 400
        
        if self.screen == 1:
            text("TIME IS UP - GAME OVER", x, y)
            text("Click to play again!", x, y + 50)
        elif self.screen == 2:
            text("You were KILLED by a campus cat!", x, y)
            text("Click to play again!", x, y + 50)
        elif self.screen == 3:
            text("You WON! Congrats on your breakfast :)", x, y)
            text("Click to play again!", x, y + 50)
        elif self.screen == 4:
            text("Level " + str(self.level - 1) + " complete!", x, y)
            text("Click to move to the next level!", x, y + 50)
        elif self.screen == 5:
            text("You have ran out of items to dig!", x, y)
            text("Click to start again!", x, y + 50)    

    def board(self):
        textSize(20)
        fill(0,0,0)
        text("LEVEL " + str(self.level), 20, 40)
        text("FOOD: " + self.food, 20, 65)
        text("Click to bring the magnet down!", 450, 40)
        text("GOAL: " + str(self.goal) + " aed", 1000, 40)
        text("BALANCE: " + str(self.score) + " aed", 1000, 65)
        self.timer()
        text("TIME: " + str(self.t) + " seconds", 1000, 115)

    def timer(self):        
        if frameCount % 60 == 0:
            self.t -= 1
        if self.t == 0:
            self.screen = 1

game = Game(1200, 800, 230) 

def setup():
    size(game.w, game.h)
    myFont = createFont("Seravek", 32);
    textFont(myFont);
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
        game.t = 30
        game.screen = 0
    elif game.screen != 0:
        game.background_sound.close()
        game = Game(1200, 800, 230)
