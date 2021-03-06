# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '2dsystem.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
#
# Developed by Caetano Colin Torres
#
# objects list.

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QInputDialog, QMainWindow, QColorDialog, QMessageBox
import random
import numpy
import math
from engine2d.ui.input_dialog import Dialog
from engine2d.ui.drawing_context import DrawingContext
from engine2d.world.geometry import Point, Line, Polygon, BezierCurve, B_SplineCurve
from engine2d.world.box import Box
from engine2d.world.window import Window
from engine2d.world.world import World
import engine2d.world.transformations as transformations
# data structure that represents the viewport


class Viewport(Box):
  pass

# transforms real world coordinates into viewport coordinates


def window_to_viewport(point: Point, w: Window, vp: Viewport) -> Point:
  scale_x = vp.width() / w.width()
  new_x = vp.x_min + (point.x - w.u_min) * scale_x

  scale_y = vp.height() / w.height()
  new_y = vp.y_min + (w.height() - (point.y - w.v_min)) * scale_y

  return Point(x=new_x, y=new_y)

# main Graphical User Interface (GUI)


class Ui_MainWindow(QMainWindow):
  BACKGROUND_COLOR = QtGui.QColor('lightgrey')
  VIEWPORT_MARGIN = 25

  # setting default pxamount (used for menu navigation) and pen color/width
  px_amount = 0.05
  pen_width = 3
  # set default drawing color to red
  color = QtGui.QColor('red')
  fill_color = QtGui.QColor('blue')

  def __init__(self, world: World):
    super().__init__()
    # world know how to draw shapes and contains a real world window (that knows how to move/zoom).
    self.world = world
    margin = Ui_MainWindow.VIEWPORT_MARGIN
    self.viewport = Viewport(margin, margin, 400-margin, 400-margin)

  # draws all objects stored in the process and prints the windows dimensions
  def refresh(self):
    self.clear_canvas()
    self.log("New Window dimensions:", 'green', True)
    self.log("Window: {}".format(self.world.window))
    self.world.draw_shapes(DrawingContext(
        self.draw_world_line, self.fill_world_polygon))
    self.view_port_label.update()

  # initialize all GUI components
  def setup_ui(self, MainWindow):

    MainWindow.setObjectName("MainWindow")
    MainWindow.resize(540, 620)
    self.centralwidget = QtWidgets.QWidget(MainWindow)
    self.centralwidget.setEnabled(True)
    self.centralwidget.setObjectName("centralwidget")

    self.vertical_layout_widget = QtWidgets.QWidget(self.centralwidget)
    self.vertical_layout_widget.setGeometry(QtCore.QRect(10, 10, 91, 205))
    self.vertical_layout_widget.setObjectName("verticalLayoutWidget")
    self.vertical_layout = QtWidgets.QVBoxLayout(self.vertical_layout_widget)
    self.vertical_layout.setContentsMargins(0, 0, 0, 0)
    self.vertical_layout.setObjectName("verticalLayout")

    self.interactivemenu_text_label = QtWidgets.QLabel(
        self.vertical_layout_widget)
    self.interactivemenu_text_label.setObjectName("interactivemenuTextLabel")
    self.vertical_layout.addWidget(self.interactivemenu_text_label)

    self.zoom_in_button = QtWidgets.QPushButton(self.vertical_layout_widget)
    self.zoom_in_button.setObjectName("zoomInButton")
    self.zoom_in_button.clicked.connect(lambda: self.zoom(self.px_amount))
    self.vertical_layout.addWidget(self.zoom_in_button)

    self.zoom_out_button = QtWidgets.QPushButton(self.vertical_layout_widget)
    self.zoom_out_button.setObjectName("zoomOutButton")
    self.zoom_out_button.clicked.connect(lambda: self.zoom(-self.px_amount))
    self.vertical_layout.addWidget(self.zoom_out_button)

    self.up_button = QtWidgets.QPushButton(self.vertical_layout_widget)
    self.up_button.setObjectName("upButton")
    self.up_button.clicked.connect(lambda: self.move(Point(0, self.px_amount)))
    self.vertical_layout.addWidget(self.up_button)

    self.down_button = QtWidgets.QPushButton(self.vertical_layout_widget)
    self.down_button.setObjectName("downButton")
    self.down_button.clicked.connect(
        lambda: self.move(Point(0, -self.px_amount)))
    self.vertical_layout.addWidget(self.down_button)

    self.left_button = QtWidgets.QPushButton(self.vertical_layout_widget)
    self.left_button.setObjectName("leftButton")
    self.left_button.clicked.connect(
        lambda: self.move(Point(-self.px_amount, 0)))
    self.vertical_layout.addWidget(self.left_button)

    self.right_button = QtWidgets.QPushButton(self.vertical_layout_widget)
    self.right_button.setObjectName("rightButton")
    self.right_button.clicked.connect(
        lambda: self.move(Point(self.px_amount, 0)))
    self.vertical_layout.addWidget(self.right_button)

    self.view_port_label = QtWidgets.QLabel(self.centralwidget)
    self.view_port_label.setGeometry(QtCore.QRect(120, 30, 400, 400))
    self.view_port_label.setMinimumSize(QtCore.QSize(400, 400))
    self.view_port_label.setMaximumSize(QtCore.QSize(400, 400))
    self.view_port_label.setAutoFillBackground(True)
    self.view_port_label.setText("")
    self.view_port_label.setObjectName("viewPortLabel")

    canvas = QtGui.QPixmap(400, 400)
    canvas.fill(QtGui.QColor('lightgrey'))
    self.view_port_label.setPixmap(canvas)

    self.text_viewport_label = QtWidgets.QLabel(self.centralwidget)
    self.text_viewport_label.setGeometry(QtCore.QRect(120, 10, 141, 16))
    self.text_viewport_label.setObjectName("text_viewport_label")

    self.output_text_edit = QtWidgets.QTextEdit(self.centralwidget)
    self.output_text_edit.setGeometry(QtCore.QRect(10, 440, 511, 130))
    self.output_text_edit.setReadOnly(True)
    self.output_text_edit.setObjectName("outputTextEdit")

    self.log("Window dimensions:\n{}".format(self.world.window), 'green', True)

    self.log("Viewport dimensions:\n{}".format(self.viewport), 'red', True)

    self.log("Instructions: Use the Cartesian coordinate system.")

    self.vertical_layout_widget_2 = QtWidgets.QWidget(self.centralwidget)
    self.vertical_layout_widget_2.setGeometry(QtCore.QRect(10, 230, 91, 180))
    self.vertical_layout_widget_2.setObjectName("verticalLayoutWidget_2")
    self.second_layout = QtWidgets.QVBoxLayout(self.vertical_layout_widget_2)
    self.second_layout.setContentsMargins(0, 0, 0, 0)
    self.second_layout.setObjectName("secondLayout")
    self.px_amount_label = QtWidgets.QLabel(self.vertical_layout_widget_2)
    self.px_amount_label.setObjectName("pxAmountLabel")
    self.px_amount_label.setToolTip(
        'This is the <b>number of pixels</b> that the object will move.')
    self.second_layout.addWidget(self.px_amount_label)

    self.px_amount_spin_box = QtWidgets.QDoubleSpinBox(
        self.vertical_layout_widget_2)
    self.px_amount_spin_box.setObjectName("pxAmountSpinBox")
    self.px_amount_spin_box.setValue(self.px_amount)
    self.px_amount_spin_box.valueChanged.connect(self.px_amount_changed)
    self.px_amount_spin_box.setToolTip(
        'This is the <b>number of pixels</b> that the object will move.')
    self.second_layout.addWidget(self.px_amount_spin_box)

    self.pen_width_label = QtWidgets.QLabel(self.vertical_layout_widget_2)
    self.pen_width_label.setObjectName("penWidthLabel")
    self.second_layout.addWidget(self.pen_width_label)
    self.pen_width_spin_box = QtWidgets.QSpinBox(self.vertical_layout_widget_2)
    self.pen_width_spin_box.setObjectName("penWidthSpinBox")
    self.pen_width_spin_box.setValue(self.pen_width)
    self.pen_width_spin_box.valueChanged.connect(self.pen_width_changed)
    self.second_layout.addWidget(self.pen_width_spin_box)

    self.obj_list_label = QtWidgets.QLabel(self.vertical_layout_widget_2)
    self.obj_list_label.setObjectName("objListLabel")
    self.second_layout.addWidget(self.obj_list_label)
    self.obj_list_combo_box = QtWidgets.QComboBox(
        self.vertical_layout_widget_2)
    self.obj_list_combo_box.setObjectName("objListComboBox")
    self.second_layout.addWidget(self.obj_list_combo_box)

    self.draw_button = QtWidgets.QPushButton(self.vertical_layout_widget_2)
    self.draw_button.setObjectName("drawButton")
    self.draw_button.clicked.connect(self.handle_draw_button)
    self.second_layout.addWidget(self.draw_button)

    MainWindow.setCentralWidget(self.centralwidget)

    self.menubar = QtWidgets.QMenuBar(MainWindow)
    self.menubar.setGeometry(QtCore.QRect(0, 0, 495, 22))
    self.menubar.setObjectName("menubar")

    self.menu_insert = QtWidgets.QMenu(self.menubar)
    self.menu_insert.setObjectName("menuInsert")

    self.menuTransform = QtWidgets.QMenu(self.menubar)
    self.menuTransform.setObjectName("menuTransform")

    self.menuRotation = QtWidgets.QMenu(self.menuTransform)
    self.menuRotation.setObjectName("menuRotation")

    MainWindow.setMenuBar(self.menubar)

    self.statusbar = QtWidgets.QStatusBar(MainWindow)
    self.statusbar.setObjectName("statusbar")
    MainWindow.setStatusBar(self.statusbar)
    # actions
    self.actiondraw_point = QtWidgets.QAction(MainWindow)
    self.actiondraw_point.setObjectName("actiondraw_point")
    self.actiondraw_point.triggered.connect(self.action_draw_point)

    self.actiondraw_line = QtWidgets.QAction(MainWindow)
    self.actiondraw_line.setObjectName("actiondraw_line")
    self.actiondraw_line.triggered.connect(self.action_draw_line)

    self.actiondraw_polygon = QtWidgets.QAction(MainWindow)
    self.actiondraw_polygon.setObjectName("actionDraw_Polygon")
    self.actiondraw_polygon.triggered.connect(self.action_draw_polygon)

    self.actiondraw_curve = QtWidgets.QAction(MainWindow)
    self.actiondraw_curve.setObjectName("actiondraw_curve")
    self.actiondraw_curve.triggered.connect(self.action_draw_curve)

    self.actionclear = QtWidgets.QAction(MainWindow)
    self.actionclear.setObjectName("actionclear")
    self.actionclear.triggered.connect(self.clear_objects)

    self.actionselect_color_2 = QtWidgets.QAction(MainWindow)
    self.actionselect_color_2.setObjectName("actionselect_color_2")
    self.actionselect_color_2.triggered.connect(self.action_select_color)

    self.actionTranslation = QtWidgets.QAction(MainWindow)
    self.actionTranslation.setObjectName("actionTranslation")
    self.actionTranslation.triggered.connect(self.action_translation)

    self.actionScaling = QtWidgets.QAction(MainWindow)
    self.actionScaling.setObjectName("actionScaling")
    self.actionScaling.triggered.connect(self.action_scaling)

    self.actionAround_the_object = QtWidgets.QAction(MainWindow)
    self.actionAround_the_object.setObjectName("actionAround_the_object")
    self.actionAround_the_object.triggered.connect(self.action_rotate_object)

    self.actionAround_the_world = QtWidgets.QAction(MainWindow)
    self.actionAround_the_world.setObjectName("actionAround_the_world")
    self.actionAround_the_world.triggered.connect(
        self.action_rotate_obj_around_world)

    self.actionAround_the_world_y = QtWidgets.QAction(MainWindow)
    self.actionAround_the_world_y.setObjectName("actionAround_the_world_y")
    self.actionAround_the_world_y.triggered.connect(
        self.build_rotation_action(transformations.rotation_matrix_3d_y))

    self.actionAround_the_world_x = QtWidgets.QAction(MainWindow)
    self.actionAround_the_world_x.setObjectName("actionAround_the_world_x")
    self.actionAround_the_world_x.triggered.connect(
        self.build_rotation_action(transformations.rotation_matrix_3d_x))

    self.actionAround_the_world_z = QtWidgets.QAction(MainWindow)
    self.actionAround_the_world_z.setObjectName("actionAround_the_world_z")
    self.actionAround_the_world_z.triggered.connect(
        self.build_rotation_action(transformations.rotation_matrix_3d_z))

    self.actionAround_a_point = QtWidgets.QAction(MainWindow)
    self.actionAround_a_point.setObjectName("actionAround_a_point")
    self.actionAround_a_point.triggered.connect(
        self.action_rotate_obj_around_point)
    self.actionRotate_window = QtWidgets.QAction(MainWindow)
    self.actionRotate_window.setObjectName("actionRotate_window")
    self.actionRotate_window.triggered.connect(
        self.action_rotate_window)
    # end actions
    self.menu_insert.addAction(self.actiondraw_point)
    self.menu_insert.addAction(self.actiondraw_line)
    self.menu_insert.addAction(self.actiondraw_polygon)
    self.menu_insert.addAction(self.actiondraw_curve)
    self.menu_insert.addAction(self.actionclear)
    self.menu_insert.addSeparator()
    self.menu_insert.addAction(self.actionselect_color_2)

    self.menuRotation.addAction(self.actionAround_the_object)
    self.menuRotation.addAction(self.actionAround_the_world)
    self.menuRotation.addAction(self.actionAround_the_world_y)
    self.menuRotation.addAction(self.actionAround_the_world_x)
    self.menuRotation.addAction(self.actionAround_the_world_z)
    self.menuRotation.addAction(self.actionAround_a_point)
    self.menuRotation.addAction(self.actionRotate_window)
    self.menuTransform.addAction(self.actionTranslation)
    self.menuTransform.addAction(self.actionScaling)
    self.menuTransform.addAction(self.menuRotation.menuAction())

    self.menubar.addAction(self.menu_insert.menuAction())
    self.menubar.addAction(self.menuTransform.menuAction())

    self.retranslate_ui(MainWindow)
    QtCore.QMetaObject.connectSlotsByName(MainWindow)

  # translates ui components

  def retranslate_ui(self, MainWindow):
    _translate = QtCore.QCoreApplication.translate
    MainWindow.setWindowTitle(_translate(
        "MainWindow", "INE5420 - Computer Graphics - Basic 2D System"))
    self.interactivemenu_text_label.setText(_translate("MainWindow", "Menu"))
    self.zoom_in_button.setText(_translate("MainWindow", "Zoom (+)"))
    self.zoom_out_button.setText(_translate("MainWindow", "Zoom (-)"))
    self.up_button.setText(_translate("MainWindow", "up"))
    self.down_button.setText(_translate("MainWindow", "down"))
    self.left_button.setText(_translate("MainWindow", "left"))
    self.draw_button.setText(_translate("MainWindow", "Draw"))
    self.right_button.setText(_translate("MainWindow", "right"))
    self.text_viewport_label.setText(
        _translate("MainWindow", "Viewport - 400x400"))
    self.menu_insert.setTitle(_translate("MainWindow", "Insert"))
    self.actiondraw_point.setText(_translate("MainWindow", "Draw Point"))
    self.actiondraw_line.setText(_translate("MainWindow", "Draw Line"))
    self.actionclear.setText(_translate("MainWindow", "Clear Viewport"))
    self.px_amount_label.setText(_translate("MainWindow", "Px Amount"))
    self.pen_width_label.setText(_translate("MainWindow", "Pen Width"))
    self.obj_list_label.setText(_translate("MainWindow", "Object list"))
    self.actiondraw_polygon.setText(_translate("MainWindow", "Draw Polygon"))
    self.actiondraw_curve.setText(_translate("MainWindow", "Draw Curve"))
    self.actionselect_color_2.setText(
        _translate("MainWindow", "Select Pen Color"))
    self.actionTranslation.setText(_translate("MainWindow", "Translation"))
    self.actionScaling.setText(_translate("MainWindow", "Scaling"))
    self.actionAround_the_object.setText(
        _translate("MainWindow", "Relative to the object"))
    self.actionAround_the_world.setText(
        _translate("MainWindow", "Relative to the world"))
    self.actionAround_the_world_y.setText(
        _translate("MainWindow", "Relative to the world (y)"))
    self.actionAround_the_world_x.setText(
        _translate("MainWindow", "Relative to the world (x)"))
    self.actionAround_the_world_z.setText(
        _translate("MainWindow", "Relative to the world (z)"))
    self.actionAround_a_point.setText(
        _translate("MainWindow", "Relative to a point"))
    self.actionRotate_window.setText(
        _translate("MainWindow", "Rotate Window"))
    self.menuTransform.setTitle(_translate("MainWindow", "Transform"))
    self.menuRotation.setTitle(_translate("MainWindow", "Rotation"))

    for i, shape in enumerate(self.world.shapes):
      self.obj_list_combo_box.addItem(
          "{}-{}".format(i, type(shape).__name__))
    self.refresh()
  # Clears the canvas - light grey - needs to be called everytime move the window, draw a single object or when we clear the viewport

  def clear_canvas(self):
    self.log("Clearing Viewport 400x400.")
    self.view_port_label.pixmap().fill(Ui_MainWindow.BACKGROUND_COLOR)
    self.view_port_label.update()
  # changes window size and redraw all objects if zoom + then positive factor, if zoom - then negative factor

  def zoom(self, factor):
    self.log("Zooming in {}px.".format(factor))
    # calls zoom method from real world window, the window knows how to zoom itself by updating the internal data structure of the object.
    self.world.window.zoom(factor)
    # redraw all objects
    self.refresh()

  # changes window size and redraw  all objects (the objects will appear to be moving up).
  def move(self, to: Point):
    self.log("Moving window in ({}, {})".format(to.x, to.y))
    # calls move method from real world window, the window knows how to move itself by updating the internal data structure of the object.
    self.world.window.move(to)
    # redraw all objects
    self.refresh()

  # when draw line is pressed call draw line function in use dialog data funcion (after receiving dialog input)
  def action_draw_line(self):
    self.log("Draw Line Trigerred, drawing line after user input.")
    dg = Dialog()
    # use_dialog_data_line will be callend when the dialog closes
    dg.accepted.connect(self.use_dialog_data_line)
    dg.exec_()
    # self.draw_line() - will be executed in use_dialog_data_line
    self.view_port_label.update()

  # draws line in viewport's coordinates
  def draw_viewport_line(self, begin: Point, end: Point):
    painter = QtGui.QPainter(self.view_port_label.pixmap())
    pen = QtGui.QPen()
    pen.setWidth(self.pen_width)
    pen.setColor(QtGui.QColor(self.color))
    painter.setPen(pen)
    painter.drawLine(begin.x, begin.y, end.x, end.y)
    painter.end()

  # draws line in world's coordinates (transforming it to viewport coordinates)
  def draw_world_line(self, begin: Point, end: Point):
    self.draw_viewport_line(
        window_to_viewport(begin, self.world.window, self.viewport),
        window_to_viewport(end, self.world.window, self.viewport),
    )

  def fill_world_polygon(self, polygon: Polygon):
    viewport_polygon = Polygon(
        *[window_to_viewport(p, self.world.window, self.viewport) for p in polygon.points])
    path = self.transform_polygon_to_path(viewport_polygon)

    painter = QtGui.QPainter(self.view_port_label.pixmap())
    painter.fillPath(path, self.fill_color)  # , QtGui.QBrush("blue"))
    painter.end()

  def transform_polygon_to_path(self, polygon: Polygon) -> QtGui.QPainterPath:

    path = QtGui.QPainterPath()
    for i, p in enumerate(polygon.points):
      if i == 0:
        path.moveTo(p.x, p.y)
      else:
        path.lineTo(p.x, p.y)
    return path
  # transforms user input data from the dialog (defined in input_dialog.py) to viewport coords and calls drawline funtion

  def use_dialog_data_line(self, values):
    line = Line(Point(int(values['x1']), int(values['y1'])), Point(
        int(values['x2']), int(values['y2'])))
    self.create_object(line)

  # when the action draw point is pressed, get user input, transform it and call drawpoint funtion
  def action_draw_point(self):
    self.log("Draw Point Trigerred, drawing point after getting values from user.")
    button = self.sender()
    x1, _ = QInputDialog.getInt(
        self, "First value (Integer)", "x:", 0, -2147483647, 2147483647, 1)
    button = self.sender()
    y1, _ = QInputDialog.getInt(
        self, "Second value (Integer)", "y:", 0, -2147483647, 2147483647, 1)

    self.create_object(Point(x1, y1))

  # get user input (point list) and draw a polygon in the viewport
  def action_draw_polygon(self):
    self.log("Draw Polygon Trigerred, drawing polygon after user input.")
    button = self.sender()
    value, _ = QInputDialog.getInt(
        self, "How many points?", "amount:", 0, -2147483647, 2147483647, 1)
    if (value <= 0):
      self.log("Try again, value must be greater than 0.", "red")
      return
    color = self.color
    points = []

    for x in range(value):
      button = self.sender()
      x1, _ = QInputDialog.getInt(self, "Enter value of (Integer)", "x{}:".format(
          x+1), 0, -2147483647, 2147483647, 1)
      button = self.sender()
      y1, _ = QInputDialog.getInt(self, "Enter value of (Integer)", "y{}:".format(
          x+1), 0, -2147483647, 2147483647, 1)
      points.append(Point(x1, y1))
    self.create_object(Polygon(*points))

  # get user input (point list) and draw a curve in the viewport
  def action_draw_curve(self):
    self.log("Draw Curve Trigerred, drawing curve after user input.")
    opt, _ = QInputDialog.getInt(
        self, "0 = Bezier || 1 = B-splines", "Curve type (0 or 1):")
    print(opt)
    button = self.sender()
    value, _ = QInputDialog.getInt(
        self, "How many points?", "amount:", 0, -2147483647, 2147483647, 1)
    if (value <= 3):
      self.log("Try again, value must be greater than 3.", "red")
      return
    color = self.color
    points = []

    for x in range(value):
      button = self.sender()
      x1, _ = QInputDialog.getInt(self, "Enter value of (Integer)", "x{}:".format(
          x+1), 0, -2147483647, 2147483647, 1)
      button = self.sender()
      y1, _ = QInputDialog.getInt(self, "Enter value of (Integer)", "y{}:".format(
          x+1), 0, -2147483647, 2147483647, 1)
      points.append(Point(x1, y1))
    print("creating curve")
    if opt == 1:
      curve = B_SplineCurve(points)
    elif opt == 0:
      curve = BezierCurve(points)
    else:
      print("invalid number")
    self.create_object(curve)

  # changes amount of pixels that will move on the interactive menu

  def px_amount_changed(self):
    value = self.px_amount_spin_box.value()
    print("New pxAmount:", value)
    self.px_amount = value
    self.log("Px amount was set to {} (Default = 5)".format(self.px_amount))

  # changes value of pen width in class
  def pen_width_changed(self):
    value = self.pen_width_spin_box.value()
    print("New pen width:", value)
    self.pen_width = value
    self.log("Pen width was set to {} (Default = 5)".format(self.pen_width))

  # when the draw button is pressed, draw the object that is selected in the object list
  def handle_draw_button(self):
    string = self.obj_list_combo_box.currentText()
    if (len(string) >= 1):
      index = string[0]
      obj = self.world.shapes[int(index)]
      self.clear_canvas()
      self.world.draw_shape(obj, DrawingContext(
          self.draw_world_line, self.fill_world_polygon))
      self.view_port_label.update()

  # handles select color action
  def action_select_color(self):
    color = QColorDialog.getColor()
    self.log("New pen color was set.", color, True)
    self.color = color
  # handles translation action

  def action_translation(self):
    index = self.obj_list_combo_box.currentIndex()
    if (index == -1):
      self.log("ERROR: There are no objects in object list")
    else:
      Dx, _ = QInputDialog.getInt(self, "Integer input dialog", "enter Dx")
      Dy, _ = QInputDialog.getInt(self, "Integer input dialog", "enter Dy")
      self.apply_transformation(
          index, transformations.translation_matrix(Point(Dx, Dy)))
  # handles scaling action

  def action_scaling(self):
    index = self.obj_list_combo_box.currentIndex()
    if (index == -1):
      self.log("ERROR: There are no objects in object list")
    else:
      Sx, _ = QInputDialog.getDouble(self, "Double input dialog", "enter Sx")
      Sy, _ = QInputDialog.getDouble(self, "Double input dialog", "enter Sy")
      object_selected = self.world.shapes[index]
      self.apply_transformation(
          index, transformations.scaling_around_object_matrix(object_selected, Sx, Sy))
  # handles rotation around the object action

  def action_rotate_object(self):
    index = self.obj_list_combo_box.currentIndex()
    if (index == -1):
      self.log("ERROR: There are no objects in object list")
    else:
      angle, _ = QInputDialog.getInt(
          self, "Integer input dialog", "enter angle (in degrees):")
      object_selected = self.world.shapes[index]
      self.apply_transformation(
          index, transformations.rotation_around_object_matrix(object_selected, angle))
  # handles rotation around the world action

  def action_rotate_obj_around_world(self):
    index = self.obj_list_combo_box.currentIndex()
    if (index == -1):
      self.log("ERROR: There are no objects in object list")
    else:
      angle, _ = QInputDialog.getInt(
          self, "Integer input dialog", "enter angle (in degrees):")
      self.apply_transformation(index, transformations.rotation_matrix(angle))

  def build_rotation_action(self, matrix_builder):
    def rotate():
      index = self.obj_list_combo_box.currentIndex()
      if (index == -1):
        self.log("ERROR: There are no objects in object list")
      else:
        angle, _ = QInputDialog.getInt(
            self, "Integer input dialog", "enter angle (in degrees):")
        self.apply_transformation(index, matrix_builder(angle))
    return rotate
  # handles rotation around an arbitrary point action

  def action_rotate_obj_around_point(self):
    index = self.obj_list_combo_box.currentIndex()
    if (index == -1):
      self.log("ERROR: There are no objects in object list")
    else:
      angle, _ = QInputDialog.getInt(
          self, "Integer input dialog", "enter angle (in degrees):")
      x, _ = QInputDialog.getInt(self, "Integer input dialog", "enter Point x")
      y, _ = QInputDialog.getInt(self, "Integer input dialog", "enter Point y")
      self.apply_transformation(
          index, transformations.rotation_around_point_matrix(Point(x, y), angle))

  def apply_transformation(self, object_index, transform_matrix):
    object_selected = self.world.shapes[object_index]
    self.log("Object type {} (index={}) was transformed with matrix: {}".format(
        type(object_selected).__name__, object_index, transform_matrix))
    transformed_object = object_selected.transform(transform_matrix)
    self.log("Selected object (after transformation): {}".format(
        transformed_object))
    self.world.shapes[object_index] = transformed_object
    self.refresh()

  def log(self, text, color='black', italic=False):
    self.output_text_edit.setTextColor(QtGui.QColor(color))
    self.output_text_edit.setFontItalic(italic)
    self.output_text_edit.append(text)
    self.output_text_edit.setFontItalic(False)
    self.output_text_edit.setTextColor(QtGui.QColor('black'))

  def create_object(self, obj):
    self.obj_list_combo_box.addItem(
        "{}-{}".format(len(self.world.shapes), type(obj).__name__))
    self.world.shapes.append(obj)
    self.refresh()
    self.log("{} was drawn".format(obj))

  def clear_objects(self, object):
    for _ in range(len(self.world.shapes)):
      self.obj_list_combo_box.removeItem(0)
    self.world.shapes = []
    self.clear_canvas()

  def action_rotate_window(self):
    angle, _ = QInputDialog.getInt(
        self, "Integer input dialog", "enter angle (in degrees):")
    self.world.window = self.world.window.transform(
        transformations.rotation_matrix(angle))
    self.refresh()
