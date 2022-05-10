import pygame
import random

pygame.init()

#program variables
screen = pygame.display.set_mode((720, 1134))
width, height = screen.get_size()
font = pygame.font.SysFont("", 80)
#game variables
start = False
dead = False
score = 0
tc = 3
to = 10
moon = 150
SPEED = 2
GRAVITY = 1
BRRR = 1

#display score
def display_score():
	sc = font.render(str(int(score)), True, (255, 255, 255))
	screen.blit(sc, (width / 2 - sc.get_width() / 2, 100))
#on-dead display
def deads():
	global dead
	dead = True
	t = f"XD"
	w, h = font.size(t)
	text = font.render(t, True, (255, 255, 255))
	screen.blit(text, (width * 0.5 - w / 2, height * 0.5))
def display(text):
	msg = font.render(text, True, (255, 255, 255))
	screen.blit(msg, (width * 0.5, height * 0.5))
#add Pipe object to the pipes list
def add_pipes():
	y_space = bird.r * 10
	Pipe.cur_space = random.randint(0, height - y_space) #randomize current top pipe height
	pipes.append(Pipe(0, Pipe.cur_space))
	pipes.append(Pipe(Pipe.cur_space + y_space, height - Pipe.cur_space - y_space))
def add_trees(n):
	for i in range(n):
		h = random.uniform(100, height - moon * 3)
		trees.append(Tree(width / n * i, h))

class Bird():
	def __init__(self, x, y, r):
		self.x = x
		self.y = y
		self.r = r
		self.yvel = 0
		self.yacc = GRAVITY
	def draw(self):
		pygame.draw.circle(screen, (255, 255, 0), (self.x, self.y), self.r)
	def move(self):
		#check if the bird is on top
		if self.y - self.r <= 0:
			self.yvel = 5
		self.y += self.yvel
		self.yvel += self.yacc
		self.yvel *= 0.9 #air resistance
	def jump(self):
		self.yvel -= self.r
class Floor():
	def draw(self):
		pygame.draw.line(screen, (0, 0, 0), (0, height), (width, height), 10)
	def check(self, obj):
		if obj.y + obj.r >= height:
			deads()
class Pipe():
	cur_space = 0 #height of the current top pipe
	def __init__(self, pos, h):
		self.pos = pos
		self.w = 100
		self.h = h
		self.x = width
		self.y = self.pos
		self.passed = False
	def draw(self):
		pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, self.w, self.h))
	def check(self, obj):
		global score
		#check pipe and bird x-collision
		if obj.x + obj.r >= self.x and obj.x - obj.r <= self.x + self.w:
			
			#check pipe and bird y-collision
			if obj.y + obj.r >= self.y and obj.y - obj.r <= self.y + self.h:
				deads()
		
		#check the bird if passed the pipe
		if not self.passed:
			if obj.x >= self.x + self.w:
				self.passed = True
				score += 0.5
class Tree():
	def __init__(self, x, h):
		self.w = 200
		self.h = h
		self.x = x + to
		self.y = height - self.h
	def draw(self):
		pygame.draw.rect(screen, (150, 150, 150), (self.x, self.y, self.w, self.h))

#objects variables
bird = Bird(170, height * 0.5, 30)
floor = Floor()
pipes = []
trees = []

add_pipes()
add_trees(tc)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			start = True
			bird.jump()
			if dead:
				start = False
				dead = False
				score = 0
				bird = Bird(170, height * 0.5, 30)
				pipes = []
				trees = []
				add_pipes()
				add_trees(tc)
	
	#add a new pipe
	if pipes[-1].x <= width - pipes[-1].w * 5:
		add_pipes()
	#remove a pipe
	if pipes[0].x + pipes[0].w <= 0:
		del pipes[0]
	
	screen.fill((12, 20, 69, 10))
	pygame.draw.circle(screen, (230, 230, 230), (width - moon - 50, moon + 50), moon)
	
	for tree in trees:
		tree.draw()
		tree.x -= 0 if dead else SPEED / 1.5 + BRRR
		if tree.x + tree.w <= 0:
			tree.x = width
			tree.h = random.uniform(100, height - moon * 3)
			tree.y = height - tree.h
	
	bird.draw()
	floor.draw()
	
	if start:
		for pipe in pipes:
			pipe.draw()
			pipe.x -= 0 if dead else SPEED + BRRR
		if not dead:
			bird.move()
	
	# check and display
	if start:
		for pipe in pipes:
			pipe.check(bird)
		BRRR += 0.0005
	floor.check(bird)
	display_score()
	
	pygame.display.flip()
