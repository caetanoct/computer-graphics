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
  z: float

  def __new__(cls, x, y, z=None):
    if z == None:
      return numpy.asarray([x, y]).view(cls)
    else:
      return numpy.asarray([x, y, z]).view(cls)

  @property
  def x(self):
    return self[0]

  @property
  def y(self):
    return self[1]

  @property
  def z(self):
    return self[2]

  @property
  def dimension(self):
    return len(self)

  # general transforming function, we can use this to any kind of transformation given the right matrix
  def transform(self, matrix: numpy.matrix):
    if len(matrix) > (self.dimension + 1):
      raise "ERROR: given matrix has more than 3 lines"
    if len(matrix[0]) > (self.dimension + 1):
      raise "ERROR: given matrix has more than 3 columns"

    if self.dimension == 2:
      res = matrix.dot(numpy.array([self.x, self.y, 1]))
      return Point(res[0], res[1])
    else:
      res = matrix.dot(numpy.array([self.x, self.y, self.z, 1]))
      return Point(res[0], res[1], res[2])

  def center(self):
    return self

  def __eq__(self, other):
    return numpy.array_equal(self, other)

  def __str__(self):
    if self.dimension == 2:
      return "({}, {})".format(self.x, self.y)
    else:
      return "({}, {}, {})".format(self.x, self.y, self.z)

  def __repr__(self):
    return str(self)

  def abs(self):
    return numpy.linalg.norm(self)

  def obj_string(self):
    return "v {} {} 0".format(self.x, self.y)

# it's the same as a Point, but has different semantics(meaning)


class Vector(Point):
  pass


# forward definition of Line(see below for full definition)
class Line:
  pass


def lines_obj_string(points):
  points_str = '\n'.join(point.obj_string() for point in points)
  return points_str + '\nf ' + ' '.join([str(n) for n in range(-len(points), 0)])

# data structure that represents a Polygon (list of connected points)


class Polygon:
  points: List[Point]
  dimension: int = 2

  def __init__(self, *points):
    self.points = points
    self._edges = None
    if len(points) > 0:
      self.dimension = points[0].dimension

  # applies a matrix to the points of the polygon and returns a new Polygon

  def transform(self, matrix: numpy.matrix):
    return self.__class__(
        *[point.transform(matrix) for point in self.points])

  def center(self):
    n = len(self.points)
    dim = self.points[0].dimension
    center_x = sum([point.x for point in self.points]) / n
    center_y = sum([point.y for point in self.points]) / n
    if dim == 3:
      center_z = sum([point.z for point in self.points]) / n
      return Point(center_x, center_y, center_z)
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

  def obj_string(self):
    return lines_obj_string(self.points)


class Wireframe(Polygon):
  points: List[Point]
  edges: List[Line]
  dimension = 3

  def __init__(self, points, edges):
    self.points = points
    self.edges_indices = edges
    self.dimension = 3
    super().__init__(*points)

  def transform(self, matrix: numpy.matrix):
    return Wireframe([point.transform(matrix) for point in self.points], self.edges_indices)

  @property
  def edges(self):
    return [Line(self.points[a], self.points[b]) for a, b in self.edges_indices]

  @staticmethod
  def build_cube(center: Point, size: float):
    s = size / 2
    points = [
        Point(x, y, z)
        for x in [-s, s]
        for y in [-s, s]
        for z in [-s, s]
    ]
    a, b, c, d, e, f, g, h = points
    edges = [
        (0, 1),
        (0, 2),
        (0, 4),

        (3, 2),
        (3, 1),
        (3, 7),

        (5, 1),
        (5, 7),
        (5, 4),

        (6, 7),
        (6, 4),
        (6, 2),
    ]
    return Wireframe(points, edges)


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


class Curve():
  def __init__(self, control_points):
    self.control_points = control_points
  # applies a matrix to the control points of the Curve and returns a new Curve

  def transform(self, matrix: numpy.matrix):
    return self.__class__(
        [point.transform(matrix) for point in self.control_points])

  # TODO: implement center method
  def center(self):
    return Point(0, 0)

  def obj_string(self):
    return lines_obj_string([line.begin for line in self.generate_segments()])

# http://www.lapix.ufsc.br/ensino/computacao-grafica/curvas-parametricas-em-2d/


class BezierCurve(Curve):
  def t(self, t1):
    t2 = t1*t1
    t3 = t2*t1
    result = numpy.array([t3, t2, t1, 1])
    return result

  def generate_segments(self):
    # product MHMHB
    segments = []
    cp = self.control_points
    M_b = numpy.array((
        [-1, 3, -3, 1],
        [3, -6,  3, 0],
        [-3, 3,  0, 0],
        [1,  0,  0, 0]))
    M_x = numpy.array((
        [cp[0].x],
        [cp[1].x],
        [cp[2].x],
        [cp[3].x]))
    M_y = numpy.array((
        [cp[0].y],
        [cp[1].y],
        [cp[2].y],
        [cp[3].y]))
    step = 0.05
    i = 0

    x_1 = cp[0].x
    y_1 = cp[0].y

    while i <= 1:
      t = self.t(i)
      # build lines
      aux = numpy.dot(t, M_b)
      x_2 = numpy.dot(aux, M_x)
      y_2 = numpy.dot(aux, M_y)
      x_2 = float(x_2)
      y_2 = float(y_2)
      segments.append(Line(Point(x_1, y_1), Point(x_2, y_2)))
      x_1 = x_2
      y_1 = y_2
      i += step
    x_end = cp[3].x
    y_end = cp[3].y
    segments.append(Line(Point(x_1, y_1), Point(x_end, y_end)))
    return segments


class B_SplineCurve(Curve):
  def generate_segments(self):
    segments = []
    Mbs = numpy.array((
        [-1, 3, -3, 1],
        [3, -6,  3, 0],
        [-3, 0,  3, 0],
        [1, 4,  1, 0]))
    Mbs = Mbs/6

    i = 3
    a = 0.01
    b = a*a
    c = b*a

    Md = numpy.array((
        [0,  0,   0,   1],
        [c, b, a, 0],
        [6*c, 2*b, 0,  0],
        [6*c,   0,   0,   0],))
    while i < len(self.control_points):
      Gx = numpy.array((
          [self.control_points[i-3].x],
          [self.control_points[i-2].x],
          [self.control_points[i-1].x],
          [self.control_points[i].x]))
      Gy = numpy.array((
          [self.control_points[i-3].y],
          [self.control_points[i-2].y],
          [self.control_points[i-1].y],
          [self.control_points[i].y]))

      cx = numpy.dot(Mbs, Gx)
      cy = numpy.dot(Mbs, Gy)
      dx = numpy.dot(Md, cx)
      dy = numpy.dot(Md, cy)

      # j+= a, in loop
      j = 0

      x_prev = dx[0]
      d_x_1 = dx[1]
      d_x_2 = dx[2]
      d_x_3 = dx[3]
      y_prev = dy[0]
      d_y_1 = dy[1]
      d_y_2 = dy[2]
      d_y_3 = dy[3]

      x = x_prev
      y = y_prev

      while j < 1.0:

        j += a

        x = x + d_x_1
        d_x_1 = d_x_1 + d_x_2
        d_x_2 = d_x_2 + d_x_3

        y = y + d_y_1
        d_y_1 = d_y_1 + d_y_2
        d_y_2 = d_y_2 + d_y_3

        x_prev = float(x_prev)
        y_prev = float(y_prev)

        x = float(x)
        y = float(y)

        segments.append(Line(Point(x_prev, y_prev), Point(x, y)))

        x_prev = x
        y_prev = y

      i += 1
    return segments


# A shape is either a Polygon, a Line or a Point
Shape = Union[Polygon, Line, Point]
