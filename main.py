import pygame
from pygame.locals import *

pygame.init()

screen_width = 800
screen_height = 800

window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Breakout')

clock = pygame.time.Clock()

running = True

def redraw_window():
    pygame.display.update()

while running:
    clock.tick(100)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    redraw_window()

pygame.quit()
