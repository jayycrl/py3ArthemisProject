# py3ArthemisProject
A Snake game made in Python for our first year Programming Logic &amp; Design class.

Demo: https://youtu.be/R4ywRMTeA7M

## About the game
Snake is a game where you control a snake, moving around the screen and eating food that randomly spawns. When the snake eats food, it grows longer and you get more points. The goal is to grow as long as possible without bumping into yourself or the walls around the playing field.
- Moving snake
- Randomly generated food
- Difficulty options
- Main menu
- Pause menu
- Enable/disable walls
- Scoring system
- Color palette switching

## Installation
1. Get the `pygame` module by running the following command: `python -m pip install -U pygame==2.3.0 --user`
2. Download the `snake.zip` file from the [releases page](https://github.com/jayycrl/py3ArthemisProject/releases/latest).

## Project Proposal
The project proposal can be found here: https://github.com/jayycrl/py3ArthemisProject/releases/tag/proposal

## IPO
| Input | Process | Output |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------- |
| User keyboard input | 1. Update the snake’s position, with the direction being influenced by the user’s input.                                                    | Graphical display of the game screen:   |
|                     | 2. Check if the snake collides with itself or a wall. End the game if so.                                                                   | - Food                                  |
|                     | 3. Check if the snake collides with food. Increase the snake’s length, get rid of the food if so, and generate new food at random position. | - Snake                                 |
|                     |                                                                                                                                             | - Score                                 |
|                     |                                                                                                                                             | - Game over message                     |

## Poster
![Python Snake Poster](https://user-images.githubusercontent.com/127172433/231917383-f16fee62-04f6-4de3-9db7-7f11590d3051.png)
