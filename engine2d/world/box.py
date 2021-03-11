from .geometry import *
from .clipping import *


@dataclass
# data structure that contains 2 points that define the box, (x_min,y_min) and (x_max,y_max)
class Box:
  x_min: float
  y_min: float
  x_max: float
  y_max: float

  def width(self):
    return self.x_max - self.x_min

  def height(self):
    return self.y_max - self.y_min

  def center(self):
    center_x = (self.x_min + self.x_max) / 2
    center_y = (self.y_min + self.y_max) / 2
    return Point(center_x, center_y)

  def is_point_inside(self, p: Point):
    inside_horizontal = self.x_min < p.x and p.x < self.x_max
    inside_vertical = self.y_min < p.y and p.y < self.y_max
    return inside_horizontal and inside_vertical

  def clip_line(self, line: Line) -> Optional[Line]:
    return cohen_sutherland_line_clipping(self, line)
