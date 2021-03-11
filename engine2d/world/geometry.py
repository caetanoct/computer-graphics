from dataclasses import dataclass
from typing import List, Union, Optional
import numpy


# rotate(circular-shift) a list, by "n" steps
def rotate(l, n):
  return l[-n:] + l[:-n]


# data structure that representas a point (x,y)
class Point(numpy.ndarray):
  x: float
  y: float

  def __new__(cls, x, y):    
    return numpy.asarray([x, y]).view(cls)

  @property
  def x(self):
    return self[0]

  @property
  def y(self):
    return self[1]  
  # general transforming function, we can use this to any kind of transformation given the right matrix
  def transform(self, matrix: numpy.matrix):
    if len(matrix) > 3:
      raise "ERROR: given matrix has more than 3 lines"
    if len(matrix[0]) > 3:
      raise "ERROR: given matrix has more than 3 columns"
    vec = numpy.array([self.x, self.y, 1])
    res = matrix.dot(vec)
    return Point(res[0], res[1])

  def center(self):
    return self

  def __eq__(self, other):
    return numpy.array_equal(self, other)

  def __str__(self):
    return "({}, {})".format(self.x, self.y)

  def __repr__(self):
    return str(self)

  def abs(self):
    return numpy.linalg.norm(self)

# it's the same as a Point, but has different semantics(meaning)


class Vector(Point):
  pass


# forward definition of Line(see below for full definition)
class Line:
  pass


# data structure that represents a Polygon (list of connected points)
class Polygon:
  points: List[Point]

  def __init__(self, *points):
    self.points = points

  # applies a matrix to the points of the polygon and returns a new Polygon
  def transform(self, matrix: numpy.matrix):
    return self.__class__(
        *[point.transform(matrix) for point in self.points])

  def center(self):
    n = len(self.points)
    center_x = sum([point.x for point in self.points]) / n
    center_y = sum([point.y for point in self.points]) / n
    return Point(center_x, center_y)

  # returns a list of the edges that the polygon consists of
  # get points[i] with [i+1] mod len(points)
  def edges(self) -> List[Line]:
    # an iterator of tuples where the first item in each passed iterator is paired together, and then the second item in each passed iterator are paired together...
    return [
        Line(a, b) for (a, b) in zip(self.points, rotate(self.points, -1))
    ]

  def __str__(self):
    return str(self.points)

  def __eq__(self, other):
    return all(a == b for (a, b) in zip(self.points, other.points))


# data structure that rerpresents a line (two connected point), that is a 2d polygon
class Line(Polygon):
  begin: Point
  end: Point

  def __init__(self, begin, end):
    self.begin = begin
    self.end = end
    super().__init__(begin, end)

  def angular_coefficient(self):
    deltax = self.end.x-self.begin.x
    deltay = self.end.y-self.begin.y
    if (deltax==0):
      print("deltax == 0!")
    return (deltay/deltax)
# A shape is either a Polygon, a Line or a Point
Shape = Union[Polygon, Line, Point]


@dataclass
# data structure that contains 2 points that define the box, (x_min,y_min) and (x_max,y_max)
class Box:
  x_min: float
  y_min: float
  x_max: float
  y_max: float

  def width(self):
    return self.x_max - self.x_min

  def height(self):
    return self.y_max - self.y_min

  def center(self):
    center_x = (self.x_min + self.x_max) / 2
    center_y = (self.y_min + self.y_max) / 2
    return Point(center_x, center_y)

  def is_point_inside(self, p: Point):
    inside_horizontal = self.x_min < p.x and p.x < self.x_max
    inside_vertical = self.y_min < p.y and p.y < self.y_max
    return inside_horizontal and inside_vertical

  def get_point_region_code(self, p: Point):
    region_code = 0
    # 8  = 1000
    # 7  = 0111
    # 4  = 0100
    # 11 = 1011
    # 2  = 0010
    # 13 = 1101
    # 1  = 0001
    # 14 = 1110    
    # CHECK X COORDINATES OF POINT
    if p.x < self.x_min:
      # rc[4] = 1
      region_code |= 1      
    else:
      # rc[4] = 0
      region_code &= 14      
    if p.x > self.x_max:
      # rc[3] = 1
      region_code |= 2      
    else:
      # rc[3] = 0
      region_code &= 13      
    if p.y < self.y_min:
      # rc[2] = 1
      region_code |= 4      
    else:
      # rc[2] = 0
      region_code &= 11      
    if p.y > self.y_max:
      # rc[1] = 1
      region_code |= 8      
    else:
      # rc[1] = 0
      region_code &= 7    
    return region_code
  
  def clip_left(self,line):
    y_intersec = line.angular_coefficient() * (self.x_min - line.end.x) + line.end.y
    return y_intersec
  def clip_right(self,line):
    y_intersec = line.angular_coefficient() * (self.x_max - line.end.x) + line.end.y
    return y_intersec
  def clip_bottom(self,line):
    x_intersec = line.end.x + ((1/line.angular_coefficient()) * (self.y_min - line.end.y))
    return x_intersec
  def clip_top(self,line):
    x_intersec = line.end.x + ((1/line.angular_coefficient()) * (self.y_max - line.end.y))
    return x_intersec
  def x_in_window(self,x):
    return (x >= self.x_min and x <= self.x_max)
  def y_in_window(self,y):
    return (y >= self.y_min and y <= self.y_max)
  # cohen-sutherland
  def clip_line(self, line: Line) -> Optional[Line]:    
    # rc[1] - above
    # rc[2] - down
    # rc[3] - right
    # rc[4] - left
    # |------|------|------|
    # | 1001 | 1000 | 1010 |
    # |------|------|------|
    # | 0001 | 0000 | 0010 |
    # |------|------|------|
    # | 0101 | 0100 | 0110 |
    # |------|------|------|

    # first part, match region codes to line points    
    begin_region_code = self.get_point_region_code(line.begin)
    end_region_code = self.get_point_region_code(line.end)
    # second part, determine if totally visible/invisible or parcially.

    # line is 100% inside window
    if (begin_region_code == end_region_code) and (end_region_code == 0):      
      return line
    # completely outside    
    if begin_region_code & end_region_code != 0:      
      return None
    # parcially, if parcially visible we have to calculate the intersections and return the altered_line
    if begin_region_code != end_region_code and ((begin_region_code & end_region_code) == 0):
      # bottom - topright or topright - bottom
      if (begin_region_code == 4 and end_region_code == 10) or (begin_region_code == 10 and end_region_code == 4):        
        x_1 = self.clip_bottom(line)
        if self.x_in_window(x_1):
          p1 = Point(x_1,self.y_min)
          x_2 = self.clip_top(line)
          if self.x_in_window(x_2):
            p2 = Point(x_2,self.y_max)
            return Line(p1,p2)
          y_2 = self.clip_right(line)
          if self.y_in_window(y_2):
            p2 = Point(self.x_max,y_2)
            return Line(p1,p2)          
        return None         
      # bottom - topleft or topleft - bottom
      if (begin_region_code == 4 and end_region_code == 9) or (begin_region_code == 9 and end_region_code == 4):        
        x_1 = self.clip_bottom(line)
        if self.x_in_window(x_1):
          p1 = Point(x_1,self.y_min)
          x_2 = self.clip_top(line)
          if self.x_in_window(x_2):
            p2 = Point(x_2,self.y_max)
            return Line(p1,p2)
          y_2 = self.clip_left(line)
          if self.y_in_window(y_2):
            p2 = Point(self.x_min,y_2)
            return Line(p1,p2)          
        return None      
      # left - topright or topright - left
      if (begin_region_code == 1 and end_region_code == 10) or (begin_region_code == 10 and end_region_code == 1):        
        y_1 = self.clip_left(line)
        if self.y_in_window(y_1):
          p1=Point(self.x_min,y_1)
          x_2 = self.clip_top(line)
          if self.x_in_window(x_2):
            p2=Point(x_2,self.y_max)
            return Line(p1,p2)
          y_2 = self.clip_right(line)
          if self.y_in_window(y_2):
            p2=Point(self.x_max,y_2)
            return Line(p1,p2)
        return None 
      # right - topleft or topleft - right      
      if (begin_region_code == 2 and end_region_code == 9) or (begin_region_code == 9 and end_region_code == 2):        
        y_1 = self.clip_right(line)
        if self.y_in_window(y_1):
          p1=Point(self.x_max,y_1)
          x_2 = self.clip_top(line)
          if self.x_in_window(x_2):
            p2=Point(x_2,self.y_max)
            return Line(p1,p2)
          y_2 = self.clip_left(line)
          if self.y_in_window(y_2):
            p2=Point(self.x_min,y_2)
            return Line(p1,p2)
        return None
      # left - bottomright or bottomright - left
      if (begin_region_code == 1 and end_region_code == 6) or (begin_region_code == 6 and end_region_code == 1):        
        y_1 = self.clip_left(line)
        if self.y_in_window(y_1):
          p1=Point(self.x_min,y_1)
          x_2 = self.clip_bottom(line)
          if self.x_in_window(x_2):
            p2=Point(x_2,self.y_min)
            return Line(p1,p2)
          y_2 = self.clip_right(line)
          if self.y_in_window(y_2):
            p2=Point(self.x_max,y_2)
            return Line(p1,p2)
        return None  
      # right - bottomleft or bottomleft - right
      if (begin_region_code == 2 and end_region_code == 5) or (begin_region_code == 5 and end_region_code == 2):        
        y_1 = self.clip_right(line)
        if self.y_in_window(y_1):
          p1=Point(self.x_max,y_1)
          x_2 = self.clip_bottom(line)
          if self.x_in_window(x_2):
            p2=Point(x_2,self.y_min)
            return Line(p1,p2)
          y_2 = self.clip_left(line)
          if self.y_in_window(y_2):
            p2=Point(self.x_min,y_2)
            return Line(p1,p2)
        return None      
      # top - bottomright or bottomright - top
      if (begin_region_code == 8 and end_region_code == 6) or (begin_region_code == 6 and end_region_code == 8):        
        x_intersec = self.clip_top(line)
        x_2 = self.clip_bottom(line)
        if self.x_in_window(x_2):          
          return Line(Point(x_intersec,self.y_max),Point(x_2,self.y_min))
        y_2 = self.clip_right(line)
        if self.y_in_window(y_2):          
          return Line(Point(x_intersec,self.y_max),Point(self.x_max,y_2))
        return None
      # top - bottomleft or bottomleft - top
      if (begin_region_code == 8 and end_region_code == 5) or (begin_region_code == 5 and end_region_code == 8):
        x_intersec = self.clip_top(line)
        x_2 = self.clip_bottom(line)
        if self.x_in_window(x_2):
          return Line(Point(x_intersec,self.y_max),Point(x_2,self.y_min))
        y_2 = self.clip_left(line)
        if self.y_in_window(y_2):
          return Line(Point(x_intersec,self.y_max),Point(self.x_min,y_2))
        return None            
      # topright - bottomleft or bottomleft - topright
      if (begin_region_code == 10 and end_region_code == 5) or (begin_region_code == 5 and end_region_code == 10):                    
        # clip top
        x_1 = self.clip_top(line)
        if self.x_in_window(x_1):
          y_1 = self.clip_left(line)
          if self.y_in_window(y_1):
            return Line(Point(x_1,self.y_max),Point(self.x_min,y_1))
        # clip right
        y_1 = self.clip_right(line)
        if self.y_in_window(y_1):
          x_1 = self.clip_bottom(line)
          if self.x_in_window(x_1):
            return Line(Point(x_1,self.y_min),Point(self.x_max,y_1))        
        return None       
      # topleft - bottomright or bottom-right - topleft
      if (begin_region_code == 9 and end_region_code == 6) or (begin_region_code == 6 and end_region_code == 9):
        # clip top
        x_1 = self.clip_top(line)
        if self.x_in_window(x_1):
          y_1 = self.clip_right(line)
          if self.y_in_window(y_1):
            return Line(Point(x_1,self.y_max),Point(self.x_max,y_1))
        # clip left
        y_1 = self.clip_left(line)
        if self.y_in_window(y_1):
          x_1 = self.clip_bottom(line)
          if self.x_in_window(x_1):
            return Line(Point(x_1,self.y_min),Point(self.x_min,y_1))        
        return None
      # top - bottom and bottom - top
      if (begin_region_code == 8 and end_region_code == 4) or (begin_region_code == 4 and end_region_code == 8):
        #clip top and bottom
        x_intersec_1 = self.clip_top(line)
        x_intersec_2 = self.clip_bottom(line)
        if self.x_in_window(x_intersec_1) and self.x_in_window(x_intersec_2):
          return Line(Point(x_intersec_1, self.y_min),Point(x_intersec_2,self.y_max))
      # left - right and right-left
      if (begin_region_code == 1 and end_region_code == 2) or (begin_region_code == 2 and end_region_code == 1):
        #clip right and left
        y_intersec_1 = self.clip_right(line)
        y_intersec_2 = self.clip_left(line)
        if self.y_in_window(y_intersec_1) and self.y_in_window(y_intersec_2):
          return Line(Point(self.x_min, y_intersec_1),Point(self.x_max,y_intersec_2))      
      # center - bottomleft
      if (begin_region_code == 0 and end_region_code == 5):
        # clip bottom        
        x_intersec = self.clip_bottom(line)
        if self.x_in_window(x_intersec):
          return Line(line.begin, Point(x_intersec,self.y_min))
        # clip left
        else:
          y_intersec = self.clip_left(line)
          if self.y_in_window(y_intersec):
            return Line(line.begin, Point(self.x_min,y_intersec))
      # bottomleft - center
      if (begin_region_code == 5 and end_region_code == 0):
        # clip bottom        
        x_intersec = self.clip_bottom(line)
        if self.x_in_window(x_intersec):
          return Line(line.end, Point(x_intersec,self.y_min))
        # clip left
        else:
          y_intersec = self.clip_left(line)
          if self.y_in_window(y_intersec):
            return Line(line.end, Point(self.x_min,y_intersec))
      # center - bottomright      
      if (begin_region_code == 0 and end_region_code == 6):
        # clip bottom        
        x_intersec = self.clip_bottom(line)
        if self.x_in_window(x_intersec):
          return Line(line.begin, Point(x_intersec,self.y_min))
        # clip right
        else:
          y_intersec = self.clip_right(line)
          if self.y_in_window(y_intersec):
            return Line(line.begin, Point(self.x_max,y_intersec))
      # bottomright-center
      if (begin_region_code == 6 and end_region_code == 0):
        # clip bottom        
        x_intersec = self.clip_bottom(line)
        if self.x_in_window(x_intersec):
          return Line(line.end, Point(x_intersec,self.y_min))
        # clip right
        else:
          y_intersec = self.clip_right(line)
          if self.y_in_window(y_intersec):
            return Line(line.end, Point(self.x_max,y_intersec))
      # center - topleft      
      if (begin_region_code == 0 and end_region_code == 9):
        # clip top        
        x_intersec = self.clip_top(line)
        if self.x_in_window(x_intersec):
          return Line(line.begin, Point(x_intersec,self.y_max))
        # clip left
        else:
          y_intersec = self.clip_left(line)
          if self.y_in_window(y_intersec):
            return Line(line.begin, Point(self.x_min,y_intersec))
      # topleft - center
      if (begin_region_code == 9 and end_region_code == 0):
        # clip top        
        x_intersec = self.clip_top(line)
        if self.x_in_window(x_intersec):
          return Line(line.end, Point(x_intersec,self.y_max))
        # clip left
        else:
          y_intersec = self.clip_left(line)
          if self.y_in_window(y_intersec):
            return Line(line.end, Point(self.x_min,y_intersec))
      # center - topright
      if (begin_region_code == 0 and end_region_code == 10):
        # clip top        
        x_intersec = line.end.x + ((1/line.angular_coefficient()) * (self.y_max - line.end.y))
        if x_intersec >= self.x_min and x_intersec <= self.x_max:
          return Line(line.begin, Point(x_intersec,self.y_max))
        # clip right
        else:
          y_intersec = line.angular_coefficient() * (self.x_max - line.end.x) + line.end.y
          if y_intersec >= self.y_min and y_intersec <= self.y_max:
            return Line(line.begin, Point(self.x_max,y_intersec))
      # topright - center
      if (begin_region_code == 10 and end_region_code == 0):
        # clip top        
        x_intersec = line.begin.x + ((1/line.angular_coefficient()) * (self.y_max - line.begin.y))
        if x_intersec >= self.x_min and x_intersec <= self.x_max:
          return Line(line.end, Point(x_intersec,self.y_max))
        # clip right
        else:
          y_intersec = line.angular_coefficient() * (self.x_max - line.begin.x) + line.begin.y
          if y_intersec >= self.y_min and y_intersec <= self.y_max:
            return Line(line.end, Point(self.x_max,y_intersec))
      # left - top and top - left, clipt left and calculate new y , clip top and calculate new x
      if (begin_region_code == 1 and end_region_code == 8) or (begin_region_code == 8 and end_region_code == 1):        
        y_intersec = line.angular_coefficient() * (self.x_min - line.begin.x) + line.begin.y
        if y_intersec >= self.y_min and y_intersec <= self.y_max:
          pass
        else:
          return None
        x_intersec = line.end.x + ((1/line.angular_coefficient()) * (self.y_max - line.end.y))
        if x_intersec >= self.x_min and x_intersec <= self.x_max:          
          return Line(Point(self.x_min,y_intersec), Point(x_intersec,self.y_max))
        else:
          return None
      # right - top and top - right, clipt right and calculate new y , clip top and calculate new x
      if (begin_region_code == 2 and end_region_code == 8) or (begin_region_code == 8 and end_region_code == 2):
        y_intersec = line.angular_coefficient() * (self.x_max - line.begin.x) + line.begin.y
        if y_intersec >= self.y_min and y_intersec <= self.y_max:
          pass
        else:
          return None
        x_intersec = line.end.x + ((1/line.angular_coefficient()) * (self.y_max - line.end.y))
        if x_intersec >= self.x_min and x_intersec <= self.x_max:          
          return Line(Point(self.x_max,y_intersec), Point(x_intersec,self.y_max))
        else:
          return None
      # right - bottom and bottom-right, clipt right and calculate new y , clip bottom and calculate new x
      if (begin_region_code == 2 and end_region_code == 4) or (begin_region_code == 4 and end_region_code == 2):
        y_intersec = line.angular_coefficient() * (self.x_max - line.begin.x) + line.begin.y
        if y_intersec >= self.y_min and y_intersec <= self.y_max:
          pass
        else:
          return None
        x_intersec = line.end.x + ((1/line.angular_coefficient()) * (self.y_min - line.end.y))
        if x_intersec >= self.x_min and x_intersec <= self.x_max:          
          return Line(Point(self.x_max,y_intersec), Point(x_intersec,self.y_min))
        else:
          return None
      # left - bottom and bottom - left, clipt left and calculate new y , clip bottom and calculate new x
      if (begin_region_code == 1 and end_region_code == 4) or (begin_region_code == 4 and end_region_code == 1):
        y_intersec = self.clip_left(line)
        if not(self.y_in_window(y_intersec)):
          return None          
        else:
          x_intersec = self.clip_bottom(line)
          if not(self.x_in_window(x_intersec)):
            return None
          else:
            return Line(Point(self.x_min,y_intersec), Point(x_intersec,self.y_min))
      # left - center, clip left and calculate new y
      if begin_region_code == 1 and end_region_code == 0:
        y_intersec = line.angular_coefficient() * (self.x_min - line.begin.x) + line.begin.y
        if y_intersec >= self.y_min and y_intersec <= self.y_max:
          return Line(Point(self.x_min,y_intersec), line.end)
      # right - center, clip right and calculate new y
      if begin_region_code == 2 and end_region_code == 0:
        y_intersec = line.angular_coefficient() * (self.x_max - line.begin.x) + line.begin.y
        if y_intersec >= self.y_min and y_intersec <= self.y_max:
          return Line(Point(self.x_max,y_intersec), line.end)
      # top - center, clip top and calculate new x
      if begin_region_code == 8 and end_region_code == 0:
        x_intersec = line.begin.x + ((1/line.angular_coefficient()) * (self.y_max - line.begin.y))
        if x_intersec >= self.x_min and x_intersec <= self.x_max:
          return Line(Point(x_intersec,self.y_max), line.end)
      # center - right, clip right and calculate new y
      if begin_region_code == 0 and end_region_code == 2:
        y_intersec = line.angular_coefficient() * (self.x_max - line.end.x) + line.end.y
        if y_intersec >= self.y_min and y_intersec <= self.y_max:
          return Line(line.begin, Point(self.x_max,y_intersec))
      # center - left, clip left and calculate new y
      if begin_region_code == 0 and end_region_code == 1:
        y_intersec = line.angular_coefficient() * (self.x_min - line.end.x) + line.end.y
        if y_intersec >= self.y_min and y_intersec <= self.y_max:
          return Line(line.begin, Point(self.x_min,y_intersec))
      # center - top, clip top and calculate new x
      if begin_region_code == 0 and end_region_code == 8:
        x_intersec = line.end.x + ((1/line.angular_coefficient()) * (self.y_max - line.end.y))        
        if x_intersec >= self.x_min and x_intersec <= self.x_max:
          return Line(line.begin, Point(x_intersec,self.y_max))

      # bottom - center, clip bottom and calculate new x
      if begin_region_code == 4 and end_region_code == 0:
        x_intersec = self.clip_bottom(line)
        if self.x_in_window(x_intersec):
          return Line(line.end,Point(x_intersec,self.y_min))
      # center - bottom, clip bottom and calculate new x
      if begin_region_code == 0 and end_region_code == 4:
        x_intersec = self.clip_bottom(line)
        if self.x_in_window(x_intersec):
          return Line(line.begin, Point(x_intersec,self.y_min))
      print("parcially inside/outside window.")
      return line