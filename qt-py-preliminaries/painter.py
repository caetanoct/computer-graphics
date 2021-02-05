import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # adds label to the window, our viewport is thatlabel after setting it to a pixmap.
        self.setWindowTitle("Computação Gráfica")
        self.setGeometry(100,100,600,600)
        self.label = QtWidgets.QLabel()
        canvas = QtGui.QPixmap(400, 400)
        canvas.fill(QtGui.QColor('grey'))
        self.label.setPixmap(canvas)
        self.setCentralWidget(self.label)
        self.draw_something()

    def draw_something(self):
        painter = QtGui.QPainter(self.label.pixmap())
        pen = QtGui.QPen()
        pen.setWidth(3)
        pen.setColor(QtGui.QColor('red'))
        painter.setPen(pen)
        painter.drawPoint(200, 200)
        painter.end()

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        # self will be painted
        painter.begin(self)
        pen = QtGui.QPen(QtGui.QColor('green'),3)
        painter.setPen(pen)
        painter.drawLine(0, 0, 600,600)
        painter.drawLine(600, 0, 0,600)
        painter.end()        

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
