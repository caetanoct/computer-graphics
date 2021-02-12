from dataclasses import dataclass
from typing import List, Union

# data structure that contains 2 points that define the box, (x_min,y_min) and (x_max,y_max)
@dataclass
class Box:
  x_min: float
  y_min: float
  x_max: float
  y_max: float
  def center() -> Point:
    center_x=(x_min+x_max)/2
    center_y=(y_min+y_max)/2
    return Point(center_x,center_y)
# data structure that representas a point (x,y)
@dataclass
class Point:
  x: float
  y: float
  def center() -> Point:
    return Point(x,y)
# data structure that rerpresents a line (two connected point) ex: drawline(begin.x,begin.y, end.x,end.y)
@dataclass
class Line:
  begin: Point
  end: Point
  def center() -> Point:
    return Point((begin.x+end.x)/2,(begin.y+end.y)/2)
# rotate(circular-shift) a list, by "n" steps
def rotate(l, n):
  return l[-n:] + l[:-n]
# data structure that represents a Polygon (list of connected points)
@dataclass
class Polygon:
  points: List[Point]
  def center() -> Point:
    sum_x=0
    sum_y=0
    for point in points:
      sum_x+=point.x
      sum_y+=point.y
    return Point(sum_x/len(points), sum_y/len(points))
  # returns a list of the edges that the polygon consists of
  # get points[i] with [i+1] mod len(points)
  def edges(self) -> List[Line]:    
    # an iterator of tuples where the first item in each passed iterator is paired together, and then the second item in each passed iterator are paired together...
    return zip(self.points, rotate(self.points, -1))

# A shape is either a Polygon, a Line or a Point  
Shape = Union[Polygon, Line, Point]