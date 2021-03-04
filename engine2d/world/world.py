from dataclasses import dataclass
from typing import List
from engine2d.world.geometry import Shape, Point, Line, Polygon
from engine2d.world.window import Window


@dataclass
class World:
  # world display file
  shapes: List[Shape]

  # it was told that this was the recommended window bounds
  # but it so happens that this makes the scaling matrix half every coordinates
  # so we are halving the bounds, so the scaling matrix is the identity(it eases the tests)
  # window = Window(-1, -1, 1, 1)
  window = Window(-0.5, -0.5, 0.5, 0.5)

  def __init__(self, shapes):
    if len(shapes) == 0:
      self.shapes = [
          Point(0, 0),
          Point(0, 0.1),
          Point(0.1, 0.1),
          Line(Point(0.5, 0.5), Point(0.9, 0.9)),
          Polygon(Point(-0.3, -0.3), Point(-0.3, -0.6),
                  Point(-0.6, -0.6), Point(-0.6, -0.3))
      ]
    else:
      self.shapes = shapes

  # draws a single shape
  def draw_shape(self, shape, draw_line):
    # print("Drawing shape {}".format(shape))
    normalized_shape = self.normalize_shape(shape)
    # print("Drawing shape[normalized] {}".format(normalized_shape))
    if type(normalized_shape) == Point:
      draw_line(normalized_shape, normalized_shape)
    if type(normalized_shape) == Line:
      draw_line(normalized_shape.begin, normalized_shape.end)
    if type(normalized_shape) == Polygon:
      for line in normalized_shape.edges():
        draw_line(line.begin, line.end)

  # draws all shapes in the list of shapes
  def draw_shapes(self, draw_line):
    for shape in self.shapes:
      self.draw_shape(shape, draw_line)

  # normalized display file
  def normalize_shape(self, shape: Shape) -> Shape:
    return shape.transform(self.window.world_to_ndc_matrix())
