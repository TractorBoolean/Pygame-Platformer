import pygame, sys, os
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()

WINDOW_SIZE = (600, 400)
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((300, 200))
pygame.display.set_caption('Myformer')

PLAYER_IMG = pygame.image.load('src/idle_0.png').convert()
PLAYER_IMG.set_colorkey((255, 255, 255))

DIRT_IMG = pygame.image.load(os.path.join('src', 'dirt.png'))
GRASS_IMG = pygame.image.load(os.path.join('src', 'grass.png'))


BG_COLOR = (146, 244, 255)

moving_right = False
moving_left = False

player_y_velocity = 0
air_timer = 0

scroll = [0, 0]

player_rect = pygame.Rect(50, 50, PLAYER_IMG.get_width(), PLAYER_IMG.get_height())

game_map = {}

background_parallax = [[0.25, [120, 10, 70, 400]],
                       [0.5, [280, 30, 40, 400]],
                       [0.25, [30, 40, 40, 400]],
                       [0.5, [130, 90, 70, 400]]]

def load_map(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()

    data = data.split('\n')
    game_map = []

    for row in data:
        game_map.append(list(row))

    return game_map

game_map = load_map('map')

def collision_test(rect, tiles):
    hit_list = []
    for tile2 in tiles:
        if rect.colliderect(tile2):
            hit_list.append(tile2)

    return hit_list

def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}

    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)

    for tile3 in hit_list:
        if movement[0] > 0:
            rect.right = tile3.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile3.right
            collision_types['left'] = True

    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)

    for tile4 in hit_list:
        if movement[1] > 0:
            rect.bottom = tile4.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile4.bottom
            collision_types['top'] = True

    return rect, collision_types

while True:
    display.fill(BG_COLOR)

    scroll[0] += (player_rect.x - scroll[0] - 132) / 20
    scroll[1] += (player_rect.y - scroll[1] - 76) / 20

    pygame.draw.rect(display, (7, 80, 75), pygame.Rect(0, 120, 300, 80))

    for bp in background_parallax:
        obj_rect = pygame.Rect(bp[1][0] - scroll[0] * bp[0], bp[1][1] - scroll[1] * bp[0],
                               bp[1][2], bp[1][3])

        if bp[0] == 0.5:
            pygame.draw.rect(display, (14, 222, 150), obj_rect)
        else:
            pygame.draw.rect(display, (9, 91, 85), obj_rect)

    tile_rects = []
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                display.blit(DIRT_IMG, (x * 16 - scroll[0], y * 16 - scroll[1]))
            if tile == '2':
                display.blit(GRASS_IMG, (x * 16 - scroll[0], y * 16 - scroll[1]))
            if tile != '0':
                tile_rects.append(pygame.Rect(x * 16, y * 16, 16, 16))

            x += 1

        y += 1

    player_movement = [0, 0]
    if moving_right:
        player_movement[0] += 2
    if moving_left:
        player_movement[0] -= 2

    if player_y_velocity > 3:
        player_y_velocity = 3

    player_y_velocity += 0.2
    player_movement[1] += player_y_velocity

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if collisions['bottom']:
        player_y_velocity = 0
        air_timer = 0
    else:
        air_timer += 1

    display.blit(PLAYER_IMG, (player_rect.x - scroll[0], player_rect.y - scroll[1]))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True

            if event.key == K_LEFT:
                moving_left = True

            if event.key == K_UP:
                if air_timer < 6:
                    player_y_velocity = -5

        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False

            if event.key == K_LEFT:
                moving_left = False

    surf = pygame.transform.scale(display, (WINDOW_SIZE[0] + 25, WINDOW_SIZE[1]))
    screen.blit(surf, (0, 0))
    pygame.display.update()
    clock.tick(60)



