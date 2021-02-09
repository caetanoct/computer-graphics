from engine2d.world.geometry import Box, Point

class Window(Box):
  def zoom(self, factor):
    self.x_min += factor
    self.y_min += factor
    self.x_max -= factor
    self.y_max -= factor
  
  def move(self, to: Point):
    self.x_min += to.x
    self.x_max += to.x
    self.y_min += to.y
    self.y_max += to.y