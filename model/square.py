from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Square(QLabel):
    """
    This class represents a square in the board.
    """

    sqSelected = pyqtSignal(QLabel)
    def __init__(self, color, pos, piece=None, *args, **kwargs):
        super(Square, self).__init__(*args, **kwargs)
        self.setAutoFillBackground(True)
        #self.setAcceptDrops(True)

        self.setSqColor(color)

        self.color = color
        self.pos = pos
        self.piece = piece
        self.refresh_pixmap()
       # if self.piece:
       #     pixmap = QPixmap(self.piece)
       #     self.setPixmap(pixmap)

    def setSqColor(self, color):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

    def refresh_pixmap(self):
        p = QPixmap() if self.piece is None else QPixmap(self.piece)
        self.setPixmap(p)



    def __repr__(self):
        return f"<Square color={self.color}, pos={self.pos}, piece={self.piece}>"

    #def paintEvent(self, event):
        #painter = QPainter(self)
        #if self.piece:
        #    pixmap = QPixmap(self.piece)
        #    self.setPixmap(pixmap)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.sqSelected.emit(self)

