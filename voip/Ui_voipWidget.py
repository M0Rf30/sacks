# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/marcello/Documenti/sacks/sacksSvnUser/voip/voipWidget.ui'
#
# Created: Mon Nov 16 17:33:06 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_voipWidget(object):
    def setupUi(self, voipWidget):
        voipWidget.setObjectName("voipWidget")
        voipWidget.resize(220, 264)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/voip/interface/images/voip/internet-telephony_online.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        voipWidget.setWindowIcon(icon)
        self.gridLayout_2 = QtGui.QGridLayout(voipWidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBoxAcquisition = QtGui.QGroupBox(voipWidget)
        self.groupBoxAcquisition.setObjectName("groupBoxAcquisition")
        self.gridLayout = QtGui.QGridLayout(self.groupBoxAcquisition)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.labelSipProvider = QtGui.QLabel(self.groupBoxAcquisition)
        self.labelSipProvider.setObjectName("labelSipProvider")
        self.horizontalLayout_2.addWidget(self.labelSipProvider)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.lineEditSipProvider = QtGui.QLineEdit(self.groupBoxAcquisition)
        self.lineEditSipProvider.setMaximumSize(QtCore.QSize(200, 16777215))
        self.lineEditSipProvider.setObjectName("lineEditSipProvider")
        self.horizontalLayout_2.addWidget(self.lineEditSipProvider)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.labelSipAccountUser = QtGui.QLabel(self.groupBoxAcquisition)
        self.labelSipAccountUser.setObjectName("labelSipAccountUser")
        self.horizontalLayout_3.addWidget(self.labelSipAccountUser)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.lineEditSipAccountUser = QtGui.QLineEdit(self.groupBoxAcquisition)
        self.lineEditSipAccountUser.setMaximumSize(QtCore.QSize(200, 16777215))
        self.lineEditSipAccountUser.setObjectName("lineEditSipAccountUser")
        self.horizontalLayout_3.addWidget(self.lineEditSipAccountUser)
        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.labelSipAccountPasswd = QtGui.QLabel(self.groupBoxAcquisition)
        self.labelSipAccountPasswd.setObjectName("labelSipAccountPasswd")
        self.horizontalLayout_4.addWidget(self.labelSipAccountPasswd)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.lineEditSipAccountPasswd = QtGui.QLineEdit(self.groupBoxAcquisition)
        self.lineEditSipAccountPasswd.setMaximumSize(QtCore.QSize(200, 16777215))
        self.lineEditSipAccountPasswd.setEchoMode(QtGui.QLineEdit.Password)
        self.lineEditSipAccountPasswd.setObjectName("lineEditSipAccountPasswd")
        self.horizontalLayout_4.addWidget(self.lineEditSipAccountPasswd)
        self.gridLayout.addLayout(self.horizontalLayout_4, 3, 0, 1, 1)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.labelSipStunServer = QtGui.QLabel(self.groupBoxAcquisition)
        self.labelSipStunServer.setObjectName("labelSipStunServer")
        self.horizontalLayout_5.addWidget(self.labelSipStunServer)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.lineEditSipStunServer = QtGui.QLineEdit(self.groupBoxAcquisition)
        self.lineEditSipStunServer.setMaximumSize(QtCore.QSize(200, 16777215))
        self.lineEditSipStunServer.setObjectName("lineEditSipStunServer")
        self.horizontalLayout_5.addWidget(self.lineEditSipStunServer)
        self.gridLayout.addLayout(self.horizontalLayout_5, 4, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBoxAcquisition, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(voipWidget)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Reset)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_2.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(voipWidget)
        QtCore.QMetaObject.connectSlotsByName(voipWidget)

    def retranslateUi(self, voipWidget):
        voipWidget.setWindowTitle(QtGui.QApplication.translate("voipWidget", "Voip", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBoxAcquisition.setTitle(QtGui.QApplication.translate("voipWidget", "Sip account configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.labelSipProvider.setText(QtGui.QApplication.translate("voipWidget", "Sip Provider", None, QtGui.QApplication.UnicodeUTF8))
        self.labelSipAccountUser.setText(QtGui.QApplication.translate("voipWidget", "Sip User", None, QtGui.QApplication.UnicodeUTF8))
        self.labelSipAccountPasswd.setText(QtGui.QApplication.translate("voipWidget", "Sip Password", None, QtGui.QApplication.UnicodeUTF8))
        self.labelSipStunServer.setText(QtGui.QApplication.translate("voipWidget", "Stun Server", None, QtGui.QApplication.UnicodeUTF8))

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    voipWidget = QtGui.QWidget()
    ui = Ui_voipWidget()
    ui.setupUi(voipWidget)
    voipWidget.show()
    sys.exit(app.exec_())

