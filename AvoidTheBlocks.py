import pygame
import time
import random

pygame.init()
display_width = 800
display_height = 600
ticks_per_sec=60

paused = False

img_width = 86
img_height = 110

blue = (7,3,160)
black=(0,0,0)
white=(255,255,255)

red = (255,0,0)
green=(0,255,0)

inactive_red = (150,0,0)
inactive_green = (0,150,0)

#Setting the display of the Game
gameDisplay=pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Let us Race')

#car for the race
car_img=pygame.image.load('race toy.png')

def car(x,y):
    gameDisplay.blit(car_img,(x,y))


def unpause():
	global paused 
	paused = False

def quit_game():
	pygame.quit()
	quit()

#game clock
clock=pygame.time.Clock()

#obstacles
def obstacles(ob_x,ob_y,ob_w,ob_h,color):
    pygame.draw.rect(gameDisplay,color,[ob_x,ob_y,ob_w,ob_h])
		
		
#text rendering
def text_objects(text,font,color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

	
#Creating an interactive button that senses mouse position
def make_button(text,x,y,w,h,active_color,inactive_color,action):
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	
	if x+w >= mouse[0] >= x and y+h >= mouse[1] >= y:
		pygame.draw.rect(gameDisplay, active_color, (x,y,w,h))
		if click[0] == 1:
			action()
	else:
		pygame.draw.rect(gameDisplay, inactive_color, (x,y,w,h))
	
	smallText = pygame.font.Font('freesansbold.ttf',20)
	textSurface, textRect = text_objects(text,smallText,black)
	textRect.center = ((x + w/2),(y + h/2))
	gameDisplay.blit(textSurface,textRect)
	

#display the text of the game.(GAME OVER).
def message_display(text):
    largeText=pygame.font.Font('freesansbold.ttf',115)
    textSurface,textRect = text_objects(text,largeText, red)
    textRect.center = ((display_width/2),(display_height/2));

    gameDisplay.blit(textSurface,textRect)
    pygame.display.update()

    time.sleep(2)

    game_loop()

def score(count):
    font = pygame.font.SysFont('comicsansms',25)
    text = font.render("Score: "+str(count),True,black)
    gameDisplay.blit(text,(0,0))

	
def game_over():
	largeText=pygame.font.SysFont('comicsansms',70)
	textSurface,textRect = text_objects("YOU CRASHED",largeText,blue)
	textRect.center = ((display_width/2),(display_height/2))
	gameDisplay.blit(textSurface,textRect)
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		
		make_button("RESTART!", 150,450,150,50, green, inactive_green, game_loop)
		make_button("QUIT!", 450,450,150,50, red, inactive_red, quit_game)
		
		pygame.display.update()
		clock.tick(15)

# Function That pauses the game
def pause():
	global paused
	gameDisplay.fill(white)
	largeText=pygame.font.SysFont('comicsansms',70)
	textSurface,textRect = text_objects("PAUSED",largeText,blue)
	textRect.center = ((display_width/2),(display_height/2))
	gameDisplay.blit(textSurface,textRect)
	while paused:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		
		make_button("CONTINUE!", 150,450,150,50, green, inactive_green, unpause)
		make_button("QUIT!", 450,450,150,50, red, inactive_red, quit_game)
		
		pygame.display.update()
		clock.tick(15)

	
def game_intro_screen():
	intro = True
	
	while intro:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		gameDisplay.fill(white)
		largeText=pygame.font.SysFont('comicsansms',60)
		textSurface,textRect = text_objects("How many can you AVOID?",largeText,blue)
		textRect.center = ((display_width/2),(display_height/2))
		gameDisplay.blit(textSurface,textRect)
		
		make_button("GO!", 150,450,100,50, green, inactive_green, game_loop)
		make_button("QUIT!", 450,450,100,50, red, inactive_red, quit_game)
		
		pygame.display.update()
		clock.tick(15)
		
def game_loop():
	x = display_width*0.45
	y = display_height*0.8
	x_change=0
	y_change=0
	#Game Exit Condition
	crashed= False

	ob_startx = random.randrange(0,display_width)
	ob_starty = -600
	ob_speed = 7
	ob_width = 100
	ob_height = 100

	speed=6
	count = 0
	global paused
	while not crashed:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					x_change = -5
				elif event.key == pygame.K_RIGHT:
					x_change = 5

				elif event.key == pygame.K_UP:
					y_change = -4
				elif event.key == pygame.K_DOWN:
					y_change = 4
				elif event.key == pygame.K_p :
					paused = True
					pause()
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					x_change=0

				if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
					y_change=0

		y=y+y_change
		x=x+x_change

		#Not letting the car exit the canvas
		if y >= display_height - img_height:
			y = display_height - img_height
		if y < 0:
			y=0
		if x >= display_width - 90 or x < 0:
			game_over()
			
		gameDisplay.fill(white)

		car(x,y)
		score(count)
		
		obstacles(ob_startx,ob_starty,ob_width,ob_height,green)
		ob_starty += ob_speed

		#crash condition for the objects
		if x + img_width >= ob_startx and x <= ob_startx + ob_width and y <= ob_starty + ob_height and y + img_height>= ob_starty:
			game_over()
			

		if ob_starty > display_height:
			ob_starty = 0 - ob_height
			ob_startx = random.randrange(0,display_width)
			ob_speed =  speed + (count/5) #random.randrange(4,7)
			count=count+1
		
		
		pygame.display.update()
		clock.tick(ticks_per_sec)
	game_intro_screen()

game_intro_screen()
game_loop()

pygame.quit()

quit()
