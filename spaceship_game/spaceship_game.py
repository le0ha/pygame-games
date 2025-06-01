import pygame
import random

#create classes for each type of rectangle (object)
class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load("resources/images/player.png")
        self.rect = self.image.get_frect(center=(window_width/2, window_height/2))
        self.direction = pygame.math.Vector2()
        self.speed = 350

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
            Laser(laser_surf, player.rect.midtop, (all_sprites, laser_sprites))
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
        laser_sound.play()

    def update(self, dt):
        self.rect.y -= 400 * dt  
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.surf = surf
        self.image = self.surf
        self.rect = self.image.get_frect(center = pos)
        self.time_created = pygame.time.get_ticks()
        self.speed = 200
        self.direction = pygame.math.Vector2(random.uniform(-0.5, 0.5),1)
        self.rotated = 0
        self.rotation = random.randint(50,100)

    def update(self, dt):
        self.rect.center += self.speed * self.direction * dt
        self.time_alive = pygame.time.get_ticks()
        if self.time_alive - self.time_created > 4000:
            self.kill()

        #add rotation
        self.rotated += self.rotation * dt
        self.image = pygame.transform.rotozoom(self.surf, self.rotated, 1)
        self.rect = self.image.get_frect(center = self.rect.center)

class Explosion(pygame.sprite.Sprite):
    def __init__(self, surf_list, pos, groups):
        super().__init__(groups)
        self.i = 0
        self.surf_list = surf_list
        self.image = self.surf_list[self.i]
        self.rect = self.image.get_frect(center = pos)

    def update(self, dt):
        self.i += 100 * dt
        self.image = self.surf_list[int(self.i)]
        if self.i >= 20:
            self.kill()

def collisions():
    global running
    meteor_collision = pygame.sprite.spritecollide(player, meteor_sprites, False, pygame.sprite.collide_mask)
    if meteor_collision:
        running = False

    for laser in laser_sprites:
        laser_collision = pygame.sprite.spritecollide(laser,meteor_sprites,True, pygame.sprite.collide_mask)
        if laser_collision:
            Explosion(explosion_surfs,laser.rect.midtop,all_sprites)
            explosion_sound.play()
            laser.kill()
            
def display_score():
    current_time = pygame.time.get_ticks() // 1000
    text_surf = font.render(f"In game for {str(current_time)} seconds",True,"#3a2e3f")
    text_rect = text_surf.get_frect(midtop = (window_width / 2, 30))
    
    #draw border
    border = pygame.draw.rect(screen, '#c1c2c7', text_rect.inflate(20,20).move(0,-5), border_radius=5)
    screen.blit(text_surf, text_rect)

#general setup
pygame.init()
window_width, window_height = 1280, 720
screen = pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption("Spaceship Game")
running = True
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group() 

#imports
star_surf = pygame.image.load("resources/images/star.png")
laser_surf = pygame.image.load("resources/images/laser.png")
meteor_surf = pygame.image.load("resources/images/meteor.png")
font = pygame.font.Font("resources/images/Oxanium-Bold.ttf", 20)
explosion_surfs = []
for i in range(21):
    explosion_surfs.append(pygame.image.load(f"resources/images/explosion/{i}.png"))

laser_sound = pygame.mixer.Sound("resources/audio/laser.wav")
laser_sound.set_volume(0.1)
game_music = pygame.mixer.Sound("resources/audio/game_music.wav")
game_music.set_volume(0.05)
game_music.play(loops=-1)
explosion_sound = pygame.mixer.Sound("resources/audio/explosion.wav")
explosion_sound.set_volume(0.1)

#create rectangles
for _ in range(20):
    Star(all_sprites, star_surf)
player = Player(all_sprites)

#meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

while running:
    dt = clock.tick() / 1000
    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            x, y = random.randint(0,1280), -10
            Meteor(meteor_surf, (x,y), (all_sprites, meteor_sprites))

    #update frame
    collisions()
    all_sprites.update(dt)

    #draw the game
    screen.fill("#3a2e3f")
    all_sprites.draw(screen)
    display_score()
    pygame.display.update()

pygame.quit()