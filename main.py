import pygame, sys
import random

def reset_game():
    global game_lost, snake_length, snake_x, snake_y, snake_body, snake_movement, snake_head, powerup, timer, food_x, food_y, consumable_x, consumable_y, consumable_num, counter, started
    # start button sprite on screen
    screen.blit(start_button, (285, 220))

    # get mouse position
    mouse = pygame.mouse.get_pos()

    # if the mouse clicks the start button, reset the game variables and start the game
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and 285 < mouse[0] < 515 and 220 < mouse[1] < 310:
            game_lost = False
            snake_length = 3
            snake_x, snake_y = 7, 8
            snake_body = [(6,8),(5,8),(4,8)]
            snake_movement = 2
            snake_head = pygame.transform.scale(pygame.image.load("snakepng/snakeright.png"), (52,52))
            powerup = 1
            timer = False
            food_x, food_y = random.randint(0,15), random.randint(0,15)
            consumable_x, consumable_y = random.randint(0,15), random.randint(0,15)
            consumable_num = random.randint(0,1)
            counter = 30   
            started = True
    pygame.display.update()

# declare movement variable (0 = no movement, 1 = left, 2 = right, 3 = up, 4 = down)
# --> snake_movement = 2
# --> press = pygame.key.get_pressed()

# declare food position (randomly)
# --> food_x = random.randint(0,15)
# --> food_y = random.randint(0,15)

# declare consumable position (randomly)
# --> consumable_x = random.randint(0,15)
# --> consumable_y = random.randint(0,15)

# this determines which consumable will spawn on map
# --> consumable_num = random.randint(0,1)
# this changes the speed of the snake (1 means normal, 1.5 means slow, 0.75 means fast)
# --> powerup = 1

# declare snake variables
# --> snake_length = 3

# initial position of snake
# --> snake_x = 7
# --> snake_y = 8
# --> snake_body = [(6,8),(5,8),(4,8)]
# boolean to check if game is lost
# --> game_lost = False

# the powerup effect should be removed after 15 sec (counter = 15) and the consumable should respawn after 30 sec (counter = 0)
# --> counter = 30

# this variable controls whether the timer is active or not
# --> timer = False

# this function changes the snake direction and head sprite, which controls movement
def move_snake(direction, sprite):
    global snake_movement, snake_head
    snake_movement = direction
    snake_head = pygame.transform.scale(pygame.image.load(sprite), (52,52))

# set up pygame screen consisting of 64 squares 25 in length
pygame.init()
screen = pygame.display.set_mode((800, 800))

# start screen boolean (False means game hasn't started and start screen is displayed, True means game has started)
started = False

# create sprites
map =  pygame.transform.scale(pygame.image.load("snakepng/map.png"), (800,800))

food = pygame.transform.scale(pygame.image.load("snakepng/apple.png"), (50,50))

snake = pygame.transform.scale(pygame.image.load("snakepng/snakebody.png"), (52,52))

snake_head = pygame.transform.scale(pygame.image.load("snakepng/snakeright.png"), (52,52))

win = pygame.transform.scale(pygame.image.load("snakepng/win.png"), (800,800))

lose = pygame.transform.scale(pygame.image.load("snakepng/lose.png"), (800,800))

fast_food = pygame.transform.scale(pygame.image.load("snakepng/fast.png"), (50,50))

slow_food = pygame.transform.scale(pygame.image.load("snakepng/slow.png"), (50,50))

start_screen = pygame.transform.scale(pygame.image.load("snakepng/start.png"), (800,800))

start_button = pygame.transform.scale(pygame.image.load("snakepng/button.png"), (230,90))

# declare timer -- this controls consumable despawn timers and power up modifier using the following counter variable by starting a user event every second
pygame.time.set_timer(pygame.USEREVENT, 1000)

# while the game has not started...
while started == False:
    # display start screen and start button
    screen.blit(start_screen, (0,0))
    screen.blit(start_button, (285, 220))
    # check if the start button is pressed
    reset_game()

# while the game is not lost or won...
while started == True:

    # change speed depending on how long the snake is and if there is a powerup active
    v = int((183 - snake_length) * powerup)

    # set screen refresh time (adjusts speed)
    pygame.time.wait(v)

    # manages movement and consumable timers
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            # if w,a,s,d is pressed, change the snake direction accordingly
            # the snake cannot move in the opposite direction of its current movement
            if event.key == pygame.K_a and snake_movement != 2:
                # move left and change sprite direction to left
                move_snake(1, "snakepng/snakeleft.png")
                
            if event.key == pygame.K_d and snake_movement != 1:
                # move right and change sprite direction to right
                move_snake(2, "snakepng/snakeright.png")
                
            if event.key == pygame.K_w and snake_movement != 4:
                # move up and change sprite direction to up
                move_snake(3, "snakepng/snakeup.png")
                
            if event.key == pygame.K_s and snake_movement != 3:
                # move down and change sprite direction to down
                move_snake(4, "snakepng/snakedown.png")

            # if m is pressed, win the game (for showcase purposes)
            if event.key == pygame.K_m:
                snake_length = 64

        # decrease the timer every second (if active)
        if event.type == pygame.USEREVENT and timer:
            counter -= 1
            # if the timer reaches 15, remove the powerup effect
            if counter == 15:
                powerup = 1
            # if the timer reaches 0, respawn the consumable and reset the timer
            if counter == 0:
                timer = False
                consumable_x, consumable_y = random.randint(0,15), random.randint(0,15)
                consumable_y = random.randint(0,15)
                counter = 30
        
    # if snake is on the same tile as the food, move food to a new random tile and add to snake length, simulating the snake eating it // if the food spawns inside the snake, move it somewhere else
    if snake_x == food_x and snake_y == food_y:
        snake_length += 1
        food_x, food_y = random.randint(0,15), random.randint(0,15)
    while (food_x, food_y) in snake_body:
        food_x, food_y = random.randint(0,15), random.randint(0,15)

    # if snake is on the same tile as the consumable, move it off screen and give a power up // if the consumable spawns inside the snake or in food, move it somewhere else
    if snake_x == consumable_x and snake_y == consumable_y:
        if consumable_num == 0:
            powerup = 0.75
        else:
            powerup = 1.5
        timer = True
        consumable_x, consumable_y = 16, 16
        consumable_num = random.randint(0,1)
    while ((consumable_x, consumable_y) == (food_x, food_y)) or (consumable_x, consumable_y) in snake_body:
        consumable_x, consumable_y = random.randint(0,15), random.randint(0,15)
        
        
    # draw the map
    screen.blit(map, (0,0))

    # detect if snake is out of bounds, if so, player loses
    if snake_x < 0 or snake_x > 15 or snake_y < 0 or snake_y > 15:
        game_lost = True
    
    # draw snake
    screen.blit(snake_head, (snake_x*49.9, snake_y*49.9))

    for i in range(len(snake_body)):
        screen.blit(snake, (49.9*snake_body[i][0], 49.9*snake_body[i][1]))
        
    # check for collision with snake body
        if snake_x == snake_body[i][0] and snake_y == snake_body[i][1]:
            game_lost = True

    # move the rest of the snake body along with the head
    snake_body.insert(0,(snake_x,snake_y))

    # move snake depending on pressed key
    if snake_movement == 1:
        snake_x -= 1
    if snake_movement == 2:
        snake_x += 1
    if snake_movement == 3:
        snake_y -= 1
    if snake_movement == 4:
        snake_y += 1
    
    # if the snake is longer than it is supposed to be, make it the right length
    if len(snake_body) > snake_length:
        snake_body.pop(snake_length)

    # draw food
    screen.blit(food, (49.9*food_x, 49.9*food_y))

    # draw consumables
    if consumable_num == 0:
        screen.blit(fast_food, (49.9*consumable_x, 49.9*consumable_y))
        
    else:
        screen.blit(slow_food, (49.9*consumable_x, 49.9*consumable_y))
        
    
    # update screen
    pygame.display.update()

    # if the game is lost or won, display the corresponding screen and reset the game when the start button is pressed
    while game_lost == True or snake_length == 64:
        if game_lost == True:
            screen.blit(lose, (0,0))
        if snake_length == 64:
            screen.blit(win, (0,0))
        reset_game()
    

