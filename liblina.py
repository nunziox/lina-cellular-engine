__author__     = "Nunzio Meli"
__copyright__  = "Copyright 2015, The GOL Project"
__credits__    = ["Nunzio Meli"]
__license__    = "GPL"
__version__    = "1.0"
__maintainer__ = "Nunzio Meli"
__email__      = "nunziomeli5@gmail.com"
__status__     = "Production"

import pygame
import copy

class GOLEvolutionModel:
  """
  Describes the evolution rules of the cellular grid.
  """

#
# Implements the GOL evolution model
#
  def check(self, point, wsum):
    """
    This method implements the evolution rules
    It returns the new cell state ALIVE or DEAD
    """
    if point == CellularGrid.ALIVE and wsum < 2:
      return CellularGrid.DEAD  # DIE FOR UNDERPOPULATION
    elif point == CellularGrid.ALIVE and (wsum == 2 or wsum == 3):
      return CellularGrid.ALIVE # LIVES TO THE NEXT GENERATION
    elif point == CellularGrid.ALIVE and wsum > 3:
      return CellularGrid.DEAD  # DIE FOR OVERPOPULATION
    elif point == CellularGrid.DEAD and wsum == 3:
      return CellularGrid.ALIVE # REPRODUCTION
    return point

class CellularGrid:
  """
  Describes the cellular logic.
  """

  #
  # Constaints
  #
  ALIVE = 1 # PIXEL STATE ALIVE
  DEAD  = 0 # PIXEL STATE DEAD

  def __init__(self, client, model, scale, fps):
    """
    Parameters:
      client - the controller class
      model  - the chosen evolution model
      scale  - The pixel scale factor
      fps    - The frame rate
    """
    self.client = client
    self.model = model
    self.scale = scale

    # List used to store the pixels state
    self.point_list = []

    pygame.init()
    self.screen   = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    width, height = self.screen.get_size()
    self.surface  = pygame.Surface(self.screen.get_size())
    clock         = pygame.time.Clock()

    self.sizeX = int(width  / self.scale)
    self.sizeY = int(height / self.scale)
    self.array = None

    # Resets the board state
    self.reset()

    # Call the init method in the ccontroller class
    self.client.init(self)

    while True:
      # Call the loop method in the controller class
      self.client.loop(self)
      for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            exit(0)
          self.client.keyPressEvent(self)
      clock.tick(fps)

  def render(self):
    """
    Renders the grid state on the screen using the pygame lib
    """
    for elem in self.point_list:
      color = (0,0,0) if elem[2] == CellularGrid.DEAD else (255,255,255)
      pygame.draw.rect(self.surface, color, pygame.Rect(elem[1]*self.scale,elem[0]*self.scale,self.scale,self.scale))
    self.screen.blit(self.surface, (0,0))
    pygame.display.flip()

  def reset(self):
    """
    Allows to reset the grid state
    """
    self.dead_list = []
    for elem in self.point_list:
      self.dead_list.append((elem[0],elem[1],CellularGrid.DEAD))
    self.point_list = []
    self.array = [[0 for x in range(self.sizeX)] for x in range(self.sizeY)]
    self.surface  = pygame.Surface(self.screen.get_size())
    self.render()

  def evolve(self):
    """
    Evolves the grid to the next state
    """
    a = list()
    newpoints = []
    for elem in self.point_list:
      i = elem[0]
      j = elem[1]
      t = self.sizeY -1 if i-1 == -1 else i-1
      k = self.sizeX -1 if j-1 == -1 else j-1
      a.append((t,j,self.array[t][j]))
      a.append((t,k,self.array[t][k]))
      a.append((t,(j+1) % self.sizeX,self.array[t][(j+1) % self.sizeX]))
      a.append(((i+1) % self.sizeY,j, self.array[(i+1) % self.sizeY][j]))
      a.append(((i+1) % self.sizeY,(j+1) % self.sizeX ,self.array[(i+1) % self.sizeY][(j+1) % self.sizeX]))
      a.append(((i+1) % self.sizeY,k, self.array[(i+1) % self.sizeY][k]))
      a.append((i,(j+1) % self.sizeX, self.array[i][(j+1) % self.sizeX]))
      a.append((i,k, self.array[i][k]))
    for elem in (set(self.point_list) | set(a)):
        i = elem[0]
        j = elem[1]
        t = self.sizeY -1 if i-1 == -1 else i-1
        k = self.sizeX -1 if j-1 == -1 else j-1
        wsum = self.array[t][j]                                   + \
               self.array[t][k]                                   + \
               self.array[t][(j+1) % self.sizeX]                  + \
               self.array[(i+1) % self.sizeY][j]                  + \
               self.array[(i+1) % self.sizeY][(j+1) % self.sizeX] + \
               self.array[(i+1) % self.sizeY][k]                  + \
               self.array[i][(j+1) % self.sizeX]                  + \
               self.array[i][k]
        state = self.model.check(self.array[i][j], wsum)
        if state != self.array[i][j]: 
          newpoints.append((i, j, state))
    self.point_list = []
    for elem in newpoints:
      self.array[elem[0]][elem[1]] = elem[2]
      self.point_list.append((elem[0], elem[1], elem[2]))

  def setPattern(self, pattern, off):
    """
    Resets the grid and sets a new pattern in the board.
    """
    self.reset()
    self.point_list = []
    for point in pattern:
      if point[0]+off[0] >= self.sizeY or point[1]+off[1] >= self.sizeX:
        self.reset()
        raise Exception("Invalid point in the pattern")
        return
      self.point_list.append((point[0]+off[0],point[1]+off[1], CellularGrid.ALIVE))
      self.array[point[0]+off[0]][point[1]+off[1]] = CellularGrid.ALIVE

  def getPatternCenterPosition(self, pattern):
    """
    Returns the offset values along the two axes in order to place the pattern 
    in the center of the screen
    """
    a = [x[0] for x in pattern]
    b = [x[1] for x in pattern]
    weight = max(a) - min(a) + 1
    height = max(b) - min(b) + 1
    return (int(self.sizeY / 2) - int(weight/2.0), int(self.sizeX / 2) - int(height/2.0))