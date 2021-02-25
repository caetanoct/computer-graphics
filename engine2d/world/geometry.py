from dataclasses import dataclass
from typing import List, Union
import numpy


@dataclass
# data structure that contains 2 points that define the box, (x_min,y_min) and (x_max,y_max)
class Box:
  x_min: float
  y_min: float
  x_max: float
  y_max: float

  def center(self):
    center_x = (self.x_min + self.x_max) / 2
    center_y = (self.y_min + self.y_max) / 2
    return Point(center_x, center_y)


# rotate(circular-shift) a list, by "n" steps
def rotate(l, n):
  return l[-n:] + l[:-n]


# data structure that representas a point (x,y)
class Point(numpy.ndarray):
  x: float
  y: float

  def __new__(cls, x, y):
    return numpy.asarray([x, y]).view(cls)

  @property
  def x(self):
    return self[0]

  @property
  def y(self):
    return self[1]

  # general transforming function, we can use this to any kind of transformation given the right matrix
  def transform(self, matrix: numpy.matrix):
    if len(matrix) > 3:
      raise "ERROR: given matrix has more than 3 lines"
    if len(matrix[0]) > 3:
      raise "ERROR: given matrix has more than 3 columns"
    res = numpy.matmul([self.x, self.y, 1], matrix)
    return Point(res[0], res[1])

  def center(self):
    return self

  def __eq__(self, other):
    return numpy.array_equal(self, other)

  def __str__(self):
    return "({}, {})".format(self.x, self.y)

  def __repr__(self):
    return str(self)

  def abs(self):
    return numpy.linalg.norm(self)

# it's the same as a Point, but has different semantics(meaning)


class Vector(Point):
  pass


# forward definition of Line(see below for full definition)
class Line:
  pass


# data structure that represents a Polygon (list of connected points)
class Polygon:
  points: List[Point]

  def __init__(self, *points):
    self.points = points

  # applies a matrix to the points of the polygon and returns a new Polygon
  def transform(self, matrix: numpy.matrix):
    return self.__class__(
        *[point.transform(matrix) for point in self.points])

  def center(self):
    n = len(self.points)
    center_x = sum([point.x for point in self.points]) / n
    center_y = sum([point.y for point in self.points]) / n
    return Point(center_x, center_y)

  # returns a list of the edges that the polygon consists of
  # get points[i] with [i+1] mod len(points)
  def edges(self) -> List[Line]:
    # an iterator of tuples where the first item in each passed iterator is paired together, and then the second item in each passed iterator are paired together...
    return [
        Line(a, b) for (a, b) in zip(self.points, rotate(self.points, -1))
    ]

  def __str__(self):
    return str(self.points)

  def __eq__(self, other):
    return all(a == b for (a, b) in zip(self.points, other.points))


# data structure that rerpresents a line (two connected point), that is a 2d polygon
class Line(Polygon):
  begin: Point
  end: Point

  def __init__(self, begin, end):
    self.begin = begin
    self.end = end
    super().__init__(begin, end)


# A shape is either a Polygon, a Line or a Point
Shape = Union[Polygon, Line, Point]
