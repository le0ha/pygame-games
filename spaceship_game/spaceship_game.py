import pygame
import random

#general setup
pygame.init()
window_width, window_height = 1280, 720
screen = pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption("Spaceship Game")
running = True
clock = pygame.time.Clock()

#importing images and creating rectangles
player = pygame.image.load("resources/images/player.png")
star = pygame.image.load("resources/images/star.png")
meteor = pygame.image.load("resources/images/meteor.png")
laser = pygame.image.load("resources/images/laser.png")
player_rect = player.get_frect(center=(window_width/2, window_height/2))
meteor_rect = meteor.get_frect(center=(window_width/2,window_height/2))
laser_rect = laser.get_frect(bottomright = (window_width - 20, window_height - 20))

star_coords = []
for _ in range(20):
    star_coords.append((random.randint(0,window_width),random.randint(0,window_height)))

player_direction = pygame.math.Vector2(0.2,-0.1)
player_speed = 500

while running:
    dt = clock.tick() / 1000
    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if player_rect.right >= window_width or player_rect.left <= 0:
        player_direction.x *= -1
    if player_rect.top <= 0 or player_rect.bottom >= window_height:
        player_direction.y *= -1
    player_rect.center += player_direction * player_speed * dt

    #draw the game
    screen.fill("turquoise4")
    for coords in star_coords:
        screen.blit(star, coords)
    screen.blit(player, player_rect)
    screen.blit(laser, laser_rect)
    screen.blit(meteor,meteor_rect)
    pygame.display.update()

pygame.quit()