from dataclasses import dataclass
from typing import List, Union
import numpy

# data structure that contains 2 points that define the box, (x_min,y_min) and (x_max,y_max)
@dataclass
class Box:
  x_min: float
  y_min: float
  x_max: float
  y_max: float
  def center(self):
    center_x=(self.x_min+self.x_max)/2
    center_y=(self.y_min+self.y_max)/2
    return Point(center_x,center_y)

# rotate(circular-shift) a list, by "n" steps
def rotate(l, n):
  return l[-n:] + l[:-n]

# data structure that representas a point (x,y)
@dataclass
class Point:
  x: float
  y: float
  # general transforming function, we can use this to any kind of transformation given the right matrix
  def transform(self, matrix: numpy.matrix):
    if (len(matrix)>3):
      raise "ERROR: given matrix has more than 3 lines"
    if (len(matrix[0])>3):
      raise "ERROR: given matrix has more than 3 columns"
    matrix_1=[self.x,self.y,1]
    matrix_2=matrix
    matrix_result=numpy.matmul(matrix_1,matrix_2)
    return Point(matrix_result[0],matrix_result[1])
  
  def center(self):
    return self

class Line:
  pass
# data structure that represents a Polygon (list of connected points)
@dataclass
class Polygon:
  points: List[Point]

  # applies a matrix to the points of the polygon and returns a new Polygon
  def transform(self, matrix: numpy.matrix):
    return Polygon([point.transform(matrix) for point in self.points])

  def center(self):
    n = len(self.points)
    center_x = sum([points.x for point in self.points]) / n
    center_y = sum([points.y for point in self.points]) / n
    return Point(center_x, center_y)

  # returns a list of the edges that the polygon consists of
  # get points[i] with [i+1] mod len(points)
  def edges(self) -> List[Line]:    
    # an iterator of tuples where the first item in each passed iterator is paired together, and then the second item in each passed iterator are paired together...
    return zip(self.points, rotate(self.points, -1))

# data structure that rerpresents a line (two connected point), that is a 2d polygon
class Line(Polygon):
  begin: Point
  end: Point
  def __init__(self, begin, end):
    self.begin = begin
    self.end = end
    super().__init__([begin, end])


# A shape is either a Polygon, a Line or a Point  
Shape = Union[Polygon, Line, Point]