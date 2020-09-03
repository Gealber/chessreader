from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Table(QTableWidget):
    def __init__(self, dark=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if dark:
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
        self.next_cell = [0, 0]

    def add_item(self, play):
        i, j = self.next_cell
        item = QTableWidgetItem()
        item.setText(play)
        if self.rowCount() < i+1:
            self.setRowCount(i+1)
        self.setItem(i, j, item)
        if j == 1:
            j = 0
            i += 1
        else:
            j = 1
        self.next_cell = [i, j]

    def remove_item(self):
        i, j = self.next_cell
        if i == 0 and j == 0:
            return
        elif j == 1:
            j = 0
            self.setRowCount(self.rowCount()-1)
        elif j == 0:
            item = self.item(i-1, 1)
            i, j= i-1, 1
            item.setText("")
        self.next_cell = [i, j]

    def clean_table(self):
        self.next_cell = [0, 0]
        self.setRowCount(0)

if __name__ == "__main__":
    app = QApplication([])
    table = Table()
    table.show()
    app.exec_()
