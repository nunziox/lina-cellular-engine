#!/usr/bin/env python

__author__     = "Nunzio Meli"
__copyright__  = "Copyright 2015, The GOL Project"
__credits__    = ["Nunzio Meli"]
__license__    = "GPL"
__version__    = "1.0"
__maintainer__ = "Nunzio Meli"
__email__      = "nunziomeli5@gmail.com"
__status__     = "Production"

import pygame
import time
import random
import copy

#
# Constaints
#
SCALE         = 40                    # PIXELS SCALE FACTOR
SCREEN_WIDTH  = 500                   # SCREEN WIDTH
SCREEN_HEIGHT = 500                   # SCREEN HEIGHT
WMAX          = SCREEN_WIDTH / SCALE  # SCALE CONVERSION X-AXE
HMAX          = SCREEN_HEIGHT / SCALE # SCALE CONVERSION Y-AXE
FPS           = 5                     # FRAME RATE
ALIVE         = 1                     # PIXEL STATE ALIVE
DEAD          = 0                     # PIXEL STATE DEAD

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
      wsum = mask[t][j]                       + \
             mask[t][k]                       + \
             mask[t][(j+1) % HMAX]            + \
             mask[(i+1) % WMAX][j]            + \
             mask[(i+1) % WMAX][(j+1) % HMAX] + \
             mask[(i+1) % WMAX][k]            + \
             mask[i][(j+1) % HMAX]            + \
             mask[i][k]
      if mask[i][j]   == 1 and wsum < 2:
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
  screen   = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
  surface  = pygame.Surface(screen.get_size())
  clock    = pygame.time.Clock()
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

#
# Main
#
if __name__ == "__main__":
  mask = [[0 for x in range(HMAX)] for x in range(WMAX)]
  go(mask)




