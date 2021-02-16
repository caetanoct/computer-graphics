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
# rotation - clockwise  [x' y' 1] = [x y 1] * [cos_ -sin_ 0]	#
#											  [sin_  cos_ 0]	#
#											  [0     0    1]	#
#---------------------------------------------------------------#
#
# TODO: implement translation of objects, scaling (without deslocating), rotations (around the world, around the object, around an arbitrary point)
#
from engine2d.world.geometry import Point, Line, Polygon
from typing import List
import numpy, math
# general transforming function, we can use this to any kind of transformation given the right matrix
def transform(point: Point, matrix):
	if (len(matrix)>3):
		print("ERROR: given matrix has more than 3 lines")
	if (len(matrix[0])>3):
		print("ERROR: given matrix has more than 3 columns")
	matrix_1=[point.x,point.y,1]
	matrix_2=matrix
	matrix_result=numpy.matmul(matrix_1,matrix_2)
	return Point(matrix_result[0],matrix_result[1])
# translates given point in Dx,Dy
def translation_matrix(Dx, Dy):
	translation_matrix=[[1,0,0], [0,1,0],[Dx,Dy,1]]
	return translation_matrix
# scaling (will move the object)
def scaling_matrix(Sx, Sy):
	scaling_matrix=[[Sx,0,0], [0,Sy,0],[0,0,1]]
	return scaling_matrix
# angle in radians (CLOCKWISE rotation)
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
# pi radians = 180degrees
#test_line=Line(Point(2,2),Point(200,200))
#test_polygon=Polygon([Point(100,100),Point(200,200),Point(200,100)])
#print(transform_object(test_line,scaling_matrix(2,2)))
#print(transform_object(test_polygon,scaling_matrix(2,2)))
#print(transform_object(test_line,rotation_matrix(math.pi/2)))