from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Dialog(QDialog):

    accepted = pyqtSignal(dict)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.x1 = QLineEdit()        
        self.y1 = QLineEdit()        
        self.x2 = QLineEdit()
        self.y2 = QLineEdit()

        self.y2.textEdited[str].connect(self.unlock)

        self.btn = QPushButton('OK')
        self.btn.setDisabled(True)
        self.btn.clicked.connect(self.ok_pressed)

        form = QFormLayout(self)
        form.addRow('X1:', self.x1)
        form.addRow('Y1:', self.y1)
        form.addRow('X2:', self.x2)
        form.addRow('Y2:', self.y2)
        form.addRow(self.btn)

    def unlock(self, text):
        if text:
            self.btn.setEnabled(True)
        else:
            self.btn.setDisabled(True)

    def ok_pressed(self):
        values = {'x1': self.x1.text(),
                  'y1': self.y1.text(),
                  'x2': self.x2.text(),
                  'y2': self.y2.text()
                  }
        self.accepted.emit(values)
        self.accept()