import pygame, sys
import random

# set up pygame screen consisting of 64 squares 25 in length
pygame.init()
screen = pygame.display.set_mode((400, 400))

# declare movement booleans
left = False
right = False
up = False
down = False
press = pygame.key.get_pressed()

# declare food position (randomly)
food_x = random.randint(0,15)
food_y = random.randint(0,15)

# declare consumable position (randomly)
consumable_x = random.randint(0,15)
consumable_y = random.randint(0,15)

# declare snake variables
snake_length = 3

# initial position of snake
snake_x = 7
snake_y = 8
snake_body = [(6,8),(5,8),(4,8)]
game_lost = False

# create sprites
map =  pygame.transform.scale(pygame.image.load("snakepng/map.png"), (400,400))

food = pygame.transform.scale(pygame.image.load("snakepng/apple.png"), (25,25))

snake = pygame.transform.scale(pygame.image.load("snakepng/snakebody.png"), (26,26))

snake_head = pygame.transform.scale(pygame.image.load("snakepng/snakeright.png"), (26,26))

win = pygame.transform.scale(pygame.image.load("snakepng/win.png"), (400,400))

lose = pygame.transform.scale(pygame.image.load("snakepng/lose.png"), (400,400))

fast_food = pygame.transform.scale(pygame.image.load("snakepng/fast.png"), (25,25))

slow_food = pygame.transform.scale(pygame.image.load("snakepng/slow.png"), (25,25))\

# while the game is not lost or won...
while True:

    # change speed
    v = 183 - snake_length

    # set refresh time
    pygame.time.wait(v)

    # check for the player pressing any movement keys
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a and right == False:
                snake_head = pygame.transform.scale(pygame.image.load("snakepng/snakeleft.png"), (26,26))
                left = True
                right = False
                up = False
                down = False
            if event.key == pygame.K_d and left == False:
                snake_head = pygame.transform.scale(pygame.image.load("snakepng/snakeright.png"), (26,26))
                left = False
                right = True
                up = False
                down = False
            if event.key == pygame.K_w and down == False:
                snake_head = pygame.transform.scale(pygame.image.load("snakepng/snakeup.png"), (26,26))
                left = False
                right = False
                up = True
                down = False
            if event.key == pygame.K_s and up == False:
                snake_head = pygame.transform.scale(pygame.image.load("snakepng/snakedown.png"), (26,26))
                left = False
                right = False
                up = False
                down = True
        
    # if snake is on the same tile as the food, move food to a new random tile and add to snake length, simulating the snake eating it
    if snake_x == food_x and snake_y == food_y:
        snake_length += 1
        food_x = random.randint(0,15)
        food_y = random.randint(0,15)

    # if the food spawns inside the snake, move it somewhere else
    while (food_x, food_y) in snake_body:
        food_x = random.randint(0,15)
        food_y = random.randint(0,15)
        
    # draw the map
    screen.blit(map, (0,0))

    # detect if snake is out of bounds, if so, player loses
    if snake_x < 0 or snake_x > 15 or snake_y < 0 or snake_y > 15:
        game_lost = True
    
    # draw snake
    screen.blit(snake_head, (snake_x*24.95, snake_y*24.95))

    for i in range(len(snake_body)):
        screen.blit(snake, (24.95*snake_body[i][0], 24.95*snake_body[i][1]))

    # check for collision
    for i in range(len(snake_body)):
        if snake_x == snake_body[i][0] and snake_y == snake_body[i][1]:
            game_lost = True

    # move the rest of the snake body along with the head
    if left == True or right == True or up == True or down == True:
        snake_body.insert(0,(snake_x,snake_y))

    # move snake depending on pressed key
    if left == True:
        snake_x -= 1
    if right == True:
        snake_x += 1
    if up == True:
        snake_y -= 1
    if down == True:
        snake_y += 1
    
    # if the snake is longer than it is supposed to be, make it the right length
    if len(snake_body) > snake_length:
        snake_body.pop(snake_length)

    # draw food
    screen.blit(food, (24.95*food_x, 24.95*food_y))
    
    # update screen
    pygame.display.update()
        
    while snake_length == 64 or game_lost == True:
        # if the game is lost, display "you lost"
        if game_lost == True:
            screen.blit(lose, (0,0))

        # if the game is won, display "you won"
        if snake_length == 64:
            screen.blit(win, (0,0))

        # update screen
        pygame.display.update()

