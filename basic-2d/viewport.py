import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont


class Viewport(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))
        self.label = QLabel("Viewport", self)
        self.setToolTip('This is a <b>Viewport(QWidget)</b> widget')
        self.setGeometry(300, 300, 600, 600)
        self.show()