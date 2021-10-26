import pygame
from random import randint
from time import time as timer

pygame.init()
HEIGHT = 900
WIDTH = 1600
window = pygame.display.set_mode((WIDTH, HEIGHT))
bg1 = pygame.transform.scale(pygame.image.load("bg1.png"), (WIDTH, HEIGHT))
bg2 = pygame.transform.scale(pygame.image.load("bg2.png"), (WIDTH, HEIGHT))
bg3 = pygame.transform.scale(pygame.image.load("bg33.png"), (WIDTH, HEIGHT))
bg4 = pygame.transform.scale(pygame.image.load("bg44.png"), (WIDTH, HEIGHT))


pygame.display.set_icon(pygame.image.load("icon.png"))
pygame.display.set_caption("Zombie City")



pygame.mixer.music.load("Game.music.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)    

player_sound = pygame.mixer.Sound("Shagi.ogg") 
player_sound.set_volume(0.7)
player_sound.play(-1)
    
shoot_sound = pygame.mixer.Sound("Vistrel1.ogg")
shoot_sound.set_volume(0.5)

reloading_sound = pygame.mixer.Sound("reloading.ogg")
reloading_sound.set_volume(0.5)

zombie_sound = pygame.mixer.Sound("Zombie.ogg")
zombie_sound.set_volume(0.8)
zombie_sound.play(-1)

Player_anim = [
pygame.transform.scale(pygame.image.load("pl0.png"), (125, 225)),
pygame.transform.scale(pygame.image.load("pl1.png"), (125, 225)),
pygame.transform.scale(pygame.image.load("pl2.png"), (125, 225)),
pygame.transform.scale(pygame.image.load("pl3.png"), (125, 225)),
pygame.transform.scale(pygame.image.load("pl4.png"), (125, 225)),
pygame.transform.scale(pygame.image.load("pl5.png"), (125, 225)),
pygame.transform.scale(pygame.image.load("pl6.png"), (125, 225)),
pygame.transform.scale(pygame.image.load("pl7.png"), (125, 225)),
pygame.transform.scale(pygame.image.load("pl8.png"), (125, 225)),
pygame.transform.scale(pygame.image.load("pl9.png"), (125, 225)),
pygame.transform.scale(pygame.image.load("pl10.png"), (125, 225)),
pygame.transform.scale(pygame.image.load("pl11.png"), (125, 225)),
pygame.transform.scale(pygame.image.load("pl12.png"), (125, 225)),
pygame.transform.scale(pygame.image.load("pl13.png"), (125, 225)),
pygame.transform.scale(pygame.image.load("pl14.png"), (125, 225)),
pygame.transform.scale(pygame.image.load("pl15.png"), (125, 225))
]

Zombie_anim = [
pygame.transform.scale(pygame.image.load("zb0.png"), (125, 200)),
pygame.transform.scale(pygame.image.load("zb1.png"), (125, 200)),
pygame.transform.scale(pygame.image.load("zb2.png"), (125, 200)),
pygame.transform.scale(pygame.image.load("zb3.png"), (125, 200)),
pygame.transform.scale(pygame.image.load("zb4.png"), (125, 200)),
pygame.transform.scale(pygame.image.load("zb5.png"), (125, 200)),
pygame.transform.scale(pygame.image.load("zb6.png"), (125, 200)),
pygame.transform.scale(pygame.image.load("zb7.png"), (125, 200)),
pygame.transform.scale(pygame.image.load("zb8.png"), (125, 200)),
]





class GameSprite(pygame.sprite.Sprite):
    def __init__(self, playerimg, x, y, width, height, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(playerimg), (width, height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
 
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
class Back(GameSprite):
    def __init__(self, playerimg, x, y, width, height, speed):
        GameSprite.__init__(self, playerimg, x, y, width, height, speed)
        self.anim_frame = 0
        self.moving = True   
        if self.moving == True:
            self.image = Zombie_anim[self.anim_frame]
            self.anim_frame += 1
            if self.anim_frame == len(Zombie_anim):
                self.anim_frame = 0
            self.moving = True   
 
class Player(GameSprite):
    def __init__(self, playerimg, x, y, width, height, speed):
        GameSprite.__init__(self, playerimg, x, y, width, height, speed)
        self.anim_frame = 0
        self.moving = True
    def move(self):
        press = pygame.key.get_pressed()
        if press[pygame.K_LEFT]:
            if self.rect.x > 10:
                self.rect.x -= self.speed
                self.moving = True
        if press[pygame.K_RIGHT]:
            if self.rect.x < WIDTH - 110:
                self.rect.x += self.speed
                self.moving = True
        if press[pygame.K_UP]:
            if self.rect.y > 10:
                self.rect.y -= self.speed
                self.moving = True
        if press[pygame.K_DOWN]:
            if self.rect.y < HEIGHT - 110:
                self.rect.y += self.speed
                self.moving = True
        if self.moving == True:
            self.image = Player_anim[self.anim_frame]
            self.anim_frame += 1
            if self.anim_frame == len(Player_anim):
                self.anim_frame = 0
            self.moving = True
    
            
    def fire(self):

        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 10)
        bullets_group.add(bullet)
        shoot_sound.play(0)
 
class Enemy(GameSprite):
    def __init__(self, playerimg, x, y, width, height, speed):
        GameSprite.__init__(self, playerimg, x, y, width, height, speed)
        self.anim_frame = 0
        self.moving = True
    def update(self):
        global failed
        self.rect.y += self.speed
        if self.rect.y >= HEIGHT:
            failed += 1
            self.rect.y = 0
            self.rect.x = randint(0, int(WIDTH - 40))
        if self.moving == True:
            self.image = Zombie_anim[self.anim_frame]
            self.anim_frame += 1
            if self.anim_frame == len(Zombie_anim):
                self.anim_frame = 0
            self.moving = True   


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
 
        if self.rect.y < 0:
            self.kill()




pl = Player("pl0.png", 500, 600, 125, 225, 15)
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
player_group.add(pl)
bullets_group = pygame.sprite.Group()
restart_button = GameSprite("restart.png",randint(0, int(WIDTH - 200)),randint(0, int(HEIGHT - 200)), 200, 100, 0)
restart_group = pygame.sprite.Group()
restart_group.add(restart_button)
ENEMIES = 4

 
for i in range(ENEMIES):
    enemy = Enemy("zb0.png", randint(0, int(WIDTH - 50)), 0, 125, 200, randint(1, 5))
    enemy_group.add(enemy)
 
# Adding some fonts
pygame.font.init()
font1 = pygame.font.Font('Shrift.ttf', 50)
font2 = pygame.font.SysFont('Shrift.ttf', 30)
font3 = pygame.font.Font('Shrift.ttf', 40)
lose_text = font1.render('You lose', True, (160, 160, 160))

levl1_text = font3.render("Level 1", True, (51,103   ,0))
levl2_text = font3.render("Level 2", True, (153,0,0))
levl3_text = font3.render("Level 3", True, (0,0,0))
levl4_text = font3.render("Level 4", True, (51,103   ,0))

win_text = font1.render('You win', True, (255, 255, 0))
reload_text = font1.render('Reloading!', True, (204, 204, 0))
clock = pygame.time.Clock()
run = True
finish = False
restart = False
 
magazine = 7
score = 0
failed = 0
reload_cooldown = False
reload_start_time = 0
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if reload_cooldown == False :
                    magazine -= 1
                    pl.fire()
    
    if not finish:
        # print(magazine)
        window.blit(bg1, (0, 0))
        
        score_text = font2.render("Score: " + str(score), True, (255, 249, 166))
        window.blit(score_text, (20, 20))
        failed_text = font2.render("Failed: " + str(failed), True, (255, 249, 166))
        window.blit(failed_text, (20, 45))
        magazine_text = font2.render("Bullets: " + str(magazine), True, (255, 249, 166))
        window.blit(magazine_text, (1450, 20))

        score_text1 = font2.render("Score: " + str(score), True, (10, 10, 10))
        
        failed_text1 = font2.render("Failed: " + str(failed), True, (10, 10, 10))
        
        magazine_text1 = font2.render("Bullets: " + str(magazine), True, (10, 10, 10))
        
    
        
        
        
        
        
        window.blit(levl1_text, (20, 800))


        pl.reset()
        pl.move()
        
        enemy_group.draw(window)
        enemy_group.update()
        
        bullets_group.update()
        bullets_group.draw(window)
 
        
        
        
        collides = pygame.sprite.groupcollide(player_group, enemy_group, False, False)
        if collides:
            window.blit(lose_text, (500, 10))
            restart = True
            
        bullet_collides = pygame.sprite.groupcollide(bullets_group, enemy_group, True, True)
        for c in bullet_collides:
            score += 1
            enemy = Enemy("zb0.png", randint(0, int(WIDTH - 50)), 0, 125, 200, randint(1, 5))
            enemy_group.add(enemy)
        
        if not restart:
            restart_button.rect.x = randint(0, int(WIDTH - 200))
            restart_button.rect.y = randint(0, int(HEIGHT - 200))
        
        
        if restart:
            
            for e in enemy_group:
                e.kill()
            
            
            restart_group.draw(window)
            restart_collides = pygame.sprite.groupcollide(bullets_group, restart_group, True, False)
            for c in restart_collides:
                finish = True

            
 
        if magazine == 0 and reload_cooldown == False:
            reload_start_time = timer()
            reload_cooldown = True
            reloading_sound.play(1)
        if reload_cooldown == True:
            window.blit(reload_text, (10, 100     ))
 
        if 4 > abs(reload_start_time - timer()) > 3 :
            magazine = 7
            reload_cooldown = False
        pygame.display.update()
        clock.tick(120)
        
        
        if score == 0:
            
            window.blit(bg1, (0, 0))
            
            window.blit(levl1_text, (20, 800))
            finish = False
        
        if score == 5:
            bg1 = bg2
            window.blit(bg2, (0, 0))
            levl1_text = levl2_text
            window.blit(levl2_text, (20, 800))
            finish = False
            if restart:
            
                for e in enemy_group:
                    e.kill()
                bg2 = bg1
                window.blit(bg1, (0, 0))
                levl2_text = levl1_text
                window.blit(levl1_text, (20, 800))
                restart_group.draw(window)
                restart_collides = pygame.sprite.groupcollide(bullets_group, restart_group, True, False)
                for c in restart_collides:
                    finish = True 
           
        
        if score == 10:
            bg1 = bg3
            window.blit(bg3, (0, 0))
            levl1_text = levl3_text
            window.blit(levl3_text, (20, 800))
            finish = False        
            score_text = score_text1
            failed_text = failed_text1
            magazine_text = magazine_text1
            if restart:
            
                for e in enemy_group:
                    e.kill()
                bg3 = bg1
                window.blit(bg1, (0, 0))
                levl3_text = levl1_text
                window.blit(levl1_text, (20, 800))
                restart_group.draw(window)
                restart_collides = pygame.sprite.groupcollide(bullets_group, restart_group, True, False)
                for c in restart_collides:
                    finish = True 
            
            
            
            window.blit(score_text1, (20, 20))
            
            window.blit(failed_text1, (20, 45))
            
            window.blit(magazine_text1, (1450, 20))
    
        if score == 15        :
            bg1 = bg4
            window.blit(bg4, (0, 0))
            levl1_text = levl4_text
            window.blit(levl3_text, (20, 800))
            finish = False
            if restart:
            
                for e in enemy_group:
                    e.kill()
                bg4 = bg1
                window.blit(bg1, (0, 0))
                levl2_text = levl1_text
                window.blit(levl1_text, (20, 800))
                restart_group.draw(window)
                restart_collides = pygame.sprite.groupcollide(bullets_group, restart_group, True, False)
                for c in restart_collides:
                    finish = True 

    
        if failed == 15:
            finish = True
            restart = True
            if restart:
            
                for e in enemy_group:
                    e.kill()
                
               
                restart_group.draw(window)
                restart_collides = pygame.sprite.groupcollide(bullets_group, restart_group, True, False)
                for c in restart_collides:
                    finish = True
    
    
    else:
        reload_cooldown = False
        magazine = 7
        failed = 0
        score = 0
        restart = False
        pygame.time.delay(1000)
        for e in enemy_group:
            e.kill()
 
        for b in bullets_group:
            b.kill()
 
        pl.rect.x = 700
        for i in range(ENEMIES):
            enemy = Enemy("zb0.png", randint(0, int(WIDTH - 50)), 0, 125, 200, randint(1, 5))
            enemy_group.add(enemy)
    
        finish = False