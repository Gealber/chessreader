from view.widget import MainWindow
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication([])
    board = MainWindow(dark=True)
    board.show()
    app.exec_()
