import math

class GOLEvolutionModel:
  #
  # Patterns
  #
  PT_GLIDER        = [[0,1], [1,2], [2,0], [2,1], [2,2]]
  PT_VERTICAL_LINE = [[1,1], [2,1], [3,1]]
  PT_TRIO          = [[0,1], [1,0], [1,1], [1,2]]
  PT_EXPLODER      = [[0,0], [1,0], [2,0], [3,0], [4,0], [0,2], [4,2], [0,4], [1,4], [2,4], [3,4], [4,4]]

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
        state = self.model.check(self.array[i][j],wsum)
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
    print(weight)
    return (int(self.sizeY / 2) - int(height/2.0), int(self.sizeX / 2) - int(weight/2.0))