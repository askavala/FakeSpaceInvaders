import pygame
from pygame.math import Vector2
import random

speed = 6
width = 900
height = 670
bullet_speed = 10

pygame.init()
screen = pygame.display.set_mode((width,height))

ENEMY_SHOOT = pygame.USEREVENT
pygame.time.set_timer(ENEMY_SHOOT,700)

test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
test_font1 = pygame.font.Font('font/Pixeltype.ttf', 100)
intro_text = test_font.render('Press space to run',False,(255,150,150))
intro_text1 = test_font.render('Press space to run',False,(222,50,50))
intro_text_rect = intro_text.get_rect(center = (width/2,100))
intro_text_rect10 = intro_text1.get_rect(center = (width/2 + 1, 99))
intro_text_rect11 = intro_text1.get_rect(center = (width/2 - 1, 99))
intro_text_rect12 = intro_text1.get_rect(center = (width/2 + 1, 101))
intro_text_rect13 = intro_text1.get_rect(center = (width/2 - 1, 101))

class Bg():
    def __init__(self) -> None:
        self.star_list = []
        self.star_rect = pygame.Rect(0,0,2,2)
        self.star_rect1 = pygame.Rect(0,0,1,1)
        self.star_rect2 = pygame.Rect(0,0,3,3)
        self.create_list()

    def create_list(self):
        for x in range(0,240):
            star_vec = Vector2(random.randint(0,width), random.randint(0,height)) 
            self.star_list.append(star_vec)
        
    def move_stars(self):
        index = 0
        for star in self.star_list:
            star.y += 1
            if star.y > 670:
                star.y = 0 
            if index % 4 == 0:
                self.star_rect2.center = star
                pygame.draw.rect(screen, (255,255,255), self.star_rect2)
            elif index % 4 == 1:
                self.star_rect1.center = star
                pygame.draw.rect(screen, (255,255,255), self.star_rect1)
            else:
                self.star_rect.center = star
                pygame.draw.rect(screen, (255,255,255), self.star_rect)
            index += 1


class Enemy():
    def __init__(self,type) -> None:
        self.move = 0
        self.right = True
        self.health = 3
        self.bullet_list = []
        self.bullet_rect = pygame.Rect(0,0,3,30)
        if type == 1:
            self.image = pygame.image.load("1.png").convert_alpha()
            self.vec = Vector2(100,100)
        if type == 2:
            self.image = pygame.image.load("2.png").convert_alpha()
            self.vec = Vector2(300,100)
        if type == 3:
            self.image = pygame.image.load("3.png").convert_alpha()
            self.vec = Vector2(500,100) 
        self.image = pygame.transform.rotozoom(self.image, 270, 0.8)
        self.image_rect = self.image.get_rect(center = self.vec)
        
    def draw(self):
        screen.blit(self.image, self.image_rect)
        
    def create_bullet(self):
        if len(self.bullet_list) < 3:
            self.bullet_list.append(Vector2(self.image_rect.centerx, self.image_rect.bottom))
        
    def move_bullet(self):
        for bullet in self.bullet_list:
            if bullet.y >= 930:
                self.bullet_list.remove(bullet)
            else:
                bullet.y += bullet_speed
                self.bullet_rect.center = bullet
                pygame.draw.rect(screen, (255,50,0), self.bullet_rect)
            
    def move_enemy(self):
        if self.move % 180 < 90:
            self.image_rect.x += 3
            
        if self.move % 180 >= 90:
            self.image_rect.x -= 3
        
        if self.move > 180:
            self.move = 0
        self.move += 1 
        
        
class Player():
    def __init__(self) -> None:        
        self.player = pygame.image.load("4.png").convert_alpha()
        self.player = pygame.transform.rotozoom(self.player,90,0.5)
        self.player_rect = self.player.get_rect(center = (width / 2, height - 100))
        self.health = 3
        self.bullet_list = []
        self.bullet_rect = pygame.Rect(0,0,3,30)

    def draw(self):
        screen.blit(self.player, self.player_rect)
    
    def create_bullet(self):
        if len(self.bullet_list) < 3:
            self.bullet_list.append(Vector2(self.player_rect.centerx, self.player_rect.y))
    
    def move_bullet(self):
        for bullet in self.bullet_list:
            if bullet.y <= -20:
                self.bullet_list.remove(bullet)
            else:
                bullet.y -= bullet_speed
                self.bullet_rect.center = bullet
                pygame.draw.rect(screen, (255,100,0), self.bullet_rect)
    
    def move_and_fire(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_d] and self.player_rect.right < width:
            self.player_rect.x += speed
        if key[pygame.K_a] and self.player_rect.left > 0:
            self.player_rect.x -= speed
        self.move_bullet()
        self.draw()


class Game():
    def __init__(self) -> None:
        self.player = Player()
        self.enemy_list = [Enemy(1), Enemy(2), Enemy(3)]
        self.boom4 = pygame.image.load("B4.png").convert_alpha()
        self.boom4 = pygame.transform.rotozoom(self.boom4, 0, 0.5)
        self.boom2 = pygame.image.load("B2.png").convert_alpha()
        self.boom4_rect = self.boom4.get_rect(center = (0,0))
        self.stage = "intro"
        
    def check_collide(self):
        for enemy in self.enemy_list:
            for bullet in self.player.bullet_list:
                self.player.bullet_rect.center = bullet
                if self.player.bullet_rect.colliderect(enemy.image_rect):
                    vec = bullet
                    self.player.bullet_list.remove(bullet)
                    return 1, vec, enemy
        for enemy in self.enemy_list:
            for bullet in enemy.bullet_list:
                enemy.bullet_rect.center = bullet
                vec = bullet
                if self.player.player_rect.colliderect(enemy.bullet_rect):
                    enemy.bullet_list.remove(bullet)
                    return 2, vec, None
        return 0, Vector2(-10, -10), None
    
    def play(self):
        rect = pygame.Rect(0,0,60,60)
        self.player.move_and_fire()
        for enemy in self.enemy_list:
            enemy.move_bullet()
            enemy.move_enemy()
            enemy.draw()
        collide, vec, enemy = self.check_collide()
        if collide == 1:
            enemy.health -= 1
            if enemy.health > 0:
                self.boom4_rect.center = vec                  
                screen.blit(self.boom4, self.boom4_rect)
            else:
                rect.center = enemy.image_rect.center
                self.enemy_list.remove(enemy)
                screen.blit(self.boom2, rect)
        elif collide == 2:
            self.player.health -= 1
            if self.player.health > 0:
                self.boom4_rect.center = vec                  
                screen.blit(self.boom4, self.boom4_rect)
            else:
                print("game over")
                
    def enemy_shoot(self):
        for enemy in self.enemy_list:
            if random.randint(0,1):
                enemy.create_bullet()
                
    def main_loop(self):
        if self.stage == "active":
            self.game_loop()
        elif self.stage == "intro":
            self.intro()
            
    def game_loop(self):
        self.play()
        pygame.display.update()
        if self.player.health <= 0 or len(self.enemy_list) <= 0:
            self.player.health = 3
            self.enemy_list = [Enemy(1), Enemy(2), Enemy(3)]
            self.player.bullet_list.clear()
            self.stage = "intro"
    
    def intro(self):
        screen.blit(intro_text1, intro_text_rect10)
        screen.blit(intro_text1, intro_text_rect11)
        screen.blit(intro_text1, intro_text_rect12)
        screen.blit(intro_text1, intro_text_rect13)
        screen.blit(intro_text, intro_text_rect)
        pygame.display.update()
    

clock = pygame.time.Clock()
game_on = 1
star_rect = pygame.rect.Rect(0,0,2,2)

game = Game()
bg = Bg()
bg.create_list()
while game_on:
    screen.fill("black")
    bg.move_stars()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game.stage == "active":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game.player.create_bullet()
            if event.type == ENEMY_SHOOT:
                game.enemy_shoot()
        if game.stage == "intro":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game.stage = "active"
            
    game.main_loop()
    clock.tick(60)

pygame.quit()