import pygame
import time
import random

snake_speed = 10

window_x = 480
window_y = 480

# catppuccin mocha color scheme: https://github.com/catppuccin/catppuccin
bgColor = pygame.Color(17, 17, 27)
fgColor = pygame.Color(205, 214, 244)
foodColor = pygame.Color(243, 139, 168)
greenColor = pygame.Color(166, 227, 161)

pygame.init()
pygame.display.set_caption('Python Snake')
game_window = pygame.display.set_mode((window_x, window_y))

fps = pygame.time.Clock()

snake_position = [230, 230]

snake_body = [
    [230, 230],
    [220, 230],
    [210, 230],
    [200, 230]
]

direction = 'RIGHT'
change_to = direction

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                change_to = 'UP'
            if event.key == pygame.K_s:
                change_to = 'DOWN'
            if event.key == pygame.K_a:
                change_to = 'LEFT'
            if event.key == pygame.K_d:
                change_to = 'RIGHT'
    
    # prevents snake from moving into two directions at a time
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'
    
    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10
    
    game_window.fill(bgColor)
    
    snake_body.insert(0, list(snake_position))
    for pos in snake_body:
        pygame.draw.rect(game_window, greenColor, pygame.Rect(pos[0], pos[1], 10, 10))
    
    # once fruit is added to the game, this pop() function will go into an if-else block.
    snake_body.pop()
    
    # refresh the game screen
    pygame.display.update()
    fps.tick(snake_speed)