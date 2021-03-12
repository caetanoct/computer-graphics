from dataclasses import dataclass
from typing import List
from engine2d.world.geometry import Shape, Point, Line, Polygon
from engine2d.world.window import Window
from engine2d.ui.drawing_context import DrawingContext


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
          Line(Point(2, 2), Point(-2, -2)),
          Line(Point(2, -2), Point(-2, 2)),
          Line(Point(2, 0), Point(-2, 0)),
          Line(Point(-2, 0), Point(2, 0)),
          Line(Point(0, 2), Point(0, -2)),
          Line(Point(0, -2), Point(0, 2)),
          Line(Point(0.3, 0.3), Point(-0.3, -0.3)),
          Line(Point(-0.3, -0.3), Point(0.3, 0.3)),
          Line(Point(-0.3, 0.3), Point(0.3, -0.3)),
          Line(Point(0.3, -0.3), Point(-0.3, 0.3)),
          Polygon(Point(-0.3, -0.3), Point(-0.3, -0.6),
                  Point(-0.6, -0.6), Point(-0.6, -0.3)),
          Polygon(Point(0, 0), Point(0.2, 0), Point(0.1, 0.2),
                  Point(0.2, 0.4), Point(0, 0.4))
      ]
    else:
      self.shapes = shapes

    self.shapes.append(self.window)

  # draws a single shape
  def draw_shape(self, shape, drawing_context: DrawingContext):
    # print("Drawing shape {}".format(shape))
    normalized_shape = self.normalize_shape(shape)
    # print("Drawing shape[normalized] {}".format(normalized_shape))
    if type(normalized_shape) == Point:
      if self.window.is_point_inside(normalized_shape):
        drawing_context.draw_line(normalized_shape, normalized_shape)
    if type(normalized_shape) == Line:
      clipped_line = self.window.clip_line(normalized_shape)
      if clipped_line is not None:
        drawing_context.draw_line(clipped_line.begin, clipped_line.end)
    if type(normalized_shape) == Polygon:
      clipped_polygon = self.window.clip_polygon(normalized_shape)
      drawing_context.fill_polygon(clipped_polygon)
    if type(normalized_shape) == Window:
      a = Point(self.window.x_min, self.window.y_min)
      b = Point(self.window.x_min, self.window.y_max)
      c = Point(self.window.x_max, self.window.y_max)
      d = Point(self.window.x_max, self.window.y_min)
      drawing_context.draw_line(a, b)
      drawing_context.draw_line(b, c)
      drawing_context.draw_line(c, d)
      drawing_context.draw_line(d, a)

  # draws all shapes in the list of shapes
  def draw_shapes(self, drawing_context: DrawingContext):
    for shape in self.shapes:
      self.draw_shape(shape, drawing_context)

  # normalized display file
  def normalize_shape(self, shape: Shape) -> Shape:
    return shape.transform(self.window.world_to_ndc_matrix())
