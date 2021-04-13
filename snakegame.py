import pygame
import random
import os
pygame.init()

#colors define
white = (255,255,255)
red = (255,0,0)
black = (0,0,0)
green = (34,139,34)

screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height)) #creating window

pygame.display.set_caption("Snakegame")
pygame.display.update() # changesUpdation

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55) #creating global variable for using default system font - initializing font

def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x,y]) #blit() for updating screen

def plot_snake(gameWindow, color, snake_list, snake_size):
    for x,y in snake_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size]) #creating snake head

def welcome():
    exit_game = False
    while not exit_game: 
        gameWindow.fill(black)
        text_screen("WELCOME TO SNAKE WORLD!!!", green, 150, 250)
        text_screen("Press SPACE to Play!!!", green, 230, 290)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gameloop()

            pygame.display.update()
            clock.tick(60)  

#Creating game loop, handling all events
def gameloop():
    #game specific variables
    exit_game = False
    game_over = False
    snake_x = 45 #position
    snake_y = 55 #position
    velocity_x = 0
    velocity_y = 0
    food_x = random.randint(20, screen_width/2) #plotting food for any random number
    food_y = random.randint(20, screen_height/2)
    score = 0
    init_velocity = 8
    snake_size = 30
    fps = 60
    snake_list = []
    snake_length = 1
    #check if highScore file exits
    if(not os.path.exists("highScore.txt")):
        with open("highScore.txt", "w") as f:
            f.write("0")

    with open("highScore.txt", "r") as f:
        highScore = f.read()

    #loop
    while not exit_game:
        if game_over:
            with open("highScore.txt", "w") as f:
               f.write(str(highScore))
            gameWindow.fill(white)
            text_screen("GAME OVER!!! Press enter to Continue", red, 100, 250)

            for event in pygame.event.get():
                if event.type== pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN: #if you press enter key game will restart
                        welcome()

        else:
            for event in pygame.event.get():
                if event.type== pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity  
                        velocity_y = 0 #for avoiding moving digonal if x=10 then y should be 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = - init_velocity   
                        velocity_y = 0 

                    if event.key == pygame.K_UP:
                        velocity_y = - init_velocity    
                        velocity_x = 0   

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity 
                        velocity_x = 0   

                    if event.key == pygame.K_q: #cheatCode
                        score +=10    

            snake_x = snake_x + velocity_x    
            snake_y = snake_y + velocity_y      

            if abs(snake_x - food_x)<8 and abs(snake_y - food_y) < 8: #eating food
                score += 10
                
                food_x = random.randint(20, screen_width/2) #position changing food for any random number
                food_y = random.randint(20, screen_height/2)
                snake_length +=4

            if score>int(highScore):
               highScore = score


            gameWindow.fill(black)  
            text_screen("Score:"+ str(score)+ "  High Score:"+str(highScore), red, 5,5)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size]) #creating snake food

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)

            if len(snake_list)>snake_length:
                del snake_list[0]

            if head in snake_list[:-1]: #handling movement of snake
                game_over == True    

            if snake_x<0 or snake_x> screen_width or snake_y<0 or snake_y> screen_height:
                game_over = True  

            # pygame.draw.rect(gameWindow, black, [snake_x, snake_y, snake_size, snake_size]) #creating snake head
            plot_snake(gameWindow, green, snake_list, snake_size)
        pygame.display.update()  
        clock.tick(fps) #frame
    pygame.quit()
    quit()    
welcome()
gameloop()