# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/daniel/svnSacks/user/interface/confDialogsContainer.ui'
#
# Created: Thu Mar  4 15:45:57 2010
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_confDialogsContainer(object):
    def setupUi(self, confDialogsContainer):
        confDialogsContainer.setObjectName("confDialogsContainer")
        confDialogsContainer.resize(334, 437)
        self.gridLayout = QtGui.QGridLayout(confDialogsContainer)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtGui.QSpacerItem(346, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.closeButton = QtGui.QPushButton(confDialogsContainer)
        self.closeButton.setObjectName("closeButton")
        self.gridLayout.addWidget(self.closeButton, 1, 1, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.listWidget = QtGui.QListWidget(confDialogsContainer)
        self.listWidget.setMinimumSize(QtCore.QSize(90, 0))
        self.listWidget.setMaximumSize(QtCore.QSize(90, 16777215))
        self.listWidget.setIconSize(QtCore.QSize(100, 100))
        self.listWidget.setMovement(QtGui.QListView.Static)
        self.listWidget.setSpacing(15)
        self.listWidget.setViewMode(QtGui.QListView.IconMode)
        self.listWidget.setObjectName("listWidget")
        self.horizontalLayout.addWidget(self.listWidget)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 2)

        self.retranslateUi(confDialogsContainer)
        self.listWidget.setCurrentRow(-1)
        QtCore.QObject.connect(self.closeButton, QtCore.SIGNAL("clicked()"), confDialogsContainer.close)
        QtCore.QMetaObject.connectSlotsByName(confDialogsContainer)

    def retranslateUi(self, confDialogsContainer):
        confDialogsContainer.setWindowTitle(QtGui.QApplication.translate("confDialogsContainer", "Config Dialogs", None, QtGui.QApplication.UnicodeUTF8))
        self.closeButton.setText(QtGui.QApplication.translate("confDialogsContainer", "&Close", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    confDialogsContainer = QtGui.QDialog()
    ui = Ui_confDialogsContainer()
    ui.setupUi(confDialogsContainer)
    confDialogsContainer.show()
    sys.exit(app.exec_())

