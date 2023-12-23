# Libraries
from pygame import *
from random import randint
from time import time as timer

window = display.set_mode((700, 500))
background = transform.scale(image.load('galaxy.jpg'), (700, 500))

win = 0
lose = 0

mixer.init()
mixer.music.load('space.ogg')
mixer.music.set_volume(0.2)
mixer.music.play()

font.init()
font2 = font.SysFont('timesnewroman', 36)
font3 = font.Font(None, 90)

game_win = font3.render("YOU WIN", 1, (255, 0, 0))
gameover = font3.render("GAME OVER", 1, (255, 0, 0))
stage = font3.render("NEXT STAGE", 1, (255, 0, 0))
rel = font3.render("Reloding...", 1, (255, 0, 0))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, x, y, size_x, size_y, speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))  
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed  

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def PlayerMovement(self):
        key_pressed = key.get_pressed()

        if key_pressed[K_d]:
            self.rect.x += 4
        if key_pressed[K_a]:
            self.rect.x -= 4
    
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.x + 30, self.rect.y, 40, 40, 15)
        bullets.add(bullet)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

class Enemy(GameSprite):
    def update(self):
        global lose
        self.rect.y += self.speed
        if self.rect.y > 500:
            lose += 1
            self.rect.y = 0
            self.rect.x = randint(10, 600)
           
monsters = sprite.Group()     

for i in range(5):
    enemy = Enemy('ufo.png', randint(0, 600), 0, 50, 50, randint(1, 2))
    monsters.add(enemy)

asteroids = sprite.Group()  

for i in range(4):
    asteroid = Enemy('asteroid.png', randint(0, 600), 0, 65, 65, randint(1, 4))
    asteroids.add(asteroid)
rocket = Player('rocket.png', 300, 400, 100, 100, 10)
bullet = Bullet('bullet.png', 100, 400, 20, 20, 5)

number = 5
finished = False
rel_time = False
clock = time.Clock()
bullets = sprite.Group()
FPS = 120
run = True
num_fire = 0

while run:
    window.blit(background, (0, 0))     

    rocket.draw()
    monsters.draw(window)
    bullets.draw(window)
    asteroids.draw(window)

    if rel_time == True:
        now_time = timer()
        if now_time - last_time < 0.7:
            window.blit(rel, (600, 400))
        else:
            num_fire = 0
            rel_time = False
    
    collide = sprite.groupcollide(monsters, bullets, True, True)
    for c in collide:
        win += 1       
        enemy = Enemy('ufo.png', randint(0, 600), 0, 50, 50, randint(1, 2))
        monsters.add(enemy)

    collide = sprite.groupcollide(asteroids, bullets, False, True)

    if win > 10:
        window.blit(game_win, (200, 200))
        finished = True
        number += 1
        win = 0 
        lose = 0
        finished = False
        for m in monsters:
            m.kill()
        for b in bullets:
            b.kill()
        for d in asteroids:
            d.kill()
        for i in range(number):
            enemy = Enemy('ufo.png', randint(0, 600), 0, 90, 90, randint(1, 4))
            monsters.add(enemy)
        for i in range(4):
            asteroid = Enemy('asteroid.png', randint(0, 600), 0, 65, 65, randint(1, 4))
            asteroids.add(asteroid)


    if sprite.spritecollide(rocket, monsters, False) or lose >= 10:
        window.blit(gameover, (200, 200))
        finished = True
        keys = key.get_pressed()
        if keys[K_r]:
            win = 0 
            lose = 0
            finished = False
            for m in monsters:
                m.kill()
            for b in bullets:
                b.kill()
            for d in asteroids:
                d.kill()
            for i in range(5):
                enemy = Enemy('ufo.png', randint(0, 600), 0, 50, 50, randint(1, 4))
                monsters.add(enemy)
            for i in range(4):
                asteroid = Enemy('asteroid.png', randint(0, 600), 0, 65, 65, randint(1, 4))
                asteroids.add(asteroid)

    if sprite.spritecollide(rocket, asteroids, False):
        window.blit(gameover, (200, 200))
        finished = True
        keys = key.get_pressed()
        if keys[K_r]:
            win = 0 
            lose = 0
            finished = False
            for m in monsters:
                m.kill()
            for b in bullets:
                b.kill()
            for d in asteroids:
                d.kill()
            for i in range(5):
                enemy = Enemy('ufo.png', randint(0, 600), 0, 50, 50, randint(1, 4))
                monsters.add(enemy)
            for i in range(4):
                asteroid = Enemy('asteroid.png', randint(0, 600), 0, 65, 65, randint(1, 4))
                asteroids.add(asteroid)

    if not finished:
        bullets.update()

        monsters.update()

        rocket.PlayerMovement()

        asteroids.update()
   
    text = font2.render('Score: ' + str(win), 1, (255, 255, 255))
    window.blit(text, (10, 20))

    text = font2.render('Miss: ' + str(lose), 1, (255, 255, 255))
    window.blit(text, (10, 60))

    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 9 and rel_time == False:
                    rocket.fire()
                    num_fire += 1
                elif num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

    display.update()
    clock.tick(FPS)
    
