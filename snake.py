import pygame
import time
import random
import sys

snake_speed = 10

window_x = 480
window_y = 520

# catppuccin mocha color scheme: https://github.com/catppuccin/catppuccin
bgColor = pygame.Color(17, 17, 27)
fgColor = pygame.Color(205, 214, 244)
buttonColor = pygame.Color(49, 50, 68)
highlightColor = pygame.Color(69, 71, 90)
foodColor = pygame.Color(243, 139, 168)
greenColor = pygame.Color(166, 227, 161)

pygame.init()
pygame.font.init()
pygame.display.set_caption('Python Snake')
game_window = pygame.display.set_mode((window_x, window_y))

fps = pygame.time.Clock()

headerFont = pygame.font.Font('assets/fonts/pixeloidBold.ttf', 20)
textFont = pygame.font.Font('assets/fonts/pixeloid.ttf', 16)

def quit():
    pygame.quit()
    sys.exit()

# game over code (remove pass)
def gameOver():
    pygame.display.flip()

def gameStart():
    snake_position = [230, 270]

    snake_body = [
        [snake_position[0], snake_position[1]],
        [snake_position[0] - 10, snake_position[1]],
        [snake_position[0] - 20, snake_position[1]],
        [snake_position[0] - 30, snake_position[1]]
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
            if event.type == pygame.QUIT:
                quit()
        
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
        
        # draw area borders
        borderWidth = 10
        
        topBorder = pygame.draw.rect(game_window, fgColor, pygame.Rect(0, 40, window_x, borderWidth))
        leftBorder = pygame.draw.rect(game_window, fgColor, pygame.Rect(0, 40, borderWidth, window_y - 40))
        rightBorder = pygame.draw.rect(game_window, fgColor, pygame.Rect(window_x - 10, 40, 10, window_y - 40))
        bottomBorder = pygame.draw.rect(game_window, fgColor, pygame.Rect(0, window_y - 10, window_x, borderWidth))    
        
        snake_body.insert(0, list(snake_position))
        for pos in snake_body:
            pygame.draw.rect(game_window, greenColor, pygame.Rect(pos[0], pos[1], 10, 10))
        
        # once fruit is added to the game, this pop() function will go into an if-else block.
        snake_body.pop()
        
        # if the snake reaches one of the borders, trigger game over.
        if snake_position[1] <= 40 or snake_position[1] >= 520 or snake_position[0] <= 0 or snake_position[0] >= 480:
            gameOver()
        
        # refresh the game screen
        pygame.display.update()
        fps.tick(snake_speed)

def menuSelector(option):
    if option == 0:
        gameStart()
    elif option == 1:
        settings()
    elif option == 2:
        quit()

def settings():
    pass

# put menu code here (remove pass)
def menu():
    option = 0
    while True:
        game_window.fill(bgColor)
        
        title = headerFont.render('Python Snake', True, fgColor)
            
        buttons = ["Start", "Settings", "Exit"]
        activeButton = buttons[option]
            
        buttonWidth = 140
        buttonHeight = 60
        buttonListXCoordinate = (window_x / 2) - (buttonWidth / 2)
        buttonListYCoordinate = 80
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    option += 1
                elif event.key == pygame.K_w or event.key == pygame.K_UP:
                    option -= 1
                elif event.key == pygame.K_RETURN:
                    menuSelector(option)
        
        if option < 0:
            option = 2
        elif option > 2:
            option = 0
        
        for button in buttons:
            buttonListYCoordinate += 90
        
            if activeButton == button:
                pygame.draw.rect(game_window, highlightColor, pygame.Rect(buttonListXCoordinate, buttonListYCoordinate, buttonWidth, buttonHeight))
                game_window.blit(textFont.render(button, True, fgColor), ((window_x / 2) - 50, buttonListYCoordinate + 20))
            else:
                pygame.draw.rect(game_window, buttonColor, pygame.Rect(buttonListXCoordinate, buttonListYCoordinate, buttonWidth, buttonHeight))
                game_window.blit(textFont.render(button, True, fgColor), ((window_x / 2) - 50, buttonListYCoordinate + 20))
        
        game_window.blit(title, ((window_x / 2) - 90, 100))
        pygame.display.update()
        fps.tick(60)

menu()