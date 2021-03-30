import numpy

class Point3D():
	def __init__(self, x: float, y: float, z: float):		
		self.x = x
		self.y = y
		self.z = z
	def __str__(self):
		return "({},{},{})".format(self.x,self.y,self.z)
class Line3D():
	def __init__(self, begin: Point3D, end: Point3D):
		self.begin = begin
		self.end = end
class Object3D():
	def __init__(self, lines):		
		self.lines = lines
class Transform3D:

	def scale(sx, sy, sz, point3d):
		x1 = sx * point3d.x
		y1 = sy * point3d.y
		z1 = sz * point3d.z
		return Point3D(x1,y1,z1)

	def traverse(tx, ty, tz, point3d):
		x1 = tx + point3d.x
		y1 = ty + point3d.y
		z1 = tz + point3d.z
		return Point3D(x1,y1,z1)

	def rotate_x(angle, point3d):
		sin = numpy.sin(angle) 
		cos = numpy.cos(angle)
		point_matrix = numpy.array(
				[point3d.x, point3d.y, point3d.z, 1])
		rotate_matrix = numpy.array((
				[1, 0, 0, 0],
				[0, cos, sin, 0],
				[0, -sin, cos, 0],
				[0, 0, 0, 1]))
		result = numpy.dot(point_matrix, rotate_matrix)
		return Point3D(result[0],result[1],result[2])

	def rotate_y(angle, point3d):
		sin = numpy.sin(angle) 
		cos = numpy.cos(angle)
		point_matrix = numpy.array((
				[point3d.x, point3d.y, point3d.z, 1]))
		rotate_matrix = numpy.array((
				[cos, 0, -sin, 0],
				[0, 1, 0, 0],
				[sin, 0, cos, 0],
				[0, 0, 0, 1])) 
		result = numpy.dot(point_matrix, rotate_matrix)
		return Point3D(result[0],result[1],result[2])

	def rotate_z(angle, point3d):
		sin = numpy.sin(angle) 
		cos = numpy.cos(angle)
		point_matrix = numpy.array(
				[point3d.x, point3d.y, point3d.z, 1])
		rotate_matrix = numpy.array((
				[cos, sin, 0, 0],
				[-sin, cos, 0, 0],
				[0, 0, 1, 0],
				[0, 0, 0, 1]))
		result = numpy.dot(point_matrix, rotate_matrix)
		return Point3D(result[0],result[1],result[2])

print(Transform3D.rotate_x(10,Point3D(2,2,2)))
print(Transform3D.rotate_y(10,Point3D(2,2,2)))
print(Transform3D.rotate_z(10,Point3D(2,2,2)))
print(Transform3D.traverse(10,10,2,Point3D(2,2,2)))
print(Transform3D.scale(1,2,3,Point3D(2,2,2)))