# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'builder_interface.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(852, 624)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.rotate_90 = QtWidgets.QPushButton(self.centralwidget)
        self.rotate_90.setObjectName("rotate_90")
        self.gridLayout_2.addWidget(self.rotate_90, 0, 3, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 4, 1, 1)
        self.add_road = QtWidgets.QPushButton(self.centralwidget)
        self.add_road.setAutoDefault(False)
        self.add_road.setDefault(False)
        self.add_road.setFlat(False)
        self.add_road.setObjectName("add_road")
        self.gridLayout_2.addWidget(self.add_road, 2, 0, 1, 1)
        self.del_object = QtWidgets.QPushButton(self.centralwidget)
        self.del_object.setObjectName("del_object")
        self.gridLayout_2.addWidget(self.del_object, 3, 0, 1, 1)
        self.add_intersection = QtWidgets.QPushButton(self.centralwidget)
        self.add_intersection.setEnabled(True)
        self.add_intersection.setObjectName("add_intersection")
        self.gridLayout_2.addWidget(self.add_intersection, 1, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 9, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem2, 5, 0, 1, 1)
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout_2.addWidget(self.graphicsView, 1, 2, 9, 3)
        self.save_json = QtWidgets.QPushButton(self.centralwidget)
        self.save_json.setObjectName("save_json")
        self.gridLayout_2.addWidget(self.save_json, 0, 0, 1, 1)
        self.rotate90 = QtWidgets.QPushButton(self.centralwidget)
        self.rotate90.setObjectName("rotate90")
        self.gridLayout_2.addWidget(self.rotate90, 0, 2, 1, 1)
        self.obj_param_b = QtWidgets.QPushButton(self.centralwidget)
        self.obj_param_b.setObjectName("obj_param_b")
        self.gridLayout_2.addWidget(self.obj_param_b, 4, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 852, 30))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.json_settings = QtWidgets.QAction(MainWindow)
        self.json_settings.setObjectName("json_settings")
        self.actionParse_items = QtWidgets.QAction(MainWindow)
        self.actionParse_items.setObjectName("actionParse_items")
        self.parse_items = QtWidgets.QAction(MainWindow)
        self.parse_items.setObjectName("parse_items")
        self.menuFile.addAction(self.parse_items)
        self.menuSettings.addAction(self.json_settings)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "RoadBuilder"))
        self.rotate_90.setText(_translate("MainWindow", "Rotate -90"))
        self.add_road.setText(_translate("MainWindow", "Add road"))
        self.del_object.setText(_translate("MainWindow", "Delete"))
        self.add_intersection.setText(_translate("MainWindow", "Add intersection"))
        self.save_json.setText(_translate("MainWindow", "Save"))
        self.rotate90.setText(_translate("MainWindow", "Rotate 90"))
        self.obj_param_b.setText(_translate("MainWindow", "Object parameters"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.json_settings.setText(_translate("MainWindow", "Object JSON settings"))
        self.actionParse_items.setText(_translate("MainWindow", "Parse items"))
        self.parse_items.setText(_translate("MainWindow", "Parse created items"))
