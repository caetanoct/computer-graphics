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
from geometry import Point
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
def translation(point: Point, Dx, Dy):
	translation_matrix=[[1,0,0], [0,1,0],[Dx,Dy,1]]
	return transform(point,translation_matrix)
# scaling (will move the object)
def regular_scaling(point: Point, Sx, Sy):
	scaling_matrix=[[Sx,0,0], [0,Sy,0],[0,0,1]]
	return transform(point, scaling_matrix)
# angle in radians
def regular_clockwise_rotation(point: Point, angle):
	rotation_matrix=[[math.cos(angle), -math.sin(angle),0], [math.sin(angle),math.cos(angle),0], [0,0,1]]
	return transform(point, rotation_matrix)

# pi radians = 180degrees
print(translation(Point(3,3),-1,-1))
print(regular_scaling(Point(3,3),2,2))
print(regular_clockwise_rotation(Point(3,3),math.pi/2))