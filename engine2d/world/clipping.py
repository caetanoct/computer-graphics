from .geometry import *
from typing import Optional


def cohen_sutherland_line_clipping(window, line: Line) -> Optional[Line]:
  def get_point_region_code(window, p: Point):
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
    if p.x < window.u_min:
      # rc[4] = 1
      region_code |= 1
    else:
      # rc[4] = 0
      region_code &= 14
    if p.x > window.u_max:
      # rc[3] = 1
      region_code |= 2
    else:
      # rc[3] = 0
      region_code &= 13
    if p.y < window.v_min:
      # rc[2] = 1
      region_code |= 4
    else:
      # rc[2] = 0
      region_code &= 11
    if p.y > window.v_max:
      # rc[1] = 1
      region_code |= 8
    else:
      # rc[1] = 0
      region_code &= 7
    return region_code

  def clip_left(window, line: Line):
    y_intersec = line.angular_coefficient() * (window.u_min - line.end.x) + line.end.y
    return y_intersec

  def clip_right(window, line: Line):
    y_intersec = line.angular_coefficient() * (window.u_max - line.end.x) + line.end.y
    return y_intersec

  def clip_bottom(window, line: Line):
    x_intersec = line.end.x + \
        ((1/line.angular_coefficient()) * (window.v_min - line.end.y))
    return x_intersec

  def clip_top(window, line: Line):
    x_intersec = line.end.x + \
        ((1/line.angular_coefficient()) * (window.v_max - line.end.y))
    return x_intersec

  def x_in_window(window, x):
    return (x >= window.u_min and x <= window.u_max)

  def y_in_window(window, y):
    return (y >= window.v_min and y <= window.v_max)
  # cohen-sutherland

  # def clip_line(window, line: Line) -> Optional[Line]:
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
  begin_region_code = get_point_region_code(window, line.begin)
  end_region_code = get_point_region_code(window, line.end)
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
      x_1 = clip_bottom(window, line)
      if x_in_window(window, x_1):
        p1 = Point(x_1, window.v_min)
        x_2 = clip_top(window, line)
        if x_in_window(window, x_2):
          p2 = Point(x_2, window.v_max)
          return Line(p1, p2)
        y_2 = clip_right(window, line)
        if y_in_window(window, y_2):
          p2 = Point(window.u_max, y_2)
          return Line(p1, p2)
      return None
    # bottom - topleft or topleft - bottom
    if (begin_region_code == 4 and end_region_code == 9) or (begin_region_code == 9 and end_region_code == 4):
      x_1 = clip_bottom(window, line)
      if x_in_window(window, x_1):
        p1 = Point(x_1, window.v_min)
        x_2 = clip_top(window, line)
        if x_in_window(window, x_2):
          p2 = Point(x_2, window.v_max)
          return Line(p1, p2)
        y_2 = clip_left(window, line)
        if y_in_window(window, y_2):
          p2 = Point(window.u_min, y_2)
          return Line(p1, p2)
      return None
    # left - topright or topright - left
    if (begin_region_code == 1 and end_region_code == 10) or (begin_region_code == 10 and end_region_code == 1):
      y_1 = clip_left(window, line)
      if y_in_window(window, y_1):
        p1 = Point(window.u_min, y_1)
        x_2 = clip_top(window, line)
        if x_in_window(window, x_2):
          p2 = Point(x_2, window.v_max)
          return Line(p1, p2)
        y_2 = clip_right(window, line)
        if y_in_window(window, y_2):
          p2 = Point(window.u_max, y_2)
          return Line(p1, p2)
      return None
    # right - topleft or topleft - right
    if (begin_region_code == 2 and end_region_code == 9) or (begin_region_code == 9 and end_region_code == 2):
      y_1 = clip_right(window, line)
      if y_in_window(window, y_1):
        p1 = Point(window.u_max, y_1)
        x_2 = clip_top(window, line)
        if x_in_window(window, x_2):
          p2 = Point(x_2, window.v_max)
          return Line(p1, p2)
        y_2 = clip_left(window, line)
        if y_in_window(window, y_2):
          p2 = Point(window.u_min, y_2)
          return Line(p1, p2)
      return None
    # left - bottomright or bottomright - left
    if (begin_region_code == 1 and end_region_code == 6) or (begin_region_code == 6 and end_region_code == 1):
      y_1 = clip_left(window, line)
      if y_in_window(window, y_1):
        p1 = Point(window.u_min, y_1)
        x_2 = clip_bottom(window, line)
        if x_in_window(window, x_2):
          p2 = Point(x_2, window.v_min)
          return Line(p1, p2)
        y_2 = clip_right(window, line)
        if y_in_window(window, y_2):
          p2 = Point(window.u_max, y_2)
          return Line(p1, p2)
      return None
    # right - bottomleft or bottomleft - right
    if (begin_region_code == 2 and end_region_code == 5) or (begin_region_code == 5 and end_region_code == 2):
      y_1 = clip_right(window, line)
      if y_in_window(window, y_1):
        p1 = Point(window.u_max, y_1)
        x_2 = clip_bottom(window, line)
        if x_in_window(window, x_2):
          p2 = Point(x_2, window.v_min)
          return Line(p1, p2)
        y_2 = clip_left(window, line)
        if y_in_window(window, y_2):
          p2 = Point(window.u_min, y_2)
          return Line(p1, p2)
      return None
    # top - bottomright or bottomright - top
    if (begin_region_code == 8 and end_region_code == 6) or (begin_region_code == 6 and end_region_code == 8):
      x_intersec = clip_top(window, line)
      x_2 = clip_bottom(window, line)
      if x_in_window(window, x_2):
        return Line(Point(x_intersec, window.v_max), Point(x_2, window.v_min))
      y_2 = clip_right(window, line)
      if y_in_window(window, y_2):
        return Line(Point(x_intersec, window.v_max), Point(window.u_max, y_2))
      return None
    # top - bottomleft or bottomleft - top
    if (begin_region_code == 8 and end_region_code == 5) or (begin_region_code == 5 and end_region_code == 8):
      x_intersec = clip_top(window, line)
      x_2 = clip_bottom(window, line)
      if x_in_window(window, x_2):
        return Line(Point(x_intersec, window.v_max), Point(x_2, window.v_min))
      y_2 = clip_left(window, line)
      if y_in_window(window, y_2):
        return Line(Point(x_intersec, window.v_max), Point(window.u_min, y_2))
      return None
    # topright - bottomleft or bottomleft - topright
    if (begin_region_code == 10 and end_region_code == 5) or (begin_region_code == 5 and end_region_code == 10):
      # clip top
      x_1 = clip_top(window, line)
      if x_in_window(window, x_1):
        y_1 = clip_left(window, line)
        if y_in_window(window, y_1):
          return Line(Point(x_1, window.v_max), Point(window.u_min, y_1))
      # clip right
      y_1 = clip_right(window, line)
      if y_in_window(window, y_1):
        x_1 = clip_bottom(window, line)
        if x_in_window(window, x_1):
          return Line(Point(x_1, window.v_min), Point(window.u_max, y_1))
      return None
    # topleft - bottomright or bottom-right - topleft
    if (begin_region_code == 9 and end_region_code == 6) or (begin_region_code == 6 and end_region_code == 9):
      # clip top
      x_1 = clip_top(window, line)
      if x_in_window(window, x_1):
        y_1 = clip_right(window, line)
        if y_in_window(window, y_1):
          return Line(Point(x_1, window.v_max), Point(window.u_max, y_1))
      # clip left
      y_1 = clip_left(window, line)
      if y_in_window(window, y_1):
        x_1 = clip_bottom(window, line)
        if x_in_window(window, x_1):
          return Line(Point(x_1, window.v_min), Point(window.u_min, y_1))
      return None
    # top - bottom and bottom - top
    if (begin_region_code == 8 and end_region_code == 4) or (begin_region_code == 4 and end_region_code == 8):
      # clip top and bottom
      x_intersec_1 = clip_top(window, line)
      x_intersec_2 = clip_bottom(window, line)
      if x_in_window(window, x_intersec_1) and x_in_window(window, x_intersec_2):
        return Line(Point(x_intersec_1, window.v_min), Point(x_intersec_2, window.v_max))
    # left - right and right-left
    if (begin_region_code == 1 and end_region_code == 2) or (begin_region_code == 2 and end_region_code == 1):
      # clip right and left
      y_intersec_1 = clip_right(window, line)
      y_intersec_2 = clip_left(window, line)
      if y_in_window(window, y_intersec_1) and y_in_window(window, y_intersec_2):
        return Line(Point(window.u_min, y_intersec_1), Point(window.u_max, y_intersec_2))
    # center - bottomleft
    if (begin_region_code == 0 and end_region_code == 5):
      # clip bottom
      x_intersec = clip_bottom(window, line)
      if x_in_window(window, x_intersec):
        return Line(line.begin, Point(x_intersec, window.v_min))
      # clip left
      else:
        y_intersec = clip_left(window, line)
        if y_in_window(window, y_intersec):
          return Line(line.begin, Point(window.u_min, y_intersec))
    # bottomleft - center
    if (begin_region_code == 5 and end_region_code == 0):
      # clip bottom
      x_intersec = clip_bottom(window, line)
      if x_in_window(window, x_intersec):
        return Line(line.end, Point(x_intersec, window.v_min))
      # clip left
      else:
        y_intersec = clip_left(window, line)
        if y_in_window(window, y_intersec):
          return Line(line.end, Point(window.u_min, y_intersec))
    # center - bottomright
    if (begin_region_code == 0 and end_region_code == 6):
      # clip bottom
      x_intersec = clip_bottom(window, line)
      if x_in_window(window, x_intersec):
        return Line(line.begin, Point(x_intersec, window.v_min))
      # clip right
      else:
        y_intersec = clip_right(window, line)
        if y_in_window(window, y_intersec):
          return Line(line.begin, Point(window.u_max, y_intersec))
    # bottomright-center
    if (begin_region_code == 6 and end_region_code == 0):
      # clip bottom
      x_intersec = clip_bottom(window, line)
      if x_in_window(window, x_intersec):
        return Line(line.end, Point(x_intersec, window.v_min))
      # clip right
      else:
        y_intersec = clip_right(window, line)
        if y_in_window(window, y_intersec):
          return Line(line.end, Point(window.u_max, y_intersec))
    # center - topleft
    if (begin_region_code == 0 and end_region_code == 9):
      # clip top
      x_intersec = clip_top(window, line)
      if x_in_window(window, x_intersec):
        return Line(line.begin, Point(x_intersec, window.v_max))
      # clip left
      else:
        y_intersec = clip_left(window, line)
        if y_in_window(window, y_intersec):
          return Line(line.begin, Point(window.u_min, y_intersec))
    # topleft - center
    if (begin_region_code == 9 and end_region_code == 0):
      # clip top
      x_intersec = clip_top(window, line)
      if x_in_window(window, x_intersec):
        return Line(line.end, Point(x_intersec, window.v_max))
      # clip left
      else:
        y_intersec = clip_left(window, line)
        if y_in_window(window, y_intersec):
          return Line(line.end, Point(window.u_min, y_intersec))
    # center - topright
    if (begin_region_code == 0 and end_region_code == 10):
      # clip top
      x_intersec = line.end.x + \
          ((1/line.angular_coefficient()) * (window.v_max - line.end.y))
      if x_intersec >= window.u_min and x_intersec <= window.u_max:
        return Line(line.begin, Point(x_intersec, window.v_max))
      # clip right
      else:
        y_intersec = line.angular_coefficient() * (window.u_max - line.end.x) + line.end.y
        if y_intersec >= window.v_min and y_intersec <= window.v_max:
          return Line(line.begin, Point(window.u_max, y_intersec))
    # topright - center
    if (begin_region_code == 10 and end_region_code == 0):
      # clip top
      x_intersec = line.begin.x + \
          ((1/line.angular_coefficient()) * (window.v_max - line.begin.y))
      if x_intersec >= window.u_min and x_intersec <= window.u_max:
        return Line(line.end, Point(x_intersec, window.v_max))
      # clip right
      else:
        y_intersec = line.angular_coefficient() * (window.u_max - line.begin.x) + \
            line.begin.y
        if y_intersec >= window.v_min and y_intersec <= window.v_max:
          return Line(line.end, Point(window.u_max, y_intersec))
    # left - top and top - left, clipt left and calculate new y , clip top and calculate new x
    if (begin_region_code == 1 and end_region_code == 8) or (begin_region_code == 8 and end_region_code == 1):
      y_intersec = line.angular_coefficient() * (window.u_min - line.begin.x) + \
          line.begin.y
      if y_intersec >= window.v_min and y_intersec <= window.v_max:
        pass
      else:
        return None
      x_intersec = line.end.x + \
          ((1/line.angular_coefficient()) * (window.v_max - line.end.y))
      if x_intersec >= window.u_min and x_intersec <= window.u_max:
        return Line(Point(window.u_min, y_intersec), Point(x_intersec, window.v_max))
      else:
        return None
    # right - top and top - right, clipt right and calculate new y , clip top and calculate new x
    if (begin_region_code == 2 and end_region_code == 8) or (begin_region_code == 8 and end_region_code == 2):
      y_intersec = line.angular_coefficient() * (window.u_max - line.begin.x) + \
          line.begin.y
      if y_intersec >= window.v_min and y_intersec <= window.v_max:
        pass
      else:
        return None
      x_intersec = line.end.x + \
          ((1/line.angular_coefficient()) * (window.v_max - line.end.y))
      if x_intersec >= window.u_min and x_intersec <= window.u_max:
        return Line(Point(window.u_max, y_intersec), Point(x_intersec, window.v_max))
      else:
        return None
    # right - bottom and bottom-right, clipt right and calculate new y , clip bottom and calculate new x
    if (begin_region_code == 2 and end_region_code == 4) or (begin_region_code == 4 and end_region_code == 2):
      y_intersec = line.angular_coefficient() * (window.u_max - line.begin.x) + \
          line.begin.y
      if y_intersec >= window.v_min and y_intersec <= window.v_max:
        pass
      else:
        return None
      x_intersec = line.end.x + \
          ((1/line.angular_coefficient()) * (window.v_min - line.end.y))
      if x_intersec >= window.u_min and x_intersec <= window.u_max:
        return Line(Point(window.u_max, y_intersec), Point(x_intersec, window.v_min))
      else:
        return None
    # left - bottom and bottom - left, clipt left and calculate new y , clip bottom and calculate new x
    if (begin_region_code == 1 and end_region_code == 4) or (begin_region_code == 4 and end_region_code == 1):
      y_intersec = clip_left(window, line)
      if not(y_in_window(window, y_intersec)):
        return None
      else:
        x_intersec = clip_bottom(window, line)
        if not(x_in_window(window, x_intersec)):
          return None
        else:
          return Line(Point(window.u_min, y_intersec), Point(x_intersec, window.v_min))
    # left - center, clip left and calculate new y
    if begin_region_code == 1 and end_region_code == 0:
      y_intersec = line.angular_coefficient() * (window.u_min - line.begin.x) + \
          line.begin.y
      if y_intersec >= window.v_min and y_intersec <= window.v_max:
        return Line(Point(window.u_min, y_intersec), line.end)
    # right - center, clip right and calculate new y
    if begin_region_code == 2 and end_region_code == 0:
      y_intersec = line.angular_coefficient() * (window.u_max - line.begin.x) + \
          line.begin.y
      if y_intersec >= window.v_min and y_intersec <= window.v_max:
        return Line(Point(window.u_max, y_intersec), line.end)
    # top - center, clip top and calculate new x
    if begin_region_code == 8 and end_region_code == 0:
      x_intersec = line.begin.x + \
          ((1/line.angular_coefficient()) * (window.v_max - line.begin.y))
      if x_intersec >= window.u_min and x_intersec <= window.u_max:
        return Line(Point(x_intersec, window.v_max), line.end)
    # center - right, clip right and calculate new y
    if begin_region_code == 0 and end_region_code == 2:
      y_intersec = line.angular_coefficient() * (window.u_max - line.end.x) + line.end.y
      if y_intersec >= window.v_min and y_intersec <= window.v_max:
        return Line(line.begin, Point(window.u_max, y_intersec))
    # center - left, clip left and calculate new y
    if begin_region_code == 0 and end_region_code == 1:
      y_intersec = line.angular_coefficient() * (window.u_min - line.end.x) + line.end.y
      if y_intersec >= window.v_min and y_intersec <= window.v_max:
        return Line(line.begin, Point(window.u_min, y_intersec))
    # center - top, clip top and calculate new x
    if begin_region_code == 0 and end_region_code == 8:
      x_intersec = line.end.x + \
          ((1/line.angular_coefficient()) * (window.v_max - line.end.y))
      if x_intersec >= window.u_min and x_intersec <= window.u_max:
        return Line(line.begin, Point(x_intersec, window.v_max))

    # bottom - center, clip bottom and calculate new x
    if begin_region_code == 4 and end_region_code == 0:
      x_intersec = clip_bottom(window, line)
      if x_in_window(window, x_intersec):
        return Line(line.end, Point(x_intersec, window.v_min))
    # center - bottom, clip bottom and calculate new x
    if begin_region_code == 0 and end_region_code == 4:
      x_intersec = clip_bottom(window, line)
      if x_in_window(window, x_intersec):
        return Line(line.begin, Point(x_intersec, window.v_min))
    print("parcially inside/outside window.")
    return line


def sutherland_hodgeman_polygon_clipping(window, polygon: Polygon) -> Optional[Polygon]:
  def clip_side(polygon: Polygon, axis: InfiniteLine, check_inside):
    new_points = []
    for edge in polygon.edges():
      a, b = edge.begin, edge.end
      a_in, b_in = check_inside(a), check_inside(b)
      if a_in and b_in:
        new_points.extend([a, b])
      if a_in and not b_in:
        new_points.extend([a, axis.intersection(edge)])
      if not a_in and b_in:
        new_points.extend([axis.intersection(edge), b])
      if not a_in and not b_in:
        pass
    return Polygon(*new_points)

  polygon = clip_side(polygon, InfiniteLine(
      1, 0, -window.u_min), lambda p: window.u_min < p.x)
  polygon = clip_side(polygon, InfiniteLine(
      0, 1, -window.v_min), lambda p: window.v_min < p.y)
  polygon = clip_side(polygon, InfiniteLine(
      1, 0, -window.u_max), lambda p: p.x < window.u_max)
  polygon = clip_side(polygon, InfiniteLine(
      0, 1, -window.v_max), lambda p: p.y < window.v_max)

  return polygon
