from dataclasses import dataclass
from typing import List
from engine2d.world.geometry import Shape, Point, Line, Polygon, Wireframe, BezierCurve, B_SplineCurve
from engine2d.world.window import Window
from engine2d.ui.drawing_context import DrawingContext


@dataclass
class World:
  # world display file
  shapes: List[Shape]

  # it was told that this was the recommended window bounds
  # but it so happens that this makes the scaling matrix half every coordinates
  # so we are halving the bounds, so the scaling matrix is the identity(it eases the tests)
  # window = Window(-1, -1, 1, 1)
  window = Window(-0.5, -0.5, 0.5, 0.5)

  def __init__(self, shapes):
    if len(shapes) == 0:
      self.shapes = [
          # Point(0, 0),
          # Point(0, 0.1),
          # Point(0.1, 0.1),
          # Line(Point(0.5, 0.5), Point(0.9, 0.9)),
          # Line(Point(2, 2), Point(-2, -2)),
          # Line(Point(2, -2), Point(-2, 2)),
          # Line(Point(2, 0), Point(-2, 0)),
          # Line(Point(-2, 0), Point(2, 0)),
          # Line(Point(0, 2), Point(0, -2)),
          # Line(Point(0, -2), Point(0, 2)),
          # Line(Point(0.3, 0.3), Point(-0.3, -0.3)),
          # Line(Point(-0.3, -0.3), Point(0.3, 0.3)),
          # Line(Point(-0.3, 0.3), Point(0.3, -0.3)),
          # Line(Point(0.3, -0.3), Point(-0.3, 0.3)),
          # Polygon(Point(0, 0, 0), Point(0.1, 0.1, 0.1),
          #         Point(0.1, 0.0, 0.1), Point(0.1, 0.0, 0.0),
          #         )
          Wireframe.build_cube(Point(0.1, 0, 0), 0.2)
          # Polygon(Point(-0.3, -0.3), Point(-0.3, -0.6),
          #         Point(-0.6, -0.6), Point(-0.6, -0.3)),
          # # Polygon(Point(0, 0), Point(0.2, 0), Point(0.1, 0.2),
          # #         Point(0.2, 0.4), Point(0, 0.4)),
          # BezierCurve([Point(0.2, 0.2), Point(0.2, 0.3),
          #              Point(0.3, 0.3), Point(0.3, 0.2)]),
          # B_SplineCurve([Point(0.05, 0.2), Point(0.1, 0.2), Point(
          #     0.2, 0.5), Point(0.3, 0.2), Point(0.35, 0.2)])
      ]
    else:
      self.shapes = shapes
    self.shapes.append(self.window)

  # draws a single shape
  def draw_shape(self, shape, drawing_context: DrawingContext):
    if shape.dimension > 2:
      for line in self.window.project(shape):
        self.draw_shape(line, drawing_context)
      return
    normalized_shape = self.normalize_shape(shape)
    if type(normalized_shape) == Point:
      if self.window.is_point_inside(normalized_shape):
        drawing_context.draw_line(normalized_shape, normalized_shape)
    if type(normalized_shape) == Line:
      clipped_line = self.window.clip_line(normalized_shape)
      if clipped_line is not None:
        drawing_context.draw_line(clipped_line.begin, clipped_line.end)
    if type(normalized_shape) == Polygon:
      clipped_polygon = self.window.clip_polygon(normalized_shape)
      for line in clipped_polygon.edges():
        drawing_context.draw_line(line.begin, line.end)
      # drawing_context.fill_polygon(clipped_polygon)
    if type(normalized_shape) == Window:
      a = Point(self.window.u_min, self.window.v_min)
      b = Point(self.window.u_min, self.window.v_max)
      c = Point(self.window.u_max, self.window.v_max)
      d = Point(self.window.u_max, self.window.v_min)
      drawing_context.draw_line(a, b)
      drawing_context.draw_line(b, c)
      drawing_context.draw_line(c, d)
      drawing_context.draw_line(d, a)
    if type(normalized_shape) == B_SplineCurve or type(normalized_shape) == BezierCurve:
      curve = normalized_shape
      for line in curve.generate_segments():
        self.draw_shape(line, drawing_context)

  # draws all shapes in the list of shapes
  def draw_shapes(self, drawing_context: DrawingContext):
    for shape in self.shapes:
      self.draw_shape(shape, drawing_context)
    # self.generate_obj_file()

  # normalized display file
  def normalize_shape(self, shape: Shape) -> Shape:
    return shape.transform(self.window.world_to_ndc_matrix())

  def generate_obj_file(self, file_name='sample.obj'):
    content = ""
    with open(file_name, 'w') as f:
      for shape in self.shapes:
        if hasattr(shape, 'obj_string'):
          f.write(shape.obj_string() + '\n')

  def import_scene(self, obj_file_location):
    obj_file_content = open(obj_file_location).read()
    print(obj_file_content)
    removed_comments = [line.strip('\n').split('#')[0]
                        for line in obj_file_content.split('\n')]
    filtered_empty_lines = [
        line for line in removed_comments if len(line.strip()) > 0]

    vertices = []
    faces = []
    for line in filtered_empty_lines:
      if line[0] == 'v':
        x, y, _z = line.strip('v ').split(' ')
        vertices.append(Point(float(x), float(y)))
      if line[0] == 'f':
        indexes = line.strip('f ').split(' ')
        try:
          faces.append([vertices[int(i)] for i in indexes])
        except:
          raise Exception("invalid/not supported obj file")

    for face in faces:
      self.shapes.append(Polygon(*face))
