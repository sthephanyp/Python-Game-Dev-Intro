import pygame
import time
import random
#initialize the font module
pygame.font.init() 

#creating a window
WIDTH, HEIGHT = 610, 380
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

#caption for the window
pygame.display.set_caption("Python Intro Game")

#setting background
BG = pygame.image.load("/Python Intro Game/background.jpg")
#setting star image
STAR_CAR = pygame.image.load("/Python Intro Game/CAR.png")
STAR_CAR = pygame.transform.scale(STAR_CAR, (60, 60))  # ← Adjust size as needed
#setting player image
PLAYER_IMG = pygame.image.load("/Mushroom.png")
PLAYER_IMG = pygame.transform.scale(PLAYER_IMG, (40, 40))

#setting player image size
PLAYER_WIDTH, PLAYER_HEIGHT = 40, 40

#setting player VELOCITY
PLAYER_VEL = 5

#setting the star width
STAR_WIDTH = 10
STAR_HEIGHT = 10
STAR_VEL = 3

#setting font size and type
FONT = pygame.font.SysFont("comicsans", 20) 

#setting draw function
#blit = makeing a surface visible on the screen (0,0) is the top left corner of the screen
def draw_window(player,elapsed_time,stars):

    WIN.blit(BG, (0, 0))

    #f string embadding the elapsed time into the text
    time_text = FONT.render(f"Time: {round(elapsed_time)}s",1,"white")
    #display on the screen
    WIN.blit(time_text, (200,9))

    for star in stars:
        #draws the star rectangles
        #pygame.draw.rect(WIN,"yellow", star) 
        #draw them as images
        WIN.blit(STAR_CAR, (star.x, star.y))


    #pygame.draw.rect(WIN,"black", player) #draws the player rectangle
    WIN.blit(PLAYER_IMG,player)

    pygame.display.update()

#main game loop
def main():
    run = True

    player = pygame.Rect(550,200, PLAYER_WIDTH, PLAYER_HEIGHT)

    clock = pygame.time.Clock()

    #keep track of time
    start_time =time.time()
    elapsed_time = 0

    #projectiles setting up 
    star_add_increment =2000 #time in milliseconds
    start_count = 0 #tells us when we should add another star
    #lits of stars
    stars = [] 
    hit = False


    while run:

        #time how fast the game runs
        start_count += clock.tick(60)
        #number of seconds since we started the game
        elapsed_time = time.time() - start_time

        if start_count >= star_add_increment:
            #add stars to the screen 
            for _ in range(3):
                star_y = random.randint(0, HEIGHT - STAR_CAR.get_height())  # anywhere vertically
                #star = pygame.Rect(0, star_y, STAR_WIDTH, STAR_HEIGHT)  # starts from left edge
                stars.append(pygame.Rect(0, star_y, STAR_CAR.get_width(), STAR_CAR.get_height()))



            star_add_increment = max(200,star_add_increment - 50) 
            start_count = 0

        #checking if user clicked th x button to close the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        #to grab which key has been pressed
        keys = pygame.key.get_pressed()  
        #code for the left key 
        #using y because the y axis is inverted in pygame
        #if you wanted to move left and irght use x axis
        #adding conidtional so the player doesnt go off the screen
        if keys[pygame.K_DOWN] and (player.y-32) - PLAYER_VEL >= 0:
            player.y += PLAYER_VEL
        if keys[pygame.K_UP]  and (player.y+32) + PLAYER_VEL + player.height <= HEIGHT:
            player.y -= PLAYER_VEL

        #moving the stars down the screen
        #making a copy of the stars list so we can modify it while iterating over it
        for star in stars[:]:
            star.x += STAR_VEL  # move right
            if star.x > WIDTH:  # if it goes off screen, remove it
                stars.remove(star)
            elif star.x + star.height >= player.x and star.colliderect(player):
                stars.remove(star)
                hit = True
                break

        #if the player has been hit by a star
        if hit:
            #display the game over text
            game_over_text = FONT.render("Game Over!",1,"red")
            #drawing the text on the screen
            WIN.blit(game_over_text,(WIDTH//2 - 50, HEIGHT//2 - 10))
            pygame.display.update()
            #freeze the game for 4 seconds so the player can see the game over text
            pygame.time.sleep(10000)
            break

        draw_window(player,elapsed_time,stars)

    pygame.quit()

if __name__ == "__main__":

    main()
