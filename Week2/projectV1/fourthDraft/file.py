# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CarScreenNew.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.leftPanel = QtWidgets.QFrame(self.centralwidget)
        self.leftPanel.setMaximumWidth(400)
        self.leftPanel.setStyleSheet("QFrame { background-color: #2c3e50; border-radius: 15px; }")
        self.leftPanel.setObjectName("leftPanel")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.leftPanel)
        self.verticalLayout.setObjectName("verticalLayout")
        self.dateLabel = QtWidgets.QLabel(self.leftPanel)
        self.dateLabel.setStyleSheet("color: white; font-size: 16px;")
        self.dateLabel.setObjectName("dateLabel")
        self.verticalLayout.addWidget(self.dateLabel)
        self.dayLabel = QtWidgets.QLabel(self.leftPanel)
        self.dayLabel.setStyleSheet("color: white; font-size: 16px;")
        self.dayLabel.setObjectName("dayLabel")
        self.verticalLayout.addWidget(self.dayLabel)
        self.horizontalLayout.addWidget(self.leftPanel)
        self.mapFrame = QtWidgets.QFrame(self.centralwidget)
        self.mapFrame.setStyleSheet("QFrame { background-color: #2c3e50; border-radius: 15px; }")
        self.mapFrame.setObjectName("mapFrame")
        self.mapLayout = QtWidgets.QVBoxLayout(self.mapFrame)
        self.mapLayout.setObjectName("mapLayout")
        self.mapView = QtWebEngineWidgets.QWebEngineView(self.mapFrame)
        self.mapView.setObjectName("mapView")
        self.mapLayout.addWidget(self.mapView)
        self.horizontalLayout.addWidget(self.mapFrame)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Smart Control Hub"))
        self.dateLabel.setText(_translate("MainWindow", "Date:"))
        self.dayLabel.setText(_translate("MainWindow", "Day:"))
from PyQt5 import QtWebEngineWidgets


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
