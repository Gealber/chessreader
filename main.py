"""
This is a widget made with PyQt5 and python-chess, with the
hope that in further works will be a kind of pgn reader with some
cool featues. The icons used until now are from
 Fuge icon made by Yusuke Kamiyamane. You can download them  here
 http://p.yusukekamiyamane.com/ and give credit to the author as I'm doing here.
"""

from view.widget import MainWindow
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication([])
    board = MainWindow(dark=True)
    board.show()
    app.exec_()
