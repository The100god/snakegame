import pygame, asyncio
import random
import os

pygame.mixer.init() #Pygame music library

pygame.init()

#Colors 
white = (255, 255, 255)
red= (255, 0, 0)
black = (0, 0, 0)
green = (0, 255, 0)
yellow=(255, 255, 0)

# creating display window for game
screen_width = 800
screen_height = 700
gameWindow = pygame.display.set_mode((screen_width, screen_height))

front = pygame.image.load("front.jpg")
front = pygame.transform.scale(front, (screen_width, screen_height)).convert_alpha()

death = pygame.image.load("gameover.jpg")
death = pygame.transform.scale(death, (screen_width, screen_height)).convert_alpha()

#background Image
bgimg = pygame.image.load("snakebg.jpg")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()


pygame.display.set_caption("Snake")  # Setting caption for our game.
pygame.display.update()

font = pygame.font.SysFont(None, 55) # declare font and font size (55)
clock = pygame.time.Clock() # For updating our game with reference of time



# Displaying Score on screen
def display_on_screen(text, color,x,y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text,[x,y]) # For updating screen

def plot_snake(gameWindow, black, snake_list, snake_size):
    for x, y in snake_list:
        pygame.draw.rect(gameWindow, black, [x, y, snake_size, snake_size])

#Creating Welcome Screen
async def welcome():
    exit_game = False
    while not exit_game:
        fps = 60 # Frame per second  
        gameWindow.blit(front, (0, 0))
        # gameWindow.fill(green)
        # display_on_screen("Welcome to Snake Game", red, (screen_width/2)-220, screen_height/2)
        # display_on_screen("Press Enter To Play", red, (screen_width/2)-180, (screen_height/2)+50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.load("bg.mp3") #for loading Pygame music library
                    pygame.mixer.music.play() 
                    gameloop()
        pygame.display.update()
        await asyncio.sleep(0)    
        clock.tick(fps)
    pygame.quit()  # for quiting pygame
    quit()  # for quiting python
         

# creating a game loop
def gameloop(): 
    # Game specific variables
    exit_game = False  # for exiting game: initially False
    game_over = False  # when game is over: initially False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    init_velocity = 2
    snake_size = 10
    food_x = random.randint(10, screen_width/2)
    food_y = random.randint(10, screen_height/2)
    fps = 60 # Frame per second
    score=0
    snake_list =[] 
    snake_length = 1
    # Check if high score file exist or not
    if(not os.path.exists("highScore.txt")):
        with open("highScore.txt","w") as f:
            f.write("0")
    with open("highScore.txt", "r") as f:
        high_score = f.read()
    
    while not exit_game:
        if game_over:
            
            with open("highScore.txt", "w") as f:
                f.write(str(high_score))
            gameWindow.blit(death, (0, 0))
            # display_on_screen("Game Over! please Enter To Continue", red, (screen_width/2)-350, screen_height/2)
            
            for event in pygame.event.get(): #Loop for handling every event in our game window
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        asyncio.run(welcome())
        else:
            for event in pygame.event.get(): #Loop for handling every event in our game window
                if event.type == pygame.QUIT:
                    exit_game = True
            
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_DOWN:
                        velocity_x = 0
                        velocity_y = init_velocity
                    
                    # adding cheat code
                    if event.key == pygame.K_q:
                        score+=10
            
            snake_x += velocity_x
            snake_y += velocity_y
            
            if abs(snake_x- food_x)<6 and abs(snake_y- food_y)<6:
                pygame.mixer.music.load("beep.mp3") #for loading Pygame music library
                pygame.mixer.music.play()
                score+=10
                snake_length+=5
                food_x = random.randint(10, screen_width/2)
                food_y = random.randint(10, screen_height/2)
                if score>int(high_score):
                    high_score = score
                if score % 100 ==0:
                    init_velocity +=2
                
            head=[]
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)
            if len(snake_list)>snake_length:
                del snake_list[0]
                
            if head in snake_list[:-1]:
                game_over = True
                pygame.mixer.music.load("gameover.mp3") #for loading Pygame music library
                pygame.mixer.music.play()
                      
            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over = True
                pygame.mixer.music.load("gameover.mp3") #for loading Pygame music library
                pygame.mixer.music.play()
            # gameWindow.fill(white)
            gameWindow.blit(bgimg, (0, 0))
            display_on_screen('Score: ' + str(score) + " High Score: " + str(high_score), yellow, 5, 5)  # Calling display_score
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size]) #Creating snake food
            pygame.draw.rect(gameWindow, black, [snake_x, snake_y, snake_size, snake_size])
            plot_snake(gameWindow, black,snake_list, snake_size)
        pygame.display.update()
        
        clock.tick(fps) # for creating frame per second    
    pygame.quit()  # for quiting pygame
    quit()  # for quiting python

asyncio.run(welcome())


