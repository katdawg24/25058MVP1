# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TempDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from random import randint
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import pyqtgraph as pg


class Ui_TempDetails(object):
    def setupUi(self, TempDetails):
        TempDetails.setObjectName("TempDetails")
        TempDetails.resize(751, 587)

        self.temp_dialog_close_button = QtWidgets.QPushButton(TempDetails)
        self.temp_dialog_close_button.setGeometry(QtCore.QRect(600, 530, 121, 31))
        self.temp_dialog_close_button.setObjectName("temp_dialog_close_button")
        self.temp_dialog_close_button.clicked.connect(self.closeWindow)

        self.tableView = QtWidgets.QTableView(TempDetails)
        self.tableView.setGeometry(QtCore.QRect(20, 390, 701, 121))
        self.tableView.setObjectName("tableView")

        self.detailed_temp_chart = pg.PlotWidget(TempDetails)
        self.detailed_temp_chart.setBackground("w")
        pen = pg.mkPen(color=(255,0,0))
        self.detailed_temp_chart.setTitle("Temperature vs Time", color="k", size="15pt")
        styles = {"color": "red", "font-size": "10px"}
        self.detailed_temp_chart.setLabel("left", "Temperature (°C)", **styles)
        self.detailed_temp_chart.setLabel("bottom", "Time (min)", **styles)
        #self.detailed_temp_chart.addLegend()
        self.detailed_temp_chart.showGrid(x=True, y=True)
        self.detailed_temp_chart.setYRange(20, 40)
        self.time = []
        self.temperature = []
        

        self.temp_line = self.detailed_temp_chart.plot(
            self.time,
            self.temperature,
            name="Temperature Sensor",
            pen=pen
        )

        # self.detailed_temp_chart = QtWidgets.QScrollArea(TempDetails)
        self.detailed_temp_chart.setGeometry(QtCore.QRect(20, 20, 701, 351))
        # self.detailed_temp_chart.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # self.detailed_temp_chart.setWidgetResizable(True)
        self.detailed_temp_chart.setObjectName("detailed_temp_chart")

        # self.scrollAreaWidgetContents = QtWidgets.QWidget()
        # self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 699, 349))
        # self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        # self.detailed_temp_chart.setWidget(self.scrollAreaWidgetContents)

        self.retranslateUi(TempDetails)
        QtCore.QMetaObject.connectSlotsByName(TempDetails)

    def retranslateUi(self, TempDetails):
        _translate = QtCore.QCoreApplication.translate
        TempDetails.setWindowTitle(_translate("TempDetails", "Dialog"))
        self.temp_dialog_close_button.setText(_translate("TempDetails", "OK"))

    def closeWindow(self):
        self.TempDetails.hide()

    def __init__(self):
        self.TempDetails = QtWidgets.QDialog()
        
        self.setupUi(self.TempDetails)
        self.TempDetails.show()

    def update_chart_data(self, data):
        #Move least recent reading off graph
        if (len(self.time) > 9):
            self.time = self.time[1:]
            self.temperature = self.temperature[1:]
        
        #Add most recent time of reading
        # self.time.append(self.time[-1] + 1)
        # self.temperature.append(self.temperature[-1] + ((randint(1, 19) - 10) * 0.1))
        # self.distance.append(self.distance[-1] + ((randint(1, 19) - 10) * 0.1))

        self.time.append(data[0])
        self.temperature.append(data[1])

        #Redraw line
        self.temp_line.setData(self.time, self.temperature)
        
        #self.temp_display.display(self.temperature[-1])
        

def TempDialog(tempData):

    TempDetails = QtWidgets.QDialog()
    ui = Ui_TempDetails()
    
    ui.setupUi(TempDetails)
    
    TempDetails.show()
    

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    TempDetails = QtWidgets.QDialog()
    ui = Ui_TempDetails()
    ui.setupUi(TempDetails)
    TempDetails.show()
    sys.exit(app.exec_())