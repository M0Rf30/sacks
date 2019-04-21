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
"""This module provides a slot manager to a session joined user  



The class is "pyuserBox", which is used to create a slot user instance with access to a relative media instance pyuserSlot. 
From this class it's possible to receive status events from server, send command request to server or chair or send message to other users, activate remote desktop session , abilitate room mode for chair operations.
"""


import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from stream.py_userSlot import pyuserSlot

class pyuserBox(QtWidgets.QWidget):
	
	def __init__(self, nameSlot, roomJidServer, jabberUser, interfaceGui=None, parent=None):
		QtWidgets.QWidget.__init__(self, parent)
		self.jabberUser = jabberUser
		self.nameSlot = nameSlot
		self.interfaceGui = interfaceGui
		self.setWindowTitle(nameSlot)
		self.roomJidServer = roomJidServer
		self.userSlot = pyuserSlot(nameSlot, self)
		self.mdiWin = self.userSlot.mdiWin
		self.info = {}
		self.info["nameSlot"] = nameSlot
		self.BoxLayout = QtGui.QGridLayout(self)
		self.BoxLayout.setMargin(0)
		self.BoxLayout.addWidget(self.userSlot)
		if self.interfaceGui:
			print("self.interfaceGui.voipInterface.voipSession.registered ", self.interfaceGui.voipInterface.voipSession.registered)
			self.userSlot.pushButtonVoipCall.setEnabled(self.interfaceGui.voipInterface.voipSession.registered)
		self.tokenAbilitated = False
		self.remoteDesktopAddress = None
		self.roomMode(False)
		self.focusStatus = False	
		self.screenSessionAddress = ""
		self.ipRemoteDesktop = None
		self.viewRemoteDesktop = None
		self.userSlot.pushButtonActiveMedia.setIcon(self.userSlot.iconActiveOff)
		self.userSlot.pushButtonRemoteDesktopControl.setIcon(self.userSlot.iconActiveOff)
		if self.jabberUser.connected:
			self.userSlot.pushButtonActiveMedia.setEnabled(True)
		else:	
			self.userSlot.pushButtonActiveMedia.setEnabled(False)
		

		QtCore.QObject.connect(self.jabberUser, QtCore.SIGNAL("connection"), self.connection)
		QtCore.QObject.connect(self.userSlot.pushButtonActiveMedia, QtCore.SIGNAL("toggled(bool)"), self.activeMedia)
		QtCore.QObject.connect(self.userSlot.pushButtonRemoteDesktopControl, QtCore.SIGNAL("toggled(bool)"), self.activeRemoteDesktopSession)
		QtCore.QObject.connect(self.userSlot.buttonRemoteDesktop, QtCore.SIGNAL("toggled(bool)"), self.screenSession)
		QtCore.QObject.connect(self.userSlot.pushButtonToken, QtCore.SIGNAL("toggled(bool)"), self.sendToken)
		QtCore.QObject.connect(self.userSlot, QtCore.SIGNAL("sendMsg"), self.sendMsg)
		QtCore.QObject.connect(self.userSlot.buttonOnFocus, QtCore.SIGNAL("toggled (bool)"), self.mediaOnFocus)		
		QtCore.QObject.connect(self.userSlot.pushButtonVoipCall, QtCore.SIGNAL("clicked ()"), self.voipCall)
		
		if self.interfaceGui:
			QtCore.QObject.connect(self.interfaceGui.voipInterface.voipSession, QtCore.SIGNAL("voipRegistrated (bool)"), self.userSlot.pushButtonVoipCall, QtCore.SLOT("setEnabled (bool)"))
			# QtCore.QObject.connect(self.interfaceGui.remoteDesktopInterface,QtCore.SIGNAL("remoteScreenRegistrated (bool)"), self.manageRemoteScreen)
		self.iconUser = self.userSlot.iconUserEnabled
# 		self.connected(False)
		self.online = False
	
	
	def initializeRemoteDesktop(self, IP, ctrlRemoteDesktop, viewRemoteDesktop):
		print("initializeRemoteDesktop on", self.nameSlot, ": ", IP, ctrlRemoteDesktop, viewRemoteDesktop)
		self.ipRemoteDesktop = IP
		self.viewRemoteDesktop = viewRemoteDesktop
		self.ctrlRemoteDesktop = ctrlRemoteDesktop
	


	def roomMode(self, roomModeStatus):
		print("room modee per " , self.nameSlot, " ", roomModeStatus)
		# l'icona parte disabilitata perche' in room mode puo' partire che non e' presente
		self.iconUser = self.userSlot.iconUserDisabled
		if roomModeStatus:
			self.userSlot.pushButtonActiveMedia.show()
			self.userSlot.pushButtonActiveMedia.setEnabled(True)
			self.userSlot.pushButtonToken.show()
			self.userSlot.pushButtonRemoteDesktopControl.show()
			if self.interfaceGui:
			# self.userSlot.labelOnline.setPixmap(self.userSlot.pixmapConnetedOn)
				QtCore.QObject.connect(self.interfaceGui.webWidget.actionSpreadLink, QtCore.SIGNAL("triggered()"), self.sendWebLink)
		else:
			self.userSlot.pushButtonActiveMedia.hide()
			self.userSlot.pushButtonActiveMedia.setEnabled(False)
			self.userSlot.pushButtonToken.hide()
			self.userSlot.pushButtonRemoteDesktopControl.hide()
			if self.interfaceGui:
				QtCore.QObject.disconnect(self.interfaceGui.webWidget.actionSpreadLink, QtCore.SIGNAL("triggered()"), self.sendWebLink)
			
	

	def sendToken(self, abilitated):
		# self.userSlot.buttonOnFocus.setChecked(abilitated)
		if self.interfaceGui:
			if abilitated:
				for userBoxIndex in range(self.interfaceGui.ui.toolBox.count()):
					userBox = self.interfaceGui.ui.toolBox.widget(userBoxIndex)
					if userBox.info["onGuiShow"] and userBox.online:
						if userBox.tokenAbilitated:						
							userBox.userSlot.pushButtonToken.setChecked(False)
			for userBoxIndex in range(self.interfaceGui.ui.toolBox.count()):
				userBox = self.interfaceGui.ui.toolBox.widget(userBoxIndex)
			# 	print userBox.info, " ",  userBox.online
				if userBox.info["onGuiShow"] and userBox.online:
					if abilitated:
					# 	if userBox.tokenAbilitated:						
					# 		userBox.userSlot.pushButtonToken.setChecked(False)
						msgActiveToken = "/userFocus " + self.nameSlot + " True"
					else:	
						msgActiveToken = "/userFocus " + self.nameSlot + " False"
					print(userBox.nameSlot, " " , msgActiveToken)
					userBox.sendMsg(msgActiveToken, True)
			self.tokenAbilitated = abilitated
			if abilitated:
				self.focusRequest(False)
				msgTokenServer = "/tokenUser " + self.nameSlot + " True"
			else:
				msgTokenServer = "/tokenUser " + self.nameSlot + " False"
			# print "send msgTokenServer: ", msgTokenServer
			self.sendMsg(msgTokenServer, True, self.roomJidServer)
			
	def sendWebLink(self):
		if self.interfaceGui:
			webLink = self.interfaceGui.webWidget.urlWeb.text()
			if webLink[0:7] == "http://":
				msgWebLink = "/webLink " + str(webLink)
				self.sendMsg(msgWebLink, True)
	

	def connection(self, connected):
		print("connected: " + str(connected))
		if connected == 1:
			self.userSlot.pushButtonActiveMedia.setEnabled(True)
	


	def presenceRoom(self, abilitated):
		if abilitated:
			self.info["roomPresence"] = True
			self.userSlot.labelOnline.setPixmap(self.userSlot.pixmapInRoom)
		else:
			self.info["roomPresence"] = False
			self.userSlot.labelOnline.setPixmap(self.userSlot.pixmapOutRoom)

	def presenceServer(self, abilitated):
		if abilitated:
			msgAddUserServer = "/linkUserServer " + self.nameSlot + " True"
			self.sendMsg(msgAddUserServer, True, self.roomJidServer)
			self.userSlot.pushButtonToken.setEnabled(True)
			if self.nameSlot in self.jabberUser.listPresence:
				if self.jabberUser.listPresence[self.nameSlot] == True:
					self.presence(True)
					msgPresence = "/presenceUser " + self.nameSlot + " True"
					self.sendMsg(msgPresence, True, self.roomJidServer)
		else:
			msgAddUserServer = "/linkUserServer " + self.nameSlot + " False"
			self.sendMsg(msgAddUserServer, True, self.roomJidServer)
			self.userSlot.pushButtonToken.setEnabled(False)
			self.presence(False)
			msgPresence = "/presenceUser " + self.nameSlot + " False"
			self.sendMsg(msgPresence, True, self.roomJidServer)						
			self.activeMedia(False)


	def presence(self, statusPresence):
		# print "OOOOOOOOOOOOOOOOOOOOO presence di ",  self.nameSlot,  " = ",  statusPresence
		if statusPresence:
			self.userSlot.labelOnline.setPixmap(self.userSlot.pixmapConnetedOn)
			self.iconUser = self.userSlot.iconUserEnabled
			self.setWindowIcon(self.iconUser)
			self.online = True
	# 		msgPresence="/presenceUser "+ self.nameSlot + " True"
	# 		self.sendMsg(msgPresence, True, self.roomJidServer)
			if self.interfaceGui:
				boxIndex = self.interfaceGui.ui.toolBox.indexOf(self)
				self.interfaceGui.ui.toolBox.setItemIcon(boxIndex, self.iconUser)
		else:	
			self.userSlot.labelOnline.setPixmap(self.userSlot.pixmapConnetedOff)
			self.iconUser = self.userSlot.iconUserDisabled
			self.setWindowIcon(self.iconUser)
			self.userSlot.pushButtonToken.setEnabled(False)
			self.userSlot.pushButtonActiveMedia.setChecked(False)
			self.online = False
	# 		msgPresence="/presenceUser "+ self.nameSlot + " False"
	# 		self.sendMsg(msgPresence,True, self.roomJidServer)			
			if self.interfaceGui:
				boxIndex = self.interfaceGui.ui.toolBox.indexOf(self)
				self.interfaceGui.ui.toolBox.setItemIcon(boxIndex, self.iconUser)

	def activeMedia(self, abilitated):
		if abilitated:
			self.userSlot.pushButtonActiveMedia.setIcon(self.userSlot.iconActiveOn)
			self.emit(QtCore.SIGNAL('activeMedia'), self.nameSlot, abilitated)
			msgActiveMedia = "/activeMedia " + self.nameSlot + " True"
		else:
			self.userSlot.pushButtonActiveMedia.setIcon(self.userSlot.iconActiveOff)
			self.emit(QtCore.SIGNAL('activeMedia'), self.nameSlot, abilitated)
			msgActiveMedia = "/activeMedia " + self.nameSlot + " False"
		self.sendMsg(msgActiveMedia, True, self.roomJidServer)


	def activeRemoteDesktopSession(self, abilitated):
		display = "2"
			# colora di verde il tasto
		if abilitated:	
			self.userSlot.pushButtonRemoteDesktopControl.setIcon(self.userSlot.iconActiveOn)
			for userBoxIndex in range(self.interfaceGui.ui.toolBox.count()):
				userBox = self.interfaceGui.ui.toolBox.widget(userBoxIndex)
				if userBox.info["onGuiShow"]:
					if userBox != self:
						if  userBox.userSlot.pushButtonRemoteDesktopControl.isChecked():
							userBox.userSlot.pushButtonRemoteDesktopControl.setChecked(False)	
		else:
			# colora di rosso il tasto
			self.userSlot.pushButtonRemoteDesktopControl.setIcon(self.userSlot.iconActiveOff)
		
		for userBoxIndex in range(self.interfaceGui.ui.toolBox.count()):
			userBox = self.interfaceGui.ui.toolBox.widget(userBoxIndex)
			if userBox.info["onGuiShow"] and userBox.online:
			# 	if 
				if abilitated:
					if userBox != self:
						# if  userBox.userSlot.pushButtonRemoteDesktopControl.isChecked():
							# userBox.userSlot.pushButtonRemoteDesktopControl.setChecked(False)
						msgDesktopSession = "/remoteDesktop " + self.nameSlot + " True " + str(self.ipRemoteDesktop) + " " + display + " " + str(self.viewRemoteDesktop)
					else:	
						msgDesktopSession = "/remoteDesktop " + self.nameSlot + " True " + str(self.ipRemoteDesktop) + " " + display + " " + str(self.ctrlRemoteDesktop)
				
						# msgDesktopSession="/remoteDesktop "+self.nameSlot+" False"
						
				else:	
					msgDesktopSession = "/remoteDesktop " + self.nameSlot + " False"
				
				print("sendMsg ", msgDesktopSession)
				userBox.sendMsg(msgDesktopSession, True)	
							
					
			


# 	def sendRemoteDesktop(self, jidCtrlSession, address, display, control, passwd ):
# 		desktopAddress=address+display
# 		print "sendRemoteDesktopStart to ", self.nameSlot, " ",  desktopAddress
		



	def mediaOnFocus(self, onFocus):	
		if self.interfaceGui:
			if onFocus:
				if not self.focusStatus:
					pushButtonShowMediaStatus = self.userSlot.pushButtonShowMedia.isChecked()
					itemverticalLayout = self.interfaceGui.ui.verticalLayoutFocus.itemAt(0)
					print("itemverticalLayout ", itemverticalLayout)
					if itemverticalLayout:
						widgetOnFocus = itemverticalLayout.widget()
						print("widgetOnFocus ", widgetOnFocus)
						for userBoxIndex in range(self.interfaceGui.ui.toolBox.count()):
							print("userBox ", userBoxIndex)
							userBox = self.interfaceGui.ui.toolBox.widget(userBoxIndex)
							print("userBox.userSlot.mdiWin ", userBox.userSlot.mdiWin)
							if userBox.userSlot.mdiWin == widgetOnFocus:
								userBox.userSlot.buttonOnFocus.setChecked(False)
					self.userSlot.mdiWin.close()					
					self.interfaceGui.ui.verticalLayoutFocus.addWidget(self.userSlot.mdiWin)
					mediaOnFocusTitle = QtCore.QString(self.tr("On Focus: %1")).arg(self.nameSlot)
					self.interfaceGui.ui.dockWidgetMediaFocus.setWindowTitle(mediaOnFocusTitle)
					self.userSlot.mdiWin.show()
					if pushButtonShowMediaStatus:
						self.userSlot.pushButtonShowMedia.setChecked(True)
					self.focusStatus = True
			else:
				if self.focusStatus:
					pushButtonShowMediaStatus = self.userSlot.pushButtonShowMedia.isChecked()
					self.interfaceGui.ui.verticalLayoutFocus.removeWidget(self.userSlot.mdiWin)
					self.userSlot.mdiWin.close()
					
					self.interfaceGui.mdi.addWindow(self.userSlot.mdiWin)
					self.userSlot.mdiWin.resize(self.userSlot.mdiWin.minimumSize())
					if pushButtonShowMediaStatus:
						self.userSlot.pushButtonShowMedia.setChecked(True)
						self.userSlot.mdiWin.show()
					mediaOnFocusTitle = QtCore.QString(self.tr("On Focus:"))
					self.interfaceGui.ui.dockWidgetMediaFocus.setWindowTitle(mediaOnFocusTitle)
					self.focusStatus = False
	

	def setScreenParameters(self, remoteDesktopAddress, remoteDesktopDisplay=None, passwd=None):
		self.remoteDesktopAddress = remoteDesktopAddress
		self.remoteDesktopDisplay = remoteDesktopDisplay
		self.remoteDesktopPasswd = passwd
		if self.remoteDesktopAddress:
			self.userSlot.buttonRemoteDesktop.setEnabled(True)
			# launchScreenClient=QtGui.QMessageBox.question(self,"Screen Session", "Launch Remote Screen session client?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
			# if launchScreenClient==QtGui.QMessageBox.Yes:
			self.userSlot.buttonRemoteDesktop.setChecked(True)
		else:
			self.userSlot.buttonRemoteDesktop.setChecked(False)
			self.userSlot.buttonRemoteDesktop.setEnabled(False)
		
		
	def screenSession(self, abilitated):		
		if abilitated:
			parameters = (self.remoteDesktopAddress, self.remoteDesktopDisplay, self.remoteDesktopPasswd)
			print(parameters)
			self.interfaceGui.remoteDesktopInterface.stop()
			self.interfaceGui.remoteDesktopInterface.setScreenParameters(parameters)
			self.interfaceGui.remoteDesktopInterface.launch()
			# self.remoteDesktop.launch(self.screenSessionAddress, self.passwdRemoteDesktop)
			# self.interfaceGui.tabWidget.addTab(self.interfaceGui.remoteDesktopWinEmbed, 'Remote desktop')
			# self.interfaceGui.remoteDesktopWinEmbed.embedWinProcess(self.remoteDesktop.screenProcess)
		else:
			# self.remoteDesktop.stop()
			# self.interfaceGui.remoteDesktopWinEmbed.discardWinProcess()
				# indexOfRemoteDesktopWinEmbed=self.interfaceGui.tabWidget.indexOf(self.interfaceGui.remoteDesktopWinEmbed)
			# print "indexOfRemoteDesktopWinEmbed:",  indexOfRemoteDesktopWinEmbed
			# self.interfaceGui.tabWidget.removeTab(indexOfRemoteDesktopWinEmbed)
			# indexOfMdi=self.interfaceGui.tabWidget.indexOf(self.interfaceGui.mdi)
			# self.interfaceGui.tabWidget.setCurrentIndex(indexOfMdi)
			remoteDesktopEmpty = True
			for userBoxIndex in range(self.interfaceGui.ui.toolBox.count()):
				userBox = self.interfaceGui.ui.toolBox.widget(userBoxIndex)
				if userBox.info["onGuiShow"]:
					print("remoteDesktop ", userBox.nameSlot, " State: ", userBox.remoteDesktopAddress)
					if userBox != self and userBox.remoteDesktopAddress:
						remoteDesktopEmpty = False
			print("remoteDesktopEmpty: ", remoteDesktopEmpty)			
			if remoteDesktopEmpty:			
				self.interfaceGui.remoteDesktopInterface.stop()
		
		
	def showMsg(self, msg, sysTrayShow=False):
		self.userSlot.listShow(msg)
		if self.interfaceGui:
				boxIndex = self.interfaceGui.ui.toolBox.indexOf(self)
				self.interfaceGui.ui.toolBox.setItemIcon(boxIndex, self.userSlot.iconEdit)
				if self.interfaceGui.ui.toolBox.currentWidget() != self:
					if sysTrayShow and self.interfaceGui.sysTrayIcon:
						sysTrayMessage = QtCore.QString(self.tr("Message from %1")).arg(self.nameSlot)
						self.interfaceGui.sysTrayIcon.showMessage(sysTrayMessage, "")
						if sys.platform != 'win32':
							QtGui.QApplication.beep()
					
	def sendMsg(self, msg, commandType=False, jid=None):
		if commandType:
			msgCommand = QtCore.QString(msg)
			if jid == self.roomJidServer:
				msgCommand.prepend("S")
			else:	
				msgCommand.prepend("C")
			msg = msgCommand
		else:
			msgMessage = QtCore.QString(msg)
			msg = msgMessage
			if self.interfaceGui:
				boxIndex = self.interfaceGui.ui.toolBox.indexOf(self)
				self.interfaceGui.ui.toolBox.setItemIcon(boxIndex, self.iconUser)
		if self.jabberUser:
			if self.jabberUser.connected:
				if jid == None:
					jid = self.nameSlot
				self.jabberUser.sendMessage(jid, msg)
	
		
	def voipCall(self):
		if self.interfaceGui:
			voipInterface = self.interfaceGui.voipInterface
			# voipInterface.lineEditUrlVoip.setText(self.nameSlot)
			voipInterface.lineEditUrlVoip.setText("")
			self.interfaceGui.setCurrentDock(self.interfaceGui.ui.dockWidgetVoip)
			voipInterface.ui.pushButtonCall.animateClick(1000)
			print("call")
			
			
	def focusRequest(self, abilitated):
		if self.interfaceGui:
			if abilitated:
				QtCore.QObject.connect(self.interfaceGui.timer, QtCore.SIGNAL("timeout()"), self.lightIcon)
			else:	
				QtCore.QObject.disconnect(self.interfaceGui.timer, QtCore.SIGNAL("timeout()"), self.lightIcon)
	
	def lightIcon(self):
		boxIndex = self.interfaceGui.ui.toolBox.indexOf(self)
		iconUser = self.interfaceGui.ui.toolBox.itemIcon(boxIndex)
		iconLight = self.interfaceGui.ui.actionFocusRequest.icon()
		self.interfaceGui.ui.toolBox.setItemIcon(boxIndex, iconLight)
		QtCore.QTimer.singleShot(1000, lambda: self.interfaceGui.ui.toolBox.setItemIcon(boxIndex, iconUser))
	
# 	def manageRemoteScreen(self,  registered):
# 		if not registered:
# 			self.userSlot.buttonRemoteDesktop.setChecked(False)
	def closeEvent(self, closeEvent):	
		print("close userBox")
		
#from jabber.py_jabber import pyjabber
if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	#a = pyjabber()
	
	#box = pyuserBox("marcello", a)
	#b = box.userSlot
	# box.show()
# 	c=QtGui.QToolBox()
# 	c.addItem(b, "uyyu")
# 	c.show()
	sys.exit(app.exec_())		
