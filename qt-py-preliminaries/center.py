import sys
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.resize(250, 150)
        self.center()

        self.setWindowTitle('Center')
        self.show()

    def center(self):
        #We get a rectangle specifying the geometry of the main window. This includes any window frame. 
        qr = self.frameGeometry()
        # We figure out the screen resolution of our monitor. And from this resolution, we get the center point.
        cp = QDesktopWidget().availableGeometry().center()
        #Our rectangle has already its width and height. Now we set the center of the rectangle to the center of the screen. The rectangle's size is unchanged. 
        qr.moveCenter(cp)
        # We move the top-left point of the application window to the top-left point of the qr rectangle, thus centering the window on our screen. 
        self.move(qr.topLeft())


def main():

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()