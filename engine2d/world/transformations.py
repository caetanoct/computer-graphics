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
import numpy, math
from engine2d.world.geometry import Shape

# translates given point in Dx,Dy
def translation_matrix(Dx: Number, Dy: Number) -> numpy.matrix:
	return [
		[1 ,0 ,0],
		[0 ,1 ,0],
		[Dx,Dy,1]
	]

# scaling (will move the object)
<<<<<<< HEAD
def scaling_matrix(Sx, Sy):
	scaling_matrix=[[Sx,0,0], [0,Sy,0],[0,0,1]]
	return scaling_matrix
# angle in radians
def rotation_matrix(angle):
	rotation_matrix=[[math.cos(angle), -math.sin(angle),0], [math.sin(angle),math.cos(angle),0], [0,0,1]]
	return rotation_matrix
# checks the type of the object and transform it
def transform_object(shape, matrix):
	if type(shape) == Point:
		return transform(shape, matrix)
	if type(shape) == Line:		
		return Line(transform(shape.begin, matrix),transform(shape.end, matrix))
	if type(shape) == Polygon:
		points_t=[]
		for point in shape.points:
			points_t.append(transform(point,matrix))
		return Polygon(points_t)
=======
def scaling_matrix(Sx: Number, Sy: Number) -> numpy.matrix:
	return [
		[Sx,0 ,0],
		[0 ,Sy,0],
		[0 ,0 ,1]
	]

# angle in radians (CLOCKWISE rotation)
def rotation_matrix(angle: Number) -> numpy.matrix:
	cos = math.cos(angle)
	sin = math.sin(angle)
	return [
		[cos,-sin , 0],
		[sin, cos , 0],
		[0  , 0   , 1]
	]

# angle in radians (CLOCKWISE rotation)
def rotation_around_object_matrix(object: Shape, angle: Number) -> numpy.matrix:
	to_origin = translation_matrix(-object.center())
	rotate = rotation_matrix(angle)
	to_center = to_origin * (-1)
	return to_origin * rotate * to_center

>>>>>>> 092652ec6292b51d0ad16c293b2154b58686645f
# pi radians = 180degrees
#test_line=Line(Point(2,2),Point(200,200))
#test_polygon=Polygon([Point(100,100),Point(200,200),Point(200,100)])
#print(transform_object(test_line,scaling_matrix(2,2)))
#print(transform_object(test_polygon,scaling_matrix(2,2)))
#print(transform_object(test_line,rotation_matrix(math.pi/2)))
#print(transform(Point(2,2), rotation_matrix(math.pi/2)))