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
"""This module provides a remote screen VNC interface  


The class is "pyvncInterface", which is used to create an Interface to a  VNC remote desktop instance. It imports an interface gui for contain the desktop screen and send connection commands.
"""


import sys
from PyQt5 import QtCore, QtGui
from .Ui_vncInterface import Ui_VncInterface
from .py_vncScreen import pyvncScreen
# from py_vncDialog import pyvncDialog
class pyvncInterface(QtGui.QMainWindow):
	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		self.ui = Ui_VncInterface()
		self.ui.setupUi(self)
		# self.show()
		self.ui.scrollArea.setFocusPolicy(QtCore.Qt.ClickFocus)
		self.vncScreen = pyvncScreen()
		self.ui.scrollArea.setWidget(self.vncScreen)
		self.setFocusProxy(self.vncScreen)
		QtCore.QObject.connect(self.ui.actionConnectScreen, QtCore.SIGNAL("toggled (bool)"), self.connectScreen)
		self.screenParameters = None
		self.menuRemoteScreen = self.ui.menuRemoteScreen
		self.menuBar = self.ui.menuBar
		self.toolBar = self.ui.toolBar
	def setScreenParameters(self, parameters=None):
		"""Method "setScreenParameters" that set the vnc-session connection parameters which are received from a protocol command and launched from a button interaction.
		"""
		if parameters:
			self.screenParameters = parameters
			
		else:	
			hostDisplay, ok = QtGui.QInputDialog.getText(self, self.tr("Parameters Screen"), self.tr("Host:Display"))
			hostDisplayList = hostDisplay.split(":")
			if ok and hostDisplayList.count() == 2:
				host = hostDisplayList[0]
				display = hostDisplayList[1]
				displayNum, ok = display.toInt()
				if ok:
					passwd, ok = QtGui.QInputDialog.getText(self, self.tr("Parameters Screen"), self.tr("Password"), QtGui.QLineEdit.Password)
					if ok:
						self.screenParameters = host, displayNum, passwd
						
	def launch(self):
		self.vncScreen.disconnect()
		print("lauch screen")
		self.ui.actionConnectScreen.setChecked(True)
	def stop(self):
		
		self.ui.actionConnectScreen.setChecked(False)
	def connectScreen(self, abilitated):
		print(abilitated)
		if abilitated:
			if not self.screenParameters:
				self.setScreenParameters()
			if self.screenParameters:
				host, display, passwd = self.screenParameters
				connected = self.vncScreen.connect(host, display, passwd)
				if connected:
					self.emit(QtCore.SIGNAL("remoteScreenRegistrated(bool)"), True)
				else: 
					self.emit(QtCore.SIGNAL("remoteScreenRegistrated(bool)"), False)
					self.ui.actionConnectScreen.setChecked(False)
			else:
				self.ui.actionConnectScreen.setChecked(False)
		else:
			self.vncScreen.disconnect()
			self.screenParameters = False

	def closeEvent(self, closeEvent):
		self.vncScreen.close()
if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	vnc = pyvncInterface()
	vnc.show()
	parameters = "193.205.171.97", 1, "g3n3r1c0"
	vnc.setScreenParameters(parameters)
	vnc.launch()
	sys.exit(app.exec_())
		

