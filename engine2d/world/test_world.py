import unittest
from .geometry import *
from .window import *
from .transformations import *
from .world import *
from math import cos, sin, pi, radians
import numpy

identity = np.array([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1],
])


class TestWorld(unittest.TestCase):
  def test_world(self):
    # point is 60 degrees(COUNTER CLOCKWISE) from the x axis
    point = Point(cos(radians(60)), sin(radians(60)))
    world = World([point])

    # rotate the window 60 degrees(CLOCKWISE)
    world.window = world.window.transform(rotation_matrix(60))

    normalized_point = world.normalize_shape(point)

    # point should be in the X axis
    self.assertEqual(normalized_point, Point(1, 0))


if __name__ == '__main__':
  unittest.main()
