# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'view/rightside.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_RightSide(object):
    def setupUi(self, RightSide):
        RightSide.setObjectName("RightSide")
        RightSide.resize(232, 505)
        self.verticalLayout = QtWidgets.QVBoxLayout(RightSide)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget = QtWidgets.QTableWidget(RightSide)
        self.tableWidget.setStyleSheet("background-color:rgb(25, 25, 25);\n"
"color: yellow")
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 1, item)
        self.verticalLayout.addWidget(self.tableWidget)
        self.line = QtWidgets.QFrame(RightSide)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)

        self.retranslateUi(RightSide)
        QtCore.QMetaObject.connectSlotsByName(RightSide)

    def retranslateUi(self, RightSide):
        _translate = QtCore.QCoreApplication.translate
        RightSide.setWindowTitle(_translate("RightSide", "Form"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("RightSide", "1"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("RightSide", "White"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("RightSide", "Black"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.item(0, 0)
        item.setText(_translate("RightSide", "e4"))
        item = self.tableWidget.item(0, 1)
        item.setText(_translate("RightSide", "e5"))
        self.tableWidget.setSortingEnabled(__sortingEnabled)

