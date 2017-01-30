# GOL

# Lina Cellular Engine

Lina is a cellular automata engine.

Lina actually implement only one Evolution Model, The Conway's Game Of Life!

## How to contribute 
Clone, create the branch and make the pull request.

## How to run the example

`python main.py`

You may need to install pygame in you enviroment.

If it's the case:

`pip install pygame`

## How to create a new app using lib lina

1) Define a new Contructor class ad shown below:

class Controller:
  #
  # Patterns
  #
  PT_PATTERN1        = [[0,1], [1,2]]

  #
  # Use this method to init your variables
  #
  def init(self, parent):
    pass

  #
  # This method is called by liblina engine each 1/FPS seconds.
  #
  def loop(self, parent):
    pass

  #
  # This method is called by liblina engine each time a new key press event occurs.
  #
  def keyPressEvent(self, parent):
    pass

2) Start the liblina engine inside your main function as shown below:

if __name__ == "__main__":
  scale = 5  # Each pixel in the grid will be 20 x 20 screen pixels
  fps   = 300 # FRAME RATE (the loop method inside the controller will be called each 1/FPS seconds)
  CellularGrid(Controller(), GOLEvolutionModel(), scale, fps)

The CellularGrid constructor accepts the folloiwng arguments:
    - Controller (The class that implements the call back functions called by the Controller)
    - Evolution model the evolution model (e.g. the Game of Life evolution model)
    - Scale: the scale factor of each pixel
    - Fps:   the number of frame for seconds (how many time in a second your loop function inside the
                                              controller will be called)