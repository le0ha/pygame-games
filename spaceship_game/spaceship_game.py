import pygame
import random

#general setup
pygame.init()
window_width, window_height = 1280, 720
screen = pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption("Spaceship Game")
running = True
clock = pygame.time.Clock()

#create classes for each type of rectangle (object)
class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load("resources/images/player.png")
        self.rect = self.image.get_frect(center=(window_width/2, window_height/2))
        self.direction = pygame.math.Vector2()
        self.speed = 300

        #laser cooldown
        self.can_shoot = True
        self.laser_shot_time = 0
        self.cooldown = 400

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shot_time >= self.cooldown:
                self.can_shoot = True


    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        player.rect.center += self.direction * self.speed * dt

        if pygame.key.get_just_pressed()[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf, player.rect.midtop, all_sprites)
            self.laser_shot_time = pygame.time.get_ticks()
            self.can_shoot = False

        self.laser_timer()

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        coords = (random.randint(0,window_width),random.randint(0,window_height))
        self.rect = self.image.get_frect(center=coords)

class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups) 
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)

    def update(self, dt):
        self.rect.y -= 400 * dt  
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.time_created = pygame.time.get_ticks()
        self.speed = 200
        self.direction = pygame.math.Vector2(random.uniform(-0.25, 0.25),1)


    def update(self, dt):
        self.rect.center += self.speed * self.direction * dt
        self.time_alive = pygame.time.get_ticks()
        if self.time_alive - self.time_created > 4000:
            self.kill()

#imports
all_sprites = pygame.sprite.Group()
star_surf = pygame.image.load("resources/images/star.png")
laser_surf = pygame.image.load("resources/images/laser.png")
meteor_surf = pygame.image.load("resources/images/meteor.png")

#create rectangles
for _ in range(20):
    Star(all_sprites, star_surf)
player = Player(all_sprites)

#meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 2000)

while running:
    dt = clock.tick() / 1000
    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            x, y = random.randint(0,1280), -10
            Meteor(meteor_surf, (x,y), all_sprites)
   
    all_sprites.update(dt)

    #draw the game
    screen.fill("turquoise4")
    all_sprites.draw(screen)
    pygame.display.update()

pygame.quit()