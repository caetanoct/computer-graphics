from dataclasses import dataclass
from typing import List
from engine2d.world.geometry import Shape, Point, Line, Polygon
from engine2d.world.window import Window



@dataclass
class World:
  shapes: List[Shape]
  window = Window(0, 0, 400, 400)
  
  def draw_shapes(self, draw_line):
    for shape in self.shapes:
      if type(shape) == Point:
        draw_line(shape, shape)
      if type(shape) == Line:
        draw_line(shape.begin, shape.end)
      if type(shape) == Polygon:
        for (begin, end) in shape.edges():
          draw_line(begin, end)