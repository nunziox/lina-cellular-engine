__author__     = "Nunzio Meli"
__copyright__  = "Copyright 2015, The GOL Project"
__credits__    = ["Nunzio Meli"]
__license__    = "GPL"
__version__    = "1.0"
__maintainer__ = "Nunzio Meli"
__email__      = "nunziomeli5@gmail.com"
__status__     = "Production"

class GOLEvolutionModel:
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

  def check(self, point, wsum):
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
    self.array = [[0 for x in range(self.sizeX)] for x in range(self.sizeY)]

  def evolve(self):
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
    self.reset()
    for point in pattern:
      self.array[point[0]+off[0]][point[1]+off[1]] = CellularGrid.ALIVE

  def getPatternCenterPosition(self, pattern):
    a = [x[0] for x in pattern]
    b = [x[1] for x in pattern]
    weight = max(a) - min(a) + 1
    height = max(b) - min(b) + 1
    return (int(self.sizeY / 2) - int(weight/2.0) -10, int(self.sizeX / 2) - int(height/2.0))