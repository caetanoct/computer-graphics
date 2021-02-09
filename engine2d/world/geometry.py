from dataclasses import dataclass
from typing import List, Union

# data structure that contains 2 points that define the box, (x_min,y_min) and (x_max,y_max)
@dataclass
class Box:
  x_min: float
  y_min: float
  x_max: float
  y_max: float
# data structure that representas a point (X,y)
@dataclass
class Point:
  x: float
  y: float
# data structure that rerpresents a line (two connected point) ex: drawline(begin.x,begin.y, end.x,end.y)
@dataclass
class Line:
  begin: Point
  end: Point

# rotate(circular-shift) a list, by "n" steps
def rotate(l, n):
  return l[-n:] + l[:-n]
# data structure that represents a Polygon (list of connected points)
@dataclass
class Polygon:
  points: List[Point]

  # returns a list of the edges that the polygon consists of
  # get points[i] with [i+1] mod len(points)
  def edges(self) -> List[Line]:    
    # an iterator of tuples where the first item in each passed iterator is paired together, and then the second item in each passed iterator are paired together...
    return zip(self.points, rotate(self.points, -1))

# A shape is either a Polygon, a Line or a Point  
Shape = Union[Polygon, Line, Point]