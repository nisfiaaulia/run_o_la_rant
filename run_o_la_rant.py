#pip install pygame
import pygame,os,threading,random,sys
pygame.init()
pygame.mixer.init()

#draw screeen & init
SCREEN_HEIGHT = 464
SCREEN_WIDTH = 821
SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT)) #screen size
pygame.display.set_caption('Run O La Rant') #window title

BACKGROUND = pygame.image.load(os.path.join('assets','Background.png')).convert()
TITLE = pygame.image.load(os.path.join('assets','tinyTitle.png')).convert_alpha()
SHIELD = pygame.image.load(os.path.join('assets','shield.png')).convert_alpha()
BG = pygame.image.load(os.path.join('assets','line.png')).convert_alpha()
HOME_BG = pygame.image.load(os.path.join('assets','titleScreen.png')).convert()



#jack
IDLE = pygame.image.load(os.path.join('assets/char','idle.png')).convert_alpha()

RUNNING = [pygame.image.load(os.path.join('assets/char/anim_run','Run (1).png')).convert_alpha(),
           pygame.image.load(os.path.join('assets/char/anim_run','Run (2).png')).convert_alpha(),
           pygame.image.load(os.path.join('assets/char/anim_run','Run (3).png')).convert_alpha(),
           pygame.image.load(os.path.join('assets/char/anim_run','Run (4).png')).convert_alpha(),
           pygame.image.load(os.path.join('assets/char/anim_run','Run (5).png')).convert_alpha(),
           pygame.image.load(os.path.join('assets/char/anim_run','Run (6).png')).convert_alpha(),
           pygame.image.load(os.path.join('assets/char/anim_run','Run (7).png')).convert_alpha(),
           pygame.image.load(os.path.join('assets/char/anim_run','Run (8).png')).convert_alpha()]

JUMPING = pygame.image.load(os.path.join('assets/char','jump.png')).convert_alpha()

SLIDE = [pygame.image.load(os.path.join('assets/char/anim_slide','Slide (1).png')).convert_alpha(),
           pygame.image.load(os.path.join('assets/char/anim_slide','Slide (2).png')).convert_alpha(),
           pygame.image.load(os.path.join('assets/char/anim_slide','Slide (3).png')).convert_alpha(),
           pygame.image.load(os.path.join('assets/char/anim_slide','Slide (4).png')).convert_alpha(),
           pygame.image.load(os.path.join('assets/char/anim_slide','Slide (5).png')).convert_alpha(),
           pygame.image.load(os.path.join('assets/char/anim_slide','Slide (6).png')).convert_alpha(),
           pygame.image.load(os.path.join('assets/char/anim_slide','Slide (7).png')).convert_alpha(),
           pygame.image.load(os.path.join('assets/char/anim_slide','Slide (8).png')).convert_alpha()]

DEAD = pygame.image.load(os.path.join('assets/char','dead.png')).convert_alpha()


#obstacles
CANDLE = [pygame.image.load(os.path.join('assets/obstacles','lilin1.png')).convert_alpha(),
          pygame.image.load(os.path.join('assets/obstacles','lilin2.png')).convert_alpha()]

SPIDER = [pygame.image.load(os.path.join('assets/obstacles','spider.png')).convert_alpha(),
          pygame.image.load(os.path.join('assets/obstacles','spider.png')).convert_alpha()]


#pumpkin
PUMPKIN = [pygame.image.load(os.path.join('assets/obstacles','labu1.png')).convert_alpha(),
          pygame.image.load(os.path.join('assets/obstacles','labu2.png')).convert_alpha()]

#sound
power_sound = pygame.mixer.Sound(os.path.join('assets/sound','sfx_powerup.wav'))
death_sound = pygame.mixer.Sound(os.path.join('assets/sound','sfx_dead.wav'))
jump_sound = pygame.mixer.Sound(os.path.join('assets/sound','sfx_jump.wav'))
slide_sound = pygame.mixer.Sound(os.path.join('assets/sound','sfx_slide.wav'))

pygame.mixer.music.load(os.path.join('assets/sound','BGM.ogg'))
pygame.mixer.music.set_volume(0.2)

###################################################################################
class Jack:
    X_POS = 20
    Y_POS = 265
    Y_POS_SLIDE = 300
    JUMP_VEL = 8.5
    
    def __init__(self):
        self.slide_img = SLIDE
        self.run_img = RUNNING
        self.jump_img = JUMPING     

        self.jack_slide = False
        self.jack_run = True
        self.jack_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.jump_vel = self.JUMP_VEL
        self.jack_rect = self.image.get_rect()
        self.jack_rect.x = self.X_POS
        self.jack_rect.y = self.Y_POS

        self.shield = 0

    def update(self, userInput):
        if self.jack_slide:
            self.slide()      
        if self.jack_run:
            self.run()
        if self.jack_jump:
            self.jump()

        if self.step_index >= 40:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.jack_jump:
            self.jack_slide = False
            self.jack_run = False
            self.jack_jump = True
            jump_sound.play()


        elif userInput[pygame.K_DOWN] and not self.jack_jump:
            self.jack_slide = True
            self.jack_run = False
            self.jack_jump = False
            slide_sound.play()


        elif not (self.jack_jump or userInput[pygame.K_DOWN]):
            self.jack_slide = False
            self.jack_run = True
            self.jack_jump = False


    #fungsi slide
    def slide(self):
        self.image = self.slide_img[self.step_index // 5]
        self.jack_rect = self.image.get_rect()
        self.jack_rect.x = self.X_POS
        self.jack_rect.y = self.Y_POS_SLIDE
        self.step_index += 1

    #fungsi run
    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.jack_rect = self.image.get_rect()
        self.jack_rect.x = self.X_POS
        self.jack_rect.y = self.Y_POS
        self.step_index += 1

    #fungsi lompat
    def jump(self):
        self.image = self.jump_img
        if self.jack_jump:
            self.jack_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL:
            self.jack_jump = False
            self.jump_vel = self.JUMP_VEL
            

    def draw(self,SCREEN):
        SCREEN.blit(self.image,(self.jack_rect.x, self.jack_rect.y))
###################################################################################
        
###################################################################################
class Power:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH + 4000

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            powers.pop()

    def draw(self,SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class Labu(Power):
    def __init__(self, image):
        self.type = random.randint(0,1)
        super().__init__(image, self.type)
        self.rect.y = 340
		
###################################################################################
def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 50
    BAR_HEIGHT = 12
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, (0,255,0), fill_rect)
    pygame.draw.rect(surf, (255,255,255), outline_rect, 2)
        
###################################################################################
class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self,SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class Candle(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0,1)
        super().__init__(image, self.type)
        self.rect.y = 330


class Spider(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 0
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1
###################################################################################
high_score = 0
font = pygame.font.SysFont('lucidasans',20,True)
def score():
    global points, game_speed
    points += 1
    if points % 100 == 0:
        game_speed +=1

    text = font.render("Score: " + str(points), True, (255,255,255))
    textRect = text.get_rect()
    textRect.center = (700,48)
    SCREEN.blit(text, textRect)

    high_score_p = font.render("High Score: " + str(high_score), True, (255,255,255))
    highScoreRect = high_score_p.get_rect()
    highScoreRect.center = (130,48)
    SCREEN.blit(high_score_p, highScoreRect)

###################################################################################
def main():
    global game_speed, x_pos_bg, y_pos_bg, points, powers, obstacles, high_score
    pygame.mixer.music.play(loops=-1)
    run = True
    clock = pygame.time.Clock()
    player = Jack()
    powers = []
    game_speed = 14
    x_pos_bg = 0
    y_pos_bg = 419
    points = 0
    obstacles = []
    death_count = 0

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG,(x_pos_bg, y_pos_bg))
        SCREEN.blit(BG,(image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

        SCREEN.blit(BACKGROUND,(0,0))
        SCREEN.blit(TITLE,(323,40))
        SCREEN.blit(SHIELD,(375,65))
        userInput = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(userInput)
           
        #obstacles
        if len(obstacles) == 0:
            if random.randint(0,1) == 0:
                obstacles.append(Candle(CANDLE))
            elif random.randint(0,1) == 1:
                obstacles.append(Spider(SPIDER))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.jack_rect.colliderect(obstacle.rect):
                if player.shield > 0:
                    player.shield -= 4
                else:
                    death_sound.play()
                    pygame.time.delay(800)
                    death_count += 1
                    menu(death_count)
        #end       

        background()

        #powerup
        if len(powers) == 0:
            if random.randint(0,1) == 0:
                powers.append(Labu(PUMPKIN))

        for power in powers:
            power.draw(SCREEN)
            power.update()
            if player.jack_rect.colliderect(power.rect):
                power_sound.play()
                player.shield += 100
                if player.shield>=100:
                    player.shield = 100
        draw_shield_bar(SCREEN, 405, 73, player.shield)
        #end 

        #score
        score()
        if (high_score < points):
            high_score=points
        #end
            
        clock.tick(30)
        pygame.display.update()
###################################################################################

###################################################################################
def menu(death_count):
    global points, high_score
    pygame.mixer.music.stop()
    run = True
    while run:
        font = pygame.font.SysFont('lucidasans',30,True)

        if death_count == 0:
            SCREEN.blit(HOME_BG,(0,0))

        #GameOverScreen
        elif death_count > 0:
            SCREEN.blit(BACKGROUND,(0,0))
            SCREEN.blit(TITLE,(323,40))
            dead_font = pygame.font.Font('assets/font.ttf',80)
            textDead = dead_font.render("YOU'RE DEAD!", True, (182,160,143))
            textDeadRect = textDead.get_rect()
            textDeadRect.center = (SCREEN_WIDTH // 2+10,100)
            SCREEN.blit(textDead, textDeadRect)
            if high_score == points:
                font2 = pygame.font.SysFont('lucidasans',15,False,True)
                txtNew = font2.render("NEW!!", True, (0,255,0))
                txtNewRect = txtNew.get_rect()
                txtNewRect.center = (288,155)
                SCREEN.blit(txtNew, txtNewRect)
                
            #High Score Text#########################################    
            high_score_t = font.render("High Score ", True, (255,255,255))
            highScoreTRect = high_score_t.get_rect()
            highScoreTRect.center = (SCREEN_WIDTH // 2, 163)
            SCREEN.blit(high_score_t, highScoreTRect)

            h_score = font.render(str(high_score), True, (225,197,136))
            h_scoreRect = h_score.get_rect()
            h_scoreRect.center = (SCREEN_WIDTH // 2, 202)
            SCREEN.blit(h_score,h_scoreRect)
            #########################################################
            
            #Score Text#########################################  
            score_t = font.render('Your Score ', True, (255, 255, 255))
            score_tRect = score_t.get_rect()
            score_tRect.center = (SCREEN_WIDTH // 2, 243)
            SCREEN.blit(score_t, score_tRect)

            score = font.render(str(points), True, (195,88,23))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, 282)
            SCREEN.blit(score,scoreRect)
            ####################################################  

            font1 = pygame.font.SysFont('lucidasans',20)
            text = font1.render('Press any Key to Restart', True, (255, 255, 255))
            textRect = text.get_rect()
            textRect.center = (SCREEN_WIDTH // 2, 318)
            SCREEN.blit(text, textRect)

            SCREEN.blit(DEAD, (SCREEN_WIDTH // 2 - 70, 328))
        #end
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                main()
###################################################################################

menu(death_count=0)

