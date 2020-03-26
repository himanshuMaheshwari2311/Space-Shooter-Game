#1. imports
import pygame, sys
from pygame.locals import*
import math
import random

#2. init
pygame.init()
width = 640
height = 480
screen = pygame.display.set_mode((width, height))
keys = [False, False, False, False]
player_pos = [120, 120]
accuracy = [0, 0]
bullets = []
rouge_timer = 100
rouge_timer_1 = 0
rouge_ship = [[640,100]]
health_value = 200

#3. load_images
player_sprite = pygame.image.load("resources/images/hero.png")
background = pygame.image.load("resources/images/space_tile.png")
space_station_sprite = pygame.image.load("resources/images/space_station.png")
bullet_sprite = pygame.image.load("resources/images/bullet_sprite.png")
rouge_ship_sprite = pygame.image.load("resources/images/rouge_ship.png")
rouge_ship_copy = rouge_ship_sprite 
health_bar = pygame.image.load("resources/images/healthbar.png")
health = pygame.image.load("resources/images/health.png")

#4. game_loop
while True:
    rouge_timer -= 1
    #5. clear_screen
    screen.fill(0)

    #6. draw_sprites

    ##6.1 background_render
    for i in range(int(width / background.get_width()) + 1):
        for j in range(int(height / background.get_height()) + 1):
            screen.blit(background, (i * 100, j * 100))
    ##6.2 space_station_render
    screen.blit(space_station_sprite,(0,20))
    screen.blit(space_station_sprite,(0,135))
    screen.blit(space_station_sprite,(0,250))
    screen.blit(space_station_sprite,(0,365))

    ##6.3 player_render_and_rotation        
    position = pygame.mouse.get_pos()
    angle = math.atan2(position[1] - (player_pos[1] + 32), position[0] - (player_pos[0] + 26))
    player_rotation = pygame.transform.rotate(player_sprite, 360 - angle * 57.29)
    player_pos_new = (player_pos[0] - player_rotation.get_rect().width / 2, player_pos[1] - player_rotation.get_rect().height / 2 )
    screen.blit(player_rotation, player_pos_new)
    

    ##6.4 fire_bullets
    for bullet in bullets:
        index = 0;
        velocity_x = math.cos(bullet[0]) * 10
        velocity_y = math.sin(bullet[0]) * 10
        bullet[1] += velocity_x;
        bullet[2] += velocity_y;
        if bullet[1] < -64 or bullet[1] > 640 or bullet[2] < -64 or bullet[2] > 480:
            bullets.pop(index)
        index += 1
        for thrust in bullets:
            bullets_new = pygame.transform.rotate(bullet_sprite, 360 - thrust[0] * 57.29)
            screen.blit(bullets_new,(thrust[1],thrust[2]))
    ##6.5 render_rouge_ships
    if rouge_timer == 0:
        rouge_ship.append([640,random.randint(50,430)])
        rouge_timer = 100 - (rouge_timer_1 * 2)
        if rouge_timer_1 >= 35:
            rouge_timer_1 = 35
        else:
            rouge_timer_1 += 5
    index = 0
    for rouge in rouge_ship:
        if rouge[0] < -64:
            rouge_ship.pop(index)
        rouge[0] -= 7
        ##space_ship_collide
        rouge_rect = pygame.Rect(rouge_ship_copy.get_rect())
        rouge_rect.top = rouge[1]
        rouge_rect.left = rouge[0]
        if rouge_rect.left < 64:
            health_value -= random.randint(5,20)
            rouge_ship.pop(index)
        ##shoot_and_kill
        index_1 = 0
        for bullet in bullets:
            bullet_rect = pygame.Rect(bullet_sprite.get_rect())
            bullet_rect.left = bullet[1]
            bullet_rect.top = bullet[2]
            if rouge_rect.colliderect(bullet_rect):
                accuracy[0] += 1
                rouge_ship.pop(index)
                bullets.pop(index)
            index_1 += 1        
        index += 1
    for rouge in rouge_ship:
        screen.blit(rouge_ship_copy, rouge)

    #6.5 health_bar
    font = pygame.font.Font(None, 24)
    survived_text = font.render(str((90000 - pygame.time.get_ticks())/60000) + ":" + str((90000 - pygame.time.get_ticks())/1000 % 60).zfill(2), True, (0, 0, 0))
    text_rect = survived_text.get_rect()
    text_rect.topright = [635,5]
    screen.blit(survived_text, text_rect)

    #6.6 health_render
    screen.blit(health_bar, (5, 5))
    for health_1 in range(health_value):
        screen.blit(health, (health_1 + 8, 8))

    #7. update_screen
    pygame.display.flip()

    #8. events
    for event in pygame.event.get():
        if event.type == pygame.QUIT or health_value < 0:
            print ("Game Over")
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == K_w:
                keys[0] = True
            elif event.key == K_a:
                keys[1] = True
            elif event.key == K_s:
                keys[2] = True
            elif event.key == K_d:
                keys[3] = True
            elif event.key == K_ESCAPE:
                exit(0)
        if event.type == pygame.KEYUP:
            if event.key == K_w:
                keys[0] = False
            elif event.key == K_a:
                keys[1] = False
            elif event.key == K_s:
                keys[2] = False
            elif event.key == K_d:
                keys[3] = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos()
            accuracy[1] += 1
            bullets.append([math.atan2(position[1] - (player_pos[1] + 32), position[0] - (player_pos[0] + 26)),player_pos_new[0] + 32,player_pos_new[1] + 32])

    #9. move_player
    if keys[0]:
        player_pos[1] -= 5
    elif keys[2]:
        player_pos[1] += 5
    elif keys[1]:
        player_pos[0] -= 5
    elif keys[3]:
        player_pos[0] += 5
