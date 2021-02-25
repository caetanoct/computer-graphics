# we use the matrixes below to multiply with the points and do the transformation that always uses the same algorithm
# example: transform (point, matrix)
# we can do a sequence of transformations as a sequence of matrix multiplications (in order) and transform the object with the resultant matrix
# example: translate the center of the object to the origin rotate the object and translate it back to where it was
# remember: object center is the arithmetic average of the coordinates
#---------------------------------------------------------------#
# translation [x' y' 1] = [x y 1] *  [1  0  0]					#
#									 [0  1  0]					#
#									 [Dx Dy 1]					#
#---------------------------------------------------------------#
# scaling [x' y' 1] = [x y 1] * [Sx 0  0]						#
#								[0  Sy 0]						#
#								[0  0  1]						#
#---------------------------------------------------------------#
# rotation -             [x' y' 1] = [x y 1] * [cos_ -sin_ 0]	#
#											  [sin_  cos_ 0]	#
#											  [0     0    1]	#
#---------------------------------------------------------------#
#
# TODO: implement translation of objects, scaling (without deslocating), rotations (around the world, around the object, around an arbitrary point)
#
from typing import List
from numbers import Number
import numpy as np
import math
from engine2d.world.geometry import Shape, Point

# translates given point in Dx,Dy


def translation_matrix(p: Point) -> np.ndarray:
  return np.array([
      [1, 0, 0],
      [0, 1, 0],
      [p.x, p.y, 1]
  ])

# scaling (will move the object)


def scaling_matrix(Sx: Number, Sy: Number) -> np.ndarray:
  return np.array([
      [Sx, 0, 0],
      [0, Sy, 0],
      [0, 0, 1]
  ])

# angle in degrees (CLOCKWISE rotation)


def rotation_matrix(angle: Number) -> np.ndarray:
  rad = math.pi / 180 * angle
  cos = math.cos(rad)
  sin = math.sin(rad)
  return np.array([
      [cos, -sin, 0],
      [sin, cos, 0],
      [0, 0, 1]
  ])

# scaling (will stretch the object)


def scaling_around_object_matrix(object: Shape, Sx: Number, Sy: Number) -> np.ndarray:
  to_origin = translation_matrix(-object.center())
  scale = scaling_matrix(Sx, Sy)
  to_center = translation_matrix(+object.center())
  return to_origin.dot(scale.dot(to_center))

# angle in degrees (CLOCKWISE rotation)


def rotation_around_point_matrix(axis: Point, angle: Number) -> np.ndarray:
  to_origin = translation_matrix(-axis)
  rotate = rotation_matrix(angle)
  to_center = translation_matrix(+axis)
  return to_origin.dot(rotate.dot(to_center))

# angle in degrees (CLOCKWISE rotation)


def rotation_around_object_matrix(object: Shape, angle: Number) -> np.ndarray:
  return rotation_around_point_matrix(object.center(), angle)
