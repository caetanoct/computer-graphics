from dataclasses import dataclass
from typing import List, Union, Optional
import numpy
import math


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
    vec = numpy.array([self.x, self.y, 1])
    res = matrix.dot(vec)
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


class InfiniteLine:
  # line of the format
  # a*x + b*y + c = 0
  # this allows us to represent infinite lines, both vertically and horizontally
  def __init__(self, a, b, c):
    self.a = a
    self.b = b
    self.c = c

  # https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection#Using_homogeneous_coordinates
  def intersection(self, line_segment: Line):
    a1 = self.a
    b1 = self.b
    c1 = self.c

    a2 = -line_segment.angular_coefficient()
    b2 = 1
    c2 = -line_segment.horizontal_intersection(0).y
    if math.isinf(a2):
      a2 = 1
      b2 = 0
      c2 = -line_segment.vertical_intersection(0).x
    ap, bp, cp = (b1*c2 - b2*c1, a2*c1 - a1*c2, a1*b2 - a2*b1)
    if cp == 0:
      return None
    return Point(ap/cp, bp/cp)

# data structure that rerpresents a line (two connected point), that is a 2d polygon


class Line(Polygon):
  begin: Point
  end: Point

  def __init__(self, begin, end):
    self.begin = begin
    self.end = end
    super().__init__(begin, end)

  def angular_coefficient(self):
    deltax = self.end.x-self.begin.x
    deltay = self.end.y-self.begin.y
    if (deltax == 0):
      print("deltax == 0!")
    return (deltay/deltax)

  def horizontal_intersection(self, x) -> Point:
    y_intersection = self.angular_coefficient() * (x - self.begin.x) + self.begin.y
    return Point(x, y_intersection)

  def vertical_intersection(self, y) -> Point:
    x_intersection = self.begin.x + \
        (y - self.begin.y) / self.angular_coefficient()
    return Point(x_intersection, y)

    y_intersection = self.angular_coefficient() * (x - self.begin.x) + self.begin.y
    return Point(x, y_intersection)


# A shape is either a Polygon, a Line or a Point
Shape = Union[Polygon, Line, Point]
