#!/usr/bin/env python

__author__     = "Nunzio Meli"
__copyright__  = "Copyright 2015, The GOL Project"
__credits__    = ["Nunzio Meli"]
__license__    = "GPL"
__version__    = "1.0"
__maintainer__ = "Nunzio Meli"
__email__      = "nunziomeli5@gmail.com"
__status__     = "Production"


from liblina import GOLEvolutionModel, CellularGrid


class Controller:
  #
  # Patterns
  #
  PT_GLIDER        = [[0,1], [1,2], [2,0], [2,1], [2,2]]
  PT_BLINKER       = [[1,1], [2,1], [3,1]]
  PT_TRIO          = [[0,1], [1,0], [1,1], [1,2]]
  PT_PULSAR        = [[0,0], [1,0], [2,0], [3,0], [4,0], [0,2], [4,2], [0,4], [1,4], [2,4], [3,4], [4,4]]

  PT_GOSPEL        = [[5,1], [5,2], [6,1], [6,2], [5,11], [6,11], [7,11], [4,12], [8,12], [3,13], [3,14],
                      [9,13], [9,14], [6,15], [4,16], [8,16], [5,17], [6,17], [7,17], [6,18], [3,21], [4,21],
                      [5,21], [3,22], [4,22], [5,22], [2,23], [6,23], [1,25], [2,25], [6,25], [7,25], [3,35],
                      [4,35], [3,36], [4,36]]

  PT_PERIOD        = [[1,1], [17,1], [1,2], [15,2], [16,2], [17,2], [1,2], [2,2], [3,2], [4,3], [14,3], [3,4],
                      [4,4], [14,4], [15,4], [5,12], [6,12], [7,12], [11,12], [12,12], [13,12], [5,13], [8,13],
                      [10,13], [13,13], [5,14], [13,14], [6,16], [12,16], [7,17], [8,17], [10,17], [11,17],
                      [3,26], [4,26], [3,27], [4,27], [14,26], [15,26], [14,27], [15,27], [7,36], [11,36],
                      [7,37], [11,37], [4,40], [5,40], [7,40], [11,40], [13,40], [14,40], [5,41], [6,41],
                      [7,41], [11,41], [12,41], [13,41], [6,42], [12,42], [3,49], [4,49], [14,49], [15,49],
                      [4,50], [14,50], [1,51], [2,51], [3,51], [15,51], [16,51], [17,51], [1,52], [17,52]]

  #
  # Use this method to init your variables
  #
  def init(self, parent):
    self.scene = [Controller.PT_GLIDER, Controller.PT_TRIO, Controller.PT_PULSAR, Controller.PT_GOSPEL, Controller.PT_PERIOD]
    self.index = 0
    self.__setPattern(parent)

  #
  # This method is called by liblina engine each time a new key press event occurs.
  #
  def keyPressEvent(self, parent):
    self.index = (self.index + 1) % len(self.scene)
    self.__setPattern(parent)

  def __setPattern(self, parent):
    parent.setPattern(self.scene[self.index], parent.getPatternCenterPosition(self.scene[self.index]))

#
# Main
#
if __name__ == "__main__":
  scale = 5  # Each pixel in the grid will be 20 x 20 screen pixels
  fps   = 300 # FRAME RATE (the loop method inside the controller will be called each 1/FPS seconds)
  CellularGrid(Controller(), GOLEvolutionModel(), scale, fps)
