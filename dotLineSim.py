import pygame
import sys
import math
import random
from pygame import gfxdraw
pygame.init()

#CONSTANTS
WIDTH,HEIGHT = 1024,780
fps = 60
background_color = (42,42,44)
#end CONSTANTS
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Dot Line Simulation - Justin Stitt")
clock = pygame.time.Clock()

mouse_pos = [0,0]
vision_range = 100 # radius that mouse cursor can see dots/lines
dots = []
num_dots = 150



class Dot:
    def __init__(self):
        self.size = random.randint(5,25) # radius of dot
        self.pos = [random.randint(0,WIDTH - self.size),random.randint(0,HEIGHT - self.size)] # x , y position
        self.variance = 50 # how much to stray from original pos
        self.line_draw_range = vision_range * 1.15 # dots draw lines to other dots within 115% of vision range
        self.color = (255,255,255) # dot color
        self.n_pos = [self.pos[0] + random.randint(-self.variance,self.variance),self.pos[1] + random.randint(-self.variance,self.variance)]
        self.speed = 1
    def update(self):
        self.random_movement()
        self.connect_lines()
        self.render()

    def render(self):
        global mouse_pos
        s = pygame.Surface((self.size ,self.size ))
        opacity = 256 - (distance(self.pos[0],self.pos[1],mouse_pos[0],mouse_pos[1]) * 1.25)
        s.set_alpha(opacity)
        s.fill(background_color)
        pygame.draw.ellipse(s,(self.color),(0,0,self.size,self.size))
        screen.blit(s,(self.pos[0],self.pos[1]))
    def connect_lines(self):
        global dots
        for dot in dots:
            p_0 = self.pos[0]#8 bytes
            if( distance(self.pos[0],self.pos[1],dot.pos[0],dot.pos[1]) < self.line_draw_range and dot != self ):
                if(distance(self.pos[0],self.pos[1],mouse_pos[0],mouse_pos[1]) <= vision_range  ):
                    pygame.gfxdraw.line(screen,self.pos[0] + self.size//2,self.pos[1] + self.size//2,dot.pos[0] + dot.size//2,dot.pos[1] + dot.size//2,self.color)
    def random_movement(self):
        if(self.pos[0] > self.n_pos[0]):
            self.pos[0] -= self.speed
        elif(self.pos[0] < self.n_pos[0]):
            self.pos[0] += self.speed
        if(self.pos[1] > self.n_pos[1]):
            self.pos[1] -= self.speed
        elif(self.pos[1] < self.n_pos[1]):
            self.pos[1] += self.speed
        if (self.pos == self.n_pos):
            self.n_pos = [self.pos[0] + random.randint(-self.variance,self.variance),self.pos[1] + random.randint(-self.variance,self.variance)]

def update():
    global mouse_pos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    mouse_pos = pygame.mouse.get_pos()
    #print(mouse_pos)
    for dot in dots:
        dot.update()
def render():
    pass

def distance(x1,y1,x2,y2):
    """computes and returns the distance between two points"""
    return math.sqrt(  (x2-x1)**2 + (y2-y1)**2 )

for x in range(num_dots):
    dots.append(Dot())


while True:
    screen.fill(background_color)
    update()
    render()
    pygame.display.flip()
    clock.tick(fps)
