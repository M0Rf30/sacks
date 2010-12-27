# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/marcello/Documenti/sacks/user/jabber/xmppDialog.ui'
#
# Created: Fri Oct  2 00:26:24 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_xmppDialog(object):
    def setupUi(self, xmppDialog):
        xmppDialog.setObjectName("xmppDialog")
        xmppDialog.resize(319, 103)
        self.gridLayout = QtGui.QGridLayout(xmppDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.labelUser = QtGui.QLabel(xmppDialog)
        self.labelUser.setObjectName("labelUser")
        self.verticalLayout_2.addWidget(self.labelUser)
        self.labelPassword = QtGui.QLabel(xmppDialog)
        self.labelPassword.setObjectName("labelPassword")
        self.verticalLayout_2.addWidget(self.labelPassword)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.lineEditUser = QtGui.QLineEdit(xmppDialog)
        self.lineEditUser.setObjectName("lineEditUser")
        self.verticalLayout.addWidget(self.lineEditUser)
        self.lineEditPassword = QtGui.QLineEdit(xmppDialog)
        self.lineEditPassword.setEchoMode(QtGui.QLineEdit.Password)
        self.lineEditPassword.setObjectName("lineEditPassword")
        self.verticalLayout.addWidget(self.lineEditPassword)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(xmppDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(xmppDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), xmppDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), xmppDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(xmppDialog)

    def retranslateUi(self, xmppDialog):
        xmppDialog.setWindowTitle(QtGui.QApplication.translate("xmppDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.labelUser.setText(QtGui.QApplication.translate("xmppDialog", "User:", None, QtGui.QApplication.UnicodeUTF8))
        self.labelPassword.setText(QtGui.QApplication.translate("xmppDialog", "Password:", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    xmppDialog = QtGui.QDialog()
    ui = Ui_xmppDialog()
    ui.setupUi(xmppDialog)
    xmppDialog.show()
    sys.exit(app.exec_())

