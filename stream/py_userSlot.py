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

"""This module provides media-slot manager and interactions for a session joined user



The class is "pyuserSlot" that import a gui interface that represent status information and manage chat messages of session joined user and run relatives media functions through the module py_stream. 

"""
#!/usr/bin/python
import sys
from PyQt4 import QtCore, QtGui
from Ui_user import Ui_User
# sys.path.append('stream')
from py_stream import pystream
# 	QWidget al posto di QMainWindow
class pyuserSlot(QtGui.QWidget):
	def __init__(self, nameSlot, parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.ui = Ui_User()
		self.ui.setupUi(self)
		self.nameSlot = nameSlot
		self.setWindowTitle(nameSlot)
		self.labelOnline = self.ui.labelOnline
		self.pushButtonActiveMedia = self.ui.pushButtonActiveMedia
		self.pushButtonToken = self.ui.pushButtonToken
		self.pushButtonShowMedia = self.ui.showMedia
		self.pushButtonVoipCall = self.ui.pushButtonVoipCall
		self.pushButtonRemoteDesktopControl = self.ui.pushButtonRemoteDesktopControl
		self.buttonRemoteDesktop = self.ui.buttonRemoteDesktop
		self.buttonOnFocus = self.ui.buttonOnFocus
		self.listWidgetReceiveMsg = self.ui.listWidgetReceiveMsg
		self.lineEditSendMsg = self.ui.lineEditSendMsg
		self.iconUser = QtGui.QIcon()		
		self.iconUser.addPixmap(QtGui.QPixmap(":/stream/interface/images/actions/user.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

		self.iconEdit = QtGui.QIcon()
		self.iconEdit.addPixmap(QtGui.QPixmap(":/stream/interface/images/actions/edit_user.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		
		self.iconUserDisabled = QtGui.QIcon()		
		self.iconUserDisabled.addPixmap(QtGui.QPixmap(":/stream/interface/images/actions/user_disabled.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

		self.iconUserEnabled = QtGui.QIcon()		
		self.iconUserEnabled.addPixmap(QtGui.QPixmap(":/stream/interface/images/actions/user.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

		self.iconActiveOff = QtGui.QIcon()
		self.iconActiveOff.addPixmap(QtGui.QPixmap(":/stream/interface/images/actions/kimproxyoffline.png"))
		
		self.iconActiveOn = QtGui.QIcon()
		self.iconActiveOn.addPixmap(QtGui.QPixmap(":/stream/interface/images/actions/kimproxyonline.png"))
		
		self.pixmapConnetedOn = QtGui.QPixmap(":/stream/interface/images/actions/connect_established.png")
		self.pixmapConnetedOff = QtGui.QPixmap(":/stream/interface/images/actions/connect_no.png")
		self.pixmapInRoom = QtGui.QPixmap(":/stream/interface/images/actions/button_ok.png")
		self.pixmapOutRoom = QtGui.QPixmap("")
		# self.pushButtonActiveMedia.setIcon(self.iconActiveOff)
		
		
		
		self.setWindowIcon(self.iconUser)
		self.interfaceDict = {}
		self.interfaceDict["percentage"] = 0
		
		imageUser = QtGui.QImage()
		imageUser.load(ur'c:\print.png')

		
		self.streamLink = 0
		
		print r'c:\print.png'
	# 	self.ui.imageUserLabel.setPixmap(QtGui.QPixmap.fromImage(imageUser))
		
		self.mdiWin = pystream()
		self.sliderVol = self.ui.sliderVolume
		self.muteFlag = self.ui.muteFlag
		
		QtCore.QObject.connect(self.ui.sliderVolume, QtCore.SIGNAL("valueChanged(int)"), self.setVolume)
		QtCore.QObject.connect(self.ui.muteFlag, QtCore.SIGNAL("clicked(bool)"), self.mdiWin.setMute)
		QtCore.QObject.connect(self.mdiWin, QtCore.SIGNAL("closeEmitApp()"), self.mdiWinFinished)
		QtCore.QObject.connect(self.ui.showMedia, QtCore.SIGNAL("toggled (bool)"), self.showMedia)
		QtCore.QObject.connect(self.ui.lineEditSendMsg, QtCore.SIGNAL("returnPressed ()"), self.sendMsg)
		# QtCore.QObject.connect(self.ui.pushButtonSendFile, QtCore.SIGNAL("clicked ()"), self.sendFile)
		QtCore.QObject.connect(self.ui.listWidgetReceiveMsg, QtCore.SIGNAL("itemChanged (QListWidgetItem *)"), self.setRightMsgItem)
	def setVolume(self, volumeValue):
		print 'Volume'	
		print volumeValue

		self.mdiWin.setVolume(volumeValue)
		self.ui.muteFlag.setChecked(False)
		
	
	def mdiWinFinished(self):
		print "mdiFinished"
		self.ui.showMedia.setChecked(False)
		


	def showMedia(self, activeMedia):
		streamInfoDict = {}
		print activeMedia
		if activeMedia:
# 			self.buttonOnFocus.setEnabled(True)
			if self.streamLink:
				if sys.platform == 'win32':
				# self.mdiWin.streamInfoDict['streamContent']=ur"c:\\fant.mpg"
					streamInfoDict['streamContent'] = self.streamLink
				else:
				# self.mdiWin.streamInfoDict['streamContent']=ur"/home/marcello/fant.mpg"
				
					streamInfoDict['streamContent'] = self.streamLink

# 			self.mdiWin.streamInfoDict['streamContent']=ur"acquisitionVideo"
# 			self.mdiWin.show()
				self.mdiWin.initialize(streamInfoDict)
				self.mdiWin.start()
				self.mdiWin.show()
# 			self.mdiWin.start(ur"c:\\fant.mpg")
# qui' punto critico
		else:
# 			self.buttonOnFocus.setEnabled(False)
			self.mdiWin.close()
			print self.mdiWin

	def sendMsg(self):
		msg = self.ui.lineEditSendMsg.text()
		self.ui.lineEditSendMsg.clear()
		msgShow = "me: " + msg
		self.listShow(msgShow)
		self.emit(QtCore.SIGNAL('sendMsg'), msg)
		
	def sendFile(self):
		homePath = QtCore.QDir.home().absolutePath()
		fileName = QtGui.QFileDialog.getOpenFileName(self, "Open File", homePath, ("All files (*)"))
		if not fileName.isEmpty():
			filename = QtCore.QFile(fileName)
			self.emit(QtCore.SIGNAL('sendFile'), self.nameSlot, filename)
		else:
			print "file non selezionato"
	def listShow(self, msg):
		itemListWidget = QtGui.QListWidgetItem(msg)
		itemListWidget.msgText = msg
		itemListWidget.setFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)
		
		self.ui.listWidgetReceiveMsg.addItem(itemListWidget)
		self.ui.listWidgetReceiveMsg.scrollToBottom() 
	def setRightMsgItem(self, itemListWidget):
		itemListWidget.setText(itemListWidget.msgText)
		
	def updateInterface(self, item, value):
		update = False
		if self.interfaceDict.has_key(item):
			if self.interfaceDict[item] != value:
				self.interfaceDict[item] = value
				update = True
				
		else:
			self.interfaceDict[item] = value
			update = True
			
		if update:
			if item == "percentage":
				self.ui.progressBar.setValue(value)
				
			
	def closeEvent(self, closeEvent):
		self.mdiWin.close()
		print "closeEvent Userslot", closeEvent
		self.ui.buttonRemoteDesktop.setChecked(False)
		
if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	mainpymplayer = pyuserSlot("marcello")
	mainpymplayer.ui.showMedia.setEnabled(True)
	mainpymplayer.streamLink = "http://82.211.18.118:1251"
	mainpymplayer.show()
	
	
	
	sys.exit(app.exec_())
