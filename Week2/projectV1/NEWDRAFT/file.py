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
        MainWindow.resize(800, 550)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.dateTimeFrame = QtWidgets.QFrame(self.centralwidget)
        self.dateTimeFrame.setGeometry(QtCore.QRect(10, 10, 380, 200))
        self.dateTimeFrame.setObjectName("dateTimeFrame")
        self.dateLabel = QtWidgets.QLabel(self.dateTimeFrame)
        self.dateLabel.setGeometry(QtCore.QRect(20, 20, 120, 30))
        self.dateLabel.setObjectName("dateLabel")
        self.dateDisplay = QtWidgets.QLabel(self.dateTimeFrame)
        self.dateDisplay.setGeometry(QtCore.QRect(20, 50, 160, 60))
        self.dateDisplay.setObjectName("dateDisplay")
        self.dayLabel = QtWidgets.QLabel(self.dateTimeFrame)
        self.dayLabel.setGeometry(QtCore.QRect(200, 20, 120, 30))
        self.dayLabel.setObjectName("dayLabel")
        self.dayDisplay = QtWidgets.QLabel(self.dateTimeFrame)
        self.dayDisplay.setGeometry(QtCore.QRect(200, 50, 160, 60))
        self.dayDisplay.setObjectName("dayDisplay")
        self.voiceCommandFrame = QtWidgets.QFrame(self.centralwidget)
        self.voiceCommandFrame.setGeometry(QtCore.QRect(10, 220, 380, 240))
        self.voiceCommandFrame.setObjectName("voiceCommandFrame")
        self.lightOnButton = QtWidgets.QPushButton(self.voiceCommandFrame)
        self.lightOnButton.setGeometry(QtCore.QRect(20, 20, 160, 50))
        self.lightOnButton.setObjectName("lightOnButton")
        self.lightOffButton = QtWidgets.QPushButton(self.voiceCommandFrame)
        self.lightOffButton.setGeometry(QtCore.QRect(200, 20, 160, 50))
        self.lightOffButton.setObjectName("lightOffButton")
        self.gpsOnButton = QtWidgets.QPushButton(self.voiceCommandFrame)
        self.gpsOnButton.setGeometry(QtCore.QRect(20, 90, 160, 50))
        self.gpsOnButton.setObjectName("gpsOnButton")
        self.gpsOffButton = QtWidgets.QPushButton(self.voiceCommandFrame)
        self.gpsOffButton.setGeometry(QtCore.QRect(200, 90, 160, 50))
        self.gpsOffButton.setObjectName("gpsOffButton")
        self.mapFrame = QtWidgets.QFrame(self.centralwidget)
        self.mapFrame.setGeometry(QtCore.QRect(400, 10, 390, 450))
        self.mapFrame.setObjectName("mapFrame")
        self.mapView = QtWebEngineWidgets.QWebEngineView(self.mapFrame)
        self.mapView.setGeometry(QtCore.QRect(10, 10, 370, 430))
        self.mapView.setObjectName("mapView")
        self.statusBar = QtWidgets.QStatusBar(self.centralwidget)
        self.statusBar.setGeometry(QtCore.QRect(0, 460, 800, 20))
        self.statusBar.setObjectName("statusBar")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Smart Control Hub"))
        MainWindow.setStyleSheet(_translate("MainWindow", "\n"
"    QMainWindow {\n"
"        background-color: #1a1a1a;\n"
"    }\n"
"    QPushButton {\n"
"        background-color: #3498db;\n"
"        color: white;\n"
"        border-radius: 10px;\n"
"        padding: 10px;\n"
"        font-size: 14px;\n"
"    }\n"
"    QLabel {\n"
"        color: white;\n"
"        font-size: 16px;\n"
"    }\n"
"   "))
        self.dateTimeFrame.setStyleSheet(_translate("MainWindow", "\n"
"      QFrame {\n"
"          background-color: #2c3e50;\n"
"          border-radius: 15px;\n"
"      }\n"
"     "))
        self.dateLabel.setText(_translate("MainWindow", "Date:"))
        self.dateLabel.setStyleSheet(_translate("MainWindow", "\n"
"       QLabel {\n"
"           color: #ecf0f1;\n"
"           font-size: 18px;\n"
"       }\n"
"      "))
        self.dateDisplay.setStyleSheet(_translate("MainWindow", "\n"
"       QLabel {\n"
"           color: #2ecc71;\n"
"           font-size: 24px;\n"
"           font-weight: bold;\n"
"       }\n"
"      "))
        self.dayLabel.setText(_translate("MainWindow", "Day:"))
        self.dayLabel.setStyleSheet(_translate("MainWindow", "\n"
"       QLabel {\n"
"           color: #ecf0f1;\n"
"           font-size: 18px;\n"
"       }\n"
"      "))
        self.dayDisplay.setStyleSheet(_translate("MainWindow", "\n"
"       QLabel {\n"
"           color: #2ecc71;\n"
"           font-size: 24px;\n"
"           font-weight: bold;\n"
"       }\n"
"      "))
        self.voiceCommandFrame.setStyleSheet(_translate("MainWindow", "\n"
"      QFrame {\n"
"          background-color: #2c3e50;\n"
"          border-radius: 15px;\n"
"      }\n"
"     "))
        self.lightOnButton.setText(_translate("MainWindow", "Lights On"))
        self.lightOffButton.setText(_translate("MainWindow", "Lights Off"))
        self.gpsOnButton.setText(_translate("MainWindow", "GPS On"))
        self.gpsOffButton.setText(_translate("MainWindow", "GPS Off"))
        self.mapFrame.setStyleSheet(_translate("MainWindow", "\n"
"      QFrame {\n"
"          background-color: #2c3e50;\n"
"          border-radius: 15px;\n"
"      }\n"
"     "))
        self.statusBar.setStyleSheet(_translate("MainWindow", "\n"
"      QStatusBar {\n"
"          background-color: #34495e;\n"
"          color: white;\n"
"      }\n"
"     "))
from PyQt5 import QtWebEngineWidgets


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
