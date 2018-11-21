# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\WinPyQt5.9-32bit-3.5.3.1\Worksapce\test\test.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
import os
import time
class Ui_Form(object):

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1316, 805)
        self.g_Image = None

        self.Clock = False
        self.running = False
        self.lineEditCircle = QtWidgets.QLineEdit(Form)
        self.lineEditCircle.setGeometry(QtCore.QRect(1230, 270, 61, 20))
        self.lineEditCircle.setObjectName("lineEditCircle")
        self.pushButtonBase = QtWidgets.QPushButton(Form)
        self.pushButtonBase.setGeometry(QtCore.QRect(1140, 430, 81, 23))
        self.pushButtonBase.setObjectName("pushButtonBase")
        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setGeometry(QtCore.QRect(1208, 180, 81, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.lineEditClass = QtWidgets.QLineEdit(Form)
        self.lineEditClass.setGeometry(QtCore.QRect(1230, 310, 61, 20))
        self.lineEditClass.setObjectName("lineEditClass")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(1070, 180, 51, 31))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(1070, 260, 51, 31))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(1150, 260, 61, 31))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(1130, 300, 91, 31))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(1070, 430, 51, 31))
        self.label_5.setObjectName("label_5")
        self.pushButtonRun = QtWidgets.QPushButton(Form)
        self.pushButtonRun.setGeometry(QtCore.QRect(1140, 480, 81, 23))
        self.pushButtonRun.setObjectName("pushButtonRun")
        self.pushButtonVer = QtWidgets.QPushButton(Form)
        self.pushButtonVer.setGeometry(QtCore.QRect(1120, 360, 81, 23))
        self.pushButtonVer.setObjectName("pushButtonVer")
        self.pushButtonSave = QtWidgets.QPushButton(Form)
        self.pushButtonSave.setGeometry(QtCore.QRect(1220, 360, 81, 23))
        self.pushButtonSave.setObjectName("pushButtonSave")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(40, 50, 961, 541))
        self.label_6.setScaledContents(True)
        self.label_6.setObjectName("label_6")
        self.pushButtonBack = QtWidgets.QPushButton(Form)
        self.pushButtonBack.setGeometry(QtCore.QRect(1230, 430, 75, 23))
        self.pushButtonBack.setObjectName("pushButtonBack")
        self.pushButtonBase.raise_()
        self.lineEditCircle.raise_()
        self.comboBox.raise_()
        self.lineEditClass.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
        self.label_4.raise_()
        self.label_5.raise_()
        self.pushButtonRun.raise_()
        self.pushButtonVer.raise_()
        self.pushButtonSave.raise_()
        self.label_6.raise_()
        self.pushButtonBack.raise_()

        self.Box = QtWidgets.QMessageBox(Form)
        self.Box.setGeometry(100, 100, 250, 150)

        self.Box.setObjectName('Tooltips')


        # self.setWindowIcon(QtGui.QIcon())
        # self.Box.center()
        # self.show()




        self.pushButtonVer.clicked.connect(self.messageBBox)
        self.pushButtonSave.clicked.connect(self.SaveBase)
        self.pushButtonBase.clicked.connect(self.BaseStandard)
        self.pushButtonRun.clicked.connect(self.Running)
        self.pushButtonBack.clicked.connect(self.UnClock)

        self.pushButtonSave.setEnabled(False)
        self.pushButtonVer.setEnabled(False)
        self.pushButtonBack.setEnabled(False)

        self.lineEditCircle.setEnabled(False)
        self.lineEditClass.setEnabled(False)
        self.comboBox.setEnabled(False)

        self.PartImg = cv2.imread('PartCut.png', cv2.IMREAD_COLOR)

        if self.PartImg!=None:
            Partrows, Partcols, _ = self.PartImg.shape

            self.PartImg = cv2.resize(self.PartImg, (int(Partrows / 2), int(Partcols / 2)))

            self.PartImg_gray = cv2.cvtColor(self.PartImg, cv2.COLOR_BGR2GRAY)

            self.Partrows, self.Partcols, _ = self.PartImg.shape
        else:
            QtWidgets.QMessageBox.warning(self.Box, "warning", "请进行基准标定!")
            # self.box = QtWidgets.QMessageBox()
            # self.box.warning(self, "warn","请进行基准标定！",QtWidgets.QMessageBox.Ok|QtWidgets.QMessageBox.Cancel,QtWidgets.QMessageBox.Ok)



        self.THRESHHOLD = 0.65



        self.timer = QtCore.QTimer()
        self.cap = cv2.VideoCapture(0)  # 开启摄像头
        size = (int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
        print(size)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 5000)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 5000)

        self.timer.timeout.connect(self.start)
        self.timer.start(0.1)  # 实时刷新，不然视频不动态
        # self.timer.setInterval(100)  # 设置刷新时间



        self.retranslateUi(Form)
        # self.start()
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.lineEditCircle.setText(_translate("Form", "规格尺寸"))
        # self.lineEditCircle
        self.pushButtonBase.setText(_translate("Form", "基准标定"))
        self.comboBox.setItemText(0, _translate("Form", "方形卡口"))
        self.comboBox.setItemText(1, _translate("Form", "圆形卡口"))
        self.lineEditClass.setText(_translate("Form", "类别选择"))
        self.label.setText(_translate("Form", "类别选择："))
        self.label_2.setText(_translate("Form", "规格尺寸："))
        self.label_3.setText(_translate("Form", "圆环半径"))
        self.label_4.setText(_translate("Form", "卡口到圆心距离"))
        self.label_5.setText(_translate("Form", "功能："))
        self.pushButtonRun.setText(_translate("Form", "运行"))
        self.pushButtonVer.setText(_translate("Form", "修改"))
        self.pushButtonSave.setText(_translate("Form", "保存"))
        self.label_6.setText(_translate("Form", "TextLabel"))
        self.pushButtonBack.setText(_translate("Form", "回到视频"))

    def start(self):
        start = time.time()
        # time.sleep(1)

        if self.Clock == True:
            return

        # print(t)  # 原始时间数据
        # print(int(t))  # 秒级时间戳
        # print(int(round(t * 1000)))  # 毫秒级时间戳

        """ 开启视频"""

        end = time.time()

        # print(int(round((end-start)*1000)))


        if (self.cap.isOpened()):
            # get a frame

            ret, img = self.cap.read()

            self.g_Image = img.copy()
            # print(self.g_Image.shape)


            # height, width, _ = img.shape
            # cv2.resize()
            # img_size = cv2.resize(img, (height//2, width // 2))
            self.Clock = False
            height, width, bytesPerComponent = img.shape
            # print(img.shape)
            bytesPerLine = bytesPerComponent * width

            # 变换彩色空间顺序

            # img_size = cv2.resize(img,(width,height/2))
            # cv2.cvtColor(img, cv2.COLOR_BGR2RGB, img)
            # 转为QImage对象
            self.image = QtGui.QImage(img.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888).rgbSwapped()
            # self.label_6.setPixmap(QtGui.QPixmap.fromImage(self.image).scaled(self.label.width(), self.label.height()))
            self.label_6.setPixmap(QtGui.QPixmap.fromImage(self.image).scaled(width,height))
            end1 = time.time()
            # print(int(round((end1 - start) * 1000)))

        else:

            res = QtWidgets.QMessageBox.warning(self.Box, "Error", "请连接摄像机!")
            if res==QtWidgets.QMessageBox.yes:
                self.Box.

    def messageBBox(self):
        self.comboBox.setEnabled(True)
        self.pushButtonSave.setEnabled(True)
        self.pushButtonVer.setEnabled(False)

        self.lineEditCircle.setEnabled(True)
        self.lineEditClass.setEnabled(True)
        # self.lineEditCircle.setText("")
        # self.lineEditClass.setText("")
    def SaveBase(self):
        self.pushButtonBack.setEnabled(False)
        self.lineEditCircle.setEnabled(False)
        self.lineEditClass.setEnabled(False)
        self.pushButtonSave.setEnabled(False)
        self.pushButtonVer.setEnabled(False)
        self.Clock = False
        str = self.lineEditCircle.text()
        print(str)
        dt = self.comboBox.currentIndex()
        print(dt)
        # box = QtWidgets.QMessageBox()
        # box.warning(self, "提示", (str))
        cv2.imwrite("base.jpg", self.g_Image)

    def BaseStandard(self):

        self.Clock = True   #lock
        self.running = False
        self.pushButtonRun.setEnabled(True)

        self.comboBox.setEnabled(True)
        self.pushButtonSave.setEnabled(True)
        self.pushButtonVer.setEnabled(True)
        self.pushButtonBack.setEnabled(True)

        self.lineEditCircle.setEnabled(True)
        self.lineEditClass.setEnabled(True)

    def UnClock(self):
        self.Clock = False  # lock
        self.comboBox.setEnabled(False)
        self.pushButtonSave.setEnabled(False)
        self.pushButtonVer.setEnabled(False)
        self.pushButtonBack.setEnabled(False)

        self.lineEditCircle.setEnabled(False)
        self.lineEditClass.setEnabled(False)


    def Running(self):

        self.running = True
        self.pushButtonRun.setEnabled(False)







