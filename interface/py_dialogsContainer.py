# Sacks: a video conference-meeting system
# Copyright (C) 2009 Associazione Intellicom
#
# Authors: Marcello Di Guglielmo, Daniel Donato
#  info_AT_riunionidigitali.org
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston MA 02110-1301, USA.
#


import sys
from PyQt4 import QtCore, QtGui
from Ui_confDialogsContainer import Ui_confDialogsContainer

#from stream.py_streamDialog import pystreamDialog
#from vpn.py_vpnDialog import pyvpnDialog


#	QWidget al posto di QMainWindow
class pydialogsContainer(QtGui.QDialog):
	def __init__(self,  parent=None):
		QtGui.QDialog.__init__(self, parent)
		self.ui = Ui_confDialogsContainer()
		self.ui.setupUi(self)
#		self.show()
		QtCore.QObject.connect(self.ui.listWidget, QtCore.SIGNAL("currentItemChanged(QListWidgetItem *, QListWidgetItem *)"), self.changePage)
		self.stackedWidget = QtGui.QStackedWidget()
		self.ui.horizontalLayout.addWidget(self.stackedWidget)
		self.closeButton=self.ui.closeButton
		
#		a=pystreamDialog()
#		vpnDialog=pyvpnDialog()
#		vpnDialog.iconDialog=a.iconDialog
#		vpnDialog.nameDialog=a.nameDialog
#		self.addDialog(vpnDialog)
	def changePage(self, currentPage, previousPage):
		if not currentPage:
			currentPage = previousPage
		print "currentIndexList: "+ str(self.ui.listWidget.row(currentPage))
		self.stackedWidget.setCurrentIndex(self.ui.listWidget.row(currentPage))

	
	def setCurrentDialog(self, dialogSlot):
		print "current dialog"
		self.ui.listWidget.setCurrentItem(dialogSlot.listWidgetItem)
		#self.stackedWidget.setCurrentWidget(dialog)
	def addDialog(self, dialogSlot):
		self.stackedWidget.addWidget(dialogSlot)
		self.ui.listWidget.addItem(dialogSlot.listWidgetItem)

	def closeEvent(self, closeEvent):
		self.closeButton.click()
	

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	dialog = pydialogsContainer()
#	vpnDialog=pyvpnDialog()
	stream=pystreamDialog()
	dialog.addDialog(stream)
	
	sys.exit(app.exec_())
