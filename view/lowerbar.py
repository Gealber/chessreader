"""
Lower Bar that contains the buttons to move forward and
backward. Need to be improved is too ugly
"""

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class LowerBar(QWidget):
    def __init__(self, *args, **kwargs):
        super(LowerBar, self).__init__(*args, **kwargs)


        self.setFixedSize(630, 30)
        self._layout = QHBoxLayout()
        self.forward = ForwardButton()
        self.backward = BackwardButton()
        self._layout.addWidget(self.backward)
        self._layout.addWidget(self.forward)
        self.setLayout(self._layout)

class ForwardButton(QLabel):
    pressed = pyqtSignal(QLabel)
    def __init__(self):
        super().__init__()

        pixmap = QPixmap('images/arrow.png')
        self.setPixmap(pixmap)
        self.setFixedSize(40, 20)

    def mousePressEvent(self, event):
        self.pressed.emit(self)

class BackwardButton(QLabel):
    pressed = pyqtSignal(QLabel)
    def __init__(self):
        super().__init__()
        pixmap = QPixmap('images/arrow-180.png')
        self.setPixmap(pixmap)
        self.setFixedSize(40, 20)
    def mousePressEvent(self, event):
        self.pressed.emit(self)


if __name__ == '__main__':
    app = QApplication([])
    bar = LowerBar()
    bar.show()
    app.exec_()

