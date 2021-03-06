# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


import pathlib

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_main_window(object):
    def setupUi(self, main_window):
        directory = str(pathlib.Path(__file__).parent.absolute())

        main_window.setObjectName("main_window")
        main_window.resize(710, 398)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        main_window.setFont(font)
        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")
        self.up_btn = QtWidgets.QPushButton(self.centralwidget)
        self.up_btn.setGeometry(QtCore.QRect(100, 10, 80, 80))
        self.up_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.up_btn.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(directory+"/images/up-arrow.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.up_btn.setIcon(icon)
        self.up_btn.setIconSize(QtCore.QSize(50, 50))
        self.up_btn.setObjectName("up_btn")
        self.left_btn = QtWidgets.QPushButton(self.centralwidget)
        self.left_btn.setGeometry(QtCore.QRect(10, 100, 80, 80))
        self.left_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.left_btn.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(directory+"/images/left-arrow.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.left_btn.setIcon(icon1)
        self.left_btn.setIconSize(QtCore.QSize(50, 50))
        self.left_btn.setObjectName("left_btn")
        self.right_btn = QtWidgets.QPushButton(self.centralwidget)
        self.right_btn.setGeometry(QtCore.QRect(190, 100, 80, 80))
        self.right_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.right_btn.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(directory+"/images/right-arrow.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.right_btn.setIcon(icon2)
        self.right_btn.setIconSize(QtCore.QSize(50, 50))
        self.right_btn.setObjectName("right_btn")
        self.down_btn = QtWidgets.QPushButton(self.centralwidget)
        self.down_btn.setGeometry(QtCore.QRect(100, 190, 80, 80))
        self.down_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.down_btn.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(directory+"/images/down-arrow.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.down_btn.setIcon(icon3)
        self.down_btn.setIconSize(QtCore.QSize(50, 50))
        self.down_btn.setObjectName("down_btn")
        self.stop_btn = QtWidgets.QPushButton(self.centralwidget)
        self.stop_btn.setGeometry(QtCore.QRect(100, 100, 80, 80))
        self.stop_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.stop_btn.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(directory+"/images/stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.stop_btn.setIcon(icon4)
        self.stop_btn.setIconSize(QtCore.QSize(50, 50))
        self.stop_btn.setObjectName("stop_btn")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 300, 291, 89))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.cmd_send_pnl = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.cmd_send_pnl.setContentsMargins(0, 0, 0, 0)
        self.cmd_send_pnl.setObjectName("cmd_send_pnl")
        self.cmd_tf = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.cmd_tf.setText("")
        self.cmd_tf.setObjectName("cmd_tf")
        self.cmd_send_pnl.addWidget(self.cmd_tf)
        self.send_btn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.send_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.send_btn.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(directory+"/images/send.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.send_btn.setIcon(icon5)
        self.send_btn.setIconSize(QtCore.QSize(40, 40))
        self.send_btn.setAutoDefault(False)
        self.send_btn.setFlat(True)
        self.send_btn.setObjectName("send_btn")
        self.cmd_send_pnl.addWidget(self.send_btn)
        self.point_loc_tab = QtWidgets.QTableWidget(self.centralwidget)
        self.point_loc_tab.setGeometry(QtCore.QRect(320, 10, 381, 192))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.point_loc_tab.setFont(font)
        self.point_loc_tab.setObjectName("point_loc_tab")
        self.point_loc_tab.setColumnCount(3)
        self.point_loc_tab.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.point_loc_tab.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.point_loc_tab.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.point_loc_tab.setHorizontalHeaderItem(2, item)
        self.process_btn = QtWidgets.QPushButton(self.centralwidget)
        self.process_btn.setGeometry(QtCore.QRect(640, 310, 60, 60))
        self.process_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.process_btn.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(directory+"/images/process.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.process_btn.setIcon(icon6)
        self.process_btn.setIconSize(QtCore.QSize(40, 40))
        self.process_btn.setObjectName("process_btn")
        self.gps_btn = QtWidgets.QPushButton(self.centralwidget)
        self.gps_btn.setGeometry(QtCore.QRect(640, 210, 60, 60))
        self.gps_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.gps_btn.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(directory+"/images/satellite.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.gps_btn.setIcon(icon7)
        self.gps_btn.setIconSize(QtCore.QSize(40, 40))
        self.gps_btn.setObjectName("gps_btn")
        self.area_lb = QtWidgets.QLabel(self.centralwidget)
        self.area_lb.setGeometry(QtCore.QRect(340, 320, 291, 41))
        self.area_lb.setFrameShape(QtWidgets.QFrame.Box)
        self.area_lb.setWordWrap(True)
        self.area_lb.setObjectName("area_lb")
        main_window.setCentralWidget(self.centralwidget)

        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "Planometer | Control Station"))
        item = self.point_loc_tab.horizontalHeaderItem(0)
        item.setText(_translate("main_window", "Latitude"))
        item = self.point_loc_tab.horizontalHeaderItem(1)
        item.setText(_translate("main_window", "Longitude"))
        item = self.point_loc_tab.horizontalHeaderItem(2)
        item.setText(_translate("main_window", "Altitude"))
        self.area_lb.setText(_translate("main_window", "Estimated Area:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = Ui_main_window()
    ui.setupUi(main_window)
    main_window.show()
    sys.exit(app.exec_())
