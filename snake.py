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
gameOverColor = pygame.Color(235, 160, 172)
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
def gameOverSequence(color, score, gameOverFont, textFont, snakeBody):        
    while True:
        game_window.fill(bgColor)
        
        game_over_surface = gameOverFont.render('Game Over', True, color)
        score_surface = textFont.render('Your score is: ' + str(score), True, color)
        instruction_surface = textFont.render('Press any key to go to the main menu.', True, fgColor)
        
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (window_x / 2, window_y / 4)
        
        score_rect = score_surface.get_rect()
        score_rect.midtop = (window_x / 2, (window_y / 4) + 30)
        
        instruction_rect = instruction_surface.get_rect()
        instruction_rect.center = (window_x / 2, (window_y / 4) + 60)
        
        game_window.blit(game_over_surface, game_over_rect)
        game_window.blit(score_surface, score_rect)
        game_window.blit(instruction_surface, instruction_rect)
        
        time.sleep(1)
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return
            if event.type == pygame.QUIT:
                quit()
        
        pygame.display.update()
        fps.tick(60)

def showScore(score, color, font):
    score_surface = font.render('Score: ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    game_window.blit(score_surface, score_rect)

def gameStart():
    snake_position = [230, 270]
    score = 0

    snake_body = [
        [snake_position[0], snake_position[1]],
        [snake_position[0] - 10, snake_position[1]],
        [snake_position[0] - 20, snake_position[1]],
        [snake_position[0] - 30, snake_position[1]]
    ]
    
    food_position = [random.randrange(20, window_x - 20, 10),
                     random.randrange(60, window_y - 20, 10)]

    food_spawn = True

    direction = 'RIGHT'
    change_to = direction
    
    gameOver = False

    while True and not gameOver:
        game_window.fill(bgColor)
        
        # draw area borders
        borderWidth = 10
        
        topBorder = pygame.draw.rect(game_window, fgColor, pygame.Rect(0, 40, window_x, borderWidth))
        leftBorder = pygame.draw.rect(game_window, fgColor, pygame.Rect(0, 40, borderWidth, window_y - 40))
        rightBorder = pygame.draw.rect(game_window, fgColor, pygame.Rect(window_x - 10, 40, 10, window_y - 40))
        bottomBorder = pygame.draw.rect(game_window, fgColor, pygame.Rect(0, window_y - 10, window_x, borderWidth))    
        
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
        
        showScore(score, fgColor, textFont)
        
        # insert object into array of snake body
        snake_body.insert(0, list(snake_position))
        if snake_position[0] == food_position[0] and snake_position[1] == food_position[1]:
            score += 10
            food_spawn = False
        else:
            snake_body.pop()
        
        # check if food has not spawned and spawn a new one
        if not food_spawn:
            food_position = [random.randrange(20, window_x - 20, 10),
                             random.randrange(60, window_y - 20, 10)]
        
        food_spawn = True
        
        # render snake body
        for pos in snake_body:
            pygame.draw.rect(game_window, greenColor, pygame.Rect(pos[0], pos[1], 10, 10))
        
        # render food
        pygame.draw.rect(game_window, foodColor, pygame.Rect(food_position[0], food_position[1], 10, 10))
        
        # if the snake reaches one of the borders, trigger game over.
        if snake_position[0] < 10 or snake_position[0] >= window_x - 10:
            gameOver = True
            gameOverSequence(gameOverColor, score, headerFont, textFont, snake_body)
        if snake_position[1] <= 40 or snake_position[1] >= window_y - 10:
            gameOver = True
            gameOverSequence(gameOverColor, score, headerFont, textFont, snake_body)
        
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

# put menu code here
def menu():
    option = 0
    while True:
        game_window.fill(bgColor)
        
        title = headerFont.render('Python Snake', True, fgColor)
        
        # list of buttons on main menu
        buttons = ["Start", "Settings", "Exit"]
        activeButton = buttons[option]
        
        # size + coordinates
        buttonWidth = 140
        buttonHeight = 60
        buttonListXCoordinate = (window_x / 2) - (buttonWidth / 2)
        buttonListYCoordinate = 80
        
        # accept input from player to navigate menu
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
        
        # if option is less than 0, select the last option. if option is greater than 2, select the first option
        if option < 0:
            option = 2
        elif option > 2:
            option = 0
        
        # render each button in the list
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