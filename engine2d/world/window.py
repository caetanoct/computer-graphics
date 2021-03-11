from __future__ import annotations
from engine2d.world.geometry import Box, Point, Vector
from engine2d.world.transformations import translation_matrix, rotation_matrix, scaling_matrix
import numpy
import math
# the window knows how to zoom/move


class Window(Box):
  up = Vector(x=0, y=1)
  right = Vector(x=1, y=0)

  def zoom(self, factor):
    self.x_min += factor
    self.y_min += factor
    self.x_max -= factor
    self.y_max -= factor

  def move(self, to: Vector):
    self.x_min += to.x
    self.x_max += to.x
    self.y_min += to.y
    self.y_max += to.y
    print(self)

  def transform(self, matrix: numpy.matrix) -> Window:
    new_window = Window(self.x_min, self.y_min, self.x_max, self.y_max)

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