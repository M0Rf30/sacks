# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/daniel/svnSacks/user/interface/processWinEmbed.ui'
#
# Created: Thu Mar  4 15:45:58 2010
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ProcessWinEmbed(object):
    def setupUi(self, ProcessWinEmbed):
        ProcessWinEmbed.setObjectName("ProcessWinEmbed")
        ProcessWinEmbed.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(ProcessWinEmbed)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollAreaScreen = QtGui.QScrollArea(ProcessWinEmbed)
        self.scrollAreaScreen.setWidgetResizable(True)
        self.scrollAreaScreen.setObjectName("scrollAreaScreen")
        self.scrollAreaWidgetContents = QtGui.QWidget(self.scrollAreaScreen)
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 386, 286))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollAreaScreen.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollAreaScreen)

        self.retranslateUi(ProcessWinEmbed)
        QtCore.QMetaObject.connectSlotsByName(ProcessWinEmbed)

    def retranslateUi(self, ProcessWinEmbed):
        ProcessWinEmbed.setWindowTitle(QtGui.QApplication.translate("ProcessWinEmbed", "Process Embedded", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ProcessWinEmbed = QtGui.QWidget()
    ui = Ui_ProcessWinEmbed()
    ui.setupUi(ProcessWinEmbed)
    ProcessWinEmbed.show()
    sys.exit(app.exec_())

