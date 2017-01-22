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

from libautomata import GOLEvolutionModel, CellularGrid

#
# Constaints
#
SCALE         = 50                    # PIXELS SCALE FACTOR
SCREEN_WIDTH  = 600                   # SCREEN WIDTH
SCREEN_HEIGHT = 600                   # SCREEN HEIGHT
FPS           = 5                     # FRAME RATE

#
# Shows cellular grid to the screen
#
def render(screen, surface, grid):
  for i in range(len(grid)):
    for j in range(len(grid[0])):
      color = (0,0,0) if grid[i][j] == 0 else (255,255,255)
      pygame.draw.rect(surface, color, pygame.Rect(j*SCALE,i*SCALE,j*SCALE+SCALE,i*SCALE+SCALE))
  screen.blit(surface, (0,0))
  pygame.display.flip()

#
# Main
#
if __name__ == "__main__":
  pygame.init()
  cellular_grid = CellularGrid(GOLEvolutionModel(),SCREEN_WIDTH / SCALE, SCREEN_HEIGHT / SCALE)
  screen        = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
  surface       = pygame.Surface(screen.get_size())
  pygame.display.flip()
  clock         = pygame.time.Clock()
  index         = -1
  fn = [GOLEvolutionModel.PT_GLIDER, GOLEvolutionModel.PT_TRIO, GOLEvolutionModel.PT_EXPLODER]
  while True:
    if cellular_grid is not None: 
      render(screen, surface, cellular_grid.array)
    cellular_grid.evolve()
    for event in pygame.event.get():
      if event.type   == pygame.QUIT:
        exit(0)
      elif event.type == pygame.KEYDOWN:
        index = (index + 1) % len(fn)
        cellular_grid.setPattern(fn[index], cellular_grid.getPatternCenterPosition(fn[index]))
    clock.tick(FPS)



