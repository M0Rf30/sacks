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
from Ui_voipInterface import Ui_VoipInterface
from py_voip import pyvoip
from py_voipDialog import pyvoipDialog
class pyvoipInterface(QtGui.QMainWindow):
	def __init__(self, voipSettings=None, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		self.ui = Ui_VoipInterface()
		print "parent Voip: ", parent
		
		self.ui.setupUi(self)
		if parent:
			self.ui.actionAbout.setVisible(False)
		else:	
			QtCore.QObject.connect(self.ui.actionAbout, QtCore.SIGNAL("triggered ()"), self.showAbout)
			
		if voipSettings:
			self.voipSettings = voipSettings
		else:
			self.voipSettings = QtCore.QSettings("Intellicom", "Voip")
		self.voipDialog = pyvoipDialog(self.voipSettings)
		
		voipParameters = self.voipDialog.returnParameters()
		self.sipStunServer = voipParameters["sipStunServer"]
		if self.sipStunServer:
			self.voipSession = pyvoip(self.sipStunServer, self)
		else:
			self.voipSession = pyvoip(self)
		self.elaboratingCallIncoming = False
		self.buttonGroup = QtGui.QButtonGroup()
		self.iconRegistering = QtGui.QIcon(self.ui.actionRegister.icon())
		self.iconRegistered = QtGui.QIcon(self.iconRegistering)
		self.iconRegistered.addPixmap(QtGui.QPixmap(":/voip/interface/images/voip/internet-telephony_online.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
		print "self.ui.gridLayoutKeys.count:", self.ui.gridLayoutKeys.count()
		for buttonIndex in range(self.ui.gridLayoutKeys.count()):
			buttonLayoutItem = self.ui.gridLayoutKeys.itemAt(buttonIndex)
			button = buttonLayoutItem.widget()
			self.buttonGroup.addButton(button)
			
			
		QtCore.QObject.connect(self.ui.actionRegister, QtCore.SIGNAL("toggled (bool)"), self.registerVoip)
		QtCore.QObject.connect(self.ui.actionConfigure, QtCore.SIGNAL("triggered()"), lambda: self.emit(QtCore.SIGNAL("configureRequest()")))
		QtCore.QObject.connect(self.ui.actionConfigure, QtCore.SIGNAL("triggered()"), self.voipDialog.show)
		QtCore.QObject.connect(self.buttonGroup, QtCore.SIGNAL("buttonClicked (QAbstractButton *)"), self.pressKeyButton)
		QtCore.QObject.connect(self.ui.pushButtonCall, QtCore.SIGNAL("clicked ()"), self.pressCallButton)
		QtCore.QObject.connect(self.ui.pushButtonHangup, QtCore.SIGNAL("clicked ()"), self.pressHangupButton)
		self.lineEditUrlVoip = self.ui.comboBoxVoipUrls.lineEdit()
		QtCore.QObject.connect(self.lineEditUrlVoip, QtCore.SIGNAL("returnPressed ()"), self.ui.pushButtonCall.animateClick)
		QtCore.QObject.connect(self.voipSession, QtCore.SIGNAL("callRequest"), self.elaborateCallRequest)
		QtCore.QObject.connect(self.voipSession, QtCore.SIGNAL("callConfirmed"), self.elaborateCallConfirmed)
		QtCore.QObject.connect(self.voipSession, QtCore.SIGNAL("callDisconnected"), self.elaborateCallDisconnected)
		QtCore.QObject.connect(self.voipSession, QtCore.SIGNAL("voipRegistrated(bool)"), self.manageRegistration)
		
	def pressHangupButton(self):
		self.voipSession.hangupCall()
		self.elaboratingCallIncoming = False
		self.lineEditUrlVoip.clear()
		self.ui.labelVoipInfo.clear()
		self.ui.labelVoipDisplay.clear()
	def pressCallButton(self):
		if self.elaboratingCallIncoming:
			self.voipSession.answer()
		else:	
			urlCallVoip = self.lineEditUrlVoip.text()
			if urlCallVoip:
				if not urlCallVoip.contains("@"):
			
					urlCallVoip = urlCallVoip + "@" + self.voipSession.hostVoipProvider
						
				self.voipSession.makeCall(str("sip:" + urlCallVoip))
				self.ui.labelVoipInfo.setText("Call to: sip:")
				self.ui.labelVoipDisplay.setText(urlCallVoip)
				self.ui.comboBoxVoipUrls.addItem(urlCallVoip)
				self.lineEditUrlVoip.clear()
		
	def pressKeyButton(self, button):
		keyButton = button.text()
		textLineEditUrl = self.lineEditUrlVoip.text()
		self.lineEditUrlVoip.setText(textLineEditUrl + keyButton)

	def elaborateCallRequest(self, urlCall):
		self.elaboratingCallIncoming = True
		self.ui.labelVoipInfo.setText("Call from sip:")
		self.ui.labelVoipDisplay.setText(urlCall)
		
	def elaborateCallConfirmed(self, urlCall):
		self.ui.labelVoipInfo.setText("Call with sip:")
		self.ui.labelVoipDisplay.setText(urlCall)
		
	def elaborateCallDisconnected(self, urlCall):	
		self.ui.labelVoipInfo.setText("Disconnected from sip:")
		print "urlCall" + urlCall
		self.ui.labelVoipDisplay.setText(urlCall)
		QtCore.QTimer.singleShot(2000, self.pressHangupButton)
	
	def manageRegistration(self, verified):
		print "manageRegistrated: ", verified
		if verified:
			self.ui.actionRegister.setIcon(self.iconRegistered)
		else:
			self.ui.actionRegister.setIcon(self.iconRegistering)
			
			
	def registerVoip(self, abilitated):
		if abilitated:
			voipParameters = self.voipDialog.returnParameters()
			if voipParameters["sipStunServer"] != self.sipStunServer:
				self.voipSession.closeSession()
				self.sipStunServer = voipParameters["sipStunServer"]
				self.voipSession = pyvoip(self.sipStunServer)
				QtCore.QObject.connect(self.voipSession, QtCore.SIGNAL("callRequest"), self.elaborateCallRequest)
				QtCore.QObject.connect(self.voipSession, QtCore.SIGNAL("callConfirmed"), self.elaborateCallConfirmed)
				QtCore.QObject.connect(self.voipSession, QtCore.SIGNAL("callDisconnected"), self.elaborateCallDisconnected)
				QtCore.QObject.connect(self.voipSession, QtCore.SIGNAL("voipRegistrated(bool)"), self.manageRegistration)

			if voipParameters["sipProvider"] and voipParameters["sipAccountUser"] and voipParameters["sipAccountPasswd"]:
				self.voipSession.registerVoip(voipParameters["sipProvider"], voipParameters["sipAccountUser"], voipParameters["sipAccountPasswd"])
				self.ui.pushButtonCall.setEnabled(True)
				self.ui.pushButtonHangup.setEnabled(True)				
			else:
				self.emit(QtCore.SIGNAL("configureRequest()"))
				# self.emit(QtCore.SIGNAL("configureRequest()"))self.voipDialog.show()
				self.ui.actionRegister.setChecked(False)				
		else:
			self.voipSession.unregisterVoip()
			self.ui.pushButtonCall.setEnabled(False)
			self.ui.pushButtonHangup.setEnabled(False)

# 	def configureManage(self,  configureEnable):
# 		if configureEnable:
# 			self.voipDialog.show()
# 		else:
# 			self.voipDialog.hide()
	def showAbout(self):
		self.aboutBox = QtGui.QMessageBox()
		self.aboutBox.setFixedSize(800, 600)
		self.aboutBox.setText(self.tr("     Sacks, video conference-meeting system module       \n\nAuthors: Marcello Di Guglielmo, Daniel Donato           \n\nLicense: GNU public license\nShow details for license            "))
		self.aboutBox.setWindowTitle(self.tr("About Sacks"))
		
		self.aboutBox.exec_()



	def closeEvent(self, closeEvent):
		print "voipInterfaceClose"
		self.voipSession.closeSession()
		
	
if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	voipInterface = pyvoipInterface()
	voipInterface.show()
	sys.exit(app.exec_())

