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
from Ui_voipWidget import Ui_voipWidget


class pyvoipDialog(QtGui.QDialog):
	def __init__(self, settings, parent=None):
		QtGui.QDialog.__init__(self, parent)
		self.ui = Ui_voipWidget()
		self.ui.setupUi(self)
		self.okClicked = False
		self.settings = settings
		self.voipParameters = {}
		
		self.iconDialog = self.windowIcon()
		self.nameDialog = self.windowTitle()
		self.listWidgetItem = QtGui.QListWidgetItem()
		self.listWidgetItem.setIcon(self.iconDialog)
		self.listWidgetItem.setText(self.nameDialog)
		
		sipProvider = self.settings.value("voip/sipProvider", QtCore.QVariant(""))
		self.voipParameters["sipProvider"] = str(sipProvider.toString())
		self.ui.lineEditSipProvider.setText(self.voipParameters["sipProvider"])
		
		sipAccountUser = self.settings.value("voip/sipAccountUser", QtCore.QVariant(""))
		self.voipParameters["sipAccountUser"] = str(sipAccountUser.toString())
		self.ui.lineEditSipAccountUser.setText(self.voipParameters["sipAccountUser"])
	
		sipAccountPasswd = self.settings.value("voip/sipAccountPasswd", QtCore.QVariant(""))
		self.voipParameters["sipAccountPasswd"] = str(sipAccountPasswd.toString())
		self.ui.lineEditSipAccountPasswd.setText(self.voipParameters["sipAccountPasswd"])
		
		sipStunServer = self.settings.value("voip/sipStunServer", QtCore.QVariant(""))
		self.voipParameters["sipStunServer"] = str(sipStunServer.toString())
		self.ui.lineEditSipStunServer.setText(self.voipParameters["sipStunServer"])
		
		QtCore.QObject.connect(self.ui.buttonBox, QtCore.SIGNAL("clicked (QAbstractButton *)"), self.buttonClicked)
# 		QtCore.QObject.connect(self.ui.checkBoxAudioSamplerate, QtCore.SIGNAL("toggled (bool)"), lambda: self.ui.spinBoxAudioSamplerate.setValue(0))
# 		QtCore.QObject.connect(self.ui.checkBoxVideoBitrate, QtCore.SIGNAL("toggled (bool)"), lambda: self.ui.spinBoxVideoBitrate.setValue(256))
# 		QtCore.QObject.connect(self.ui.checkBoxAudioBitrate, QtCore.SIGNAL("toggled (bool)"), lambda: self.ui.spinBoxAudioBitrate.setValue(16))
			
	def returnParameters(self):
		return self.voipParameters
	def buttonClicked(self, button):
		buttonClickedRole = self.ui.buttonBox.buttonRole(button)
		
		if buttonClickedRole == QtGui.QDialogButtonBox.ResetRole:
			self.ui.lineEditSipProvider.clear()
			self.ui.lineEditSipAccountUser.clear()
			self.ui.lineEditSipAccountPasswd.clear()
			self.ui.lineEditSipStunServer.clear()
		elif buttonClickedRole == QtGui.QDialogButtonBox.AcceptRole:
			sipProvider = self.ui.lineEditSipProvider.text()
			self.voipParameters["sipProvider"] = sipProvider
			sipAccountUser = self.ui.lineEditSipAccountUser.text()
			self.voipParameters["sipAccountUser"] = sipAccountUser
			sipAccountPasswd = self.ui.lineEditSipAccountPasswd.text()
			self.voipParameters["sipAccountPasswd"] = sipAccountPasswd				
			sipStunServer = self.ui.lineEditSipStunServer.text()
			self.voipParameters["sipStunServer"] = sipStunServer
			
			self.settings.setValue("voip/sipProvider", QtCore.QVariant(self.voipParameters["sipProvider"]))
			self.settings.setValue("voip/sipAccountUser", QtCore.QVariant(self.voipParameters["sipAccountUser"]))
			self.settings.setValue("voip/sipAccountPasswd", QtCore.QVariant(self.voipParameters["sipAccountPasswd"]))
			self.settings.setValue("voip/sipStunServer", QtCore.QVariant(self.voipParameters["sipStunServer"]))
		
			print "sipProvider: " + self.voipParameters["sipProvider"]
			print "sipAccountUser: " + self.voipParameters["sipAccountUser"]
			print "sipAccountPasswd: " + self.voipParameters["sipAccountPasswd"]
			print "sipStunServer: " + self.voipParameters["sipStunServer"]
	
	def showEvent(self, showEvent):
		print "showEvent"
		self.ui.lineEditSipProvider.setText(self.voipParameters["sipProvider"])
		self.ui.lineEditSipAccountUser.setText(self.voipParameters["sipAccountUser"])
		self.ui.lineEditSipAccountPasswd.setText(self.voipParameters["sipAccountPasswd"])
		self.ui.lineEditSipStunServer.setText(self.voipParameters["sipStunServer"])
	
	
if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	settings = QtCore.QSettings("Intellicom", "Prove")
	mainpymplayer = pyvoipDialog(settings)
	mainpymplayer.show()
	sys.exit(app.exec_())
