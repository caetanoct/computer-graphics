import unittest
from .geometry import *
from .transformations import *
from math import cos, sin, pi

class TestGeometry(unittest.TestCase):
    def test_point_translation(self):
        point = Point(1, 2)
        matrix = translation_matrix(Point(-3, 5))
        transformed = point.transform(matrix)
        self.assertEqual(transformed, Point(-2, 7))
    
    def test_point_rotation(self):
        angle = 30
        rad = pi/180 * angle
        point = Point(1, 0)
        matrix = rotation_matrix(angle)
        transformed = point.transform(matrix)
        self.assertEqual(transformed, Point(cos(rad), -sin(rad)))

        matrix = rotation_around_object_matrix(point, angle)
        transformed_around = point.transform(matrix)
        # should be equal because it is a point
        self.assertEqual(point, transformed_around)
    
    def test_polygon_edges(self):
        a = Point(0, 0)
        b = Point(2, 0)
        c = Point(1, 1)
        poly = Polygon(a, b, c)
        x, y, z = poly.edges()
        self.assertEqual(x, Line(a, b))
        self.assertEqual(y, Line(b, c))
        self.assertEqual(z, Line(c, a))
        self.assertEqual(x.begin.x, a.x)
        self.assertEqual(x.begin.y, a.y)
        self.assertEqual(x.end, b)

if __name__ == '__main__':
    unittest.main()
