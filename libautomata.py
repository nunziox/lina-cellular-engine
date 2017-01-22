__author__     = "Nunzio Meli"
__copyright__  = "Copyright 2015, The GOL Project"
__credits__    = ["Nunzio Meli"]
__license__    = "GPL"
__version__    = "1.0"
__maintainer__ = "Nunzio Meli"
__email__      = "nunziomeli5@gmail.com"
__status__     = "Production"

class GOLEvolutionModel:
  """
  Describes the evolution rules of the cellular grid.
  """
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

  def __init__(self, model, sizeX, sizeY):
    self.model = model
    self.sizeX = sizeX
    self.sizeY = sizeY
    self.array = None
    self.reset()

  def reset(self):
    """
    Allows to reset the grid
    """
    self.array = [[0 for x in range(self.sizeX)] for x in range(self.sizeY)]

  def evolve(self):
    """
    Evolves the grid to the next state
    """
    newpoints = []
    for i in range(self.sizeY):
      for j in range(self.sizeX):
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
        if state != self.array[i][j]: newpoints.append((i,j, state))
    for elem in newpoints:
      self.array[elem[0]][elem[1]] = elem[2]

  def setPattern(self, pattern, off):
    """
    Resets the grid and sets a new pattern in the board.
    """
    self.reset()
    for point in pattern:
      self.array[point[0]+off[0]][point[1]+off[1]] = CellularGrid.ALIVE

  def getPatternCenterPosition(self, pattern):
    a = [x[0] for x in pattern]
    b = [x[1] for x in pattern]
    weight = max(a) - min(a) + 1
    height = max(b) - min(b) + 1
    return (int(self.sizeY / 2) - int(weight/2.0), int(self.sizeX / 2) - int(height/2.0))