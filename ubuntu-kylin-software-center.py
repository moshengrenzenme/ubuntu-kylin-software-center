#!/usr/bin/python
# -*- coding: utf-8 -*-

### BEGIN LICENSE

# Copyright (C) 2013 National University of Defense Technology(NUDT) & Kylin Ltd

# Author:
#     Shine Huang<shenghuang@ubuntukylin.com>
#     maclin <majun@ubuntukylin.com>
# Maintainer:
#     Shine Huang<shenghuang@ubuntukylin.com>
#     maclin <majun@ubuntukylin.com>

# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import dbus
import dbus.service
import webbrowser
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from ui.mainwindow import Ui_MainWindow
from ui.rcmdcard import RcmdCard
from ui.normalcard import NormalCard
from ui.wincard import WinCard, WinGather
from ui.listitemwidget import ListItemWidget
from ui.tasklistitemwidget import TaskListItemWidget
from ui.ranklistitemwidget import RankListItemWidget
from ui.pointlistitemwidget import PointListItemWidget
from ui.adwidget import *
from ui.detailscrollwidget import DetailScrollWidget
from ui.loadingdiv import *
from ui.messagebox import MessageBox
from ui.confirmdialog import ConfirmDialog
from ui.configwidget import ConfigWidget
from ui.pointoutwidget import PointOutWidget
from ui.singleprocessbar import SingleProcessBar
from ui.xpitemwidget import XpItemWidget, DataModel
from ui.cardwidget import CardWidget

from utils import vfs
from utils import log
from backend.search import *

from backend.service.appmanager import AppManager
from backend.installbackend import InstallBackend
from backend.utildbus import UtilDbus

from models.enums import (UBUNTUKYLIN_RES_PATH, AppActions,AptActionMsg)
from models.globals import Globals

from models.enums import Signals

from models.enums import UBUNTUKYLIN_RES_TMPICON_PATH, UBUNTUKYLIN_RES_ICON_PATH, UBUNTUKYLIN_RES_WIN_PATH

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from dbus.mainloop.glib import DBusGMainLoop
mainloop = DBusGMainLoop(set_as_default=True)

LOG = logging.getLogger("uksc")


class SoftwareCenter(QMainWindow):

    # recommend number in function "fill"
    recommendNumber = 0
    # now page
    nowPage = ''
    # his page
    hisPage = ''
    # search delay timer
    searchDTimer = ''
    # fx(name, taskitem) map
    stmap = {}
    # drag window x,y
    dragPosition = -1
    xp_exists = 0

    def __init__(self, parent=None):
        QMainWindow.__init__(self,parent)

        # singleton check
        self.check_singleton()

        # init dbus backend
        self.init_dbus()

        # init ui
        self.init_main_view()

        # init main service
        self.init_main_service()

        # check ukid
        self.check_user()

        # check apt source and update it
        self.check_source()

    def init_main_view(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # do not cover the launch loading div
        self.resize(0,0)

        self.setWindowTitle("Ubuntu Kylin 软件中心")
        self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WA_TranslucentBackground, True)

        # init components

        # point out widget
        self.pointout = PointOutWidget(self)
        # recommend card widget
        self.recommendWidget = CardWidget(Globals.NORMALCARD_WIDTH, Globals.NORMALCARD_HEIGHT, 2, self.ui.homepageWidget)
        self.recommendWidget.setGeometry(0, 298, 640, 268)
        self.recommendWidget.calculate_data()
        # un card widget
        self.unListWidget = CardWidget(Globals.NORMALCARD_WIDTH, Globals.NORMALCARD_HEIGHT, 4, self.ui.unWidget)
        self.unListWidget.setGeometry(0, 50, 860 + 6 + (20 - 6) / 2, 466)   # 6 + (20 - 6) / 2 is verticalscrollbar space
        self.unListWidget.calculate_data()
        # detail page
        self.detailScrollWidget = DetailScrollWidget(self)
        self.detailScrollWidget.raise_()
        # loading div
        self.launchLoadingDiv = LoadingDiv(None)
        self.loadingDiv = LoadingDiv(self)
        self.topratedload = MiniLoadingDiv(self.ui.rankView, self.ui.rankWidget)

        # alert message box
        self.messageBox = MessageBox(self)
        # first update process bar
        self.updateSinglePB = SingleProcessBar(self)
        # config widget
        self.configWidget = ConfigWidget(self)
        self.connect(self.configWidget, Signals.click_update_source, self.slot_click_update_source)
        self.connect(self.configWidget, Signals.task_cancel, self.slot_click_cancel)
        # history manager
        # self.history = History(self.ui)
        # search trigger
        self.searchDTimer = QTimer(self)
        self.searchDTimer.timeout.connect(self.slot_searchDTimer_timeout)

        # style by code
        self.ui.centralwidget.setAutoFillBackground(True)
        palette = QPalette()
        # palette.setColor(QPalette.Background, QColor(234, 240, 243))
        palette.setColor(QPalette.Background, QColor(238, 237, 240))
        self.ui.centralwidget.setPalette(palette)

        self.ui.rankWidget.setAutoFillBackground(True)
        palette = QPalette()
        # palette.setColor(QPalette.Background, QColor(234, 240, 243))
        palette.setColor(QPalette.Background, QColor(238, 237, 240))
        self.ui.rankWidget.setPalette(palette)

        # self.ui.categoryView.setFocusPolicy(Qt.NoFocus)
        self.ui.btnLogin.setFocusPolicy(Qt.NoFocus)
        self.ui.btnReg.setFocusPolicy(Qt.NoFocus)
        self.ui.btnLogout.setFocusPolicy(Qt.NoFocus)
        self.ui.btnClose.setFocusPolicy(Qt.NoFocus)
        self.ui.btnMin.setFocusPolicy(Qt.NoFocus)
        self.ui.btnMaxNormal.setFocusPolicy(Qt.NoFocus)
        self.ui.btnConf.setFocusPolicy(Qt.NoFocus)
        self.ui.btnHomepage.setFocusPolicy(Qt.NoFocus)
        self.ui.btnAll.setFocusPolicy(Qt.NoFocus)
        self.ui.btnUp.setFocusPolicy(Qt.NoFocus)
        self.ui.btnUn.setFocusPolicy(Qt.NoFocus)
        self.ui.btnXp.setFocusPolicy(Qt.NoFocus)
        self.ui.btnTask.setFocusPolicy(Qt.NoFocus)
        self.ui.allsListWidget.setFocusPolicy(Qt.NoFocus)
        self.ui.upListWidget.setFocusPolicy(Qt.NoFocus)
        self.ui.unListWidget.setFocusPolicy(Qt.NoFocus)
        self.ui.searchListWidget.setFocusPolicy(Qt.NoFocus)
        self.ui.taskListWidget.setFocusPolicy(Qt.NoFocus)
        self.ui.rankView.setFocusPolicy(Qt.NoFocus)

        # self.ui.lebg.stackUnder(self.ui.leSearch)
        self.ui.leSearch.stackUnder(self.ui.lebg)
        self.ui.rankView.setCursor(Qt.PointingHandCursor)
        self.ui.rankView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.rankView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.softCountText1 = QLabel(self.ui.homeMsgWidget)
        self.softCountText1.setGeometry(QRect(744, 14, 50, 15))
        self.softCountText1.setObjectName("softCountText1")
        self.softCountText1.setText("共有")
        self.softCount = QLabel(self.ui.homeMsgWidget)
        self.softCount.setGeometry(QRect(770, 14, 50, 15))
        self.softCount.setText("")
        self.softCount.setObjectName("softCount")
        self.softCountText2 = QLabel(self.ui.homeMsgWidget)
        self.softCountText2.setGeometry(QRect(818, 14, 44, 15))
        self.softCountText2.setObjectName("softCountText2")
        self.softCountText2.setText("款软件")

        self.softCount.setAlignment(Qt.AlignCenter)

        self.ui.btnLogin.setText("请登录")
        self.ui.btnReg.setText("免费注册")
        self.ui.welcometext.setText("欢迎您")
        self.ui.btnLogout.setText("退出")

        self.ui.hometext1.setText("推荐软件")
        self.ui.hometext2.setText("评分排行")

        self.ui.texticon.setText("图标")
        self.ui.textappname.setText("软件名")
        self.ui.textsize.setText("大小")
        self.ui.textprocess.setText("任务进度")
        self.ui.textstatus.setText("状态信息")

        self.ui.texticon_un.setText("图标")
        self.ui.textappname_un.setText("软件名")
        self.ui.textsize_un.setText("大小")
        self.ui.textversion_un.setText("版本")
        self.ui.textrating_un.setText("评分")
        self.ui.textaction_un.setText("操作")

        self.ui.texticon_up.setText("图标")
        self.ui.textappname_up.setText("软件名")
        self.ui.textsize_up.setText("大小")
        self.ui.textversion_up.setText("版本")
        self.ui.textrating_up.setText("评分")
        self.ui.textaction_up.setText("操作")

        self.ui.texticon_all.setText("图标")
        self.ui.textappname_all.setText("软件名")
        self.ui.textsize_all.setText("大小")
        self.ui.textversion_all.setText("版本")
        self.ui.textrating_all.setText("评分")
        self.ui.textaction_all.setText("操作")

        # self.ui.userName.setText("未登陆")
        # self.ui.userLv.setText("Lv 0")
        self.ui.leSearch.setPlaceholderText("请输入您要搜索的软件")


        #kobe 0904
        self.ui.wintitle.setText("Windowns常用软件替换")
        self.ui.winlabel1.setText("共有")
        # self.ui.wincountlabel.setText("37")
        self.ui.wincountlabel.setAlignment(Qt.AlignCenter)
        self.ui.winlabel2.setText("款软件")
        self.ui.winline.setStyleSheet("QLabel{background-color:#CCCCCC;}")
        self.ui.wintitle.setStyleSheet("QLabel{color:#777777;font-size:14px;}")
        self.ui.winlabel1.setStyleSheet("QLabel{color:#666666;font-size:14px;}")
        self.ui.winlabel2.setStyleSheet("QLabel{color:#666666;font-size:14px;}")
        self.ui.wincountlabel.setStyleSheet("QLabel{color:#FA7053;font-size:15px;}")


        # style by qss
        self.ui.userLogo.setStyleSheet("QLabel{background-image:url('res/userlogo.png')}")
        self.ui.userLogoafter.setStyleSheet("QLabel{background-image:url('res/userlogo.png')}")
        self.ui.btnLogin.setStyleSheet("QPushButton{border:0px;text-align:left;font-size:14px;color:#0F84BC;}QPushButton:hover{color:#0396DC;}")
        self.ui.btnReg.setStyleSheet("QPushButton{border:0px;text-align:left;font-size:14px;color:#666666;}QPushButton:hover{color:#0396DC;}")
        self.ui.welcometext.setStyleSheet("QLabel{text-align:left;font-size:14px;color:#666666;}")
        self.ui.username.setStyleSheet("QLabel{text-align:left;font-size:14px;color:#0396DC;}")
        self.ui.btnLogout.setStyleSheet("QPushButton{border:0px;text-align:left;font-size:14px;color:#666666;}QPushButton:hover{color:#0396DC;}")
        self.softCountText1.setStyleSheet("QLabel{color:#666666;font-size:14px;}")
        self.softCountText2.setStyleSheet("QLabel{color:#666666;font-size:14px;}")
        self.softCount.setStyleSheet("QLabel{color:#FA7053;font-size:15px;}")
        self.ui.hometext1.setStyleSheet("QLabel{color:#777777;font-size:14px;}")
        self.ui.hometext2.setStyleSheet("QLabel{color:#777777;font-size:14px;}")
        self.ui.homeline1.setStyleSheet("QLabel{background-color:#CCCCCC;}")
        self.ui.homeline2.setStyleSheet("QLabel{background-color:#CCCCCC;}")
        self.ui.navWidget.setStyleSheet("QWidget{background-image:url('res/nav-bg.png');}")
        # self.ui.shadowleft.setStyleSheet("QLabel{background-image:url('res/sleft.png')}")
        # self.ui.shadowright.setStyleSheet("QLabel{background-image:url('res/sright.png')}")
        # self.ui.shadowup.setStyleSheet("QLabel{background-image:url('res/sup.png')}")
        # self.ui.shadowbottom.setStyleSheet("QLabel{background-image:url('res/sbottom.png')}")
        # self.ui.btnBack.setStyleSheet(HEADER_BUTTON_STYLE % (UBUNTUKYLIN_RES_PATH + "nav-back-1.png", UBUNTUKYLIN_RES_PATH + "nav-back-2.png", UBUNTUKYLIN_RES_PATH + "nav-back-3.png"))
        # self.ui.btnNext.setStyleSheet("QPushButton{background-image:url('res/nav-next-1.png');border:0px;}QPushButton:hover{background:url('res/nav-next-2.png');}QPushButton:pressed{background:url('res/nav-next-3.png');}")
        self.ui.btnHomepage.setStyleSheet("QPushButton{background-image:url('res/nav-homepage-1.png');border:0px;}QPushButton:hover{background:url('res/nav-homepage-2.png');}QPushButton:pressed{background:url('res/nav-homepage-3.png');}")
        self.ui.btnAll.setStyleSheet("QPushButton{background-image:url('res/nav-all-1.png');border:0px;}QPushButton:hover{background:url('res/nav-all-2.png');}QPushButton:pressed{background:url('res/nav-all-3.png');}")
        self.ui.btnUp.setStyleSheet("QPushButton{background-image:url('res/nav-up-1.png');border:0px;}QPushButton:hover{background:url('res/nav-up-2.png');}QPushButton:pressed{background:url('res/nav-up-3.png');}")
        self.ui.btnUn.setStyleSheet("QPushButton{background-image:url('res/nav-un-1.png');border:0px;}QPushButton:hover{background:url('res/nav-un-2.png');}QPushButton:pressed{background:url('res/nav-un-3.png');}")
        self.ui.btnXp.setStyleSheet("QPushButton{background-image:url('res/nav-windows-1.png');border:0px;}QPushButton:hover{background:url('res/nav-windows-2.png');}QPushButton:pressed{background:url('res/nav-windows-3.png');}")
        self.ui.btnTask.setStyleSheet("QPushButton{background-image:url('res/nav-task-1.png');border:0px;}QPushButton:hover{background:url('res/nav-task-2.png');}QPushButton:pressed{background:url('res/nav-task-3.png');}")
        self.ui.logoImg.setStyleSheet("QLabel{background-image:url('res/logo.png')}")
        self.ui.lebg.setStyleSheet("QLabel{background-image:url('res/search-1.png')}")
        self.ui.leSearch.setStyleSheet("QLineEdit{background-color:#EEEDF0;border:1px solid #CCCCCC;color:#999999;font-size:13px;}")
        # self.ui.leSearch.setStyleSheet("QLineEdit{background-color:#EAF0F3;border:1px solid #CCCCCC;color:#999999;font-size:13px;}QLineEdit:hover{border:1px solid #0396DC;}QLineEdit:focus{border:1px solid #0396DC;color:#666666;}")

        # self.ui.userLabel.setStyleSheet("QLabel{background-image:url('res/user.png')}")
        # self.ui.userName.setStyleSheet("QLabel{color:white;}")
        # self.ui.userLv.setStyleSheet("QLabel{color:white;}")
        self.ui.btnClose.setStyleSheet("QPushButton{background-image:url('res/close-1.png');border:0px;}QPushButton:hover{background:url('res/close-2.png');}QPushButton:pressed{background:url('res/close-3.png');}")
        self.ui.btnMin.setStyleSheet("QPushButton{background-image:url('res/min-1.png');border:0px;}QPushButton:hover{background:url('res/min-2.png');}QPushButton:pressed{background:url('res/min-3.png');}")
        self.ui.btnMaxNormal.setStyleSheet("QPushButton{background-image:url('res/max-1.png');border:0px;}QPushButton:hover{background:url('res/max-2.png');}QPushButton:pressed{background:url('res/max-3.png');}")
        self.ui.btnConf.setStyleSheet("QPushButton{background-image:url('res/conf-1.png');border:0px;}QPushButton:hover{background:url('res/conf-2.png');}QPushButton:pressed{background:url('res/conf-3.png');}")
        # self.ui.categoryView.setStyleSheet("QListWidget{border:0px;background-color:#30323F;font-size:13px;}QListWidget::item{height:36px;padding-left:24px;margin-top:0px;border:0px;color:#A8A9AE;}QListWidget::item:hover{background-color:#282937;}QListWidget::item:selected{background-color:#232230;color:white;}")
        # self.ui.vline1.setStyleSheet("QLabel{background-color:#BBD1E4;}")
        # self.ui.rankLogo.setStyleSheet("QLabel{background-image:url('res/rankLogo.png')}")
        # self.ui.rankText.setStyleSheet("QLabel{color:#7E8B97;font-size:13px;font-weight:bold;}")
        self.ui.rankView.setStyleSheet("QListWidget{border:0px;background-color:#EEEDF0;}QListWidget::item{height:24px;border:0px;font-size:13px;color:#666666;}QListWidget::item:hover{height:52;}")
        # self.ui.btnDay.setStyleSheet("QPushButton{background-image:url('res/day1.png');border:0px;}")
        # self.ui.btnWeek.setStyleSheet("QPushButton{background-image:url('res/week1.png');border:0px;}")
        # self.ui.btnMonth.setStyleSheet("QPushButton{background-image:url('res/month1.png');border:0px;}")
        # self.ui.btnDownTimes.setStyleSheet("QPushButton{font-size:14px;color:#2B8AC2;background-color:white;border:0px;}")
        # self.ui.btnGrade.setStyleSheet("QPushButton{font-size:14px;color:#2B8AC2;background-color:#C3E0F4;border:0px;}")
        # self.ui.bottomImg.setStyleSheet("QLabel{background-image:url('res/bottomicon.png')}")
        # self.ui.bottomText1.setStyleSheet("QLabel{color:white;font-size:14px;}")
        # self.ui.bottomText2.setStyleSheet("QLabel{color:white;font-size:14px;}")
        self.ui.allsMSGBar.setStyleSheet("QLabel{background-color:white;font-size:14px;padding-top:32px;padding-left:7px;}")
        self.ui.upMSGBar.setStyleSheet("QLabel{background-color:white;font-size:14px;padding-top:32px;padding-left:7px;}")
        self.ui.unMSGBar.setStyleSheet("QLabel{background-color:white;font-size:14px;padding-top:32px;padding-left:7px;}")
        self.ui.searchMSGBar.setStyleSheet("QLabel{background-color:white;font-size:14px;padding-top:32px;padding-left:7px;}")
        self.ui.taskMSGBar.setStyleSheet("QLabel{background-color:white;font-size:14px;padding-top:2px;padding-left:2px;}")
        # self.ui.xpMSGBar.setStyleSheet("QLabel{background-color:white;font-size:14px;padding-top:2px;padding-left:2px;}")
        self.ui.texticon.setStyleSheet("QLabel{font-size:14px;}")
        self.ui.textappname.setStyleSheet("QLabel{font-size:14px;}")
        self.ui.textsize.setStyleSheet("QLabel{font-size:14px;}")
        self.ui.textprocess.setStyleSheet("QLabel{font-size:14px;}")
        self.ui.textstatus.setStyleSheet("QLabel{font-size:14px;}")
        self.ui.texticon_un.setStyleSheet("QLabel{font-size:14px;}")
        self.ui.textappname_un.setStyleSheet("QLabel{font-size:14px;}")
        self.ui.textsize_un.setStyleSheet("QLabel{font-size:14px;}")
        self.ui.textversion_un.setStyleSheet("QLabel{font-size:14px;}")
        self.ui.textrating_un.setStyleSheet("QLabel{font-size:14px;}")
        self.ui.textaction_un.setStyleSheet("QLabel{font-size:14px;}")
        self.ui.texticon_up.setStyleSheet("QLabel{font-size:14px;}")
        self.ui.textappname_up.setStyleSheet("QLabel{font-size:14px;}")
        self.ui.textsize_up.setStyleSheet("QLabel{font-size:14px;}")
        self.ui.textversion_up.setStyleSheet("QLabel{font-size:14px;}")
        self.ui.textrating_up.setStyleSheet("QLabel{font-size:14px;}")
        self.ui.textaction_up.setStyleSheet("QLabel{font-size:14px;}")
        self.ui.texticon_all.setStyleSheet("QLabel{font-size:14px;}")
        self.ui.textappname_all.setStyleSheet("QLabel{font-size:14px;}")
        self.ui.textsize_all.setStyleSheet("QLabel{font-size:14px;}")
        self.ui.textversion_all.setStyleSheet("QLabel{font-size:14px;}")
        self.ui.textrating_all.setStyleSheet("QLabel{font-size:14px;}")
        self.ui.textaction_all.setStyleSheet("QLabel{font-size:14px;}")
        self.ui.allsHeader.setStyleSheet("QLabel{background-image:url('res/listwidgetheader.png')}")
        self.ui.upHeader.setStyleSheet("QLabel{background-image:url('res/listwidgetheader.png')}")
        self.ui.unHeader.setStyleSheet("QLabel{background-image:url('res/listwidgetheader.png')}")
        self.ui.searchHeader.setStyleSheet("QLabel{background-image:url('res/listwidgetheader.png')}")
        self.ui.taskHeader.setStyleSheet("QLabel{background-image:url('res/taskwidgetheader.png')}")
        self.ui.allsListWidget.setStyleSheet("QListWidget{border:0px;}QListWidget::item{height:66px;margin-top:-1px;border:1px solid #d5e3ec;}QListWidget::item:hover{background-color:#E4F1F8;}")
        self.ui.upListWidget.setStyleSheet("QListWidget{border:0px;}QListWidget::item{height:66px;margin-top:-1px;border:1px solid #d5e3ec;}QListWidget::item:hover{background-color:#E4F1F8;}")
        self.ui.unListWidget.setStyleSheet("QListWidget{border:0px;}QListWidget::item{height:66px;margin-top:-1px;border:1px solid #d5e3ec;}QListWidget::item:hover{background-color:#E4F1F8;}")
        self.ui.searchListWidget.setStyleSheet("QListWidget{border:0px;}QListWidget::item{height:66px;margin-top:-1px;border:1px solid #d5e3ec;}QListWidget::item:hover{background-color:#E4F1F8;}")
        self.ui.taskListWidget.setStyleSheet("QListWidget{border:0px;}QListWidget::item{height:45;margin-top:-1px;border:1px solid #d5e3ec;}QListWidget::item:hover{background-color:#E4F1F8;}")
        self.ui.allsListWidget.verticalScrollBar().setStyleSheet("QScrollBar:vertical{width:12px;background-color:black;margin:0px,0px,0px,0px;padding-top:0px;padding-bottom:0px;}"
                                                                 "QScrollBar:sub-page:vertical{background:qlineargradient(x1: 0.5, y1: 1, x2: 0.5, y2: 0, stop: 0 #D4DCE1, stop: 1 white);}QScrollBar:add-page:vertical{background:qlineargradient(x1: 0.5, y1: 0, x2: 0.5, y2: 1, stop: 0 #D4DCE1, stop: 1 white);}"
                                                                 "QScrollBar:handle:vertical{background:qlineargradient(x1: 0, y1: 0.5, x2: 1, y2: 0.5, stop: 0 #CACACA, stop: 1 #818486);}QScrollBar:add-line:vertical{background-color:green;}")
        self.ui.upListWidget.verticalScrollBar().setStyleSheet("QScrollBar:vertical{width:12px;background-color:black;margin:0px,0px,0px,0px;padding-top:0px;padding-bottom:0px;}"
                                                                 "QScrollBar:sub-page:vertical{background:qlineargradient(x1: 0.5, y1: 1, x2: 0.5, y2: 0, stop: 0 #D4DCE1, stop: 1 white);}QScrollBar:add-page:vertical{background:qlineargradient(x1: 0.5, y1: 0, x2: 0.5, y2: 1, stop: 0 #D4DCE1, stop: 1 white);}"
                                                                 "QScrollBar:handle:vertical{background:qlineargradient(x1: 0, y1: 0.5, x2: 1, y2: 0.5, stop: 0 #CACACA, stop: 1 #818486);}QScrollBar:add-line:vertical{background-color:green;}")
        self.ui.unListWidget.verticalScrollBar().setStyleSheet("QScrollBar:vertical{width:12px;background-color:black;margin:0px,0px,0px,0px;padding-top:0px;padding-bottom:0px;}"
                                                                 "QScrollBar:sub-page:vertical{background:qlineargradient(x1: 0.5, y1: 1, x2: 0.5, y2: 0, stop: 0 #D4DCE1, stop: 1 white);}QScrollBar:add-page:vertical{background:qlineargradient(x1: 0.5, y1: 0, x2: 0.5, y2: 1, stop: 0 #D4DCE1, stop: 1 white);}"
                                                                 "QScrollBar:handle:vertical{background:qlineargradient(x1: 0, y1: 0.5, x2: 1, y2: 0.5, stop: 0 #CACACA, stop: 1 #818486);}QScrollBar:add-line:vertical{background-color:green;}")
        self.ui.searchListWidget.verticalScrollBar().setStyleSheet("QScrollBar:vertical{width:12px;background-color:black;margin:0px,0px,0px,0px;padding-top:0px;padding-bottom:0px;}"
                                                                 "QScrollBar:sub-page:vertical{background:qlineargradient(x1: 0.5, y1: 1, x2: 0.5, y2: 0, stop: 0 #D4DCE1, stop: 1 white);}QScrollBar:add-page:vertical{background:qlineargradient(x1: 0.5, y1: 0, x2: 0.5, y2: 1, stop: 0 #D4DCE1, stop: 1 white);}"
                                                                 "QScrollBar:handle:vertical{background:qlineargradient(x1: 0, y1: 0.5, x2: 1, y2: 0.5, stop: 0 #CACACA, stop: 1 #818486);}QScrollBar:add-line:vertical{background-color:green;}")
        self.ui.taskListWidget.verticalScrollBar().setStyleSheet("QScrollBar:vertical{width:12px;background-color:black;margin:0px,0px,0px,0px;padding-top:0px;padding-bottom:0px;}"
                                                                 "QScrollBar:sub-page:vertical{background:qlineargradient(x1: 0.5, y1: 1, x2: 0.5, y2: 0, stop: 0 #D4DCE1, stop: 1 white);}QScrollBar:add-page:vertical{background:qlineargradient(x1: 0.5, y1: 0, x2: 0.5, y2: 1, stop: 0 #D4DCE1, stop: 1 white);}"
                                                                 "QScrollBar:handle:vertical{background:qlineargradient(x1: 0, y1: 0.5, x2: 1, y2: 0.5, stop: 0 #CACACA, stop: 1 #818486);}QScrollBar:add-line:vertical{background-color:green;}")

        # signal / slot
        # self.ui.btnBack.clicked.connect(self.history.history_back)
        # self.ui.btnNext.clicked.connect(self.history.history_next)
        # self.ui.categoryView.itemClicked.connect(self.slot_change_category)
        self.ui.rankView.itemClicked.connect(self.slot_click_rank_item)
        self.ui.allsListWidget.itemClicked.connect(self.slot_click_item)
        self.ui.upListWidget.itemClicked.connect(self.slot_click_item)
        self.ui.unListWidget.itemClicked.connect(self.slot_click_item)
        self.ui.searchListWidget.itemClicked.connect(self.slot_click_item)
        self.ui.allsListWidget.verticalScrollBar().valueChanged.connect(self.slot_softwidget_scroll_end)
        self.ui.upListWidget.verticalScrollBar().valueChanged.connect(self.slot_softwidget_scroll_end)
        self.ui.searchListWidget.verticalScrollBar().valueChanged.connect(self.slot_softwidget_scroll_end)
        self.ui.unListWidget.verticalScrollBar().valueChanged.connect(self.slot_softwidget_scroll_end)
        self.unListWidget.scrollArea.verticalScrollBar().valueChanged.connect(self.slot_softwidget_scroll_end)
        self.ui.btnHomepage.pressed.connect(self.slot_goto_homepage)
        self.ui.btnAll.pressed.connect(self.slot_goto_allpage)
        self.ui.btnUp.pressed.connect(self.slot_goto_uppage)
        self.ui.btnUn.pressed.connect(self.slot_goto_unpage)
        self.ui.btnTask.pressed.connect(self.slot_goto_taskpage)
        self.ui.btnXp.pressed.connect(self.slot_goto_xppage)
        # self.ui.btnClose.clicked.connect(self.hide)
        self.ui.btnClose.clicked.connect(self.slot_close)
        self.ui.btnMaxNormal.clicked.connect(self.slot_max_normal)
        self.ui.btnMin.clicked.connect(self.slot_min)
        self.ui.btnConf.clicked.connect(self.slot_show_config)
        self.ui.leSearch.textChanged.connect(self.slot_search_text_change)

        self.connect(self, Signals.click_item, self.slot_show_app_detail)
        self.connect(self, Signals.install_app, self.slot_click_install)
        self.connect(self.detailScrollWidget, Signals.install_debfile, self.slot_click_install_debfile)
        self.connect(self.detailScrollWidget, Signals.install_app, self.slot_click_install)
        self.connect(self.detailScrollWidget, Signals.upgrade_app, self.slot_click_upgrade)
        self.connect(self.detailScrollWidget, Signals.remove_app, self.slot_click_remove)
        self.connect(self, Signals.update_source,self.slot_update_source)

        # widget status
        # self.ui.categoryView.setEnabled(False)
        self.ui.btnUp.setEnabled(False)
        self.ui.btnUn.setEnabled(False)
        self.ui.btnTask.setEnabled(False)
        self.ui.btnXp.setEnabled(False)

        self.ui.allsWidget.hide()
        self.ui.upWidget.hide()
        self.ui.unWidget.hide()
        self.ui.searchWidget.hide()
        self.ui.taskWidget.hide()
        # self.ui.xpWidget.hide()
        self.ui.winpageWidget.hide()
        # self.ui.categoryView.hide()
        self.ui.headerWidget.hide()
        self.ui.centralwidget.hide()
        # self.ui.leftWidget.hide()

        # loading
        self.launchLoadingDiv.start_loading("系统正在初始化...")

    def init_main_service(self):
        self.appmgr = AppManager()

        # add by kobe for test xp
        self.xp_exists = 0
        self.winnum = 0
        self.xp_model = DataModel(self.appmgr)

        self.connect(self.appmgr, Signals.init_models_ready,self.slot_init_models_ready)
        self.connect(self.appmgr, Signals.ads_ready, self.slot_advertisement_ready)
        self.connect(self.appmgr, Signals.recommend_ready, self.slot_recommend_apps_ready)
        self.connect(self.appmgr, Signals.ratingrank_ready, self.slot_ratingrank_apps_ready)
        self.connect(self.appmgr, Signals.rating_reviews_ready, self.slot_rating_reviews_ready)
        self.connect(self.appmgr, Signals.app_reviews_ready, self.slot_app_reviews_ready)
        self.connect(self.appmgr, Signals.app_screenshots_ready, self.slot_app_screenshots_ready)
        self.connect(self.appmgr, Signals.apt_cache_update_ready, self.slot_apt_cache_update_ready)

        self.connect(self, Signals.count_application_update,self.slot_count_application_update)
        self.connect(self, Signals.apt_process_finish,self.slot_apt_process_finish)

    def init_dbus(self):
        self.backend = InstallBackend()
        self.connect(self.backend, Signals.dbus_apt_process,self.slot_status_change)
        res = self.backend.init_dbus_ifaces()
        while res == False:
            button=QMessageBox.question(self,"初始化提示",
                                    self.tr("初始化失败 (DBus服务)\n请确认是否正确安装,忽略将不能正常进行软件安装等操作\n请选择:"),
                                    "重试", "忽略", "退出", 0)
            if button == 0:
                res = self.backend.init_dbus_ifaces()
            elif button == 1:
                LOG.warning("failed to connecting dbus service, you still choose to continue...")
                break
            else:
                LOG.warning("dbus service init failed, you choose to exit.\n\n")
                sys.exit(0)

    def check_source(self):
        if(self.appmgr.check_source_update()):
            if(Globals.LAUNCH_MODE == 'quiet'):
                button = QMessageBox.question(self,"软件源更新提示",
                                        self.tr("您是第一次进入系统 或 软件源发生异常\n要在系统中 安装/卸载/升级 软件，需要连接网络更新软件源\n如没有网络或不想更新，下次可通过运行软件中心触发此功能\n\n请选择:"),
                                        "更新", "不更新", "", 0)

                # show loading and update processbar this moment
                self.show()

                if button == 0:
                    LOG.info("update source when first start...")
                    self.updateSinglePB.show()
                    self.backend.update_source_first_os()
                elif button == 1:
                    LOG.warning("dbus service init failed, you choose to exit.\n\n")
                    sys.exit(0)
            else:
                button = QMessageBox.question(self,"软件源更新提示",
                                        self.tr("您是第一次进入系统 或 软件源发生异常\n要在系统中 安装/卸载/升级 软件，需要连接网络更新软件源\n如果不更新，也可以运行软件中心，但部分操作无法执行\n\n请选择:"),
                                        "更新", "不更新", "", 0)

                # show loading and update processbar this moment
                self.show()

                if button == 0:
                    LOG.info("update source when first start...")
                    self.updateSinglePB.show()
                    self.backend.update_source_first_os()
                elif button == 1:
                    self.appmgr.init_models()
        else:
            if(Globals.LAUNCH_MODE == 'normal'):
                self.show()
            self.appmgr.init_models()

    def check_singleton(self):
        try:
            bus = dbus.SessionBus()
        except:
            LOG.exception("could not initiate dbus")
            sys.exit(0)

        # if there is an instance running, call to bring it to frontend
        try:
            proxy_obj = bus.get_object('com.ubuntukylin.softwarecenter', '/com/ubuntukylin/softwarecenter')
            iface = dbus.Interface(proxy_obj, 'com.ubuntukylin.utiliface')
            iface.bring_to_front()

            # user clicked local deb file, show info
            if(Globals.LOCAL_DEB_FILE != None):
                iface.show_loading_div()
                iface.show_deb_file(Globals.LOCAL_DEB_FILE)
            sys.exit(0)

        # else startup one instance
        except dbus.DBusException:
            bus_name = dbus.service.BusName('com.ubuntukylin.softwarecenter', bus)
            self.dbusControler = UtilDbus(self, bus_name)

    def check_user(self):
        self.ui.beforeLoginWidget.show()
        self.ui.afterLoginWidget.hide()

    def init_last_data(self):
        # init category list
        # self.init_category_view()

        # add by kobe
        # init uk xp solution
        # self.init_xp_solution_widget()

        # init search
        self.searchDB = Search()
        self.searchList = {}

        # init others
        self.category = ""
        self.nowPage = "homepage"

        # init data flags
        self.ads_ready = False
        self.rec_ready = False
        self.rnr_ready = True

        # check uksc upgradable
        self.check_uksc_update()

        self.topratedload.start_loading()

        self.appmgr.get_advertisements()
        self.appmgr.get_recommend_apps()
        self.appmgr.get_ratingrank_apps()

    # check base init
    def check_init_ready(self):
        LOG.debug("check init data stat:%d,%d,%d",self.ads_ready,self.rec_ready,self.rnr_ready)

        # base init finished
        if self.ads_ready and self.rec_ready and self.rnr_ready:
            # self.ui.categoryView.setEnabled(True)
            self.ui.btnUp.setEnabled(True)
            self.ui.btnUn.setEnabled(True)
            self.ui.btnTask.setEnabled(True)
            self.ui.btnXp.setEnabled(True)

            # self.ui.categoryView.show()
            self.ui.headerWidget.show()
            self.ui.centralwidget.show()
            # self.ui.leftWidget.show()

            self.slot_goto_homepage()
            self.launchLoadingDiv.stop_loading()
            self.resize(Globals.MAIN_WIDTH, Globals.MAIN_HEIGHT)

            windowWidth = QApplication.desktop().width()
            windowHeight = QApplication.desktop().height()
            self.move((windowWidth - self.width()) / 2, (windowHeight - self.height()) / 2)
            # self.trayicon.show()

            # user clicked local deb file, show info
            if(Globals.LOCAL_DEB_FILE != None):
                self.slot_show_deb_detail(Globals.LOCAL_DEB_FILE)

            if(Globals.LAUNCH_MODE == 'quiet'):
                self.hide()

            # base loading finish, start backend work
            self.start_silent_work()

    # silent background works
    def start_silent_work(self):
        # init pointout
        self.init_pointout()

        # pingback_main
        self.appmgr.submit_pingback_main()

        # update cache db
        self.appmgr.get_newer_application_info()
        self.appmgr.get_all_ratings()
        self.appmgr.get_all_categories()
        self.appmgr.get_all_rank_and_recommend()

    def slot_init_models_ready(self, step, message):
        if step == "fail":
            LOG.warning("init models failed:%s",message)
            sys.exit(0)
        elif step == "ok":
            LOG.debug("init models successfully and ready to setup ui...")
            self.init_last_data()

    def init_category_view(self):
        cat_list_orgin = self.appmgr.get_category_list()

        cmp_rating = lambda x, y: \
            cmp(x[1].index,y[1].index)
        cat_list = sorted(cat_list_orgin.iteritems(),
                        cmp_rating,
                        reverse=False)

        for item in cat_list:
            catname = item[0]
            cat = item[1]
            if cat.visible is False:
                continue
            zh_name = cat.name
            oneitem = QListWidgetItem(zh_name)
            icon = QIcon()
            icon.addFile(cat.iconfile,QSize(), QIcon.Normal, QIcon.Off)
            oneitem.setIcon(icon)
            oneitem.setWhatsThis(catname)
            # self.ui.categoryView.addItem(oneitem)

    def getItem(self, row=0, column = 0):
        pass
        # print row
        # print column
        # if self.software_index[row] not in ('ppstream', 'wine-qq'):
        #     app = self.appmgr.get_application_by_name(self.software_index[row])
        #     self.emit(Signals.show_app_detail, app)

    def set_tablewidget_stylesheet(self, xp_rows):
        pass
        #------------表格创建和美化------------
        # self.ui.xpWidget.setWindowOpacity(1)
        # self.ui.xptableWidget.setRowCount(xp_rows)
        # self.ui.xptableWidget.setColumnCount(5)
        # self.ui.xptableWidget.setHorizontalHeaderLabels(['分类','Windows软件','替代软件','替代软件简介','替代软件状态'])
        # self.ui.xptableWidget.setFrameShape(QFrame.NoFrame)
        # self.ui.xptableWidget.setStyleSheet("gridline-color: rgb(255, 0, 0)")
        # self.ui.xptableWidget.verticalHeader().setVisible(False)
        # self.ui.xptableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        # self.ui.xptableWidget.setSelectionBehavior(QTableWidget.SelectRows)
        # self.ui.xptableWidget.setMouseTracking(True)
        # self.ui.xptableWidget.setSelectionMode(QTableWidget.SingleSelection)
        # self.ui.xptableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.ui.xptableWidget.horizontalHeader().setHighlightSections(False)
        # self.ui.xptableWidget.setStyleSheet("QTableWidget::item:hover{background:#e4f1f8;color: black;}")
        # self.ui.xptableWidget.verticalScrollBar().setStyleSheet("QScrollBar:vertical{width:12px;background-color:black;margin:0px,0px,0px,0px;padding-top:0px;padding-bottom:0px;}"
        #                                                          "QScrollBar:sub-page:vertical{background:qlineargradient(x1: 0.5, y1: 1, x2: 0.5, y2: 0, stop: 0 #D4DCE1, stop: 1 white);}QScrollBar:add-page:vertical{background:qlineargradient(x1: 0.5, y1: 0, x2: 0.5, y2: 1, stop: 0 #D4DCE1, stop: 1 white);}"
        #                                                          "QScrollBar:handle:vertical{background:qlineargradient(x1: 0, y1: 0.5, x2: 1, y2: 0.5, stop: 0 #CACACA, stop: 1 #818486);}QScrollBar:add-line:vertical{background-color:green;}")
        # self.ui.xptableWidget.resizeColumnsToContents()
        # for m in range(xp_rows):
        #     self.ui.xptableWidget.setRowHeight(m,40)
        # self.connect(self.ui.xptableWidget, SIGNAL("cellDoubleClicked(int, int)"), self.getItem)
        # self.ui.xptableWidget.connect(self, Signals.show_app_detail, self.slot_show_app_detail)
        # self.ui.xptableWidget.setIconSize(QSize(32, 32))
        # # 表头设置
        # self.ui.xptableWidget.horizontalHeader().setClickable(False)
        # self.ui.xptableWidget.horizontalHeader().resizeSection(0,100)
        # self.ui.xptableWidget.horizontalHeader().resizeSection(1,150)
        # self.ui.xptableWidget.horizontalHeader().resizeSection(2,150)
        # self.ui.xptableWidget.horizontalHeader().resizeSection(3,310)
        # self.ui.xptableWidget.horizontalHeader().setFixedHeight(25)
        # self.ui.xptableWidget.horizontalHeader().setStretchLastSection(True)
        # self.ui.xptableWidget.horizontalHeader().setStyleSheet("QHeaderView::section {background-color:#e4f1f8;color: black;}")#设置表头字体，颜色，模式  padding-left: 4px;border: 1px solid #6c6c6c;

    def push_date_into_table(self, category_list, software_list):
        pass
        # current_row = 0
        # self.software_index = []#显示列表中记录软件名的一个的顺序列表，方便双击时根据索引值获取软件名
        # for category in category_list:
        #     app_list = self.appmgr.search_app_display_info(category)
        #     for context in app_list:
        #         if context[0] in software_list:
        #             self.software_index.append(context[0])
        #             if context[0] == 'wine-qq' or context[0] == 'ppstream':
        #                 app = None
        #             else:
        #                 app = self.appmgr.get_application_by_name(context[0])
        #             for i in range(self.ui.xptableWidget.columnCount()):
        #                 if i == 0:
        #                     cnt = category
        #                 elif i == 1:
        #                     cnt = context[3]
        #                 elif i == 2:
        #                     cnt = context[1]
        #                 elif i == 3:
        #                     cnt = context[4]
        #                 else:
        #                     cnt = ''
        #                 if i == 1:
        #                     if(os.path.isfile(UBUNTUKYLIN_RES_WIN_PATH + str(context[2]) + ".png")):
        #                         software_icon = UBUNTUKYLIN_RES_WIN_PATH + context[2]+".png"
        #                     elif(os.path.isfile(UBUNTUKYLIN_RES_WIN_PATH + str(context[2]) + ".jpg")):
        #                         software_icon = UBUNTUKYLIN_RES_WIN_PATH + context[2]+".jpg"
        #                     else:
        #                         software_icon = UBUNTUKYLIN_RES_WIN_PATH + "default.png"
        #                     self.ui.xptableWidget.setItem(current_row, i, QTableWidgetItem(QIcon(software_icon), cnt))
        #                 elif i == 2:
        #                     if context[0] in ('ppstream', 'wine-qq'):
        #                         if(os.path.isfile(UBUNTUKYLIN_RES_ICON_PATH + context[0] + ".png")):
        #                             software_icon = UBUNTUKYLIN_RES_ICON_PATH + context[0] + ".png"
        #                         elif(os.path.isfile(UBUNTUKYLIN_RES_ICON_PATH + context[0] + ".jpg")):
        #                             software_icon = UBUNTUKYLIN_RES_ICON_PATH + context[0] + ".jpg"
        #                         elif(os.path.isfile(UBUNTUKYLIN_RES_TMPICON_PATH + context[0] + ".png")):
        #                             software_icon = UBUNTUKYLIN_RES_TMPICON_PATH + context[0] + ".png"
        #                         elif(os.path.isfile(UBUNTUKYLIN_RES_TMPICON_PATH + context[0] + ".jpg")):
        #                             software_icon = UBUNTUKYLIN_RES_TMPICON_PATH + context[0] + ".jpg"
        #                         else:
        #                             software_icon = UBUNTUKYLIN_RES_TMPICON_PATH + "default.png"
        #                     else:
        #                         if(os.path.isfile(UBUNTUKYLIN_RES_ICON_PATH + str(app.name) + ".png")):
        #                             software_icon = UBUNTUKYLIN_RES_ICON_PATH + app.name + ".png"
        #                         elif(os.path.isfile(UBUNTUKYLIN_RES_ICON_PATH + str(app.name) + ".jpg")):
        #                             software_icon = UBUNTUKYLIN_RES_ICON_PATH + app.name + ".jpg"
        #                         elif(os.path.isfile(UBUNTUKYLIN_RES_TMPICON_PATH + app.name + ".png")):
        #                             software_icon = UBUNTUKYLIN_RES_TMPICON_PATH + app.name + ".png"
        #                         elif(os.path.isfile(UBUNTUKYLIN_RES_TMPICON_PATH + app.name + ".jpg")):
        #                             software_icon = UBUNTUKYLIN_RES_TMPICON_PATH + app.name + ".jpg"
        #                         else:
        #                             software_icon = UBUNTUKYLIN_RES_TMPICON_PATH + "default.png"
        #                     self.ui.xptableWidget.setItem(current_row, i, QTableWidgetItem(QIcon(software_icon), cnt))
        #                 else:
        #                     newItem = QTableWidgetItem(cnt)
        #                     newItem.setTextAlignment(Qt.AlignCenter)
        #                     self.ui.xptableWidget.setItem(current_row,i,newItem)
        #             btn = XpItemWidget(context[0], app, self.backend, self)
        #             self.connect(btn, Signals.install_app, self.slot_click_install)
        #             self.ui.xptableWidget.setCellWidget(current_row,self.ui.xptableWidget.columnCount()-1,btn)
        #             current_row += 1

    # add by kobe
    def init_xp_solution_widget(self):
        # def slot_recommend_apps_ready(self,applist):
    # LOG.debug("receive recommend apps ready, count is %d", len(applist))
        self.winnum = 0
        count_per_line = 2
        index = int(0)
        x = y = int(0)

        # for app in applist:
        #     recommend = NormalCard(app, self.ui.recommendWidget)
        #     # self.connect(recommend, Signals.show_app_detail, self.slot_show_app_detail)
        #     # self.connect(recommend, Signals.install_app, self.slot_click_install)
        #     # self.connect(self, Signals.apt_process_finish, recommend.slot_work_finished)
        #     # self.connect(self, Signals.apt_process_cancel, recommend.slot_work_cancel)
        #
        #     if index % count_per_line == 0:
        #         x = 0
        #     x = int(index % count_per_line) * (212 + 2)
        #     y = int(index / count_per_line) * (88 + 2)
        #     index = index + 1
        #     recommend.move(x, y)
        #
        # self.rec_ready = True
        # self.check_init_ready()
        # pass
        #------------获取数据------------
        self.xp_model.init_data_model()
        # applist = self.xp_model.get_soft_app_list()
        # for app in applist:
        #得到xp表中所有按优先级排序的软件名列表

        category_list = self.xp_model.get_xp_category_list()#xp替换分类在xp数据表中的所有分类列表，无重复

        # applist = self.xp_model.get_soft_app_list()
        # for eachapp in applist:
        #     app = self.appmgr.get_application_by_name(eachapp)
        #     if app is not None:
        #         recommend = WinCard("kobe", "lixiang", app, self.ui.winListWidget)
        #     # self.connect(recommend, Signals.show_app_detail, self.slot_show_app_detail)
        #     # self.connect(recommend, Signals.install_app, self.slot_click_install)
        #     # self.connect(self, Signals.apt_process_finish, recommend.slot_work_finished)
        #     # self.connect(self, Signals.apt_process_cancel, recommend.slot_work_cancel)
        #
        #         if index % count_per_line == 0:
        #             x = 0
        #         x = int(index % count_per_line) * (420 + 2)
        #         y = int(index / count_per_line) * (88 + 2)
        #         index = index + 1
        #         recommend.move(x, y)



        for category in category_list:
            app_list = self.appmgr.search_app_display_info(category)
            #"select app_name,display_name,windows_app_name,display_name_windows,description from xp where categories='%s'"
            for context in app_list:
                if context[0] == 'wine-qq' or context[0] == 'ppstream':
                    self.winnum += 1
                    app = None
                    winstat = WinGather(context[0], context[1], context[2], context[3], context[4], category)
                    recommend = WinCard(winstat, app, self.ui.winListWidget)
                    if index % count_per_line == 0:
                        x = 0
                    x = int(index % count_per_line) * (427 + 2)
                    y = int(index / count_per_line) * (88 + 2)
                    index = index + 1
                    recommend.move(x, y)
                else:
                    app = self.appmgr.get_application_by_name(context[0])
                    if app is not None:
                        self.winnum += 1
                    winstat = WinGather(context[0], context[1], context[2], context[3], context[4], category)
                    recommend = WinCard(winstat, app, self.ui.winListWidget)
                    if index % count_per_line == 0:
                        x = 0
                    x = int(index % count_per_line) * (427 + 2)
                    y = int(index / count_per_line) * (88 + 2)
                    index = index + 1
                    recommend.move(x, y)
        self.xp_exists = 1

        # xp_rows = self.xp_model.get_table_rows_num()#要建立的表格的行数
        # (category_pos_list, category_offset_list) = self.xp_model.get_category_cell_position_offset()
        # (win_pos_list, win_offset_list) = self.xp_model.get_win_cell_position_offset()
        # category_list = self.xp_model.get_xp_category_list()#xp替换分类在xp数据表中的所有分类列表，无重复
        # software_list = self.xp_model.get_xp_software_list_()#xp替换软件在软件源中的有效列表
        #
        # #------------表格创建和美化------------
        # self.set_tablewidget_stylesheet(xp_rows)
        #
        # #------------数据填充------------
        # self.push_date_into_table(category_list, software_list)
        #
        # # 合并category的单元格
        # for i in range(len(category_pos_list)):
        #     self.ui.xptableWidget.setSpan(category_pos_list[i], 0, int(category_offset_list[i]), 1)
        #
        # # 合并windows软件的单元格
        # for i in range(len(win_pos_list)):
        #     self.ui.xptableWidget.setSpan(win_pos_list[i], 1, int(win_offset_list[i]), 1)
        # self.xp_exists = 1

    def show_to_frontend(self):
        self.show()
        self.raise_()

    def slot_show_loading_div(self):
        self.loadingDiv.start_loading("")

    def mousePressEvent(self, event):
        if (event.button() == Qt.LeftButton):
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if (event.buttons() == Qt.LeftButton and self.dragPosition != -1):
            self.move(event.globalPos() - self.dragPosition)
            event.accept()

    def show_more_search_result(self, listWidget):
        listLen = len(listWidget)

        count = 0
        for appname in self.searchList:
            app = self.appmgr.get_application_by_name(appname)
            if app is None:
                continue

            if count < listLen:
                count = count + 1
                continue
            if(count > (Globals.SOFTWARE_STEP_NUM + listLen)):
                break

            oneitem = QListWidgetItem()
            liw = ListItemWidget(app, self.backend, self.nowPage, self)
            self.connect(liw, Signals.show_app_detail, self.slot_show_app_detail)
            self.connect(liw, Signals.install_app, self.slot_click_install)
            self.connect(liw, Signals.upgrade_app, self.slot_click_upgrade)
            self.connect(liw, Signals.remove_app, self.slot_click_remove)
            listWidget.addItem(oneitem)
            listWidget.setItemWidget(oneitem, liw)
            count = count + 1

        return True

    def show_more_software(self, listWidget):
        if self.nowPage == "searchpage":
            self.show_more_search_result(listWidget)
        else:
            listLen = listWidget.count()
            apps = self.appmgr.get_category_apps(self.category)

            count = 0
            for pkgname, app in apps.iteritems():

                if self.nowPage ==  "uppage":
                    if app.is_installed is False:
                        continue
                    if app.is_installed is True and app.is_upgradable is False:
                        continue
                if self.nowPage == "unpage" and app.is_installed is False:
                    continue

                if count < listLen:
                    count = count + 1
                    continue

                # if(count > (Globals.showSoftwareStep + listLen)):
                #     break


                # oneitem = QListWidgetItem()
                # liw = ListItemWidget(app, self.nowPage, self)
                # self.connect(liw, Signals.show_app_detail, self.slot_show_app_detail)
                # self.connect(liw, Signals.install_app, self.slot_click_install)
                # self.connect(liw, Signals.upgrade_app, self.slot_click_upgrade)
                # self.connect(liw, Signals.remove_app, self.slot_click_remove)
                # listWidget.addItem(oneitem)
                # listWidget.setItemWidget(oneitem, liw)

                card = NormalCard(app, self.nowPage, self.unListWidget.cardPanel)
                self.unListWidget.add_card(card)
                self.connect(card, Signals.show_app_detail, self.slot_show_app_detail)
                self.connect(card, Signals.install_app, self.slot_click_install)
                self.connect(card, Signals.upgrade_app, self.slot_click_upgrade)
                self.connect(card, Signals.remove_app, self.slot_click_remove)
                self.connect(self, Signals.apt_process_finish, card.slot_work_finished)
                self.connect(self, Signals.apt_process_cancel, card.slot_work_cancel)

                count = count + 1

                if(count >= (Globals.SOFTWARE_STEP_NUM + listLen)):
                    break

    def get_current_listWidget(self):
        listWidget = ''
        if(self.nowPage == "allpage"):
            listWidget = self.ui.allsListWidget
        elif(self.nowPage == "uppage"):
            listWidget = self.ui.upListWidget
        elif(self.nowPage == "unpage"):
            listWidget = self.unListWidget
        elif(self.nowPage == "searchpage"):
            listWidget = self.ui.searchListWidget
        return listWidget

    def switch_to_category(self, category, forcechange):
        LOG.debug("switch category from %s to %s", self.category, category)
        if self.category == category and forcechange == False:
            return

        if(category is not None):
            self.category = category

        listWidget = self.get_current_listWidget()

        listWidget.scrollToTop()            # if not, the func will trigger slot_softwidget_scroll_end()
        listWidget.setWhatsThis(category)   # use whatsThis() to save each selected category
        listWidget.clear()                  # empty it

        self.show_more_software(listWidget)

        self.emit(Signals.count_application_update)

    def add_task_item(self, app, isdeb=False):
        # add a deb file task
        if(isdeb == True):
            oneitem = QListWidgetItem()
            tliw = TaskListItemWidget(app, self, isdeb=True)
            # self.connect(tliw, Signals.task_cancel, self.slot_click_cancel)
            self.connect(tliw, Signals.task_remove, self.slot_remove_task)
            self.ui.taskListWidget.addItem(oneitem)
            self.ui.taskListWidget.setItemWidget(oneitem, tliw)
            self.stmap[app.name] = tliw
        else:
            oneitem = QListWidgetItem()
            tliw = TaskListItemWidget(app,self)
            self.connect(tliw, Signals.task_cancel, self.slot_click_cancel)
            self.connect(tliw, Signals.task_remove, self.slot_remove_task)
            self.ui.taskListWidget.addItem(oneitem)
            self.ui.taskListWidget.setItemWidget(oneitem, tliw)
            self.stmap[app.name] = tliw

    def del_task_item(self, pkgname):
        count = self.ui.taskListWidget.count()
        print "del_task_item:",count
        for i in range(count):
            item = self.ui.taskListWidget.item(i)
            taskitem = self.ui.taskListWidget.itemWidget(item)
            if taskitem.app.name == pkgname:
                print "del_task_item: found an item",i,pkgname
                delitem = self.ui.taskListWidget.takeItem(i)
                self.ui.taskListWidget.removeItemWidget(delitem)
                del delitem
                break

    def reset_nav_bar(self):
        self.ui.btnHomepage.setEnabled(True)
        self.ui.btnUp.setEnabled(True)
        self.ui.btnUn.setEnabled(True)
        self.ui.btnTask.setEnabled(True)
        self.ui.btnXp.setEnabled(True)
        self.ui.btnHomepage.setStyleSheet("QPushButton{background-image:url('res/nav-homepage-1.png');border:0px;}QPushButton:hover{background:url('res/nav-homepage-2.png');}QPushButton:pressed{background:url('res/nav-homepage-3.png');}")
        self.ui.btnAll.setStyleSheet("QPushButton{background-image:url('res/nav-all-1.png');border:0px;}QPushButton:hover{background:url('res/nav-all-2.png');}QPushButton:pressed{background:url('res/nav-all-3.png');}")
        self.ui.btnUp.setStyleSheet("QPushButton{background-image:url('res/nav-up-1.png');border:0px;}QPushButton:hover{background:url('res/nav-up-2.png');}QPushButton:pressed{background:url('res/nav-up-3.png');}")
        self.ui.btnUn.setStyleSheet("QPushButton{background-image:url('res/nav-un-1.png');border:0px;}QPushButton:hover{background:url('res/nav-un-2.png');}QPushButton:pressed{background:url('res/nav-un-3.png');}")
        self.ui.btnTask.setStyleSheet("QPushButton{background-image:url('res/nav-task-1.png');border:0px;}QPushButton:hover{background:url('res/nav-task-2.png');}QPushButton:pressed{background:url('res/nav-task-3.png');}")
        self.ui.btnXp.setStyleSheet("QPushButton{background-image:url('res/nav-windows-1.png');border:0px;}QPushButton:hover{background:url('res/nav-windows-2.png');}QPushButton:pressed{background:url('res/nav-windows-3.png');}")

    def check_uksc_update(self):
        self.uksc = self.appmgr.get_application_by_name("ubuntu-kylin-software-center")
        if(self.uksc != None):
            if(self.uksc.is_upgradable == True):
                cd = ConfirmDialog("软件中心有新版本，是否升级？", self)
                self.connect(cd, SIGNAL("confirmdialogok"), self.update_uksc)
                cd.exec_()

    def update_uksc(self):
        self.emit(Signals.install_app, self.uksc)

    def restart_uksc(self):
        os.execv("/usr/bin/ubuntu-kylin-software-center", ["uksc"])

    # get the point out app
    def init_pointout(self):
        # check user config is show
        flag = self.appmgr.get_pointout_is_show_from_db()
        if(flag == True):
            self.get_pointout()

    def get_pointout(self):
        # find not installed pointout apps
        pl = self.appmgr.get_pointout_apps()

        if(len(pl) > 0):
            self.pointout.ui.contentliw.clear()
            for p in pl:
                oneitem = QListWidgetItem()
                pliw = PointListItemWidget(p, self.backend, self)
                self.connect(pliw, Signals.show_app_detail, self.slot_show_app_detail)
                self.connect(pliw, Signals.install_app_rcm, self.slot_click_install_rcm)
                # self.connect(pliw, Signals.install_app, self.slot_click_install)
                self.pointout.ui.contentliw.addItem(oneitem)
                self.pointout.ui.contentliw.setItemWidget(oneitem, pliw)

            self.pointout.show_animation()
        else:
            # in quiet mode, no pointout app.  quit uksc
            if(Globals.LAUNCH_MODE == 'quiet'):
                self.slot_close()


    #-------------------------------------------------slots-------------------------------------------------

    def slot_change_category(self, citem):
        category = str(citem.whatsThis())

        if(self.nowPage == "searchpage"):
            self.ui.searchWidget.setVisible(False)
            self.nowPage = self.hisPage

        self.switch_to_category(category, False)

        if(self.nowPage == "homepage"):
            self.reset_nav_bar()
        if(self.nowPage == "homepage" and self.ui.allsWidget.isVisible() == False):
            self.ui.allsWidget.setVisible(True)
        if(self.nowPage == "uppage" and self.ui.upWidget.isVisible() == False):
            self.ui.upWidget.setVisible(True)
        if(self.nowPage == "unpage" and self.ui.unWidget.isVisible() == False):
            self.ui.unWidget.setVisible(True)
        if(self.nowPage == "xppage" and self.ui.winpageWidget.isVisible() == False):
            self.ui.winpageWidget.setVisible(True)
        # if(self.nowPage == "xppage" and self.ui.xpWidget.isVisible() == False):
        #     self.ui.xpWidget.setVisible(True)

    def slot_softwidget_scroll_end(self, now):
        listWidget = self.get_current_listWidget()
        max = listWidget.verticalScrollBar().maximum()
        if(now == max):
            self.show_more_software(listWidget)

    def slot_advertisement_ready(self,adlist):
        LOG.debug("receive ads ready, count is %d", len(adlist))
        if adlist is not None:
            self.adw = ADWidget(adlist, self)
            self.adw.move(0, 44)
            (sum_inst,sum_up, sum_all) = self.appmgr.get_application_count()
            self.softCount.setText(str(sum_all))

        self.ads_ready = True
        self.check_init_ready()

    def slot_recommend_apps_ready(self,applist):
        LOG.debug("receive recommend apps ready, count is %d", len(applist))

        for app in applist:
            recommend = RcmdCard(app, self.recommendWidget.cardPanel)
            self.recommendWidget.add_card(recommend)
            self.connect(recommend, Signals.show_app_detail, self.slot_show_app_detail)
            self.connect(recommend, Signals.install_app, self.slot_click_install)
            self.connect(self, Signals.apt_process_finish, recommend.slot_work_finished)
            self.connect(self, Signals.apt_process_cancel, recommend.slot_work_cancel)

        self.rec_ready = True
        self.check_init_ready()

    def slot_ratingrank_apps_ready(self, applist):
        LOG.debug("receive rating rank apps ready, count is %d", len(applist))
        self.ui.rankView.clear()
        for app in applist:
            if app is not None:
                oneitem = QListWidgetItem()
                oneitem.setWhatsThis(app.name)
                rliw = RankListItemWidget(app.displayname, self.ui.rankView.count() + 1)
                self.ui.rankView.addItem(oneitem)
                self.ui.rankView.setItemWidget(oneitem, rliw)
        self.ui.rankWidget.setVisible(True)

        self.topratedload.stop_loading()

    def slot_rating_reviews_ready(self,rnrlist):
        LOG.debug("receive ratings and reviews ready, count is %d", len(rnrlist))
        print "receive ratings and reviews ready, count is:",len(rnrlist)
        self.rnr_ready = True

    def slot_app_reviews_ready(self,reviewlist):
        LOG.debug("receive reviews for an app, count is %d", len(reviewlist))

        self.detailScrollWidget.add_review(reviewlist)

    def slot_app_screenshots_ready(self,sclist):
        LOG.debug("receive screenshots for an app, count is %d", len(sclist))

        self.detailScrollWidget.add_sshot(sclist)

    def slot_count_application_update(self):
        (inst,up, all) = self.appmgr.get_application_count()
        (cat_inst,cat_up, cat_all) = self.appmgr.get_application_count(self.category)

        LOG.debug("receive installed app count: %d", inst)
        if len(self.category)>0:
            self.ui.allsMSGBar.setText("所有软件 <font color='#009900'>" + str(all) + "</font> 款,当前分类有 <font color='#009900'>" + str(cat_all) +"</font> 款")
            self.ui.unMSGBar.setText("可卸载软件 <font color='#009900'>" + str(inst) + "</font> 款,当前分类有 <font color='#009900'>" + str(cat_inst) +"</font> 款")
            self.ui.upMSGBar.setText("可升级软件 <font color='#009900'>" + str(up) + "</font> 款,当前分类有 <font color='#009900'>" + str(cat_up) +"</font> 款")
        else:
            self.ui.allsMSGBar.setText("所有软件 <font color='#009900'>" + str(all) + "</font> 款,系统盘可用空间 <font color='#009900'>" + vfs.get_available_size() + "</font>")
            self.ui.unMSGBar.setText("可卸载软件 <font color='#009900'>" + str(inst) + "</font> 款,系统盘可用空间 <font color='#009900'>" + vfs.get_available_size() + "</font>")
            self.ui.upMSGBar.setText("可升级软件 <font color='#009900'>" + str(up) + "</font> 款,系统盘可用空间 <font color='#009900'>" + vfs.get_available_size() + "</font>")
        self.ui.taskMSGBar.setText("已安装软件 <font color='#009900'>" + str(inst) + "</font> 款,系统盘可用空间 <font color='#009900'>" + vfs.get_available_size() + "</font>")
        # self.ui.xpMSGBar.setText("当前可替换 <font color='#009900'>" + str(self.ui.xptableWidget.rowCount()) + "</font> 款软件")
        self.ui.wincountlabel.setText(str(self.winnum))

    def slot_goto_homepage(self, ishistory=False):
        # if(ishistory == False):
        #     self.history.history_add(self.slot_goto_homepage)

        if self.nowPage != 'homepage':
            forceChange = True
        else:
            forceChange = False
        self.nowPage = 'homepage'
        # self.ui.categoryView.setEnabled(True)
        # self.switch_to_category(self.category,forceChange)
        self.detailScrollWidget.hide()
        # self.ui.searchBG.setVisible(True)
        self.ui.homepageWidget.setVisible(True)
        self.ui.rankWidget.setVisible(True)
        self.ui.allsWidget.setVisible(False)
        self.ui.upWidget.setVisible(False)
        self.ui.unWidget.setVisible(False)
        # self.ui.xpWidget.setVisible(False)
        self.ui.winpageWidget.setVisible(False)
        self.ui.searchWidget.setVisible(False)
        self.ui.taskWidget.setVisible(False)
        self.ui.btnHomepage.setEnabled(False)
        self.ui.btnAll.setEnabled(True)
        self.ui.btnUp.setEnabled(True)
        self.ui.btnUn.setEnabled(True)
        self.ui.btnTask.setEnabled(True)
        self.ui.btnXp.setEnabled(True)
        self.ui.btnHomepage.setStyleSheet("QPushButton{background-image:url('res/nav-homepage-3.png');border:0px;}")
        self.ui.btnAll.setStyleSheet("QPushButton{background-image:url('res/nav-all-1.png');border:0px;}QPushButton:hover{background:url('res/nav-all-2.png');}QPushButton:pressed{background:url('res/nav-all-3.png');}")
        self.ui.btnUp.setStyleSheet("QPushButton{background-image:url('res/nav-up-1.png');border:0px;}QPushButton:hover{background:url('res/nav-up-2.png');}QPushButton:pressed{background:url('res/nav-up-3.png');}")
        self.ui.btnUn.setStyleSheet("QPushButton{background-image:url('res/nav-un-1.png');border:0px;}QPushButton:hover{background:url('res/nav-un-2.png');}QPushButton:pressed{background:url('res/nav-un-3.png');}")
        self.ui.btnTask.setStyleSheet("QPushButton{background-image:url('res/nav-task-1.png');border:0px;}QPushButton:hover{background:url('res/nav-task-2.png');}QPushButton:pressed{background:url('res/nav-task-3.png');}")
        self.ui.btnXp.setStyleSheet("QPushButton{background-image:url('res/nav-windows-1.png');border:0px;}QPushButton:hover{background:url('res/nav-windows-2.png');}QPushButton:pressed{background:url('res/nav-windows-3.png');}")

    def slot_goto_allpage(self):
        if self.nowPage != 'allpage':
            forceChange = True
        else:
            forceChange = False
        self.nowPage = 'allpage'
        # self.ui.categoryView.setEnabled(True)
        self.switch_to_category(self.category,forceChange)
        self.detailScrollWidget.hide()
        # self.ui.searchBG.setVisible(True)
        self.ui.homepageWidget.setVisible(False)
        self.ui.allsWidget.setVisible(True)
        self.ui.upWidget.setVisible(False)
        self.ui.unWidget.setVisible(False)
        # self.ui.xpWidget.setVisible(False)
        self.ui.winpageWidget.setVisible(False)
        self.ui.searchWidget.setVisible(False)
        self.ui.taskWidget.setVisible(False)
        self.ui.btnHomepage.setEnabled(True)
        self.ui.btnAll.setEnabled(False)
        self.ui.btnUp.setEnabled(True)
        self.ui.btnUn.setEnabled(True)
        self.ui.btnTask.setEnabled(True)
        self.ui.btnXp.setEnabled(True)
        self.ui.btnHomepage.setStyleSheet("QPushButton{background-image:url('res/nav-homepage-1.png');border:0px;}QPushButton:hover{background:url('res/nav-homepage-2.png');}QPushButton:pressed{background:url('res/nav-homepage-3.png');}")
        self.ui.btnAll.setStyleSheet("QPushButton{background-image:url('res/nav-all-3.png');border:0px;}")
        self.ui.btnUp.setStyleSheet("QPushButton{background-image:url('res/nav-up-1.png');border:0px;}QPushButton:hover{background:url('res/nav-up-2.png');}QPushButton:pressed{background:url('res/nav-up-3.png');}")
        self.ui.btnUn.setStyleSheet("QPushButton{background-image:url('res/nav-un-1.png');border:0px;}QPushButton:hover{background:url('res/nav-un-2.png');}QPushButton:pressed{background:url('res/nav-un-3.png');}")
        self.ui.btnTask.setStyleSheet("QPushButton{background-image:url('res/nav-task-1.png');border:0px;}QPushButton:hover{background:url('res/nav-task-2.png');}QPushButton:pressed{background:url('res/nav-task-3.png');}")
        self.ui.btnXp.setStyleSheet("QPushButton{background-image:url('res/nav-windows-1.png');border:0px;}QPushButton:hover{background:url('res/nav-windows-2.png');}QPushButton:pressed{background:url('res/nav-windows-3.png');}")

    def slot_goto_uppage(self, ishistory=False):
        # if(ishistory == False):
        #     self.history.history_add(self.slot_goto_uppage)

        if self.nowPage != 'uppage':
            forceChange = True
        else:
            forceChange = False

        self.nowPage = 'uppage'
        # self.ui.categoryView.setEnabled(True)
        self.switch_to_category(self.category,forceChange)
        self.detailScrollWidget.hide()
        # self.ui.searchBG.setVisible(True)
        self.ui.homepageWidget.setVisible(False)
        self.ui.allsWidget.setVisible(False)
        self.ui.upWidget.setVisible(True)
        self.ui.unWidget.setVisible(False)
        # self.ui.xpWidget.setVisible(False)
        self.ui.winpageWidget.setVisible(False)
        self.ui.searchWidget.setVisible(False)
        self.ui.taskWidget.setVisible(False)
        self.ui.btnHomepage.setEnabled(True)
        self.ui.btnAll.setEnabled(True)
        self.ui.btnUp.setEnabled(False)
        self.ui.btnUn.setEnabled(True)
        self.ui.btnTask.setEnabled(True)
        self.ui.btnXp.setEnabled(True)
        self.ui.btnHomepage.setStyleSheet("QPushButton{background-image:url('res/nav-homepage-1.png');border:0px;}QPushButton:hover{background:url('res/nav-homepage-2.png');}QPushButton:pressed{background:url('res/nav-homepage-3.png');}")
        self.ui.btnAll.setStyleSheet("QPushButton{background-image:url('res/nav-all-1.png');border:0px;}QPushButton:hover{background:url('res/nav-all-2.png');}QPushButton:pressed{background:url('res/nav-all-3.png');}")
        self.ui.btnUp.setStyleSheet("QPushButton{background-image:url('res/nav-up-3.png');border:0px;}")
        self.ui.btnUn.setStyleSheet("QPushButton{background-image:url('res/nav-un-1.png');border:0px;}QPushButton:hover{background:url('res/nav-un-2.png');}QPushButton:pressed{background:url('res/nav-un-3.png');}")
        self.ui.btnTask.setStyleSheet("QPushButton{background-image:url('res/nav-task-1.png');border:0px;}QPushButton:hover{background:url('res/nav-task-2.png');}QPushButton:pressed{background:url('res/nav-task-3.png');}")
        self.ui.btnXp.setStyleSheet("QPushButton{background-image:url('res/nav-windows-1.png');border:0px;}QPushButton:hover{background:url('res/nav-windows-2.png');}QPushButton:pressed{background:url('res/nav-windows-3.png');}")

    def slot_goto_unpage(self, ishistory=False):
        # if(ishistory == False):
        #     self.history.history_add(self.slot_goto_unpage)

        if self.nowPage != 'unpage':
            forceChange = True
        else:
            forceChange = False

        self.nowPage = 'unpage'
        # self.ui.categoryView.setEnabled(True)
        self.switch_to_category(self.category, forceChange)
        self.detailScrollWidget.hide()
        # self.ui.searchBG.setVisible(True)
        self.ui.homepageWidget.setVisible(False)
        self.ui.allsWidget.setVisible(False)
        self.ui.upWidget.setVisible(False)
        self.ui.unWidget.setVisible(True)
        # self.ui.xpWidget.setVisible(False)
        self.ui.winpageWidget.setVisible(False)
        self.ui.searchWidget.setVisible(False)
        self.ui.taskWidget.setVisible(False)
        self.ui.btnHomepage.setEnabled(True)
        self.ui.btnAll.setEnabled(True)
        self.ui.btnUp.setEnabled(True)
        self.ui.btnUn.setEnabled(False)
        self.ui.btnTask.setEnabled(True)
        self.ui.btnXp.setEnabled(True)
        self.ui.btnHomepage.setStyleSheet("QPushButton{background-image:url('res/nav-homepage-1.png');border:0px;}QPushButton:hover{background:url('res/nav-homepage-2.png');}QPushButton:pressed{background:url('res/nav-homepage-3.png');}")
        self.ui.btnAll.setStyleSheet("QPushButton{background-image:url('res/nav-all-1.png');border:0px;}QPushButton:hover{background:url('res/nav-all-2.png');}QPushButton:pressed{background:url('res/nav-all-3.png');}")
        self.ui.btnUp.setStyleSheet("QPushButton{background-image:url('res/nav-up-1.png');border:0px;}QPushButton:hover{background:url('res/nav-up-2.png');}QPushButton:pressed{background:url('res/nav-up-3.png');}")
        self.ui.btnUn.setStyleSheet("QPushButton{background-image:url('res/nav-un-3.png');border:0px;}")
        self.ui.btnTask.setStyleSheet("QPushButton{background-image:url('res/nav-task-1.png');border:0px;}QPushButton:hover{background:url('res/nav-task-2.png');}QPushButton:pressed{background:url('res/nav-task-3.png');}")
        self.ui.btnXp.setStyleSheet("QPushButton{background-image:url('res/nav-windows-1.png');border:0px;}QPushButton:hover{background:url('res/nav-windows-2.png');}QPushButton:pressed{background:url('res/nav-windows-3.png');}")

    def slot_goto_taskpage(self, ishistory=False):
        # if(ishistory == False):
        #     self.history.history_add(self.slot_goto_taskpage)

        self.nowPage = 'taskpage'
        self.emit(Signals.count_application_update)
        # self.ui.categoryView.setEnabled(False)
        # self.ui.categoryView.clearSelection()
        self.detailScrollWidget.hide()
        # self.ui.searchBG.setVisible(False)
        self.ui.homepageWidget.setVisible(False)
        self.ui.allsWidget.setVisible(False)
        self.ui.upWidget.setVisible(False)
        self.ui.unWidget.setVisible(False)
        self.ui.searchWidget.setVisible(False)
        self.ui.taskWidget.setVisible(True)
        # self.ui.xpWidget.setVisible(False)
        self.ui.winpageWidget.setVisible(False)
        self.ui.btnHomepage.setEnabled(True)
        self.ui.btnAll.setEnabled(True)
        self.ui.btnUp.setEnabled(True)
        self.ui.btnUn.setEnabled(True)
        self.ui.btnTask.setEnabled(False)
        self.ui.btnXp.setEnabled(True)
        self.ui.btnHomepage.setStyleSheet("QPushButton{background-image:url('res/nav-homepage-1.png');border:0px;}QPushButton:hover{background:url('res/nav-homepage-2.png');}QPushButton:pressed{background:url('res/nav-homepage-3.png');}")
        self.ui.btnAll.setStyleSheet("QPushButton{background-image:url('res/nav-all-1.png');border:0px;}QPushButton:hover{background:url('res/nav-all-2.png');}QPushButton:pressed{background:url('res/nav-all-3.png');}")
        self.ui.btnUp.setStyleSheet("QPushButton{background-image:url('res/nav-up-1.png');border:0px;}QPushButton:hover{background:url('res/nav-up-2.png');}QPushButton:pressed{background:url('res/nav-up-3.png');}")
        self.ui.btnUn.setStyleSheet("QPushButton{background-image:url('res/nav-un-1.png');border:0px;}QPushButton:hover{background:url('res/nav-un-2.png');}QPushButton:pressed{background:url('res/nav-un-3.png');}")
        self.ui.btnTask.setStyleSheet("QPushButton{background-image:url('res/nav-task-3.png');border:0px;}")
        self.ui.btnXp.setStyleSheet("QPushButton{background-image:url('res/nav-windows-1.png');border:0px;}QPushButton:hover{background:url('res/nav-windows-2.png');}QPushButton:pressed{background:url('res/nav-windows-3.png');}")

    def goto_search_page(self, ishistory=False):
        # if(ishistory == False):
        #     self.history.history_add(self.goto_search_page)

        if self.nowPage != 'searchpage':
            self.hisPage = self.nowPage
        self.nowPage = 'searchpage'
        self.reset_nav_bar()
        # self.ui.categoryView.setEnabled(True)
        self.switch_to_category(self.category,True)
        self.detailScrollWidget.hide()
        self.ui.homepageWidget.setVisible(False)
        self.ui.allsWidget.setVisible(False)
        self.ui.upWidget.setVisible(False)
        self.ui.unWidget.setVisible(False)
        self.ui.searchWidget.setVisible(True)
        self.ui.taskWidget.setVisible(False)
        # self.ui.xpWidget.setVisible(False)
        self.ui.winpageWidget.setVisible(False)


    def slot_goto_xppage(self, ishistory=False):
        # if(ishistory == False):
        #     self.history.history_add(self.slot_goto_xppage)

        self.nowPage = 'xppage'
        # self.emit(Signals.count_application_update)
        # self.ui.categoryView.setEnabled(False)
        # self.ui.categoryView.clearSelection()
        self.detailScrollWidget.hide()
        # self.ui.searchBG.setVisible(False)
        self.ui.homepageWidget.setVisible(False)
        self.ui.allsWidget.setVisible(False)
        self.ui.upWidget.setVisible(False)
        self.ui.unWidget.setVisible(False)
        self.ui.searchWidget.setVisible(False)
        self.ui.taskWidget.setVisible(False)
        # self.ui.xpWidget.setVisible(True)
        # self.ui.xpWidget.setVisible(False)
        self.ui.winpageWidget.setVisible(True)
        # self.ui.winMsgWidget.show()
        self.ui.btnHomepage.setEnabled(True)
        self.ui.btnAll.setEnabled(True)
        self.ui.btnUp.setEnabled(True)
        self.ui.btnUn.setEnabled(True)
        self.ui.btnTask.setEnabled(True)
        self.ui.btnXp.setEnabled(False)
        self.ui.btnHomepage.setStyleSheet("QPushButton{background-image:url('res/nav-homepage-1.png');border:0px;}QPushButton:hover{background:url('res/nav-homepage-2.png');}QPushButton:pressed{background:url('res/nav-homepage-3.png');}")
        self.ui.btnAll.setStyleSheet("QPushButton{background-image:url('res/nav-all-1.png');border:0px;}QPushButton:hover{background:url('res/nav-all-2.png');}QPushButton:pressed{background:url('res/nav-all-3.png');}")
        self.ui.btnUp.setStyleSheet("QPushButton{background-image:url('res/nav-up-1.png');border:0px;}QPushButton:hover{background:url('res/nav-up-2.png');}QPushButton:pressed{background:url('res/nav-up-3.png');}")
        self.ui.btnUn.setStyleSheet("QPushButton{background-image:url('res/nav-un-1.png');border:0px;}QPushButton:hover{background:url('res/nav-un-2.png');}QPushButton:pressed{background:url('res/nav-un-3.png');}")
        self.ui.btnTask.setStyleSheet("QPushButton{background-image:url('res/nav-task-1.png');border:0px;}QPushButton:hover{background:url('res/nav-task-2.png');}QPushButton:pressed{background:url('res/nav-task-3.png');}")
        self.ui.btnXp.setStyleSheet("QPushButton{background-image:url('res/nav-windows-3.png');border:0px;}")
        if not self.xp_exists:
            self.init_xp_solution_widget()
            self.emit(Signals.count_application_update)

    def slot_close(self):
        self.dbusControler.stop()
        sys.exit(0)

    def slot_max_normal(self):
        self.unListWidget.clear()

    def slot_min(self):
        self.showMinimized()

    def slot_show_config(self):
        self.configWidget.show()

    def slot_show_or_hide(self):
        if(self.isHidden()):
            self.show()
        else:
            self.hide()

    def slot_trayicon_activated(self, reason):
        if(reason == QSystemTrayIcon.Trigger):
            self.slot_show_or_hide()

    def slot_click_ad(self, ad):
        if(ad.type == "pkg"):
            app = self.appmgr.get_application_by_name(ad.urlorpkgid)
            self.slot_show_app_detail(app)
        elif(ad.type == "url"):
            webbrowser.open_new_tab(ad.urlorpkgid)

    def slot_click_item(self, item):
        liw = ''
        if(self.nowPage == 'homepage'):
            liw = self.ui.allsListWidget.itemWidget(item)
        if(self.nowPage == 'uppage'):
            liw = self.ui.upListWidget.itemWidget(item)
        if(self.nowPage == 'unpage'):
            liw = self.ui.unListWidget.itemWidget(item)
        if(self.nowPage == 'searchpage'):
            liw = self.ui.searchListWidget.itemWidget(item)
        self.emit(SIGNAL("clickitem"), liw.app)

    def slot_click_rank_item(self, item):
        pkgname = item.whatsThis()
        app = self.appmgr.get_application_by_name(str(pkgname))
        if app is not None:
            self.slot_show_app_detail(app)
        else:
            LOG.debug("rank item does not have according app...")

    def slot_show_app_detail(self, app, ishistory=False):
        self.reset_nav_bar()
        self.detailScrollWidget.showSimple(app)

    def slot_show_deb_detail(self, path):
        self.reset_nav_bar()
        self.detailScrollWidget.show_by_local_debfile(path)

    def slot_update_source(self,quiet=False):
        LOG.info("add an update task:%s","###")
        self.backend.update_source(quiet)

    def slot_click_update_source(self):
        self.emit(Signals.update_source)

    def slot_click_install_debfile(self, debfile):
        LOG.info("add an install debfile task:%s", debfile.path)
        # install deb deps
        res = self.backend.install_deps(debfile.path)
        if res:
            # install deb
            res = self.backend.install_debfile(debfile.path)
        if res:
            self.add_task_item(debfile, isdeb=True)

    def slot_click_install(self, app):
        LOG.info("add an install task:%s",app.name)
        self.appmgr.submit_pingback_app(app.name)
        res = self.backend.install_package(app.name)
        if res:
            self.add_task_item(app)

    def slot_click_install_rcm(self, app):
        LOG.info("add an install task:%s",app.name)
        self.appmgr.submit_pingback_app(app.name, isrcm=True)
        res = self.backend.install_package(app.name)
        if res:
            self.add_task_item(app)


    def slot_click_upgrade(self, app):
        LOG.info("add an upgrade task:%s",app.name)

        res = self.backend.upgrade_package(app.name)
        if res:
            self.add_task_item(app)

    def slot_click_remove(self, app):
        LOG.info("add a remove task:%s",app.name)

        res = self.backend.remove_package(app.name)
        if res:
            self.add_task_item(app)

    def slot_click_cancel(self, appname):
        LOG.info("cancel an task:%s",appname)
        self.backend.cancel_package(appname)

    def slot_remove_task(self, app):
        self.del_task_item(app.name)
        del self.stmap[app.name]

    # search
    def slot_searchDTimer_timeout(self):
        self.searchDTimer.stop()
        if self.ui.leSearch.text():
            s = self.ui.leSearch.text().toUtf8()
            if len(s) < 2:
                return

            reslist = self.searchDB.search_software(s)

            LOG.debug("search result:%d",len(reslist))
            self.searchList = reslist
            count = 0
            for appname in self.searchList:
                app = self.appmgr.get_application_by_name(appname)
                if app is None:
                    continue
                count = count + 1
            self.goto_search_page()
            self.ui.searchMSGBar.setText("共搜索到软件 <font color='#009900'>" + str(count) + "</font> 款")

    def slot_search_text_change(self, text):
        self.searchDTimer.stop()
        self.searchDTimer.start(500)

    # name:app name ; processtype:fetch/apt ;
    def slot_status_change(self, name, processtype, action, percent, msg):
        if action == AppActions.UPDATE:
            if int(percent) == 0:
                self.configWidget.slot_update_status_change(1)
            elif int(percent) == 100:
                self.configWidget.slot_update_status_change(99)
            elif int(percent) >= 200:
                self.appmgr.update_models(AppActions.UPDATE,"")
            else:
                self.configWidget.slot_update_status_change(percent)
        elif action == AppActions.UPDATE_FIRST:
            if int(percent) >= 200:
                self.appmgr.update_models(AppActions.UPDATE_FIRST,"")
            else:
                self.updateSinglePB.value_change(percent)
        else:
            if processtype=='cancel':
                self.emit(Signals.apt_process_cancel,name,action)

            if self.stmap.has_key(name) is False:
                print "has no key :  ",name
                LOG.warning("there is no task for this app:%s",name)
            else:
                taskItem = self.stmap[name]
                if processtype=='cancel':
                    self.del_task_item(name)
                    del self.stmap[name]
                    #self.emit(Signals.apt_process_cancel,name,action)
                else:
                    if processtype=='apt' and int(percent)>=200:
                        # (install debfile deps finish) is not the (install debfile task) finish
                        if(action != AppActions.INSTALLDEPS):
                            self.emit(Signals.apt_process_finish,name,action)
                    else:
                        taskItem.status_change(processtype, percent, msg)

    # call the backend models update opeartion
    def slot_apt_process_finish(self,pkgname,action):
        self.appmgr.update_models(action,pkgname)

    # update backend models ready
    def slot_apt_cache_update_ready(self, action, pkgname):
        if(action == AppActions.UPDATE_FIRST):
            self.updateSinglePB.hide()
            self.appmgr.init_models()
        else:
            (inst,up, all) = self.appmgr.get_application_count(self.category)
            (cat_inst,cat_up, cat_all) = self.appmgr.get_application_count()
            self.emit(Signals.count_application_update)

            msg = "软件" + AptActionMsg[action] + "操作完成"

            if(action == AppActions.UPDATE):
                self.configWidget.slot_update_finish()
                if(self.configWidget.iscanceled == True):
                    self.messageBox.alert_msg("已取消更新软件源")
                else:
                    self.messageBox.alert_msg(msg)
            else:
                if(pkgname == "ubuntu-kylin-software-center"):
                    cd = ConfirmDialog("软件中心升级完成，重启程序？", self)
                    self.connect(cd, SIGNAL("confirmdialogok"), self.restart_uksc)
                    cd.exec_()
                else:
                    self.messageBox.alert_msg(msg)


def check_local_deb_file(url):
    return os.path.isfile(url)


def main():
    app = QApplication(sys.argv)

    QTextCodec.setCodecForTr(QTextCodec.codecForName("UTF-8"))
    QTextCodec.setCodecForCStrings(QTextCodec.codecForName("UTF-8"))

    globalfont = QFont()
    # globalfont.setFamily("")
    # 文泉驿微米黑
    # 文泉驿等宽微米黑
    # 方正书宋_GBK
    # 方正仿宋_GBK
    # 方正姚体_GBK
    # 方正宋体S-超大字符集
    # 方正宋体S-超大字符集(SIP)
    # 方正小标宋_GBK
    # 方正楷体_GBK
    # 方正细黑一_GBK
    # 方正行楷_GBK
    # 方正超粗黑_GBK
    # 方正隶书_GBK
    # 方正魏碑_GBK
    # 方正黑体_GBK
    globalfont.setPixelSize(14)
    app.setFont(globalfont)
    app.setWindowIcon(QIcon(UBUNTUKYLIN_RES_PATH +"uksc.png"))

    # check show quiet
    argn = len(sys.argv)
    if(argn == 1):
        Globals.LAUNCH_MODE = 'normal'
    elif(argn > 1):
        arg = sys.argv[1]
        if(arg == '-quiet'):
            Globals.LAUNCH_MODE = 'quiet'
        else:
            Globals.LAUNCH_MODE = 'normal'
            if(check_local_deb_file(arg)):
                Globals.LOCAL_DEB_FILE = arg
            else:
                sys.exit(0)

    mw = SoftwareCenter()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()