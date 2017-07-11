# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'zhihu_registeraccount.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form_RegisterAccount(object):
    def setupUi(self, Form_RegisterAccount):
        Form_RegisterAccount.setObjectName("Form_RegisterAccount")
        Form_RegisterAccount.resize(342, 159)
        self.comboBox_registerType = QtWidgets.QComboBox(Form_RegisterAccount)
        self.comboBox_registerType.setGeometry(QtCore.QRect(90, 30, 69, 22))
        self.comboBox_registerType.setObjectName("comboBox_registerType")
        self.label = QtWidgets.QLabel(Form_RegisterAccount)
        self.label.setGeometry(QtCore.QRect(20, 32, 61, 20))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form_RegisterAccount)
        self.label_2.setGeometry(QtCore.QRect(30, 70, 54, 21))
        self.label_2.setObjectName("label_2")
        self.lineEdit_registerCount = QtWidgets.QLineEdit(Form_RegisterAccount)
        self.lineEdit_registerCount.setGeometry(QtCore.QRect(90, 70, 71, 20))
        self.lineEdit_registerCount.setObjectName("lineEdit_registerCount")
        self.label_3 = QtWidgets.QLabel(Form_RegisterAccount)
        self.label_3.setGeometry(QtCore.QRect(180, 70, 61, 21))
        self.label_3.setObjectName("label_3")
        self.lineEdit_registerCompleteCount = QtWidgets.QLineEdit(Form_RegisterAccount)
        self.lineEdit_registerCompleteCount.setGeometry(QtCore.QRect(250, 70, 71, 20))
        self.lineEdit_registerCompleteCount.setObjectName("lineEdit_registerCompleteCount")
        self.pushButton_registerStart = QtWidgets.QPushButton(Form_RegisterAccount)
        self.pushButton_registerStart.setGeometry(QtCore.QRect(90, 110, 75, 23))
        self.pushButton_registerStart.setObjectName("pushButton_registerStart")
        self.pushButton_registerStop = QtWidgets.QPushButton(Form_RegisterAccount)
        self.pushButton_registerStop.setGeometry(QtCore.QRect(190, 110, 75, 23))
        self.pushButton_registerStop.setObjectName("pushButton_registerStop")

        self.retranslateUi(Form_RegisterAccount)
        QtCore.QMetaObject.connectSlotsByName(Form_RegisterAccount)

    def retranslateUi(self, Form_RegisterAccount):
        _translate = QtCore.QCoreApplication.translate
        Form_RegisterAccount.setWindowTitle(_translate("Form_RegisterAccount", "账号注册"))
        self.label.setText(_translate("Form_RegisterAccount", "是否有头像"))
        self.label_2.setText(_translate("Form_RegisterAccount", "注册数量"))
        self.label_3.setText(_translate("Form_RegisterAccount", "已完成数量"))
        self.pushButton_registerStart.setText(_translate("Form_RegisterAccount", "开始注册"))
        self.pushButton_registerStop.setText(_translate("Form_RegisterAccount", "停止注册"))

