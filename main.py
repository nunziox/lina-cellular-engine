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

from liblina import GOLEvolutionModel, CellularGrid

#
# Constaints
#
SCALE = 5 # PIXELS SCALE FACTOR
FPS   = 25 # FRAME RATE

#
# Shows cellular grid to the screen
#
def render(screen, surface, portion, grid, scale):
  for i in range(portion[0], portion[1]):
    for j in range(portion[2], portion[3]):
      color = (0,0,0) if grid[i][j] == 0 else (255,255,255)
      pygame.draw.rect(surface, color, pygame.Rect(j*scale,i*scale,j*scale+scale,i*scale+scale))
  screen.blit(surface, (0,0))
  pygame.display.flip()

#
# Main
#
if __name__ == "__main__":
  pygame.init()
  screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
  width, height = screen.get_size()
  cellular_grid = CellularGrid(GOLEvolutionModel(), width / SCALE, height / SCALE)
  surface       = pygame.Surface(screen.get_size())
  pygame.display.flip()
  clock         = pygame.time.Clock()
  index         = -1
  fn = [GOLEvolutionModel.PT_GLIDER, 
        GOLEvolutionModel.PT_TRIO, 
        GOLEvolutionModel.PT_PULSAR, 
        GOLEvolutionModel.PT_GOSPEL,
        GOLEvolutionModel.PT_PERIOD]
  while True:
    if cellular_grid is not None: 
      render(screen, surface,(cellular_grid.startY,cellular_grid.finalY,cellular_grid.startX,cellular_grid.finalX),cellular_grid.array, SCALE)
    cellular_grid.evolve()
    for event in pygame.event.get():
      if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
        exit(0)
      elif event.type == pygame.KEYDOWN:
        index = (index + 1) % len(fn)
        cellular_grid.setPattern(fn[index], cellular_grid.getPatternCenterPosition(fn[index]))
        if event.key == pygame.K_ESCAPE:
          exit(0)
    clock.tick(FPS)



