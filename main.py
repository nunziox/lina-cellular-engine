#!/usr/bin/env python

__author__     = "Nunzio Meli"
__copyright__  = "Copyright 2015, The GOL Project"
__credits__    = ["Nunzio Meli"]
__license__    = "GPL"
__version__    = "1.0"
__maintainer__ = "Nunzio Meli"
__email__      = "nunziomeli5@gmail.com"
__status__     = "Production"

import json
from os import stat
from liblina import GOLEvolutionModel, CellularGrid

class NoOpEvolutionModel:
  def evolve(self, cellState, neighbourCount):
      return cellState

class Controller:

  #
  # Use this method to init your variables
  #
  def init(self, grid):
    self.scene = []
    for pattern in self.loadPatterns('patterns.json'):
      self.scene.append(pattern['points'])
    # display first pattern at startup
    self.index = 0
    self.__setPattern(grid)

  #
  # This method is called by liblina engine each time a new key press event occurs.
  #
  def keyPressEvent(self, grid):
    # when a key is pressed, display next pattern
    self.index = (self.index + 1) % len(self.scene)
    self.__setPattern(grid)

  def __setPattern(self, grid):
    grid.setPattern(self.scene[self.index], grid.getPatternCenterPosition(self.scene[self.index]))


  def loadPatterns(self, fileName):
    if (stat(fileName).st_size == 0):
      return []
    with open(fileName) as fp:
      return json.load(fp)

#
# Main
#
if __name__ == "__main__":
  scale = 5  # Each pixel in the grid will be 20 x 20 screen pixels
  fps   = 300 # FRAME RATE (the loop method inside the controller will be called each 1/FPS seconds)
  CellularGrid(Controller(), GOLEvolutionModel(), scale, fps)
  #CellularGrid(Controller(), NoOpEvolutionModel(), scale, fps)
