import unittest
from .geometry import *
from .window import *
from .transformations import *
from math import cos, sin, pi
import numpy

identity = np.array([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1],
])


class TestWindow(unittest.TestCase):
  def test_window_translation(self):
    window = Window(-0.5, -0.5,  0.5, 0.5)
    matrix = window.world_to_ndc_matrix()

    self.assertTrue(numpy.array_equal(matrix, identity))

    window.move(Vector(1, 0))
    inverse_movement = translation_matrix(Vector(-1, 0))
    matrix = window.world_to_ndc_matrix()

    self.assertTrue(numpy.array_equal(
        matrix, inverse_movement))

  def test_window_rotation(self):
    window = Window(-0.5, -0.5,  0.5, 0.5)
    matrix = window.world_to_ndc_matrix()

    rotate = rotation_matrix(60)
    window = window.transform(rotate)
    inverse_rotate = rotation_matrix(-60)

    matrix = window.world_to_ndc_matrix()

    self.assertTrue(numpy.array_equal(
        matrix, inverse_rotate))


#   def test_window_all(self):
#     window = Window(-0.5, -0.5,  0.5, 0.5)
#     matrix = window.world_to_ndc_matrix()

#     rotate = rotation_matrix(60)
#     window = window.transform(rotate)
#     inverse_rotate = rotation_matrix(-60)

#     matrix = window.world_to_ndc_matrix()

#     self.assertTrue(numpy.array_equal(
#         matrix, inverse_rotate))


if __name__ == '__main__':
  unittest.main()
