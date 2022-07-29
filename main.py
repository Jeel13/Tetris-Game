import pygame
import random

pygame.init()
SCREEN = WIDTH, HEIGHT = 400, 800    #Width and Height of the entire screen
win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)			#This command intialises the window screen of the game

#Declaring the size of each block and then making the rows and cols accordingly
CELLSIZE = 20
ROWS = (HEIGHT-120) // CELLSIZE
COLS = WIDTH // CELLSIZE

clock = pygame.time.Clock()
FPS = 24

#COLORS
BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,255,0)
WHITE = (255, 255, 255)
BLACK = (21, 24, 29)
GREY = (220,220,220)

#FONTS
font = pygame.font.Font('Fonts/Tetris Mania Type.ttf', 50)
font2 = pygame.font.SysFont('consolas', 20)
font3= pygame.font.Font('Fonts/Tetris Mania Type.ttf', 30)

#Images
BlueBox = pygame.image.load('Images/Blue.png')
GreenBox = pygame.image.load('Images/Green.png')
RedBox = pygame.image.load('Images/Red.png')
YellowBox = pygame.image.load('Images/Yellow.png')

Colors = {
	1 : BlueBox,
	2 : GreenBox,
	3 : RedBox,
	4 : YellowBox
}


#OBJECTS
class TETRIS:
	# matrix
	# 0   1   2   3
	# 4   5   6   7
	# 8   9   10  11
	# 12  13  14  15

	Shapes= {
		#This is the list of rotations for each shape
		'I' : [[1, 5, 9, 13],
			   [4, 5, 6, 7]],
        'Z' : [[4, 5, 9, 10],
			   [2, 6, 5, 9]],
        'S' : [[6, 7, 9, 10],
			   [1, 5, 6, 10]],
        'L' : [[1, 2, 5, 9],
			   [0, 4, 5, 6],
			   [1, 5, 9, 8],
			   [4, 5, 6, 10]],
        'J' : [[1, 2, 6, 10],
			   [5, 6, 7, 9],
			   [2, 6, 10, 11],
			   [3, 5, 6, 7]],
        'T' : [[1, 4, 5, 6],
			   [1, 4, 5, 9],
			   [4, 5, 6, 9],
			   [1, 5, 6, 9]],
        'O' : [[1, 2, 5, 6]]
	}
	ShapeType = ['I', 'Z', 'S', 'L', 'J', 'T', 'O']

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.type = random.choice(self.ShapeType)
		self.shape = self.Shapes[self.type]
		self.color = random.randint(1, 4)
		self.rotation = 0

	def image(self):		#This function returns the current rotation of the shape
		return self.shape[self.rotation]

	def rotate(self):
		self.rotation = (self.rotation + 1) % len(self.shape)

class Tetris:
	def __init__(self, rows, cols):
		self.rows = rows
		self.cols = cols
		self.score = 0
		self.level = 1
		self.board = [[0 for j in range(cols)] for i in range(rows)]
		self.next = None
		self.gameover = False
		self.new_figure()

	def new_figure(self):
		if not self.next:
			self.next = TETRIS(8, 0)	#This spawns a new shape
		self.figure = self.next
		self.next = TETRIS(8, 0)	#This provides the position for the next shape

	def intersects(self):		#This function checks for if the shape has reached the brim of the screen or not
		intersection = False
		for i in range(4):
			for j in range(4):
				if i * 4 + j in self.figure.image():
					if i + self.figure.y > self.rows - 1 or \
					   j + self.figure.x > self.cols - 1 or \
					   j + self.figure.x < 0 or \
					   self.board[i + self.figure.y][j + self.figure.x] > 0:
						intersection = True
		return intersection

	def remove_line(self):		#This function checks for if the line is full or not
		rerun = False
		for y in range(self.rows-1, 0, -1):
			is_full = True
			for x in range(0, self.cols):	#This loops through all the cols in that row to check if there are any blocks in it
				if self.board[y][x] == 0:
					is_full = False
			if is_full:
				del self.board[y]
				self.board.insert(0, [0 for i in range(self.cols)])		#Making the blocks empty again for all the columns of that row
				self.score += 1
				if self.score % 10 == 0:
					self.level += 1		#Increases the level if the intital score increases by 10
				rerun = True

		if rerun:		#If a row is removed than this function is run again to check if the newly formed board has the same situation or not
			self.remove_line()

	def lock(self):		#This function locks the position of the shape
		for i in range(4):
			for j in range(4):
				if i * 4 + j in self.figure.image():
					self.board[i + self.figure.y][j + self.figure.x] = self.figure.color
		self.remove_line()
		self.new_figure()
		if self.intersects():	#This checks for if the new incoming shape has any space to fall or not
			self.gameover = True

	def spacePress(self):			#This function is used to move the piece directly to the most bottom position possible
		while not self.intersects():
			self.figure.y += 1
		self.figure.y -= 1
		self.lock()

	def downPress(self):			#This function is used to move the piece in the downward position
		self.figure.y += 1
		if self.intersects():
			self.figure.y -= 1
			self.lock()

	def sidePress(self, dx):		#This funciton is used to move the piece in sideward position
		self.figure.x += dx
		if self.intersects():
			self.figure.x -= dx

	def rotate(self):			#This function is used to rotate the shape
		rotation = self.figure.rotation
		self.figure.rotate()
		if self.intersects():	#This checks for if the rotation is possible or not
			self.figure.rotation = rotation

def draw_grid(surface,rows,cols):
	for i in range(rows):
		pygame.draw.line(surface, GREY, (0, CELLSIZE*i), (WIDTH, CELLSIZE*i))
		for j in range(cols):
			pygame.draw.line(surface, GREY, (CELLSIZE*j, 0), (CELLSIZE*j, HEIGHT-120))

#Initial conditions
counter = 0
move_down = False
valid_space = True

#Establishing the board and starting the game
tetris = Tetris(ROWS, COLS)
running = True

while running:
	win.fill(WHITE)			#This command fills the whole window with a specific colour
	draw_grid(win,ROWS,COLS)
	counter += 1
	if counter >= 10000:
		counter = 0

	if valid_space:
		if counter % (FPS // (tetris.level * 2)) == 0 or move_down:
			if not tetris.gameover:			#This condition checks whether the game is still running or not
				tetris.downPress()

	#EVENT HANDLING
	for event in pygame.event.get():	#This will get the current event happening
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if valid_space and not tetris.gameover:
				#Different events of left, right, up, down and space
				if event.key == pygame.K_LEFT:
					tetris.sidePress(-1)

				if event.key == pygame.K_RIGHT:
					tetris.sidePress(1)

				if event.key == pygame.K_UP:
					tetris.rotate()

				if event.key == pygame.K_DOWN:
					move_down = True

				if event.key == pygame.K_SPACE:
					tetris.spacePress()

			if event.key == pygame.K_r:		#It resets the whole game
				tetris.__init__(ROWS, COLS)

			if event.key == pygame.K_p:		#It pauses the whole game
				valid_space = not valid_space

			if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:		#It quits the whole game
				running = False

		if event.type == pygame.KEYUP:		#This basically is used to continuously move the piece if the down button is kept pressed
			if event.key == pygame.K_DOWN:
				move_down = False


	for x in range(ROWS):
		for y in range(COLS):
			if tetris.board[x][y] > 0:
				val = tetris.board[x][y]
				img = Colors[val]
				win.blit(img, (y*CELLSIZE, x*CELLSIZE))
				pygame.draw.rect(win, WHITE, (y*CELLSIZE, x*CELLSIZE,
									CELLSIZE, CELLSIZE), 1)

	if tetris.figure:
		for i in range(4):
			for j in range(4):
				if i * 4 + j in tetris.figure.image():
					img = Colors[tetris.figure.color]
					x = CELLSIZE * (tetris.figure.x + j)
					y = CELLSIZE * (tetris.figure.y + i)
					win.blit(img, (x, y))
					pygame.draw.rect(win, WHITE, (x, y, CELLSIZE, CELLSIZE), 1)


	#This handles the scenario when the game is over
	if tetris.gameover:
		rect = pygame.Rect((50, 200, WIDTH-100, HEIGHT-500))	#A new rectangle for showing the message over game
		pygame.draw.rect(win, BLACK, rect)
		pygame.draw.rect(win, BLUE, rect, 5)

		over = font3.render('Game Over', True, WHITE)
		msg1 = font2.render('Press r to restart', True, GREEN)
		msg2 = font2.render('Press q to quit', True, RED)

		win.blit(over, (rect.centerx-over.get_width()/2, rect.y + 80))
		win.blit(msg1, (rect.centerx-msg1.get_width()/2, rect.y + 150))
		win.blit(msg2, (rect.centerx-msg2.get_width()/2, rect.y + 180))

	#This handles the whole HUD of the game
	pygame.draw.rect(win, BLACK, (0, HEIGHT-120, WIDTH, 120))	#This rectangle holds the image, title and score

	#This renders the image on the bottom left of the next figure
	if tetris.next:
		for i in range(4):
			for j in range(4):
				if i * 4 + j in tetris.next.image():
					img = Colors[tetris.next.color]
					x = CELLSIZE * (tetris.next.x + j - 4)-50
					y = HEIGHT - 100 + CELLSIZE * (tetris.next.y + i)
					win.blit(img, (x, y))

	showName = font3.render(f'Tetris', True, WHITE)			#This renders the title
	win.blit(showName,(190-showName.get_width()//2,HEIGHT-80))

	#This renders the current score and level
	showScore = font.render(f'{tetris.score}', True, WHITE)
	showLevel = font2.render(f'Level : {tetris.level}', True, WHITE)
	win.blit(showScore, (320-showScore.get_width()//2, HEIGHT-110))
	win.blit(showLevel, (320-showLevel.get_width()//2, HEIGHT-50))

	pygame.draw.rect(win, RED, (0, 0, WIDTH, HEIGHT-120), 5)		#This is the upper rectangel with border 5
	clock.tick(FPS)
	pygame.display.update()
pygame.quit()