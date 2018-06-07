"""
Bryan Moore, W00995619
CSCI 321 - Game Programming
WWU, Fall 2017, Geoffrey Matthews

INTERGALACTIC
This is my 2D space shooter/adventure game for assignment 1.
Borrowed some initial code from the following:
http://kidscancode.org/blog/2016/08/pygame_shmup_part_1/
"""

import pygame, random
from os import path


met_dir = path.join(path.dirname(__file__), 'data/sprites/Meteors')
exp_dir = path.join(path.dirname(__file__), 'data/sprites/explosions')
pow_dir = path.join(path.dirname(__file__), 'data/sprites/powerups')
ufo_dir = path.join(path.dirname(__file__), 'data/sprites/Enemies')

#Setting the screen dimensions
WIDTH = 1000
HEIGHT = 600
#Setting the frame speed
FPS = 70
#Time for Powerups
POWERUP_TIME = 5000

#Define some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#Initialize a new pygame and create the window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("INTERGALACTIC")
clock = pygame.time.Clock()

"""
Class: Background

Used for the background image of my game
"""
class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


"""
Class: Player
This is the class for the player object, AKA Gil's spaceship.
"""
class Player(pygame.sprite.Sprite):
    def __init__(self):
        #Load the image and set its rectangle
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("data/newsprites/player1.png").convert()
        transColor1 = self.image.get_at((0,0))
        self.image.set_colorkey(transColor1)
        self.rect = self.image.get_rect()
        self.radius = 20
        #Code below shows the collision circle
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 30
        self.speedx = 0
        self.speedy = 0
        self.lives = 3
        self.shoot_delay = 300
        self.last_shot = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()

    #Sprite Movement
    def update(self):
        #Move the sprite at whatever speed it is currently at.
        self.speedx = 0
        self.speedy = 0
        keyaction = pygame.key.get_pressed()

        #Defining the left and right arrow keys
        if keyaction[pygame.K_LEFT]:
            self.speedx = -5
        if keyaction[pygame.K_RIGHT]:
            self.speedx = 5
        if keyaction[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx

        #Defining the up and down arrow keys
        if keyaction[pygame.K_UP]:
            self.speedy = -5
        if keyaction[pygame.K_DOWN]:
            self.speedy = 5
        self.rect.y += self.speedy

        #Staying on the screen
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        #When the powerup timer runs out
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top, "data/sprites/laserGreen.png")
                all_sprites.add(bullet)
                bullets.add(bullet)
            #Double Bullets Definition
            if self.power >= 2:
                leftbullet = Bullet(self.rect.left, self.rect.centery, "data/sprites/laserGreen.png")
                rightbullet = Bullet(self.rect.right, self.rect.centery, "data/sprites/laserGreen.png")
                all_sprites.add(leftbullet)
                all_sprites.add(rightbullet)
                bullets.add(leftbullet)
                bullets.add(rightbullet)


    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()


"""
Class: Asteroid

This is the class for the flying asteroids that appear in the game.
"""
class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(asteroid_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width *0.85 / 2)
        #Code Below shows the asteroid collision circle
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        #Spawn the asteroids above the screen
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.y = random.randrange(-100, -40)
        #Assign them a random x and y speed
        self.speedx = random.randrange(-3,3)
        self.speedy = random.randrange(1,8)
        self.rotation = 0
        self.rotation_speed = random.randrange(-10,10)
        self.last_update = pygame.time.get_ticks()

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        #Move the asteroid to a random spot above the screen
        #after it goes off of the bottom of the screen
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedx = random.randrange(-3,3)
            self.speedy = random.randrange(1,8)
        self.rotate()

    def rotate(self):
        time = pygame.time.get_ticks()
        #If more that 50 millisecons have gone by, update the image.
        if time - self.last_update > 50:
            self.last_update = time
            self.rotation = (self.rotation + self.rotation_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rotation)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center


"""
Class: Bullet

This is the class for the bullets that shoot from the ship.\
"""
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, image_file):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10


    def update(self):
        self.rect.y += self.speedy
        #Delete if it moves off of the top of the screen
        if self.rect.bottom < 0:
            self.kill()


"""
Class: Explosion

This is the class for the explosion images when something gets shot.
"""
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_image[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 30

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_image[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_image[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

"""
Class: powerup

This is the class for the powerups that the player can obtain
"""
class Powerup(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['doublebullets', 'life'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        #Delete if it moves off of the bottom of the screen
        if self.rect.top > HEIGHT:
            self.kill()


"""
Class: Enemyufo

This is the class used to spawn enemy ships for level 2
"""
class Enemyufo(pygame.sprite.Sprite):
    def __init__(self):
        #load the image and set its rectangle
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(ufo_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = 40
        #Code below shows the collision circle
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(-90, -40)
        self.rect.y = random.randrange(0, 250)
        #Assign them a random x and y speed
        self.speedx = random.randrange(5,15)
        #Bullet location

    #Sprite Movement
    def update(self):
        #Move the sprite at whatever speed it is currently at.
        self.rect.x += self.speedx
        #Randomly move the UFO's when they get past a certain point on the screen
        if self.rect.left < -120 or self.rect.right > WIDTH + 120:
            self.speedx *= -1
            self.rect.x += self.speedx
            self.rect.y = random.randrange(0, 250)

"""
Class: Starlord

This is the class to spawn enemy ships for level 3
"""
class Starlord(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("data/sprites/Enemies/boss3.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = random.randrange(0, WIDTH-10)
        self.rect.bottom = random.randrange(10, 20)
        self.speedx = random.randrange(4,8)
        self.speedy = random.randrange(-4,-2)
        self.lives = 5
        self.power = 1


    def update(self):
        self.rect.centerx += self.speedx
        self.rect.bottom += self.speedy
        #Staying on the screen
        if self.rect.right >= WIDTH:
            self.speedx = random.randrange(-8,-3)
        if self.rect.left <= 0:
            self.speedx = random.randrange(3,8)
        if self.rect.top <= 0:
            self.speedy = random.randrange(2,4)
        if self.rect.bottom >= HEIGHT / 2:
            self.speedy = random.randrange(-4,-2)

        #Randomly shoot
        if self.power == 1:
            if random.randrange(0,75) == 0:
                self.shoot()
        if self.power == 2:
            if random.randrange(0,30) == 0:
                self.shoot()


    def shoot(self):
        if self.power == 1:
            bullet = Enemybullet(self.rect.left, self.rect.centery)
            all_sprites.add(bullet)
            enemybullets.add(bullet)
        if self.power == 2:
            leftbullet = Enemybullet(self.rect.left, self.rect.centery)
            rightbullet = Enemybullet(self.rect.right, self.rect.centery)
            all_sprites.add(leftbullet)
            all_sprites.add(rightbullet)
            enemybullets.add(leftbullet)
            enemybullets.add(rightbullet)


"""
Class: Enemybullet

This is the class for the bullets that shoot from the ship.\
"""
class Enemybullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = pygame.image.load("data/sprites/laserRed.png").convert()
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = 20

        #pygame.draw.rect(self.image, RED, (x, y, 100, 100), self.radius)
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedx = 0
        self.speedy = 8
        pygame.draw.circle(self.image, WHITE, self.rect.center, self.radius)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        #Delete if it moves off of the bottom of the screen
        if self.rect.bottom > HEIGHT:
            self.kill()

"""
Function: draw_text
This function is used to draw text to the screen during gameplay.
"""
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface, text_rect)


"""
Function: gameoverscreen()
This function provides a template for when the game is over.
"""
def gameoverscreen():
    screen.blit(BackGround.image, BackGround.rect)
    draw_text(screen, "INTERGALACTIC", 104, WIDTH/2, HEIGHT/4)

    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP:
                if 300+100 > mouse[0] > 300 and 450 + 50 > mouse[1] > 450:
                    waiting = False
                if 600+100 > mouse[0] > 600 and 450+50 > mouse[1] > 450:
                    infoscreen()


        #Using the mouse's position to click on a button
        mouse = pygame.mouse.get_pos()

        if 300+100 > mouse[0] > 300 and 450 + 50 > mouse[1] > 450:
            pygame.draw.rect(screen, RED, (300, 450, 100, 50))
        else:
            pygame.draw.rect(screen, BLUE, (300, 450, 100, 50))

        if 600+100 > mouse[0] > 600 and 450+50 > mouse[1] > 450:
            pygame.draw.rect(screen, RED, (600, 450, 100, 50))
        else:
            pygame.draw.rect(screen, BLUE, (600, 450, 100, 50))

        draw_text(screen, "ENTER", 22, 350, 460)
        draw_text(screen, "RULES", 22, 650, 460)

        pygame.display.flip()

"""
Function: infoscreen()
This function displays the information screen at startup if the RULES button
is pressed.
"""
def infoscreen():
    screen.fill(WHITE)
    screen.blit(BackGround.image, BackGround.rect)

    draw_text(screen, "WELCOME TO INTERGALACTIC", 50, WIDTH/2, 10)
    draw_text(screen, "You are now co-pilot with the universe's most extreme pilot, Gil Manson.", 30, WIDTH/2, 80)
    draw_text(screen, "Navigate the perils of space alongside Manson if you dare", 25, WIDTH/2, 120)
    draw_text(screen, "to see what truly lies at the end of the universe...", 25, WIDTH/2, 150)
    draw_text(screen, "How far can you make it without losing your lives?", 25, WIDTH/2, 180)
    #Controls
    draw_text(screen, "CONTROLS", 40, WIDTH*1/4, 250)
    draw_text(screen, "ARROW KEYS:  Up, Down, Left, Right", 25, 230, 300)
    draw_text(screen, "SPACEBAR:        Shooting the guns", 25, 212, 330)
    draw_text(screen, "ESCAPE KEY:     Pause Menu", 25, 185, 360)
    #Powerups
    draw_text(screen, "POWERUPS", 40, WIDTH*3/4, 250)
    draw_text(screen, "DOUBLE BULLETS:", 25, 680, 300)
    bullet = pygame.image.load(path.join(pow_dir, 'doublebullets.png'))
    screen.blit(bullet, (800, 297))
    pygame.display.flip()
    draw_text(screen, "EXTRA LIFE:", 25, 640, 330)
    life = pygame.image.load(path.join(pow_dir, 'life.png'))
    screen.blit(life, (720, 330))

"""
Function: pausescreen()
This function displays the pause screen when the player presses the escape key.
"""
def pausescreen():
    draw_text(screen, "PAUSED GAME", 104, WIDTH/2, HEIGHT/4)
    draw_text(screen, "Press any key to continue", 50, WIDTH/2, HEIGHT*3/4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                waiting = False

#Loading the background image

BackGround = Background("data/images/IntergalacticWallpaper.jpg", [0,0])
#Loading the asteroid graphics
asteroid_images = []
asteroid_list = ['meteorBrown_big1.png', 'meteorBrown_med1.png', 'meteorBrown_med1.png',
'meteorBrown_med3.png', 'meteorBrown_small1.png', 'meteorBrown_small2.png', 'meteorBrown_tiny1.png']
for img in asteroid_list:
    asteroid_images.append(pygame.image.load(path.join(met_dir, img)).convert())
#Explosion animation handling for both the collisions and the player explosion.
explosion_image = {}
explosion_image['lg'] = []
explosion_image['player'] = []
for i in range(9):
    #Collision image handling
    filename = 'explosions{}.png'.format(i)
    image = pygame.image.load(path.join(exp_dir, filename)).convert()
    image.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(image, (75,75))
    explosion_image['lg'].append(img_lg)
    #Player Explosion Handline
    filename = 'playerexplosion{}.png'.format(i)
    img = pygame.image.load(path.join(exp_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_image['player'].append(img)

#Powerup Image handling
powerup_images = {}
powerup_images['doublebullets'] = pygame.image.load(path.join(pow_dir, 'doublebullets.png')).convert()
#powerup_images['halfspeed'] = pygame.image.load(path.join(pow_dir, 'halfspeed.png')).convert()
powerup_images['life'] = pygame.image.load(path.join(pow_dir, 'life.png')).convert()
#powerup_images['invincible'] = pygame.image.load(path.join(pow_dir, 'invincible.png')).convert()

#Loading the UFO graphics
ufo_images = []
ufo_list = ['ufoBlue.png', 'ufoGreen.png', 'ufoRed.png', 'ufoYellow.png']
for img in ufo_list:
    ufo_images.append(pygame.image.load(path.join(ufo_dir, img)).convert())


#Game loop
gameover = True
running = True
paused = False
currentlevel = 0
ufoflag = True
ufoscore = 0
starlordflag = True
starlordscore = 0
level1flag = False
level2flag = False
level3flag = False
level4flag = False
l4flag = False
level5flag = False
l5flag = False
level6flag = False
level7flag = False

while running:
    if gameover:
        gameoverscreen()
        gameover = False
        #Creating groups for the sprites
        all_sprites = pygame.sprite.Group()
        asteroid_sprites = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        ufo_sprites = pygame.sprite.Group()
        enemybullets = pygame.sprite.Group()
        starlord_sprites = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)

        #Initalize the player's score
        score = 0
        currentlevel = 0

    #Keep the loop running at the right speed
    clock.tick(FPS)
    for event in pygame.event.get():
        #Quitting the game
        if event.type == pygame.QUIT:
            running = False
        #Pause Menu by pressing the escape key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pausescreen()
                paused = False

            #Infinite lives cheat code
            if event.key == pygame.K_TAB:
                player.lives = 10000
                player.power = 2

    #Update
    all_sprites.update()

    #When the player shoots an asteroid
    hits = pygame.sprite.groupcollide(asteroid_sprites, bullets, True, True)
    for hit in hits:
        score += 50 - hit.radius    #Score of shooting an asteroid.
        if currentlevel == 1:
            asteroid = Asteroid()
            all_sprites.add(asteroid)
            asteroid_sprites.add(asteroid)
        if currentlevel == 4:
            asteroid = Asteroid()
            all_sprites.add(asteroid)
            asteroid_sprites.add(asteroid)
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        #Random chance that a powerup happens
        if random.random() > 0.8:
            powerup = Powerup(hit.rect.center)
            all_sprites.add(powerup)
            powerups.add(powerup)

    #When the player shoots a UFO
    hits = pygame.sprite.groupcollide(ufo_sprites, bullets, True, True)
    for hit in hits:
        score += 100
        ufoscore += 1
        if ufoscore <= 35:
            ufo = Enemyufo()
            all_sprites.add(ufo)
            ufo_sprites.add(ufo)
        if currentlevel == 4:
            ufo = Enemyufo()
            all_sprites.add(ufo)
            ufo_sprites.add(ufo)
        expl = Explosion(hit.rect.center, 'player')
        all_sprites.add(expl)
        if random.random() > 0.8:
            powerup = Powerup(hit.rect.center)
            all_sprites.add(powerup)
            powerups.add(powerup)

    #When the player shoots a starlord character
    hits = pygame.sprite.groupcollide(starlord_sprites, bullets, False, True)
    for hit in hits:
        starlord.lives -= 1
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if starlord.lives <= 0:
            finalexplosion = Explosion(starlord.rect.center, 'player')
            all_sprites.add(finalexplosion)
            starlord.kill()
            score += 1000
            starlordscore += 1
        if random.random() > 0.8:
            powerup = Powerup(hit.rect.center)
            all_sprites.add(powerup)
            powerups.add(powerup)

    #When a starlord character shoots the player
    hits = pygame.sprite.spritecollide(player, enemybullets, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.lives -= 1
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if player.lives <= 0:
            finalexplosion = Explosion(player.rect.center, 'player')
            all_sprites.add(finalexplosion)
            player.kill()


    #When an asteroid collides with the player ship.
    hits = pygame.sprite.spritecollide(player, asteroid_sprites, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.lives -= 1
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if player.lives <= 0:
            finalexplosion = Explosion(player.rect.center, 'player')
            all_sprites.add(finalexplosion)
            player.kill()

    #When the player collides with a powerup
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'doublebullets':
            player.powerup()
        #if hit.type == 'halfspeed':
            #player.halfspeed()
        if hit.type == 'life':
            player.lives += 1
        #if hit.type == 'invincible':
            #pass

    #End the game after the player's ship explosion
    if player.lives <= 0 and not finalexplosion.alive():
        draw_text(screen, "FINAL SCORE: " + str(score), 80, WIDTH/2, HEIGHT/2)
        pygame.display.flip()
        pygame.time.delay(3000)
        gameover = True

    #Advancing the levels
    if currentlevel == 0:
        #Spawn asteroids for level 1
        for i in range(15):
            asteroid = Asteroid()
            all_sprites.add(asteroid)
            asteroid_sprites.add(asteroid)
        currentlevel = 1
        level1flag = True
    if score >= 4000:
        currentlevel = 2
        if ufoflag == True and len(asteroid_sprites) == 0:
            level1flag = False
            level2flag = True
            for i in range(5):
                ufo = Enemyufo()
                all_sprites.add(ufo)
                ufo_sprites.add(ufo)
            ufoflag = False
    if ufoscore >= 35:
        currentlevel = 3
        if starlordflag == True and len(ufo_sprites) == 0:
            level2flag = False
            level3flag = True
            starlord = Starlord()
            all_sprites.add(starlord)
            starlord_sprites.add(starlord)
            starlordflag = False
    if starlordscore >= 1:
        currentlevel = 4
        #Spawn asteroids for level 4
        if l4flag == False:
            level3flag = False
            level4flag = True
            for i in range(15):
                asteroid = Asteroid()
                all_sprites.add(asteroid)
                asteroid_sprites.add(asteroid)
            for i in range(5):
                ufo = Enemyufo()
                all_sprites.add(ufo)
                ufo_sprites.add(ufo)
            l4flag = True
    if score >= 25000:
        currentlevel = 5
        if l5flag == False and len(asteroid_sprites) == 0 and len(ufo_sprites) == 0:
            level4flag = False
            level5flag = True
            starlord = Starlord()
            starlord.power = 2
            all_sprites.add(starlord)
            starlord_sprites.add(starlord)
            l5flag = True

    if starlordscore >= 2:
        draw_text(screen, "GAME OVER " + str(score), 100, WIDTH/2, HEIGHT * 1/4)
        draw_text(screen, "FINAL SCORE: " + str(score), 80, WIDTH/2, HEIGHT/2)

    #Drawing code
    screen.fill(WHITE)
    screen.blit(BackGround.image, BackGround.rect)
    all_sprites.draw(screen)
    draw_text(screen, "SCORE " + str(score), 18, WIDTH / 2, HEIGHT - 30)
    draw_text(screen, "LIVES " + str(player.lives), 18, 50, HEIGHT - 30)
    draw_text(screen, "LEVEL " + str(currentlevel), 18, WIDTH - 50, HEIGHT - 30)
    draw_text(screen, "STAR SCORE " + str(starlordscore), 18, WIDTH - 100, HEIGHT - 70)
    if level1flag == True:
        draw_text(screen, "LEVEL 1: Navigate the Asteroid Field: Destroy all asteroids", 20, WIDTH/2, 20)
    if level2flag == True:
        draw_text(screen, "LEVEL 2: Destroy the enemy UFO's", 20, WIDTH/2, 20)
    if level3flag == True:
        draw_text(screen, "LEVEL 3: Defeat starlords enemy ships", 20, WIDTH/2, 20)
    if level4flag == True:
        draw_text(screen, "LEVEL 4: Destroy asteroids and defeat the alien UFO's", 20, WIDTH/2, 20)
    if level5flag == True:
        draw_text(screen, "LEVEL 5: GOOD LUCK", 20, WIDTH/2, 20)

    pygame.display.flip()

pygame.quit()
