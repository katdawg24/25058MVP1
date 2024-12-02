# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TempDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


import math
from random import randint
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import pyqtgraph as pg
from PyQt5.QtGui import QStandardItem, QStandardItemModel


class Ui_DistanceDetails(object):
    def setupUi(self, DistanceDetails, df):
        DistanceDetails.setObjectName("DistanceDetails")
        DistanceDetails.resize(1050, 500)

        self.Distance_dialog_close_button = QtWidgets.QPushButton(DistanceDetails)
        self.Distance_dialog_close_button.setGeometry(QtCore.QRect(890, 450, 121, 31))
        self.Distance_dialog_close_button.setObjectName("Distance_dialog_close_button")
        self.Distance_dialog_close_button.clicked.connect(self.closeWindow)

        self.tableView = QtWidgets.QTableWidget(DistanceDetails)
        self.tableView.setGeometry(QtCore.QRect(770, 20, 255, 380))
        self.tableView.setObjectName("Distance_table")
        self.last_time = 0
        self.tableView.setColumnCount(2)
        self.tableView.setHorizontalHeaderLabels(["Time (s)", "Distance (mm)"])
        # Create a model for the table
        # self.table_model = QStandardItemModel()
        # self.table_model.setHorizontalHeaderLabels(["Time", "Temperature"])
        # self.tableView.setModel(self.table_model)

        self.detailed_distance_chart = pg.PlotWidget(DistanceDetails)
        self.detailed_distance_chart.setBackground("w")
        pen = pg.mkPen(color=(255,0,0))
        self.detailed_distance_chart.setTitle("Distance vs Time", color="k", size="15pt")
        styles = {"color": "red", "font-size": "10px"}
        self.detailed_distance_chart.setLabel("left", "Distance ", **styles)
        self.detailed_distance_chart.setLabel("bottom", "Time (min)", **styles)
        #self.detailed_distance_chart.addLegend()
        self.detailed_distance_chart.showGrid(x=True, y=True)
        self.detailed_distance_chart.setYRange(4, 12)
        self.time = df['Time'].tolist()
        self.distance = df['Distance'].tolist()
        

        self.distance_line = self.detailed_distance_chart.plot(
            self.time,
            self.distance,
            name="Distance Sensor",
            pen=pen
        )

        for index, row in df.iterrows():
            self.tableView.setRowCount(self.tableView.rowCount() + 1)
            self.tableView.setItem(self.tableView.rowCount() - 1, 0, QtWidgets.QTableWidgetItem(str(row['Time'])))
            self.tableView.setItem(self.tableView.rowCount() - 1, 1, QtWidgets.QTableWidgetItem(str(row['Distance'])))

        # self.detailed_distance_chart = QtWidgets.QScrollArea(DistanceDetails)
        self.detailed_distance_chart.setGeometry(QtCore.QRect(20, 20, 720, 380))
        # self.detailed_distance_chart.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # self.detailed_distance_chart.setWidgetResizable(True)
        self.detailed_distance_chart.setObjectName("detailed_distance_chart")

        # self.scrollAreaWidgetContents = QtWidgets.QWidget()
        # self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 699, 349))
        # self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        # self.detailed_distance_chart.setWidget(self.scrollAreaWidgetContents)

        self.retranslateUi(DistanceDetails)
        QtCore.QMetaObject.connectSlotsByName(DistanceDetails)

    def retranslateUi(self, DistanceDetails):
        _translate = QtCore.QCoreApplication.translate
        DistanceDetails.setWindowTitle(_translate("DistanceDetails", "Dialog"))
        self.Distance_dialog_close_button.setText(_translate("DistanceDetails", "Close"))


    def closeWindow(self):
        self.DistanceDetails.hide()

    def __init__(self, df):
        self.DistanceDetails = QtWidgets.QDialog()
        
        self.setupUi(self.DistanceDetails, df)
        self.DistanceDetails.show()

    def update_chart_data(self, data):
        #Move least recent reading off graph
        if (len(self.time) > 9):
            self.time = self.time[1:]
            self.distance = self.distance[1:]

        self.time.append(data[0])
        self.distance.append(data[2])

        #Redraw line
        self.distance_line.setData(self.time, self.distance)

        
        # if (math.floor(data[0]) - math.floor(self.last_time) > 0):
        self.update_table_data(data[0], data[2])
            
        self.last_time = data[0]
        
        #self.distance_display.display(self.distance[-1])

    def update_table_data(self, time, distance):
        self.tableView.setRowCount(self.tableView.rowCount() + 1)
        self.tableView.setItem(self.tableView.rowCount() - 1, 0, QtWidgets.QTableWidgetItem(str(time)))
        self.tableView.setItem(self.tableView.rowCount() - 1, 1, QtWidgets.QTableWidgetItem(str(distance)))

    def update_table(self, data):
        # Add the most recent data to the table
        if len(data) == 2:  # Check that data contains 2 fields [time, distance]
            time, distance = data
            time_item = QStandardItem(str(time))
            distance_item = QStandardItem(f"{distance:.2f}mm")

            # Insert the new row at the top
            self.table_model.insertRow(0, [time_item, distance_item])

            # limit the number of rows displayed
            if self.table_model.rowCount() > 20:
                self.table_model.removeRow(self.table_model.rowCount() - 1)

    

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    DistanceDetails = QtWidgets.QDialog()
    ui = Ui_DistanceDetails()
    ui.setupUi(DistanceDetails)
    DistanceDetails.show()
    sys.exit(app.exec_())