#!/usr/bin/env python

__author__     = "Nunzio Meli"
__copyright__  = "Copyright 2015, The GOL Project"
__credits__    = ["Nunzio Meli"]
__license__    = "GPL"
__version__    = "1.0"
__maintainer__ = "Nunzio Meli"
__email__      = "nunziomeli5@gmail.com"
__status__     = "Production"

import sys
import logging
from argparse import ArgumentParser
import json
from os import stat
from liblina import NoOpEvolutionModel, GOLEvolutionModel, CellularGrid


def optSetup():
    parser = ArgumentParser()

    parser.add_argument("--fps",
        type = int,
        default = 30,
        help = "animation frame rate (frames per second)")

    parser.add_argument("--scale",
        type = int,
        default = 5,
        help = "size of each cell (pixel)")

    parser.add_argument("--model",
        type = str,
        choices = ["GOL", "NOP"],
        default = "GOL",
        help = "evolution model; GOL = Game Of Life, NOP = Null")

    parser.add_argument("--log-level",
        type = str,
        choices = ["DEBUG", "INFO", "ERROR"],
        default = "INFO",
        help = "Set log level")

    return parser


def logSetup(logLevel):
    rootLogger = logging.getLogger()
    rootLogger.setLevel(logLevel)

    logHandler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logHandler.setFormatter(formatter)
    rootLogger.addHandler(logHandler)


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


def main():
    parser = optSetup()
    args = parser.parse_args()
    logSetup(logging.getLevelName(args.log_level))

    logger=logging.getLogger("main")

    scale = args.scale
    fps = args.fps

    if args.model == "GOL":
        model = GOLEvolutionModel()
    elif args.model == "NOP":
        model = NoOpEvolutionModel()
    else:
        raise Exception("Unknown evolution model.")

    CellularGrid(Controller(), model, scale, fps)


#
# Main
#
if __name__ == "__main__":
    main()
