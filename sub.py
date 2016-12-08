# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sub.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.btn_cancel = QtWidgets.QPushButton(Dialog)
        self.btn_cancel.setGeometry(QtCore.QRect(300, 250, 75, 23))
        self.btn_cancel.setObjectName("btn_cancel")
        self.txt_jitikai = QtWidgets.QLineEdit(Dialog)
        self.txt_jitikai.setGeometry(QtCore.QRect(160, 50, 113, 20))
        self.txt_jitikai.setObjectName("txt_jitikai")
        self.txt_kumi = QtWidgets.QLineEdit(Dialog)
        self.txt_kumi.setGeometry(QtCore.QRect(30, 50, 113, 20))
        self.txt_kumi.setObjectName("txt_kumi")
        self.txt_han = QtWidgets.QLineEdit(Dialog)
        self.txt_han.setGeometry(QtCore.QRect(30, 90, 113, 20))
        self.txt_han.setObjectName("txt_han")
        self.txt_name = QtWidgets.QLineEdit(Dialog)
        self.txt_name.setGeometry(QtCore.QRect(30, 120, 113, 20))
        self.txt_name.setObjectName("txt_name")
        self.txt_address = QtWidgets.QLineEdit(Dialog)
        self.txt_address.setGeometry(QtCore.QRect(30, 160, 113, 20))
        self.txt_address.setObjectName("txt_address")
        self.txt_tel1 = QtWidgets.QLineEdit(Dialog)
        self.txt_tel1.setGeometry(QtCore.QRect(30, 200, 113, 20))
        self.txt_tel1.setObjectName("txt_tel1")
        self.txt_tel2 = QtWidgets.QLineEdit(Dialog)
        self.txt_tel2.setGeometry(QtCore.QRect(40, 240, 113, 20))
        self.txt_tel2.setObjectName("txt_tel2")
        self.lbl_no = QtWidgets.QLabel(Dialog)
        self.lbl_no.setGeometry(QtCore.QRect(50, 20, 50, 12))
        self.lbl_no.setObjectName("lbl_no")
        self.btnMap = QtWidgets.QPushButton(Dialog)
        self.btnMap.setGeometry(QtCore.QRect(300, 210, 75, 23))
        self.btnMap.setObjectName("btnMap")

        self.retranslateUi(Dialog)
        self.btn_cancel.clicked.connect(Dialog.close)
        self.btnMap.clicked.connect(Dialog.map_show)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.btn_cancel.setText(_translate("Dialog", "キャンセル"))
        self.lbl_no.setText(_translate("Dialog", "TextLabel"))
        self.btnMap.setText(_translate("Dialog", "地図表示"))

