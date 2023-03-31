import sys
import json
try:
    import pygame
except:
    print("Pygame is not installed.\nPlease run: 'python -m pip install -U pygame==2.3.0 --user'")
    sys.exit()
import time
import random

window_x = 480
window_y = 520

# catppuccin mocha color scheme: https://github.com/catppuccin/catppuccin
# nord color color scheme: https://www.nordtheme.com
# rose pine dawn color scheme: https://rosepinetheme.com/palette
defaultSettings = {
    "difficulty": 10,
    "chosenPalette": "old-school",
    "colorPalette": {
        "catppuccin-mocha": {
            "bgColor"       : (17, 17, 27),
            "fgColor"       : (205, 214, 244),
            "buttonColor"   : (49, 50, 68),
            "highlightColor": (69, 71, 90),
            "gameOverColor" : (235, 160, 172),
            "foodColor"     : (243, 139, 168),
            "snakeColor"    : (166, 227, 161)
        },
        "nord": {
            "bgColor"       : ('#2E3440'),
            "fgColor"       : ('#ECEFF4'),
            "buttonColor"   : ('#3B4252'),
            "highlightColor": ('#4C566A'),
            "gameOverColor" : ('#BF616A'),
            "foodColor"     : ('#D08770'),
            "snakeColor"    : ('#AEBE8C')
        },
        "rose-pine-dawn": {
            "bgColor"       : ('#faf4ed'),
            "fgColor"       : ('#575279'),
            "buttonColor"   : ('#fffaf3'),
            "highlightColor": ('#f2e9e1'),
            "gameOverColor" : ('#b4637a'),
            "foodColor"     : ('#d7827e'),
            "snakeColor"    : ('#56949f')
        },
        "old-school": {
            "bgColor"       : ('#d1e37b'),
            "fgColor"       : ('#0f1105'),
            "buttonColor"   : ('#d1e37b'),
            "highlightColor": ('#6e7a37'),
            "gameOverColor" : ('#0f1105'),
            "foodColor"     : ('#0f1105'),
            "snakeColor"    : ('#0f1105')
        }
    },
    "walls": True
}

# check if settings file exists
try:
    file = open('settings.json', mode = 'x')
    file.close()
    # if not, create settings.json with default settings
    with open('settings.json', mode = 'w') as file:
        file.write(json.dumps(defaultSettings, indent = 4))
except FileExistsError:
    # if file exists, do nothing
    pass
finally:
    # read settings.json file and define color palette, snake speed, and walls
    with open('settings.json', mode = 'r') as file:
        settings = json.load(file)
        palette = settings["chosenPalette"]
        colors = settings["colorPalette"][palette]
        
        bgColor = pygame.Color(colors["bgColor"])
        fgColor = pygame.Color(colors["fgColor"])
        buttonColor = pygame.Color(colors["buttonColor"])
        highlightColor = pygame.Color(colors["highlightColor"])
        gameOverColor = pygame.Color(colors["gameOverColor"])
        foodColor = pygame.Color(colors["foodColor"])
        snakeColor = pygame.Color(colors["snakeColor"])
        
        snake_speed = settings["difficulty"]
        walls = settings["walls"]

# initialize pygame
pygame.init()
pygame.font.init()
pygame.display.set_caption('Python Snake')
game_window = pygame.display.set_mode((window_x, window_y))

fps = pygame.time.Clock()

headerFont = pygame.font.Font('assets/fonts/pixeloidBold.ttf', 20)
textFont = pygame.font.Font('assets/fonts/pixeloid.ttf', 16)

# quit pygame and python
def quit():
    file.close()
    pygame.quit()
    sys.exit()

# game over code (remove pass)
def gameOverSequence(color, score, gameOverFont, textFont, snakeBody):        
    while True:
        game_window.fill(bgColor)
        
        game_over_surface = gameOverFont.render('Game Over', True, color)
        score_surface = textFont.render('Your score is: ' + str(score), True, color)
        instruction_surface = textFont.render('Press ENTER to go to the main menu.', True, fgColor)
        
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (window_x / 2, window_y / 4)
        
        score_rect = score_surface.get_rect()
        score_rect.midtop = (window_x / 2, (window_y / 4) + 30)
        
        instruction_rect = instruction_surface.get_rect()
        instruction_rect.center = (window_x / 2, (window_y / 4) + 70)
        
        game_window.blit(game_over_surface, game_over_rect)
        game_window.blit(score_surface, score_rect)
        game_window.blit(instruction_surface, instruction_rect)
                
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
            if event.type == pygame.QUIT:
                quit()
        
        pygame.display.update()
        fps.tick(60)

def showScore(score, color, font):
    # render score
    score_surface = font.render('Score: ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    score_rect.midleft =  (10, 20)
    
    # render pause instructions
    instruction_surface = font.render('Press ESCAPE to pause.', True, color)
    instruction_rect = instruction_surface.get_rect()
    instruction_rect.midright = (window_x - 10, 20)
    
    # display text on screen
    game_window.blit(score_surface, score_rect)
    game_window.blit(instruction_surface, instruction_rect)
    
# this allows the user to take a break from the game
def gamePause(color):
    while True:
        # cover the screen
        game_window.fill(bgColor)
        
        # render text telling the user that the game is paused and how to get back to the game
        paused_surface = headerFont.render('Paused', True, color)
        instruction_surface = textFont.render('Press ENTER or ESCAPE to go back to the game.', True, fgColor)
        control_surface = textFont.render('Control the snake with W A S D or the arrow keys.', True, fgColor)
        
        # position the text
        paused_rect = paused_surface.get_rect()
        paused_rect.center = (window_x / 2, window_y / 4)
        
        instruction_rect = instruction_surface.get_rect()
        instruction_rect.center = (window_x / 2, (window_y / 4) + 40)
        
        control_rect = control_surface.get_rect()
        control_rect.center = (window_x / 2, window_y - 40)
        
        # display text on the screen
        game_window.blit(paused_surface, paused_rect)
        game_window.blit(instruction_surface, instruction_rect)
        game_window.blit(control_surface, control_rect)
        
        # accept input to take user back to the game
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                    return False
            if event.type == pygame.QUIT:
                quit()
        
        pygame.display.update()
        fps.tick(60)

def gameStart():
    # initial position and score
    snake_position = [230, 270]
    score = 0

    # initial snake body
    snake_body = [
        [snake_position[0], snake_position[1]],
        [snake_position[0] - 10, snake_position[1]],
        [snake_position[0] - 20, snake_position[1]],
        [snake_position[0] - 30, snake_position[1]]
    ]
    
    # spawns initial food randomly
    food_position = [random.randrange(20, window_x - 20, 10),
                     random.randrange(60, window_y - 20, 10)]

    # manages whether food can spawn or not
    food_spawn = True

    # sets direction of snake and direction to turn to. (default snake movement is right)
    direction = 'RIGHT'
    change_to = direction
    
    # manages game states (paused or game over)
    gameOver = False
    isPaused = False

    while True and not gameOver and not isPaused:
        game_window.fill(bgColor)
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    change_to = 'UP'
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'
                if event.key == pygame.K_ESCAPE:
                    isPaused = True
                    isPaused = gamePause(fgColor)
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
        
        # draw area borders
        borderWidth = 10
        
        topBorder = pygame.draw.rect(game_window, fgColor, pygame.Rect(0, 40, window_x, borderWidth))
        leftBorder = pygame.draw.rect(game_window, fgColor, pygame.Rect(0, 40, borderWidth, window_y - 40))
        rightBorder = pygame.draw.rect(game_window, fgColor, pygame.Rect(window_x - 10, 40, 10, window_y - 40))
        bottomBorder = pygame.draw.rect(game_window, fgColor, pygame.Rect(0, window_y - 10, window_x, borderWidth))    
        
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
            pygame.draw.rect(game_window, snakeColor, pygame.Rect(pos[0], pos[1], 10, 10))
        
        # render food
        pygame.draw.rect(game_window, foodColor, pygame.Rect(food_position[0], food_position[1], 10, 10))
        
        # if the snake reaches one of the borders, trigger game over.
        if snake_position[0] < 10 or snake_position[0] >= window_x - 10:
            gameOver = True
            gameOverSequence(gameOverColor, score, headerFont, textFont, snake_body)
        if snake_position[1] <= 40 or snake_position[1] >= window_y - 10:
            gameOver = True
            gameOverSequence(gameOverColor, score, headerFont, textFont, snake_body)
        
        # check if snake collides with body
        for block in snake_body[1:]:
            if snake_position[0] == block[0] and snake_position[1] == block[1]:
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
    
    # intro animation
    titleString = ""
    for letter in "Python Snake":
        game_window.fill(bgColor)
        
        titleString += letter
        title = headerFont.render(titleString, True, fgColor)
        game_window.blit(title, ((window_x / 2) - 90, 100))
        pygame.display.update()
        fps.tick(15)
            
    while True:
        game_window.fill(bgColor)
        
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
