# Lina Cellular Engine

Lina is a cellular automata engine.

Lina actually implement only one Evolution Model, The Conway's Game Of Life!

## How to define a new evolution model 
Clone, create the branch and make the pull request.

## How to clone

`git clone https://github.com/nunziox/lina-cellular-engine`

## How to run

`python main.py`

You may need to install pygame in you enviroment.

If it's the case:

`pip install pygame`

## How to create your own app using liblina

1) Import liblina

```python
from liblina import GOLEvolutionModel, CellularGrid
```

2) Create your Controller class as shown below:

```python
class Controller:
  #
  # Patterns
  #
  PT_PATTERN1        = [[0,1], [1,2],, [1,3]]

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
```

3) Start liblina engine inside your main function as shown below:

```python
if __name__ == "__main__":
  scale = 5  # Each pixel in the grid will be 20 x 20 screen pixels
  fps   = 300 # FRAME RATE (the loop method inside the controller will be called each 1/FPS seconds)
  CellularGrid(Controller(), GOLEvolutionModel(), scale, fps)
```

The CellularGrid constructor accepts the folloiwng arguments:
     
* Controller (The class that implements the call back functions called by the Controller)
* Evolution model the evolution model (e.g. the Game of Life evolution model)
* Scale: the scale factor of each pixel
* Fps:   the number of frame for seconds (how many time in a second your loop function inside the controller will be called)

4) Define your initial pattern as a list of points (e.g. PT_PATTERN1 in the Controller class)

```python
PT_PATTERN1        = [[0,1], [1,2],, [1,3]]
```

5) Call the render and evolve function inside the loop method as shown before:

```python
def loop(self, parent):
  parent.render()
  parent.evolve()
```

6) Define the patter, that you would like to use, inside your init function:
```python
  def init(self, parent):
    self.scene = [Controller.PT_PATTERN1]
    parent.setPattern(self.scene[0], parent.getPatternCenterPosition(self.scene[0]))
```

Look at the main.py file for a more complex example.  