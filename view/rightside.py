from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Table(QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet(
            "background-color: #3a3a3a;\n"
            "color: white"
        )

        self.setFixedSize(200, 600)
        self.setColumnCount(2)
        white = QTableWidgetItem()
        white.setText("White")
        self.setHorizontalHeaderItem(0, white)
        black = QTableWidgetItem()
        black.setText("Black")
        self.setHorizontalHeaderItem(1, black)

        self.add_item(0,0, "e4")

    def add_item(self, i, j, play):
        print("Adding item:")
        item = QTableWidgetItem()
        item.setText(play)
        if self.rowCount() < i+1:
            self.setRowCount(i+1)
        self.setItem(i, j, item)

if __name__ == "__main__":
    app = QApplication([])
    table = Table()
    table.show()
    app.exec_()
