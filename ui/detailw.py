# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'detailw.ui'
#
# Created: Wed Sep 24 10:03:53 2014
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_DetailWidget(object):
    def setupUi(self, DetailWidget):
        DetailWidget.setObjectName(_fromUtf8("DetailWidget"))
        DetailWidget.resize(873, 920)
        DetailWidget.setStyleSheet(_fromUtf8(""))
        self.iconBG = QtGui.QLabel(DetailWidget)
        self.iconBG.setGeometry(QtCore.QRect(25, 0, 80, 80))
        self.iconBG.setText(_fromUtf8(""))
        self.iconBG.setObjectName(_fromUtf8("iconBG"))
        self.status = QtGui.QLabel(DetailWidget)
        self.status.setGeometry(QtCore.QRect(88, 48, 16, 16))
        self.status.setText(_fromUtf8(""))
        self.status.setObjectName(_fromUtf8("status"))
        self.splitText1 = QtGui.QLabel(DetailWidget)
        self.splitText1.setGeometry(QtCore.QRect(25, 124, 66, 17))
        self.splitText1.setObjectName(_fromUtf8("splitText1"))
        self.summary = QtGui.QTextEdit(DetailWidget)
        self.summary.setGeometry(QtCore.QRect(25, 150, 824, 40))
        self.summary.setObjectName(_fromUtf8("summary"))
        self.description = QtGui.QTextEdit(DetailWidget)
        self.description.setGeometry(QtCore.QRect(25, 190, 824, 81))
        self.description.setObjectName(_fromUtf8("description"))
        self.sshotBG = QtGui.QLabel(DetailWidget)
        self.sshotBG.setGeometry(QtCore.QRect(25, 290, 824, 200))
        self.sshotBG.setText(_fromUtf8(""))
        self.sshotBG.setObjectName(_fromUtf8("sshotBG"))
        self.btnSshotBack = QtGui.QPushButton(DetailWidget)
        self.btnSshotBack.setGeometry(QtCore.QRect(25, 370, 40, 40))
        self.btnSshotBack.setText(_fromUtf8(""))
        self.btnSshotBack.setObjectName(_fromUtf8("btnSshotBack"))
        self.btnSshotNext = QtGui.QPushButton(DetailWidget)
        self.btnSshotNext.setGeometry(QtCore.QRect(807, 370, 40, 40))
        self.btnSshotNext.setText(_fromUtf8(""))
        self.btnSshotNext.setObjectName(_fromUtf8("btnSshotNext"))
        self.splitText3 = QtGui.QLabel(DetailWidget)
        self.splitText3.setGeometry(QtCore.QRect(25, 660, 66, 17))
        self.splitText3.setObjectName(_fromUtf8("splitText3"))
        self.reviewListWidget = QtGui.QListWidget(DetailWidget)
        self.reviewListWidget.setGeometry(QtCore.QRect(25, 810, 824, 85))
        self.reviewListWidget.setAutoFillBackground(True)
        self.reviewListWidget.setObjectName(_fromUtf8("reviewListWidget"))
        self.thumbnail = QtGui.QPushButton(DetailWidget)
        self.thumbnail.setGeometry(QtCore.QRect(350, 380, 1, 1))
        self.thumbnail.setText(_fromUtf8(""))
        self.thumbnail.setObjectName(_fromUtf8("thumbnail"))
        self.sshot = QtGui.QPushButton(DetailWidget)
        self.sshot.setGeometry(QtCore.QRect(350, 410, 1, 1))
        self.sshot.setText(_fromUtf8(""))
        self.sshot.setObjectName(_fromUtf8("sshot"))
        self.splitText2 = QtGui.QLabel(DetailWidget)
        self.splitText2.setGeometry(QtCore.QRect(25, 490, 66, 17))
        self.splitText2.setObjectName(_fromUtf8("splitText2"))
        self.btnUpdate = QtGui.QPushButton(DetailWidget)
        self.btnUpdate.setGeometry(QtCore.QRect(700, 24, 148, 40))
        self.btnUpdate.setText(_fromUtf8(""))
        self.btnUpdate.setObjectName(_fromUtf8("btnUpdate"))
        self.btnInstall = QtGui.QPushButton(DetailWidget)
        self.btnInstall.setGeometry(QtCore.QRect(700, 24, 148, 40))
        self.btnInstall.setText(_fromUtf8(""))
        self.btnInstall.setObjectName(_fromUtf8("btnInstall"))
        self.btnUninstall = QtGui.QPushButton(DetailWidget)
        self.btnUninstall.setGeometry(QtCore.QRect(700, 24, 148, 40))
        self.btnUninstall.setText(_fromUtf8(""))
        self.btnUninstall.setObjectName(_fromUtf8("btnUninstall"))
        self.gradeBG = QtGui.QWidget(DetailWidget)
        self.gradeBG.setGeometry(QtCore.QRect(25, 516, 810, 132))
        self.gradeBG.setObjectName(_fromUtf8("gradeBG"))
        self.gradeText2 = QtGui.QLabel(self.gradeBG)
        self.gradeText2.setGeometry(QtCore.QRect(15, 100, 151, 17))
        self.gradeText2.setText(_fromUtf8(""))
        self.gradeText2.setAlignment(QtCore.Qt.AlignCenter)
        self.gradeText2.setObjectName(_fromUtf8("gradeText2"))
        self.gradeText1 = QtGui.QLabel(self.gradeBG)
        self.gradeText1.setGeometry(QtCore.QRect(520, 60, 90, 17))
        self.gradeText1.setText(_fromUtf8(""))
        self.gradeText1.setObjectName(_fromUtf8("gradeText1"))
        self.grade = QtGui.QLabel(self.gradeBG)
        self.grade.setGeometry(QtCore.QRect(60, 13, 60, 41))
        self.grade.setText(_fromUtf8(""))
        self.grade.setAlignment(QtCore.Qt.AlignCenter)
        self.grade.setObjectName(_fromUtf8("grade"))
        self.vline = QtGui.QLabel(self.gradeBG)
        self.vline.setGeometry(QtCore.QRect(450, 6, 1, 120))
        self.vline.setText(_fromUtf8(""))
        self.vline.setObjectName(_fromUtf8("vline"))
        self.gradetitle = QtGui.QLabel(self.gradeBG)
        self.gradetitle.setGeometry(QtCore.QRect(120, 35, 31, 21))
        self.gradetitle.setText(_fromUtf8(""))
        self.gradetitle.setAlignment(QtCore.Qt.AlignCenter)
        self.gradetitle.setObjectName(_fromUtf8("gradetitle"))
        self.icon = QtGui.QLabel(DetailWidget)
        self.icon.setGeometry(QtCore.QRect(41, 16, 48, 48))
        self.icon.setText(_fromUtf8(""))
        self.icon.setObjectName(_fromUtf8("icon"))
        self.widget = QtGui.QWidget(DetailWidget)
        self.widget.setGeometry(QtCore.QRect(120, 0, 501, 121))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.scoretitle = QtGui.QLabel(self.widget)
        self.scoretitle.setGeometry(QtCore.QRect(0, 96, 66, 18))
        self.scoretitle.setText(_fromUtf8(""))
        self.scoretitle.setObjectName(_fromUtf8("scoretitle"))
        self.size = QtGui.QLabel(self.widget)
        self.size.setGeometry(QtCore.QRect(210, 40, 140, 18))
        self.size.setText(_fromUtf8(""))
        self.size.setObjectName(_fromUtf8("size"))
        self.candidateVersion = QtGui.QLabel(self.widget)
        self.candidateVersion.setGeometry(QtCore.QRect(0, 68, 200, 18))
        self.candidateVersion.setText(_fromUtf8(""))
        self.candidateVersion.setObjectName(_fromUtf8("candidateVersion"))
        self.installedVersion = QtGui.QLabel(self.widget)
        self.installedVersion.setGeometry(QtCore.QRect(0, 38, 200, 18))
        self.installedVersion.setText(_fromUtf8(""))
        self.installedVersion.setObjectName(_fromUtf8("installedVersion"))
        self.name = QtGui.QLabel(self.widget)
        self.name.setGeometry(QtCore.QRect(0, 0, 501, 30))
        self.name.setText(_fromUtf8(""))
        self.name.setObjectName(_fromUtf8("name"))
        self.size_install = QtGui.QLabel(self.widget)
        self.size_install.setGeometry(QtCore.QRect(210, 68, 140, 18))
        self.size_install.setText(_fromUtf8(""))
        self.size_install.setObjectName(_fromUtf8("size_install"))
        self.split1 = QtGui.QLabel(self.widget)
        self.split1.setGeometry(QtCore.QRect(200, 38, 1, 18))
        self.split1.setText(_fromUtf8(""))
        self.split1.setObjectName(_fromUtf8("split1"))
        self.split2 = QtGui.QLabel(self.widget)
        self.split2.setGeometry(QtCore.QRect(200, 68, 1, 18))
        self.split2.setText(_fromUtf8(""))
        self.split2.setObjectName(_fromUtf8("split2"))
        self.fen = QtGui.QLabel(self.widget)
        self.fen.setGeometry(QtCore.QRect(160, 96, 21, 18))
        self.fen.setText(_fromUtf8(""))
        self.fen.setObjectName(_fromUtf8("fen"))
        self.scorelabel = QtGui.QLabel(self.widget)
        self.scorelabel.setGeometry(QtCore.QRect(136, 96, 21, 18))
        self.scorelabel.setText(_fromUtf8(""))
        self.scorelabel.setObjectName(_fromUtf8("scorelabel"))
        self.reviewText = QtGui.QTextEdit(DetailWidget)
        self.reviewText.setGeometry(QtCore.QRect(25, 685, 824, 76))
        self.reviewText.setObjectName(_fromUtf8("reviewText"))
        self.bntSubmit = QtGui.QPushButton(DetailWidget)
        self.bntSubmit.setGeometry(QtCore.QRect(749, 762, 100, 32))
        self.bntSubmit.setText(_fromUtf8(""))
        self.bntSubmit.setObjectName(_fromUtf8("bntSubmit"))

        self.retranslateUi(DetailWidget)
        QtCore.QMetaObject.connectSlotsByName(DetailWidget)

    def retranslateUi(self, DetailWidget):
        DetailWidget.setWindowTitle(_translate("DetailWidget", "Form", None))
        self.splitText1.setText(_translate("DetailWidget", "软件介绍", None))
        self.splitText3.setText(_translate("DetailWidget", "用户评论", None))
        self.splitText2.setText(_translate("DetailWidget", "软件评分", None))

