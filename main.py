from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
import sys
from engine2d.ui.viewport import Ui_MainWindow
from engine2d.world.world import World
from engine2d.world.geometry import BezierCurve, Point, Line
from engine2d.world.transformations import rotation_matrix

if __name__ == "__main__":
  import sys
  app = QtWidgets.QApplication(sys.argv)
  MainWindow = QtWidgets.QMainWindow()
  world = World([])
  # world.import_scene('sample.obj')
  # world.generate_obj_file('sample.obj')
  ui = Ui_MainWindow(world)
  ui.setup_ui(MainWindow)
  MainWindow.show()
  sys.exit(app.exec_())
