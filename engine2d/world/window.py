from __future__ import annotations
from engine2d.world.geometry import Point, Vector, Polygon
from engine2d.world.clipping import *
from engine2d.world.box import Box
from engine2d.world.transformations import translation_matrix, rotation_matrix, scaling_matrix
import numpy
import math
# the window knows how to zoom/move


class Window:
  up = Vector(x=0, y=1)
  right = Vector(x=1, y=0)
  # view reference point
  vrp = Vector(0, 0, 0)
  # view plane normal
  vpn = Vector(0, 0, -1)

  def __init__(self, u_min, v_min, u_max, v_max):
    self.u_min = u_min
    self.u_max = u_max
    self.v_min = v_min
    self.v_max = v_max
    self.dimension = 2

  def width(self):
    return self.u_max - self.u_min

  def height(self):
    return self.v_max - self.v_min

  def center(self):
    center_x = (self.u_min + self.u_max) / 2
    center_y = (self.v_min + self.v_max) / 2
    return Point(center_x, center_y)

  # projects a 3D shape to a 2D shape
  def project(self, shape) -> List[Line]:
    # view reference point
    self.vrp
    # passo1 = self.vrp - Vector(0, 0)
    # passo2 = vpn  # view plane normal
    # passo3 = 3  # rotacionar o mundo em X e Y, p alinhar VPN com Z
    # passo 4 - ignorar vertices de objetos

    def project_point(p: Point):
      return Point(p.x, p.y)

    def project_line(l: Line):
      return Line(project_point(l.begin), project_point(l.end))

    if type(shape) == Wireframe:
      return [project_line(edge) for edge in shape.edges]

  def zoom(self, factor):
    self.u_min += factor
    self.v_min += factor
    self.u_max -= factor
    self.v_max -= factor

  def move(self, to: Vector):
    self.u_min += to.x
    self.u_max += to.x
    self.v_min += to.y
    self.v_max += to.y

  def transform(self, matrix: numpy.matrix) -> Window:
    new_window = Window(self.u_min, self.v_min, self.u_max, self.v_max)

    new_window.up = self.up.transform(matrix)
    new_window.right = self.right.transform(matrix)

    return new_window

  # world to normalized coordinates system transform
  def world_to_ndc_matrix(self) -> numpy.matrix:
    to_origin = translation_matrix(-self.center())
    # in radians
    diff_y_axis_up_vector = Vector(x=0, y=1).dot(self.up)
    angle_correction = - math.acos(diff_y_axis_up_vector) * 180 / math.pi
    correct_angle = rotation_matrix(angle_correction)

    scale = scaling_matrix(1 / self.width(), 1 / self.height())

    matrix = to_origin.dot(correct_angle.dot(scale))
    return matrix

  def is_point_inside(self, p: Point):
    inside_horizontal = self.u_min < p.x and p.x < self.u_max
    inside_vertical = self.v_min < p.y and p.y < self.v_max
    return inside_horizontal and inside_vertical

  def clip_line(self, line: Line) -> Optional[Line]:
    return cohen_sutherland_line_clipping(self, line)

  def clip_polygon(self, polygon: Polygon) -> Optional[Polygon]:
    return sutherland_hodgeman_polygon_clipping(self, polygon)
