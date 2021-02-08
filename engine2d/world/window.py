from engine2d.world.geometry import Box

class Window(Box):
  def zoom(self, factor):
    self = Window(self.x_min + factor, self.x_max - factor, self.y_min + factor, self.y_max - factor)