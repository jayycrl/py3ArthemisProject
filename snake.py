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
    "chosenPalette": "rose-pine-dawn",
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

inGameSettings = dict()

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
        inGameSettings = settings

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
def gameOverSequence(color, score, gameOverFont, textFont, snakeBody, bgColor, fgColor):
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
def gamePause(color, bgColor):
    while True:
        # cover the screen
        game_window.fill(bgColor)
        
        # render text telling the user that the game is paused and how to get back to the game
        paused_surface = headerFont.render('Paused', True, color)
        instruction_surface = textFont.render('Press ENTER or ESCAPE to go back to the game.', True, color)
        control_surface = textFont.render('Control the snake with W A S D or the arrow keys.', True, color)
        
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

def gameStart(snakeSpeed, walls, bgColor, fgColor, foodColor, snakeColor, gameOverColor):
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
                    isPaused = gamePause(fgColor, bgColor)
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
            pygame.draw.rect(game_window, snakeColor, pygame.Rect(pos[0], pos[1], 10, 10))
        
        # render food
        pygame.draw.rect(game_window, foodColor, pygame.Rect(food_position[0], food_position[1], 10, 10))
        
        if walls:
            # draw area borders
            borderWidth = 10
            topBorder = pygame.draw.rect(game_window, fgColor, pygame.Rect(0, 40, window_x, borderWidth))
            leftBorder = pygame.draw.rect(game_window, fgColor, pygame.Rect(0, 40, borderWidth, window_y - 40))
            rightBorder = pygame.draw.rect(game_window, fgColor, pygame.Rect(window_x - 10, 40, 10, window_y - 40))
            bottomBorder = pygame.draw.rect(game_window, fgColor, pygame.Rect(0, window_y - 10, window_x, borderWidth))
            # if the snake reaches one of the borders, trigger game over.
            if snake_position[0] < 10 or snake_position[0] >= window_x - 10:
                gameOver = True
                gameOverSequence(gameOverColor, score, headerFont, textFont, snake_body, bgColor, fgColor)
            if snake_position[1] <= 40 or snake_position[1] >= window_y - 10:
                gameOver = True
                gameOverSequence(gameOverColor, score, headerFont, textFont, snake_body, bgColor, fgColor)
        else:
            # if the snake reaches one of the borders, trigger game over.
            if snake_position[0] < 0:
                snake_position[0] = window_x
            elif snake_position[0] >= window_x:
                snake_position[0] = 0
            
            if snake_position[1] <= 40:
                snake_position[1] = window_y
            elif snake_position[1] >= window_y:
                snake_position[1] = 40
        # check if snake collides with body
        for block in snake_body[1:]:
            if snake_position[0] == block[0] and snake_position[1] == block[1]:
                gameOver = True
                gameOverSequence(gameOverColor, score, headerFont, textFont, snake_body, bgColor, fgColor)
        
        # refresh the game screen
        pygame.display.update()
        fps.tick(snakeSpeed)

def menuSelector(option, palette, snake_speed, walls, highlightColor, bgColor, fgColor, foodColor, snakeColor, gameOverColor, buttonColor):
    if option == 0:
        gameStart(snake_speed, walls, bgColor, fgColor, foodColor, snakeColor, gameOverColor)
    elif option == 1:
        settings(palette, snake_speed, walls, highlightColor, bgColor, fgColor, foodColor, buttonColor)
    elif option == 2:
        quit()

# chooses the setting when the user hits the enter key. it returns the chosen option to update the red square that shows the user what option is selected.
def settingsSelector(horizontalOption, verticalOption):
    # this changes the settings dictionary ingame. the changes are reflected to the json file later on.
    # difficulty settings
    if verticalOption == 0:
        if horizontalOption == 0:
            inGameSettings["difficulty"] = 10
        elif horizontalOption == 1:
            inGameSettings["difficulty"] = 20
        elif horizontalOption == 2:
            inGameSettings["difficulty"] = 30

        selectedOption = horizontalOption
    
    # walls settings
    elif verticalOption == 1:
        if horizontalOption == 0:
            inGameSettings["walls"] = True
        elif horizontalOption == 1:
            inGameSettings["walls"] = False
        
        selectedOption = horizontalOption
    
    # palette settings
    elif verticalOption == 2:
        if horizontalOption == 0:
            inGameSettings["chosenPalette"] = "catppuccin-mocha"
        elif horizontalOption == 1:
            inGameSettings["chosenPalette"] = "nord"
        elif horizontalOption == 2:
            inGameSettings["chosenPalette"] = "old-school"
        elif horizontalOption == 3:
            inGameSettings["chosenPalette"] = "rose-pine-dawn"
        
        selectedOption = horizontalOption
    
    # write all changes to inGameSettings to settings.json file.
    with open('settings.json', mode = 'w') as file:
        file.write(json.dumps(inGameSettings, indent = 4))
    return selectedOption
    

def settings(palette, snake_speed, walls, highlightColor, bgColor, fgColor, foodColor, buttonColor):
    verticalOption = 0
    horizontalOption = 0
    # initialize selected options from settings parameters (palette, snake_speed, walls)
    selectedOption = 0
    
    # this allows the correct options to be highlighted as selected upon opening the settings menu.
    if snake_speed == 10:
        selectedDifficulty = 0
    elif snake_speed == 20:
        selectedDifficulty = 1
    elif snake_speed == 30:
        selectedDifficulty = 2
        
    if walls == True:
        selectedWalls = 0
    else:
        selectedWalls = 1
    
    if palette == "catppuccin-mocha":
        selectedPalette = 0
    elif palette == "nord":
        selectedPalette = 1
    elif palette == "old-school":
        selectedPalette = 2
    elif palette == "rose-pine-dawn":
        selectedPalette = 3
    
    while True:        
        game_window.fill(bgColor)
        settings = [["Easy", "Medium", "Hard"], ["On", "Off"], ["Catppuccin Mocha", "Nord", "Old School", "Rose Pine Dawn"]]
        
        # accept input from player to navigate menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    verticalOption += 1
                    horizontalOption = 0
                elif event.key == pygame.K_w or event.key == pygame.K_UP:
                    verticalOption -= 1
                    horizontalOption = 0
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    horizontalOption -= 1
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    horizontalOption += 1
                elif event.key == pygame.K_RETURN:
                    # set the temp variable selectedOption to the return value of settingsSelector. the function returns the index of the option that the user chose.
                    selectedOption = settingsSelector(horizontalOption, verticalOption)
                    # this updates the square that indicates that an option is selected as soon as the user selects it.
                    if verticalOption == 0:
                        selectedDifficulty = selectedOption
                    elif verticalOption == 1:
                        selectedWalls = selectedOption
                    elif verticalOption == 2:
                        selectedPalette = selectedOption
                elif event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                    return

        # if option is less than 0, select the last option. if option is greater than 2, select the first option
        if verticalOption > len(settings) - 1:
            verticalOption = 0
        elif verticalOption < 0:
            verticalOption = len(settings) - 1
        
        if horizontalOption > len(settings[verticalOption]) - 1:
            horizontalOption = 0
        elif horizontalOption < 0:
            horizontalOption = len(settings[verticalOption]) - 1
            
        activeButton = settings[verticalOption][horizontalOption]
                
        # size + coordinates
        buttonWidth = 100
        buttonHeight = 50
        buttonListXCoordinate = 20
        difficultyListYCoordinate = 80
        wallsListYCoordinate = 180
        paletteListYCoordinate = 280
        
        for count, difficulty in enumerate(settings[0]):
            if activeButton == difficulty:
                pygame.draw.rect(game_window, highlightColor, pygame.Rect(buttonListXCoordinate, difficultyListYCoordinate, buttonWidth, buttonHeight))
            else:
                pygame.draw.rect(game_window, buttonColor, pygame.Rect(buttonListXCoordinate, difficultyListYCoordinate, buttonWidth, buttonHeight))
            
            button_surface = textFont.render(difficulty, True, fgColor)
            button_label = button_surface.get_rect()
            button_label.midtop = buttonListXCoordinate + 50, difficultyListYCoordinate + 15
            
            # render the red square if this setting is the one chosen
            if count == selectedDifficulty:
                button_label.midtop = buttonListXCoordinate + 60, difficultyListYCoordinate + 15
                pygame.draw.rect(game_window, foodColor, pygame.Rect(buttonListXCoordinate + 10, difficultyListYCoordinate + 20, 10, 10))
                
            game_window.blit(button_surface, button_label)
            
            buttonListXCoordinate += 120
        
        buttonListXCoordinate = 20
        
        for count, wallsButton in enumerate(settings[1]):
            if activeButton == wallsButton:
                pygame.draw.rect(game_window, highlightColor, pygame.Rect(buttonListXCoordinate, wallsListYCoordinate, buttonWidth, buttonHeight))
            else:
                pygame.draw.rect(game_window, buttonColor, pygame.Rect(buttonListXCoordinate, wallsListYCoordinate, buttonWidth, buttonHeight))
            
            button_surface = textFont.render(wallsButton, True, fgColor)
            button_label = button_surface.get_rect()
            button_label.midtop = buttonListXCoordinate + 50, wallsListYCoordinate + 15
            
            if count == selectedWalls:
                button_label.midtop = buttonListXCoordinate + 60, wallsListYCoordinate + 15
                pygame.draw.rect(game_window, foodColor, pygame.Rect(buttonListXCoordinate + 10, wallsListYCoordinate + 20, 10, 10))
            
            game_window.blit(button_surface, button_label)
            
            buttonListXCoordinate += 120
        
        buttonListXCoordinate = 20
        
        buttonWidth = 200
        for count, palette in enumerate(settings[2]):
            if count != 0 and count % 2 == 0:
                paletteListYCoordinate += 60
                buttonListXCoordinate = 20
            
            if activeButton == palette:
                pygame.draw.rect(game_window, highlightColor, pygame.Rect(buttonListXCoordinate, paletteListYCoordinate, buttonWidth, buttonHeight))
            else:
                pygame.draw.rect(game_window, buttonColor, pygame.Rect(buttonListXCoordinate, paletteListYCoordinate, buttonWidth, buttonHeight))
            
            button_surface = textFont.render(palette, True, fgColor)
            button_label = button_surface.get_rect()
            button_label.midtop = buttonListXCoordinate + 100, paletteListYCoordinate + 15
            
            if count == selectedPalette:
                button_label.midtop = buttonListXCoordinate + 110, paletteListYCoordinate + 15
                pygame.draw.rect(game_window, foodColor, pygame.Rect(buttonListXCoordinate + 10, paletteListYCoordinate + 20, 10, 10))
            
            game_window.blit(button_surface, button_label)
            
            buttonListXCoordinate += 240
        
        # render category names
        difficultyTitle_surface = textFont.render('Difficulty', True, foodColor)
        difficultyTitle_rect = difficultyTitle_surface.get_rect()
        difficultyTitle_rect.midleft = (20, 60)
        
        wallsTitle_surface = textFont.render('Walls', True, foodColor)
        wallsTitle_rect = wallsTitle_surface.get_rect()
        wallsTitle_rect.midleft = (20, 160)
        
        colorPaletteTitle_surface = textFont.render('Color Palette (takes effect after leaving settings)', True, foodColor)
        colorPaletteTitle_rect = colorPaletteTitle_surface.get_rect()
        colorPaletteTitle_rect.midleft = (20, 260)
        
        game_window.blit(difficultyTitle_surface, difficultyTitle_rect)
        game_window.blit(wallsTitle_surface, wallsTitle_rect)
        game_window.blit(colorPaletteTitle_surface, colorPaletteTitle_rect)
        
        # render instructions
        instruction_surface = textFont.render('Navigate between categories with W and S.', True, fgColor)
        instruction2_surface = textFont.render('Choose an option with A and D.', True, fgColor)
        instruction3_surface = textFont.render('Select an option with ENTER.', True, fgColor)
        instruction4_surface = textFont.render('Press ESCAPE to go back to the main menu.', True, fgColor)        
        
        instruction_rect = instruction_surface.get_rect()
        instruction2_rect = instruction2_surface.get_rect()
        instruction3_rect = instruction3_surface.get_rect()
        instruction4_rect = instruction4_surface.get_rect()
        
        instruction_rect.center = (window_x / 2, window_y - 80)
        instruction2_rect.center = (window_x / 2, window_y - 60)
        instruction3_rect.center = (window_x / 2, window_y - 40)
        instruction4_rect.center = (window_x / 2, 20)
        
        game_window.blit(instruction_surface, instruction_rect)
        game_window.blit(instruction2_surface, instruction2_rect)
        game_window.blit(instruction3_surface, instruction3_rect)
        game_window.blit(instruction4_surface, instruction4_rect)
        
        pygame.display.update()
        fps.tick(60)
        
# put menu code here
def menu():
    palette = inGameSettings["chosenPalette"]
    colors = inGameSettings["colorPalette"][palette]

    bgColor = pygame.Color(colors["bgColor"])
    fgColor = pygame.Color(colors["fgColor"])
    buttonColor = pygame.Color(colors["buttonColor"])
    highlightColor = pygame.Color(colors["highlightColor"])
    gameOverColor = pygame.Color(colors["gameOverColor"])
    foodColor = pygame.Color(colors["foodColor"])
    snakeColor = pygame.Color(colors["snakeColor"])

    snake_speed = inGameSettings["difficulty"]
    walls = inGameSettings["walls"]
    
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
        # update the variables when the user changes settings
        palette = inGameSettings["chosenPalette"]
        colors = inGameSettings["colorPalette"][palette]

        bgColor = pygame.Color(colors["bgColor"])
        fgColor = pygame.Color(colors["fgColor"])
        buttonColor = pygame.Color(colors["buttonColor"])
        highlightColor = pygame.Color(colors["highlightColor"])
        gameOverColor = pygame.Color(colors["gameOverColor"])
        foodColor = pygame.Color(colors["foodColor"])
        snakeColor = pygame.Color(colors["snakeColor"])

        snake_speed = inGameSettings["difficulty"]
        walls = inGameSettings["walls"]

        game_window.fill(bgColor)
        
        title = headerFont.render(titleString, True, fgColor)
        game_window.blit(title, ((window_x / 2) - 90, 100))
        
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
                    menuSelector(option, palette, snake_speed, walls, highlightColor, bgColor, fgColor, foodColor, snakeColor, gameOverColor, buttonColor)
        
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
            else:
                pygame.draw.rect(game_window, buttonColor, pygame.Rect(buttonListXCoordinate, buttonListYCoordinate, buttonWidth, buttonHeight))
            
            button_surface = textFont.render(button, True, fgColor)
            button_label = button_surface.get_rect()
            button_label.midtop = (window_x / 2), buttonListYCoordinate + 20
            game_window.blit(button_surface, button_label)
        
        game_window.blit(title, ((window_x / 2) - 90, 100))
        pygame.display.update()
        fps.tick(60)

menu()