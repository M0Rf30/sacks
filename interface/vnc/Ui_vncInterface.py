# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/marcello/Documenti/sacks/sacksSvnUser/interface/vnc/vncInterface.ui'
#
# Created: Thu Dec 17 23:59:49 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_VncInterface(object):
    def setupUi(self, VncInterface):
        VncInterface.setObjectName("VncInterface")
        VncInterface.resize(509, 381)
        VncInterface.setDockNestingEnabled(False)
        self.centralwidget = QtGui.QWidget(VncInterface)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea = QtGui.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtGui.QWidget(self.scrollArea)
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 503, 319))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)
        VncInterface.setCentralWidget(self.centralwidget)
        self.menuBar = QtGui.QMenuBar(VncInterface)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 509, 26))
        self.menuBar.setObjectName("menuBar")
        self.menuRemoteScreen = QtGui.QMenu(self.menuBar)
        self.menuRemoteScreen.setObjectName("menuRemoteScreen")
        VncInterface.setMenuBar(self.menuBar)
        self.toolBar = QtGui.QToolBar(VncInterface)
        self.toolBar.setObjectName("toolBar")
        VncInterface.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionConnectScreen = QtGui.QAction(VncInterface)
        self.actionConnectScreen.setCheckable(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/vnc/images/vnc/rfbdrake.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionConnectScreen.setIcon(icon)
        self.actionConnectScreen.setObjectName("actionConnectScreen")
        self.menuRemoteScreen.addAction(self.actionConnectScreen)
        self.menuRemoteScreen.addSeparator()
        self.menuBar.addAction(self.menuRemoteScreen.menuAction())
        self.toolBar.addAction(self.actionConnectScreen)

        self.retranslateUi(VncInterface)
        QtCore.QMetaObject.connectSlotsByName(VncInterface)

    def retranslateUi(self, VncInterface):
        VncInterface.setWindowTitle(QtGui.QApplication.translate("VncInterface", "RemoteScreen Interface", None, QtGui.QApplication.UnicodeUTF8))
        self.menuRemoteScreen.setTitle(QtGui.QApplication.translate("VncInterface", "Screen", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("VncInterface", "RemoteScreen ToolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionConnectScreen.setText(QtGui.QApplication.translate("VncInterface", "Connect Screen", None, QtGui.QApplication.UnicodeUTF8))

import vnc_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    VncInterface = QtGui.QMainWindow()
    ui = Ui_VncInterface()
    ui.setupUi(VncInterface)
    VncInterface.show()
    sys.exit(app.exec_())

