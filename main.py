import pygame
import time
import random
import copy



SCALE = 40

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

WMAX = SCREEN_WIDTH/SCALE
HMAX = SCREEN_HEIGHT/SCALE

FPS = 5

ALIVE = 1
DEAD = 0

def render(screen, surface, mask):
	for i in range(WMAX):
        	for j in range(HMAX):
                	color = (0,0,0) if mask[i][j] == 0 else (255,255,255)
                        pygame.draw.rect(surface, color, pygame.Rect(i*SCALE,j*SCALE,i*SCALE+SCALE,j*SCALE+SCALE))
	screen.blit(surface, (0,0))

def next(mask):
        newmask = [[0 for x in range(HMAX)] for x in range(WMAX)] 
	for i in range(WMAX):
		for j in range(HMAX):
                        newmask[i][j] = 0
			t = WMAX -1 if i-1 == -1 else i-1
			k = HMAX -1 if j-1 == -1 else j-1
			wsum = mask[t][j] + \
			       mask[t][k] + \
                               mask[t][(j+1) % HMAX] + \
                               mask[(i+1) % WMAX][j] + \
                               mask[(i+1) % WMAX][(j+1) % HMAX] + \
                               mask[(i+1) % WMAX][k] + \
                               mask[i][(j+1) % HMAX] + \
                               mask[i][k]
                        if mask[i][j] == 1 and wsum < 2:
				newmask[i][j] = DEAD #DIE FOR UNDERPOPULATION
                        elif mask[i][j] == 1 and (wsum == 2 or wsum == 3):
				newmask[i][j] = ALIVE #LIVES TO THE NEXT GENERATION
			elif mask[i][j] == 1 and wsum > 3:
				newmask[i][j] = DEAD #DIE FOR OVERPOPULATION
                        elif mask[i][j] == 0 and wsum == 3:
				newmask[i][j] = ALIVE #REPRODUCTION
	return newmask

def go(mask):
	pygame.init()
	screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
	surface = pygame.Surface(screen.get_size())
	clock = pygame.time.Clock()
	mainLoop = True	
        index = 0
	while mainLoop:
		clock.tick(FPS) 
		render(screen, surface, mask)
                mask=next(mask)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
      				mainLoop = False
			elif event.type == pygame.KEYDOWN:
				mask = [[0 for x in range(HMAX)] for x in range(WMAX)]
                                if index == 0:
					setGliderPattern(mask,0,0)
				elif index == 1:
					setTrioPattern(mask,WMAX/2-2,HMAX/2-2)
				else:
					setExploderPattern(mask,WMAX/2-2,HMAX/2-2)
				index = (index + 1) % 3;	
		pygame.display.flip()


def setGliderPattern(mask,xoffset,yoffset):
  mask[1+xoffset][0+yoffset] = ALIVE
  mask[2+xoffset][1+yoffset] = ALIVE
  mask[0+xoffset][2+yoffset] = ALIVE
  mask[1+xoffset][2+yoffset] = ALIVE
  mask[2+xoffset][2+yoffset] = ALIVE


def setVerticalLinePattern(mask,xoffset,yoffset):
  mask[1+xoffset][1+yoffset] = ALIVE
  mask[1+xoffset][2+yoffset] = ALIVE
  mask[1+xoffset][3+yoffset] = ALIVE

def setTrioPattern(mask, xoffset,yoffset):
  mask[1+xoffset][0+yoffset] = ALIVE
  mask[0+xoffset][1+yoffset] = ALIVE
  mask[1+xoffset][1+yoffset] = ALIVE
  mask[2+xoffset][1+yoffset] = ALIVE


def setExploderPattern(mask, xoffset, yoffset):
  mask[0+yoffset][0+xoffset] = ALIVE
  mask[0+yoffset][1+xoffset] = ALIVE
  mask[0+yoffset][2+xoffset] = ALIVE
  mask[0+yoffset][3+xoffset] = ALIVE
  mask[0+yoffset][4+xoffset] = ALIVE
  mask[2+yoffset][0+xoffset] = ALIVE
  mask[2+yoffset][4+xoffset] = ALIVE
  mask[4+yoffset][0+xoffset] = ALIVE
  mask[4+yoffset][1+xoffset] = ALIVE
  mask[4+yoffset][2+xoffset] = ALIVE
  mask[4+yoffset][3+xoffset] = ALIVE
  mask[4+yoffset][4+xoffset] = ALIVE
 




if __name__ == "__main__":
	mask = [[0 for x in range(HMAX)] for x in range(WMAX)]  


        	
	#for x in range(5):
        #	xoffset = random.randint(0,WMAX-5)
	#	yoffset = random.randint(0,HMAX-5)
	#        r = random.randint(0,2)
        #        if r==1:
#			setVerticalLinePattern(mask,xoffset,yoffset)
#                elif r==2:
#			setGliderPattern(mask,xoffset,yoffset)
#		else:
#			setTrioPattern(mask,xoffset,yoffset)
	go(mask)




