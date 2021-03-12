from typing import Callable
from engine2d.world.geometry import *


class DrawingContext:
  draw_line: Callable[[Point, Point], None]
  fill_polygon: Callable[[Polygon], None]

  def __init__(self, draw_line, fill_polygon):
    self.draw_line = draw_line
    self.fill_polygon = fill_polygon
