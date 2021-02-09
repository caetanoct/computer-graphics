from dataclasses import dataclass
from typing import List, Union

@dataclass
class Box:
  x_min: float
  y_min: float
  x_max: float
  y_max: float

@dataclass
class Point:
  x: float
  y: float

@dataclass
class Line:
  begin: Point
  end: Point

# rotate(circular-shift) a list, by "n" steps
def rotate(l, n):
  return l[-n:] + l[:-n]
@dataclass
class Polygon:
  points: List[Point]

  # returns a list of the edges that the polygon consists of
  # get points[i] with [i+1] mod len(points)
  def edges(self) -> List[Line]:
    return zip(self.points, rotate(self.points, -1))
  
Shape = Union[Polygon, Line, Point]