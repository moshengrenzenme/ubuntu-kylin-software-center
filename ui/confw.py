# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'confw.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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

class Ui_ConfigWidget(object):
    def setupUi(self, ConfigWidget):
        ConfigWidget.setObjectName(_fromUtf8("ConfigWidget"))
        ConfigWidget.resize(568, 480)
        self.pageListWidget = QtGui.QListWidget(ConfigWidget)
        self.pageListWidget.setGeometry(QtCore.QRect(16, 33, 96, 391))
        self.pageListWidget.setObjectName(_fromUtf8("pageListWidget"))
        self.sourceWidget = QtGui.QWidget(ConfigWidget)
        self.sourceWidget.setGeometry(QtCore.QRect(130, 50, 480, 361))
        self.sourceWidget.setObjectName(_fromUtf8("sourceWidget"))

        self.passwordWidget = QtGui.QWidget(ConfigWidget)
        self.passwordWidget.setGeometry(QtCore.QRect(0, 0, 480, 461))
        self.passwordWidget.setObjectName(_fromUtf8("passwordWidget"))

        self.groupBox_password = QtGui.QGroupBox(self.passwordWidget)
        self.groupBox_password.setGeometry(QtCore.QRect(0, 0, 480, 200))
        self.text8 = QtGui.QLabel(self.groupBox_password)
        self.text8.setGeometry(QtCore.QRect(140, 60, 200, 20))
        self.text8.setText(_fromUtf8(""))
        self.text8.setObjectName(_fromUtf8("text8"))
        #self.checkBox_8.setFont(font)
        #self.checkBox_8.setObjectName(_fromUtf8("checkBox_8"))
        #self.checkBox_8 = QtGui.QCheckBox(self.groupBox_password)
        #self.checkBox_8.setGeometry(QtCore.QRect(90, 80, 81, 24))
        self.lesource8 = QtGui.QLineEdit(self.groupBox_password)
        self.lesource8.setGeometry(QtCore.QRect(200, 90, 230, 32))
        self.lesource8.setObjectName(_fromUtf8("lesource8"))
        self.lesource9 = QtGui.QLineEdit(self.groupBox_password)
        self.lesource9.setGeometry(QtCore.QRect(200,130 , 230, 32))
        self.lesource9.setObjectName(_fromUtf8("lesource9"))
        self.text16 = QtGui.QLabel(self.groupBox_password)
        self.text16.setGeometry(QtCore.QRect(150, 95, 50, 20))
        self.text16.setText(_fromUtf8(""))
        self.text16.setObjectName(_fromUtf8("text16"))
        self.text17 = QtGui.QLabel(self.groupBox_password)
        self.text17.setGeometry(QtCore.QRect(150, 135, 50, 20))
        self.text17.setText(_fromUtf8(""))
        self.text17.setObjectName(_fromUtf8("text17"))


        self.groupBox_recover = QtGui.QGroupBox(self.passwordWidget)
        self.groupBox_recover.setGeometry(QtCore.QRect(0, 200, 480, 460))
        self.lesource11 = QtGui.QLineEdit(self.groupBox_recover)
        self.lesource11.setGeometry(QtCore.QRect(200, 50, 230, 32))
        self.lesource11.setObjectName(_fromUtf8("lesource11"))
        self.lesource12 = QtGui.QLineEdit(self.groupBox_recover)
        self.lesource12.setGeometry(QtCore.QRect(200, 90 , 230, 32))
        self.lesource12.setObjectName(_fromUtf8("lesource12"))

        self.lesource13 = QtGui.QLineEdit(self.groupBox_recover)
        self.lesource13.setGeometry(QtCore.QRect(200,130 , 230, 32))
        self.lesource13.setObjectName(_fromUtf8("lesource13"))
        self.text18 = QtGui.QLabel(self.groupBox_recover)
        self.text18.setGeometry(QtCore.QRect(150, 55, 50, 20))
        self.text18.setText(_fromUtf8(""))
        self.text18.setObjectName(_fromUtf8("text18"))
        self.text19 = QtGui.QLabel(self.groupBox_recover)
        self.text19.setGeometry(QtCore.QRect(150, 95, 50, 20))
        self.text19.setText(_fromUtf8(""))
        self.text19.setObjectName(_fromUtf8("text19"))
        self.text20 = QtGui.QLabel(self.groupBox_recover)
        self.text20.setGeometry(QtCore.QRect(150, 135, 50, 20))
        self.text20.setText(_fromUtf8(""))
        self.text20.setObjectName(_fromUtf8("text20"))


        self.text9 = QtGui.QLabel(self.groupBox_recover)
        self.text9.setGeometry(QtCore.QRect(140, 0, 200, 20))
        self.text9.setText(_fromUtf8(""))
        self.text9.setObjectName(_fromUtf8("text9"))

        self.btnAdd_2 = QtGui.QPushButton(self.groupBox_password)
        self.btnAdd_2.setGeometry(QtCore.QRect(400,170,80,25))
        self.btnAdd_2.setText(_fromUtf8(""))
        self.btnAdd_2.setObjectName(_fromUtf8("btnAdd_2"))
        self.btnAdd_3 = QtGui.QPushButton(self.groupBox_recover)
        self.btnAdd_3.setGeometry(QtCore.QRect(400,180,80,25))
        self.btnAdd_3.setText(_fromUtf8(""))
        self.btnAdd_3.setObjectName(_fromUtf8("btnAdd_3"))


        #self.recoverWidget = QtGui.QWidget(ConfigWidget)
        #self.recoverWidget.setGeometry(QtCore.QRect(0, 0, 480, 461))
        #self.recoverWidget.setObjectName(_fromUtf8("recoverWidget"))
        #self.groupBox_recover = QtGui.QGroupBox(self.recoverWidget)
        #self.groupBox_recover.setGeometry(QtCore.QRect(10, 90, 472, 185))
        #self.text11 = QtGui.QLabel(self.groupBox_recover)
        #self.text11.setGeometry(QtCore.QRect(140, 60, 200, 20))
        #self.text11.setText(_fromUtf8(""))
        #self.text11.setObjectName(_fromUtf8("text11"))
        #self.checkBox_8.setFont(font)
        #self.checkBox_8.setObjectName(_fromUtf8("checkBox_8"))
        #self.checkBox_8 = QtGui.QCheckBox(self.groupBox_password)
        #self.checkBox_8.setGeometry(QtCore.QRect(90, 60, 81, 24))
        #self.lesource11 = QtGui.QLineEdit(self.groupBox_recover)
        #self.lesource11.setGeometry(QtCore.QRect(130, 100, 230, 32))
        #self.lesource11.setObjectName(_fromUtf8("lesource11"))
        #self.lesource12 = QtGui.QLineEdit(self.groupBox_recover)
        #self.lesource12.setGeometry(QtCore.QRect(130,140 , 230, 32))
        #self.lesource12.setObjectName(_fromUtf8("lesource12"))
        #self.lesource13 = QtGui.QLineEdit(self.groupBox_recover)
        #self.lesource13.setGeometry(QtCore.QRect(130,160 , 230, 32))
        #self.lesource13.setObjectName(_fromUtf8("lesource13"))
        


        self.userWidget = QtGui.QWidget(ConfigWidget)
        self.userWidget.setGeometry(QtCore.QRect(0, 0, 480, 461))
        self.userWidget.setObjectName(_fromUtf8("userWidget"))
        self.groupBox_user = QtGui.QGroupBox(self.userWidget)
        self.groupBox_user.setGeometry(QtCore.QRect(0, 0, 480, 461))
        self.text2 = QtGui.QLabel(self.groupBox_user)
        self.text2.setGeometry(QtCore.QRect(140, 240, 100, 20))
        self.text2.setText(_fromUtf8(""))
        self.text2.setObjectName(_fromUtf8("text2"))

        self.btnAdd_4 = QtGui.QPushButton(self.groupBox_user)
        self.btnAdd_4.setGeometry(QtCore.QRect(400,155,80,25))
        self.btnAdd_4.setText(_fromUtf8(""))
        self.btnAdd_4.setObjectName(_fromUtf8("btnAdd_4"))


        self.lesource14 = QtGui.QLineEdit(self.groupBox_user)
        self.lesource14.setGeometry(QtCore.QRect(200,100 ,230, 32))
        self.lesource14.setObjectName(_fromUtf8("lesource14"))

#        self.lesource15 = QtGui.QLineEdit(self.groupBox_user)
#        self.lesource15.setGeometry(QtCore.QRect(180,130 , 230, 32))
#        self.lesource15.setObjectName(_fromUtf8("lesource15"))


        self.text14 = QtGui.QLabel(self.groupBox_user)
        self.text14.setGeometry(QtCore.QRect(140, 60, 300, 20))
        self.text14.setText(_fromUtf8(""))
        self.text14.setObjectName(_fromUtf8("text14"))

        self.text15 = QtGui.QLabel(self.groupBox_user)
        self.text15.setGeometry(QtCore.QRect(150, 105, 50, 20))
        self.text15.setText(_fromUtf8(""))
        self.text15.setObjectName(_fromUtf8("text15"))


        #self.checkBox_13 = QtGui.QCheckBox(self.groupBox_user)
        #self.checkBox_13.setGeometry(QtCore.QRect(180, 130, 81, 24))
        #font = QtGui.QFont()
        #font.setFamily(_fromUtf8("Serif"))
        #font.setPointSize(10)
        #self.checkBox_13.setFont(font)
        #self.checkBox_13.setObjectName(_fromUtf8("checkBox_13"))

        #self.checkBox_14 = QtGui.QCheckBox(self.groupBox_user)
        #self.checkBox_14.setGeometry(QtCore.QRect(280, 130, 81, 24))
        #font = QtGui.QFont()
        #font.setFamily(_fromUtf8("Serif"))
        #font.setPointSize(10)
        #self.checkBox_14.setFont(font)
        #self.checkBox_14.setObjectName(_fromUtf8("checkBox_14"))

        self.text13 = QtGui.QLabel(self.groupBox_user)
        self.text13.setGeometry(QtCore.QRect(160, 270, 200, 20))
        self.text13.setText(_fromUtf8(""))
        self.text13.setObjectName(_fromUtf8("text13"))

        self.text21 = QtGui.QLabel(self.groupBox_user)
        self.text21.setGeometry(QtCore.QRect(160, 300, 300, 20))
        self.text21.setText(_fromUtf8(""))
        self.text21.setObjectName(_fromUtf8("text21"))

        self.text3 = QtGui.QLabel(self.groupBox_user)
        self.text3.setGeometry(QtCore.QRect(160, 330, 200, 20))
        self.text3.setText(_fromUtf8(""))
        self.text3.setObjectName(_fromUtf8("text3"))

        self.text4 = QtGui.QLabel(self.groupBox_user)
        self.text4.setGeometry(QtCore.QRect(160, 360, 300, 20))
        self.text4.setText(_fromUtf8(""))
        self.text4.setObjectName(_fromUtf8("text4"))

        self.text1 = QtGui.QLabel(self.sourceWidget)
        self.text1.setGeometry(QtCore.QRect(0, 100, 80, 17))
        self.text1.setText(_fromUtf8(""))
        self.text1.setObjectName(_fromUtf8("text1"))
        self.splitline = QtGui.QLabel(self.sourceWidget)
        self.splitline.setGeometry(QtCore.QRect(0, 20, 408, 1))
        self.splitline.setStyleSheet(_fromUtf8(""))
        self.splitline.setText(_fromUtf8(""))
        self.splitline.setObjectName(_fromUtf8("splitline"))
        self.groupBox = QtGui.QGroupBox(self.sourceWidget)
        self.groupBox.setGeometry(QtCore.QRect(0, 10, 411, 121))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(148, 144, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(148, 144, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(190, 190, 190))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.groupBox.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.groupBox.setFont(font)
        self.groupBox.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.checkBox = QtGui.QCheckBox(self.groupBox)
        self.checkBox.setGeometry(QtCore.QRect(10, 60, 81, 24))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(100, 100, 100))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(100, 100, 100))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(190, 190, 190))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(100, 100, 100))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        self.checkBox.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Serif"))
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.checkBox.setFont(font)
        self.checkBox.setChecked(False)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.checkBox_2 = QtGui.QCheckBox(self.groupBox)
        self.checkBox_2.setGeometry(QtCore.QRect(10, 80, 81, 24))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Serif"))
        font.setPointSize(10)
        self.checkBox_2.setFont(font)
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        self.checkBox_3 = QtGui.QCheckBox(self.groupBox)
        self.checkBox_3.setGeometry(QtCore.QRect(90, 60, 81, 24))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Serif"))
        font.setPointSize(10)
        self.checkBox_3.setFont(font)
        self.checkBox_3.setObjectName(_fromUtf8("checkBox_3"))
        self.checkBox_4 = QtGui.QCheckBox(self.groupBox)
        self.checkBox_4.setGeometry(QtCore.QRect(150, 60, 91, 24))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Serif"))
        font.setPointSize(10)
        self.checkBox_4.setFont(font)
        self.checkBox_4.setObjectName(_fromUtf8("checkBox_4"))
        self.checkBox_5 = QtGui.QCheckBox(self.groupBox)
        self.checkBox_5.setGeometry(QtCore.QRect(240, 60, 81, 24))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Serif"))
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.checkBox_5.setFont(font)
        self.checkBox_5.setObjectName(_fromUtf8("checkBox_5"))
        self.checkBox_6 = QtGui.QCheckBox(self.groupBox)
        self.checkBox_6.setGeometry(QtCore.QRect(320, 60, 91, 24))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Serif"))
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.checkBox_6.setFont(font)
        self.checkBox_6.setObjectName(_fromUtf8("checkBox_6"))
        self.lesource = QtGui.QLineEdit(self.groupBox)
        self.lesource.setGeometry(QtCore.QRect(10, 30, 391, 20))
        self.lesource.setObjectName(_fromUtf8("lesource"))
        self.btnAdd = QtGui.QPushButton(self.groupBox)
        self.btnAdd.setGeometry(QtCore.QRect(310, 90, 90, 20))
        self.btnAdd.setText(_fromUtf8(""))
        self.btnAdd.setObjectName(_fromUtf8("btnAdd"))
        self.groupBox_2 = QtGui.QGroupBox(self.sourceWidget)
        self.groupBox_2.setGeometry(QtCore.QRect(0, 130, 411, 231))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(148, 144, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(148, 144, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(190, 190, 190))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.groupBox_2.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.btnUpdate = QtGui.QPushButton(self.groupBox_2)
        self.btnUpdate.setGeometry(QtCore.QRect(310, 200, 90, 20))
        self.btnUpdate.setText(_fromUtf8(""))
        self.btnUpdate.setObjectName(_fromUtf8("btnUpdate"))
        self.processwidget = QtGui.QWidget(self.groupBox_2)
        self.processwidget.setGeometry(QtCore.QRect(0, 190, 271, 31))
        self.processwidget.setObjectName(_fromUtf8("processwidget"))
        self.btnCancel = QtGui.QPushButton(self.processwidget)
        self.btnCancel.setGeometry(QtCore.QRect(250, 10, 13, 13))
        self.btnCancel.setText(_fromUtf8(""))
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))
        self.progressBar = QtGui.QProgressBar(self.processwidget)
        self.progressBar.setGeometry(QtCore.QRect(10, 10, 194, 17))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.sourceListWidget = QtGui.QListWidget(self.groupBox_2)
        self.sourceListWidget.setGeometry(QtCore.QRect(10, 30, 391, 161))
        self.sourceListWidget.setObjectName(_fromUtf8("sourceListWidget"))
        self.bg = QtGui.QLabel(ConfigWidget)
        self.bg.setGeometry(QtCore.QRect(0, 0, 568, 480))
        self.bg.setText(_fromUtf8(""))
        self.bg.setObjectName(_fromUtf8("bg"))
        self.btnClose = QtGui.QPushButton(ConfigWidget)
        self.btnClose.setGeometry(QtCore.QRect(130, 17, 28, 35))
        self.btnClose.setText(_fromUtf8(""))
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.label = QtGui.QLabel(ConfigWidget)
        self.label.setGeometry(QtCore.QRect(16, 32, 96, 1))
        self.label.setText(_fromUtf8(""))
        self.label.setObjectName(_fromUtf8("label"))
        self.cbhideubuntu = QtGui.QPushButton(ConfigWidget)
        self.cbhideubuntu.setGeometry(QtCore.QRect(190, 440, 100, 20))
        self.cbhideubuntu.setText(_fromUtf8(""))
        self.cbhideubuntu.setObjectName(_fromUtf8("cbhideubuntu"))
        self.btnReset = QtGui.QPushButton(ConfigWidget)
        self.btnReset.setGeometry(QtCore.QRect(330, 430, 90, 20))
        self.btnReset.setText(_fromUtf8(""))
        self.btnReset.setObjectName(_fromUtf8("btnReset"))
        self.bg.raise_()
        self.pageListWidget.raise_()
        self.sourceWidget.raise_()
        self.btnClose.raise_()
        self.label.raise_()
        self.cbhideubuntu.raise_()
        self.btnReset.raise_()

        self.retranslateUi(ConfigWidget)
        QtCore.QMetaObject.connectSlotsByName(ConfigWidget)

    def retranslateUi(self, ConfigWidget):
        ConfigWidget.setWindowTitle(_translate("ConfigWidget", "Form", None))
        self.groupBox.setTitle(_translate("ConfigWidget", "软件源配置", None))
        self.checkBox.setText(_translate("ConfigWidget", "deb", None))
        self.checkBox_2.setText(_translate("ConfigWidget", "deb-src", None))
        self.checkBox_3.setText(_translate("ConfigWidget", "main", None))
        self.checkBox_4.setText(_translate("ConfigWidget", "restricted", None))
        self.checkBox_5.setText(_translate("ConfigWidget", "universe", None))
        self.checkBox_6.setText(_translate("ConfigWidget", "multiverse", None))
        self.groupBox_2.setTitle(_translate("ConfigWidget", "软件源列表", None))
        #self.checkBox_14.setText(_translate("ConfigWidget", "普通用户", None))
        #self.checkBox_13.setText(_translate("ConfigWidget", "开发者", None))

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ConfigWidget = QtGui.QWidget()
    ui = Ui_ConfigWidget()
    ui.setupUi(ConfigWidget)
    ConfigWidget.show()
    sys.exit(app.exec_())

