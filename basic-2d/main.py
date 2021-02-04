import sys
from PyQt5.QtWidgets import QMainWindow,QPushButton, QApplication, QInputDialog
from PyQt5.QtCore import QSize, Qt, QLine, QPoint
from PyQt5.QtGui import QPainter, QPen

class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle('INE5420 - Computer Graphics - 800x800 Viewport')
        self.setToolTip('This is a 800x800 <b>Viewport</b>')
        drawButton = QPushButton('draw line', self)
        drawButton.clicked.connect(self.draw_line)
        #drawButton.move(0,803)

        increaseXwminButton = QPushButton('increase Xwmin', self)
        increaseXwminButton.clicked.connect(self.increaseXwmin)
        increaseXwminButton.move(200,803)

        decreaseXwminButton = QPushButton('decrease Xwmin', self)
        decreaseXwminButton.clicked.connect(self.decreaseXwmin)
        decreaseXwminButton.move(200,903)

        increaseYwminButton = QPushButton('increase Ywmin', self)
        increaseYwminButton.clicked.connect(self.increaseYwmin)
        increaseYwminButton.move(400,803)

        decreaseYwminButton = QPushButton('decrease Ywmin', self)
        decreaseYwminButton.clicked.connect(self.decreaseYwmin)
        decreaseYwminButton.move(400,903)

        increaseXwmaxButton = QPushButton('increase Xwmax', self)
        increaseXwmaxButton.clicked.connect(self.increaseXwmax)
        increaseXwmaxButton.move(600,803)

        decreaseXwmaxButton = QPushButton('decrease Xwmax', self)
        decreaseXwmaxButton.clicked.connect(self.decreaseXwmax)
        decreaseXwmaxButton.move(600,903)

        increaseYwmaxButton = QPushButton('increase Ywmax', self)
        increaseYwmaxButton.clicked.connect(self.increaseYwmax)
        increaseYwmaxButton.move(800,803)

        decreaseYwmaxButton = QPushButton('decrease Ywmax', self)
        decreaseYwmaxButton.clicked.connect(self.decreaseYwmax)
        decreaseYwmaxButton.move(800,903)
        # window data structure, real world coordinates
        self.Xwmin = 0
        self.Ywmin = 0
        self.Xwmax = 400
        self.Ywmax = 400
        # viewport data structure, what is drawn
        self.Xvmin = 400
        self.Yvmin = 0
        self.Xvmax = 800
        self.Yvmax = 400
        self.cords = [0,0,0,0]
        self.precords = [0,0,0,0]

    def draw_line_after_update(self):        
        d1 = self.precords[0]
        d2 = self.precords[1]
        d3 = self.precords[2]
        d4 = self.precords[3]
        Xvp1 = ((d1 - self.Xwmin) / (self.Xwmax - self.Xwmin)) * (self.Xvmax - self.Xvmin)
        Yvp1 = (1 - ((d2-self.Ywmin)/(self.Ywmax-self.Ywmin))) * (self.Yvmax - self.Yvmin)
        Xvp2 = ((d3 - self.Xwmin) / (self.Xwmax - self.Xwmin)) * (self.Xvmax - self.Xvmin)
        Yvp2 = (1 - ((d4-self.Ywmin)/(self.Ywmax-self.Ywmin))) * (self.Yvmax - self.Yvmin)
        print("Calculos:")
        print(Xvp1)
        print(Yvp1)
        print(Xvp2)
        print(Yvp2)        
        self.cords = [Xvp1,Yvp1,Xvp2,Yvp2]
        self.update()

    def increaseXwmin(self):
        self.Xwmin += 10
        print(self.Xwmin)
        self.draw_line_after_update()

    def decreaseXwmin(self):
        self.Xwmin -= 10
        print(self.Xwmin)
        self.draw_line_after_update()

    def increaseYwmin(self):
        self.Ywmin += 10
        print(self.Ywmin)
        self.draw_line_after_update()

    def decreaseYwmin(self):
        self.Ywmin -= 10
        print(self.Ywmin)
        self.draw_line_after_update()

    def increaseXwmax(self):
        self.Xwmax += 10
        print(self.Xwmax)
        self.draw_line_after_update()

    def decreaseXwmax(self):
        self.Xwmax -= 10
        print(self.Xwmax)
        self.draw_line_after_update()

    def increaseYwmax(self):
        self.Ywmax += 10
        print(self.Ywmax)
        self.draw_line_after_update()

    def decreaseYwmax(self):
        self.Ywmax -= 10
        print(self.Ywmax)
        self.draw_line_after_update()
    
    def draw_line(self):
        button = self.sender()
        i, okPressed = QInputDialog.getInt(self, "Get integer","x1:", 0, -2147483647, 2147483647, 1)
        if okPressed:
            print(i)
        d1 = i
        i, okPressed = QInputDialog.getInt(self, "Get integer","y1:", 0, -2147483647, 2147483647, 1)
        if okPressed:
            print(i)
        d2 = i
        i, okPressed = QInputDialog.getInt(self, "Get integer","x2:", 0, -2147483647, 2147483647, 1)
        if okPressed:
            print(i)
        d3 = i
        i, okPressed = QInputDialog.getInt(self, "Get integer","y2:", 0, -2147483647, 2147483647, 1)
        if okPressed:
            print(i)
        d4 = i
        Xvp1 = ((d1 - self.Xwmin) / (self.Xwmax - self.Xwmin)) * (self.Xvmax - self.Xvmin)
        Yvp1 = (1 - ((d2-self.Ywmin)/(self.Ywmax-self.Ywmin))) * (self.Yvmax - self.Yvmin)
        Xvp2 = ((d3 - self.Xwmin) / (self.Xwmax - self.Xwmin)) * (self.Xvmax - self.Xvmin)
        Yvp2 = (1 - ((d4-self.Ywmin)/(self.Ywmax-self.Ywmin))) * (self.Yvmax - self.Yvmin)
        print("Calculos:")
        print(Xvp1)
        print(Yvp1)
        print(Xvp2)
        print(Yvp2)
        self.precords = [d1,d2,d3,d4]
        self.cords = [Xvp1,Yvp1,Xvp2,Yvp2]
        self.update()


    def paintEvent(self,event):
        QMainWindow.paintEvent(self, event)
        painter = QPainter(self)
        pen = QPen(Qt.black, 1)
        painter.setPen(pen)
        # positive coordinate system positive x and positive y
        painter.drawLine(400,0,400,800)
        painter.drawLine(0,400,800,400)
        # limit lime
        painter.drawLine(0,800,800,800)        
        painter.setPen(QPen(Qt.red, 3))
        painter.drawLine(self.cords[0],self.cords[1],self.cords[2],self.cords[3])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    # viewport resolution/size in pixels 800x800
    # window (real world) size/resolution is variable
    mainWin.resize(800,832)
    mainWin.show()    
    sys.exit(app.exec_())
