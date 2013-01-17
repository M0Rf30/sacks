#!/usr/bin/env python2 
#
# Sacks: a video conference-meeting system
# Copyright (C) 2009 Associazione Intellicom
#
# Authors: Marcello Di Guglielmo, Daniel Donato
#  info_AT_riunionidigitali.org

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
"""This main module of Sacks video conference-meeting system


The class is "pyriunioni", which is used to authenticate, create jabber comunication instance, receive messages and manage protocol commands from chair and from server, elaborate presence functions, activate chair role.

"""


# -*- coding: iso-8859-1 -*-
import sys
from PyQt4 import QtCore, QtGui, QtNetwork
from interface.py_mainWindow import pymainWindow
from jabber.py_jabber import pyjabber
from stream.py_stream import pystream
from stream.py_streamDialog import pystreamDialog
from py_userBox import pyuserBox
from jabber.Ui_xmppDialog import Ui_xmppDialog
# from py_elabCommand import pyelabCommand
from voip.py_voipInterface import pyvoipInterface
class pyriunioni(QtGui.QMainWindow):

	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		self.settings = QtCore.QSettings("Intellicom", "Sacks")
		self.media = {}
		streamDialog = pystreamDialog(self.settings)
		self.media["streamSession"] = pystream(streamDialog)
		self.media["voip"] = pyvoipInterface(self.settings, self)
		self.interfaceGui = pymainWindow(self.media)
		self.usersRoomList = {}
		
		self.clientParameters = {}
		self.clientParameters["urlServer"] = "riunionidigitali.net"
		self.clientParameters["jidServer"] = "server@riunionidigitali.net"
		self.clientParameters["jidMaxLenght"] = 30
		self.clientParameters["ipAddrServer"] = ""
		self.clientParameters["jidChair"] = ""
		self.clientParameters["portToken"] = None
		self.clientParameters["passwdCtrlRemoteScreen"] = ""
		self.clientParameters["passwdViewRemoteScreen"] = ""
		self.clientParameters["ipRemoteScreen"] = ""
		self.httpRequestCheckRiunioni = QtNetwork.QHttp()
		self.httpRequestCheckRiunioni.setHost(self.clientParameters["urlServer"])
		QtCore.QObject.connect(self.httpRequestCheckRiunioni, QtCore.SIGNAL("readyRead(const QHttpResponseHeader&)"), self.httpCheckRiunioniRead)

		licenceFile = QtCore.QFile("COPYING")
		if not licenceFile.open(QtCore.QIODevice.ReadOnly | QtCore.QIODevice.Text):	
			print "missing license"
			exit()
		self.licenseText = QtCore.QString(licenceFile.readAll())
		
		# lista degli slot Widget
		self.usersList = {}
		
		# lista con informazioni sugli eventuali stream da leggere
		self.readMediaList = {}		
		self.interfaceGui.show()
		QtCore.QObject.connect(self.interfaceGui.ui.actionConnection, QtCore.SIGNAL("toggled(bool)"), self.connJabber)
		QtCore.QObject.connect(self.interfaceGui.ui.actionNew, QtCore.SIGNAL("triggered()"), self.addRoomUser)
		QtCore.QObject.connect(self.interfaceGui.ui.actionDelete, QtCore.SIGNAL("triggered()"), self.delRoomUser)
		QtCore.QObject.connect(self.interfaceGui.ui.actionAbout, QtCore.SIGNAL("triggered()"), self.showAbout)
		QtCore.QObject.connect(self.interfaceGui.ui.actionFocusRequest, QtCore.SIGNAL("triggered()"), self.focusRequestUser)
		QtCore.QObject.connect(self.interfaceGui.ui.actionExit, QtCore.SIGNAL("triggered()"), self.close)
		QtCore.QObject.connect(self.interfaceGui, QtCore.SIGNAL("msgOut"), self.sendJabberRoom)

# definizione jabber con le sue connessioni
		self.jabberUser = pyjabber(self)
		# self.elabCommand=pyelabCommand(self.jabberUser, self.usersList, self.usersRoomList)
		QtCore.QObject.connect(self.jabberUser, QtCore.SIGNAL("jabberMessage"), self.menageIncomingJabberMsg)
		QtCore.QObject.connect(self.jabberUser, QtCore.SIGNAL("fileIncomingRequest"), self.menageJabberFileIncomingRequest)
		QtCore.QObject.connect(self.jabberUser, QtCore.SIGNAL("presence"), self.elaboratePresence)
		QtCore.QObject.connect(self.jabberUser, QtCore.SIGNAL("subscriptionRequest"), self.userRoomSubscriptionRequest)
		QtCore.QObject.connect(self.jabberUser, QtCore.SIGNAL("connection"), self.connection)
		QtCore.QObject.connect(self.jabberUser, QtCore.SIGNAL("userInterface"), self.userInterface)
		# lista degli utenti aggiunti nella stanza del chair, e mi informa se son presenti o no in quella stanza
		
		self.connectedChair = False
		self.udpSendReq = QtNetwork.QUdpSocket()
		self.chairModeStatus = False
		self.focusStatus = False
		self.remoteDesktopStatus = False
		

	def connJabber(self, connection):
		print "def connJabber(self,  connection):"
		if connection:
			self.xmppDialog = QtGui.QDialog()
			self.xmppDialog.ui = Ui_xmppDialog()
			self.xmppDialog.ui.setupUi(self.xmppDialog)
			self.xmppDialog.show()
			self.xmppDialog.setWindowModality(QtCore.Qt.NonModal)
			settingsUser = self.settings.value("jabber/user", QtCore.QVariant(""))
			self.xmppDialog.ui.lineEditUser.setText(settingsUser.toString())
			QtCore.QObject.connect(self.xmppDialog.ui.buttonBox, QtCore.SIGNAL("accepted()"), self.xmppStart)
			QtCore.QObject.connect(self.xmppDialog.ui.buttonBox, QtCore.SIGNAL("rejected()"), self.interfaceGui.ui.actionConnection, QtCore.SLOT("toggle()"))

		else: 	
			self.xmppDialog.close()
			if self.jabberUser:
				if self.jabberUser.connected > 0:
					self.chairMode(False)
					self.jabberUser.xmppDisconnect()
				print "disconnect"
				self.interfaceGui.ui.lineEditRoomMsg.clear()
				self.interfaceGui.ui.lineEditRoomMsg.setEnabled(False)
				for userJid, userBox in self.usersList.iteritems():
					if self.usersRoomList.has_key(userJid) and userJid != self.userJid:
						userBox.presenceServer(False)
					else:	
						userBox.close()
						self.interfaceGui.delWindow(userBox)
					
				self.interfaceGui.boxActivatedNumber = -1	
				# icona per lo stato di on che ora diventa creating
				self.interfaceGui.ui.actionConnection.setIcon(self.interfaceGui.iconDisconnected)
				sysTrayToolTipMsg = QtCore.QString(self.tr("Sacks - Disconnected"))
				self.interfaceGui.sysTrayIcon.setToolTip(sysTrayToolTipMsg)
				self.interfaceGui.ui.labelLinkToServer.setPixmap(QtGui.QPixmap(""))	
				self.clientParameters["jidChair"] = ""

	def xmppStart(self):		
		self.clientParameters["user"] = str(self.xmppDialog.ui.lineEditUser.text())
		self.clientParameters["jidUser"] = self.clientParameters["user"] + "@" + self.clientParameters["urlServer"]
		self.userJid = self.clientParameters["jidUser"]
		self.settings.setValue("jabber/user", QtCore.QVariant(self.clientParameters["user"]))
		print "User: ", str(self.xmppDialog.ui.lineEditUser.text())
		self.clientParameters["passwdUser"] = str(self.xmppDialog.ui.lineEditPassword.text())
		userJidParams = {}
		userJidParams["jid"] = self.clientParameters["jidUser"]
		userJidParams["password"] = str(QtCore.QCryptographicHash.hash(self.clientParameters["passwdUser"], QtCore.QCryptographicHash.Md5).toHex())
		print "jabber md5 password: ", userJidParams["password"]
		self.jabberUser.auth(userJidParams)
		self.interfaceGui.setWindowTitle(self.clientParameters["jidUser"])

	def connection(self, connected):
		print "parent" + str(self.parent())
		print "connected: " + str(connected)
		if connected == 1:
			# icona per lo stato di on che ora diventa connesso
			self.interfaceGui.ui.actionConnection.setIcon(self.interfaceGui.iconConnected)
			sysTrayToolTipMsg = QtCore.QString(self.tr("Sacks - Connected: %1")).arg(self.userJid)
			self.interfaceGui.sysTrayIcon.setToolTip(sysTrayToolTipMsg)
			self.interfaceGui.ui.lineEditRoomMsg.setEnabled(True)
			self.interfaceGui.setCurrentDock(self.interfaceGui.ui.dockWidgetUser)
			self.localUserBox = pyuserBox(self.userJid, self.clientParameters["jidServer"], self.jabberUser, self.interfaceGui)
			self.usersList[self.userJid] = self.localUserBox
			self.interfaceGui.newWindow(self.localUserBox)
			self.localUserBox.info["onGuiShow"] = True
			self.localUserBox.presence(True)
			self.localUserBox.userSlot.lineEditSendMsg.hide()
			self.localUserBox.userSlot.listWidgetReceiveMsg.hide()
			
		elif connected == -1 or connected == -2:
			self.interfaceGui.ui.actionConnection.setChecked(False)
			

	def sendJabberRoom(self, msg):
		if self.clientParameters["jidChair"]:
			msgToRoom = "/msgToRoom " + msg
			self.localUserBox.sendMsg(msgToRoom, True, self.clientParameters["jidChair"])
			
		
	def menageIncomingJabberMsg(self, msgJid, msgType, msgIncoming):
		print "Incoming Msg from: " + msgJid + " : " + msgIncoming			
		jidMsgReceived = QtCore.QString(msgJid)
		msgReceived = QtCore.QString(unicode(msgIncoming))
		if self.chairModeStatus:			
			if jidMsgReceived != self.clientParameters["jidServer"]:
				typeCommand = msgReceived.left(1)
				if msgIncoming:
					if typeCommand == "C":
						msgCommand = msgReceived.mid(1)
						self.elaborateCommandForChair(msgJid, msgCommand)

		if jidMsgReceived and msgIncoming:			
			typeCommand = msgReceived.left(1)
			if jidMsgReceived == self.clientParameters["jidChair"]:			
				if typeCommand == "C":
					msgCommand = msgReceived.mid(1)
					self.elabCommandFromChair(jidMsgReceived, msgCommand)
				else:
					self.elaborateMsgForUser(jidMsgReceived, msgReceived)
			elif jidMsgReceived == self.clientParameters["jidServer"]:
				msgReceived = QtCore.QString(unicode(msgIncoming))
				if msgIncoming:
					if typeCommand == "S":
						msgCommand = msgReceived.mid(1)
						self.elabCommandFromServer(jidMsgReceived, msgCommand)
			else:
				if typeCommand != "C":					
					self.elaborateMsgForUser(jidMsgReceived, msgReceived)
				
	def elaborateMsgForUser(self, jidMsgIncoming, msgIncoming):
		print "command for user"
		jidMsgIncomingName = jidMsgIncoming.left(jidMsgIncoming.indexOf("@"))
		msgReceived = QtCore.QString(unicode(msgIncoming))
		stringMsgShow = jidMsgIncomingName + ": " + msgReceived
		if self.usersList.has_key(str(jidMsgIncoming)):
			userBox = self.usersList[str(jidMsgIncoming)]
			if msgIncoming:
				userBox.showMsg(stringMsgShow, True)
		else:
			if msgIncoming:			
				self.interfaceGui.showMsg(msgReceived)
					
	def menageJabberFileIncomingRequest(self, fromJid , fileName, fileDim):
		msgAcceptRequest = QtCore.QString("<p>" + fromJid + " want to send you the file</p>"
		"<p>'" + fileName + "' of dim " + fileDim + " byte.</p>"
		"<p>Do you want to accept?</p>")
		reply = QtGui.QMessageBox.question(self, "Question", msgAcceptRequest, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)		
		if reply == QtGui.QMessageBox.Yes:
			acceptedFile = True
			self.jabberUser.acceptFile(acceptedFile, fromJid, fileName, fileDim)
		elif reply == QtGui.QMessageBox.No:
			acceptedFile = False
			self.jabberUser.acceptFile(acceptedFile, fromJid, fileName, fileDim)


	def elaboratePresence(self, jid, jidInfo, jidStatusInfo):
		print "jidPresence: " + jid + " jidInfo: " + jidInfo
		print self.usersList
		print "***********"
		print self.usersRoomList
		if jid:
			if jidInfo == "available":				
				if  self.usersList.has_key(jid):
					userBox = self.usersList[jid]					
				elif self.usersRoomList.has_key(jid):
					userBox = self.usersRoomList[jid]
					self.usersList[jid] = userBox
				else:
					userBox = pyuserBox(jid, self.clientParameters["jidServer"], self.jabberUser, self.interfaceGui)
					self.usersList[jid] = userBox
				userBox.presence(True)
				if self.chairModeStatus:
					if self.usersRoomList.has_key(jid):						
						if jid != self.clientParameters["jidChair"]:				
							userBox = self.usersRoomList[jid]
							userBox.presenceServer(True)
							print "userBox.presence in elaboratePresence"
				else: 
									
					self.interfaceGui.newWindow(userBox)
					userBox.info["onGuiShow"] = True
				
				self.readMedia(jid)
				
			
			elif 	jidInfo == "unavailable":
				# caso chair Mode: l'utente non e' piu' presente, viene solo segnalato come assente
				if self.chairModeStatus:
					if self.usersRoomList.has_key(jid):
						if jid != self.clientParameters["jidChair"]:
							userBox = self.usersRoomList[jid]
							userBox.presenceServer(False)

				else:	
				# caso uuse normale: l'utente viene tolto dalla lista degli user e levato dalla mostra nel toolbox	
					if self.usersList.has_key(jid):
						userBox = self.usersList[jid]
						userSlot = userBox.userSlot
						self.interfaceGui.delWindow(userBox)
						self.interfaceGui.boxActivatedNumber = -1
						userBox.info["onGuiShow"] = False
						userBox.presence(False)
						userSlot.close()
						del self.usersList[jid]
						if jid == self.clientParameters["jidChair"]:
							self.connectedChair = False
							self.interfaceGui.ui.labelLinkToServer.setPixmap(QtGui.QPixmap(""))
							for userBox in self.usersList.iteritems():
								userSlot = userBox.userSlot
								userSlot.ui.labelonGuiShow.setPixmap(QtGui.QPixmap(""))
								userBox.info["roomPresence"] = False


	def sendFileJid(self, destJid, filename):
		if self.jabberUser.connected == 1:
			self.jabberUser.sendFile(destJid, filename)
			
	def userInterface(self, destJid, item, value):
		userBox = self.usersList[destJid]
		userSlot = userBox.userSlot
		userSlot.updateInterface(item, value)
		
	def elabCommandFromChair(self, jid, msg):
		print "command from chair"
# self.clientParameters["jidChair"] e' sicuramente stato attivato altrimenti qui' nn vi arriva		
		msgCommand = QtCore.QString(unicode(msg))
		commandList = msgCommand.split(" ")
		command = commandList.first()
		parametersList = commandList.mid(1)

		if jid == self.clientParameters["jidChair"] and command == "/addRoomUser":
			roomUser = str(parametersList.first())
			if not self.usersList.has_key(roomUser):
				if roomUser != self.clientParameters["jidUser"]:
					userBox = pyuserBox(roomUser, self.clientParameters["jidServer"], self.jabberUser, self.interfaceGui)
					self.usersList[roomUser] = userBox
					self.jabberUser.subscriptionRequestSend(roomUser)
					print "subscriptionRequestSend: " + roomUser
			else:
				userBox = self.usersList[roomUser]
			userBox.presenceRoom(True)
		
		if jid == self.clientParameters["jidChair"] and command == "/userFocus":
			userFocusJid = str(parametersList.takeFirst())
			userFocusStatus = str(parametersList.takeFirst())
			if self.usersList.has_key(userFocusJid):
				userBox = self.usersList[userFocusJid]
				if userFocusStatus == "True":
					self.focusStatus = True
					userBox.userSlot.buttonOnFocus.setEnabled(True)
					userBox.userSlot.buttonOnFocus.setChecked(True)
					
				elif userFocusStatus == "False":
					self.focusStatus = False
					userBox.userSlot.buttonOnFocus.setChecked(False)
					userBox.userSlot.buttonOnFocus.setEnabled(False)
		
		if jid == self.clientParameters["jidChair"] and command == "/webLink":
			linkPage = str(parametersList.takeFirst())
			self.interfaceGui.webWidget.urlWeb.setText(linkPage)
			self.interfaceGui.webWidget.urlChanged()
			
			
		if jid == self.clientParameters["jidChair"] and command == "/remoteDesktop":
			jidRemoteDesktop = str(parametersList.takeFirst())
			remoteScreenStatus = str(parametersList.takeFirst())
			if self.usersList.has_key(jidRemoteDesktop):
				userBox = self.usersList[jidRemoteDesktop]
				if remoteScreenStatus == "True":
					self.remoteDesktopStatus = True
				elif 	remoteScreenStatus == "False":
					self.remoteDesktopStatus = False
			
				if self.remoteDesktopStatus:
					addressRemoteDesktop = str(parametersList.takeFirst())
					display = int(parametersList.takeFirst())
					passwd = str(parametersList.takeFirst())
					print "userbox.online: ", userBox.nameSlot, " online= ", userBox.online  
					userBox.setScreenParameters(addressRemoteDesktop, display, passwd)
					self.jidRemoteDesktop = jidRemoteDesktop
				else:
					userBox.setScreenParameters(None)
							
			
# devrebbe indicare quali sono i nuovi utenti
# anche se il mittente e' l'utente stesso in modo da tener aggiornata la lista
		if jid == self.clientParameters["jidChair"] and command == "/newRoomUser":
			roomUser = str(parametersList.first())
			if roomUser != self.clientParameters["jidUser"]:
				if not self.usersList.has_key(roomUser):	
					userBox = pyuserBox(roomUser, self.clientParameters["jidServer"], self.jabberUser, self.interfaceGui)
					self.usersList[roomUser] = userBox			
				else:
					userBox = self.usersList[roomUser]
				userBox.presenceRoom(True)
				
				
		if jid == self.clientParameters["jidChair"] and command == "/delRoomUser":
			roomUser = str(parametersList.first())
			if self.usersList.has_key(roomUser):
				userBox = self.usersList[roomUser]
				userBox.presenceRoom(False)
				
				
		if jid == self.clientParameters["jidChair"] and command == "/userRoomChecked":
			roomUser = str(parametersList.first())
			self.jabberUser.jidSubscribe(roomUser, True)
			print "userRoomChecked: " + roomUser
			
		if jid == self.clientParameters["jidChair"] and command == "/msgRoom":
			msgRoom = parametersList.join(" ")
			self.interfaceGui.showMsg(msgRoom)
			
	def elabCommandFromServer(self, jid, msg):		
		msgCommand = QtCore.QString(unicode(msg))
		commandList = msgCommand.split(" ")
		command = commandList.first()
		parametersList = commandList.mid(1)	
		print "command from server"
		
		if jid == self.clientParameters["jidServer"] and command == "/abilitateDesktopSession":
			self.clientParameters["passwdCtrlRemoteScreen"] = str(parametersList.takeFirst())
			self.clientParameters["passwdViewRemoteScreen"] = str(parametersList.takeFirst())
			self.clientParameters["ipRemoteScreen"] = str(parametersList.takeFirst())
			self.localUserBox.initializeRemoteDesktop(self.clientParameters["ipRemoteScreen"], self.clientParameters["passwdCtrlRemoteScreen"], self.clientParameters["passwdViewRemoteScreen"])
			
			for userBox in self.usersRoomList.iteritems():
				userBox.initializeRemoteDesktop(self.clientParameters["ipRemoteScreen"], self.clientParameters["passwdCtrlRemoteScreen"], self.clientParameters["passwdViewRemoteScreen"])
	
	
# messaggio del server di avvenuta  associazione alla riunione come da approvazione da parte del chair. L'approvazione del chair e' immediata.
# Viene fornito: lo stato, l'ip del server, il mediaId generato per questo utente, il jid del chair, la porta del token.
		if jid == self.clientParameters["jidServer"] and command == "/linkServer":
			linkStatus = str(parametersList.takeFirst())
			if linkStatus == "True":
				# prelievo dell'indirizzo del server
				self.clientParameters["ipAddrServer"] = str(parametersList.takeFirst())
				destDatagramAddress = QtNetwork.QHostAddress(self.clientParameters["ipAddrServer"])
				mediaId = str(parametersList.takeFirst())
				jidChair = str(parametersList.takeFirst())
				self.clientParameters["portToken"] = str(parametersList.takeFirst())
				print "Connection to server === jidChair:", jidChair, " addrServer: ", self.clientParameters["ipAddrServer"], " tokenPortServer: ", self.clientParameters["portToken"]
				self.connectedChair = True
				self.interfaceGui.ui.labelLinkToServer.setPixmap(QtGui.QPixmap(":/new/prefix2/images/actions/button_ok.png"))
		# 		controllo per evitare che' l'operazione venga ripetuta inutilmente piu' volte
				if jidChair != self.clientParameters["jidChair"]:
					self.clientParameters["jidChair"] = jidChair				
					self.jabberUser.subscriptionRequestSend(jidChair)
					if self.userJid == jidChair:
						self.chairMode(True)
					else:
						self.chairMode(False)
						if self.clientParameters["jidChair"]:
# messaggio che informa il chair che il campo self.clientParameters["jidChair"] e' stato settato
							msgChairSetupDone = "/setupChair " + str(True)
							self.localUserBox.sendMsg(msgChairSetupDone, True, self.clientParameters["jidChair"])	
		
					msgReq = "/mediaReq:" + mediaId
					datagramReq = QtCore.QByteArray(msgReq)
					print datagramReq
# invio del datagram su udp per informare farsi convalidare dal server					
					self.udpSendReq.writeDatagram(datagramReq, destDatagramAddress, 8080)
					print "labelLinkToServer On"
				
			elif linkStatus == "False":
				self.connectedChair = False	
				self.interfaceGui.ui.labelLinkToServer.setPixmap(QtGui.QPixmap(""))
	

		if jid == self.clientParameters["jidServer"] and command == "/activeMedia":
			mediaStatus = str(parametersList.takeFirst())
			
			if mediaStatus == "True":
				self.interfaceGui.ui.actionSendVideo.setEnabled(True)
				self.interfaceGui.ui.actionSendDesktop.setEnabled(True)
				
			elif mediaStatus == "False":
				self.interfaceGui.ui.actionSendVideo.setChecked(False)
				self.interfaceGui.ui.actionSendDesktop.setChecked(False)
				self.interfaceGui.ui.actionSendVideo.setEnabled(False)
				self.interfaceGui.ui.actionSendDesktop.setEnabled(False)



		if jid == self.clientParameters["jidServer"] and command == "/sendMedia":
			self.addressUdpMedia = str(parametersList.takeFirst())
			self.portUdpMedia = str(parametersList.takeFirst())
			streamDestination = self.addressUdpMedia + ":" + self.portUdpMedia
			self.interfaceGui.streamSessionInit(streamDestination)
			


		if jid == self.clientParameters["jidServer"] and command == "/readMedia":
			jidMedia = str(parametersList.takeFirst())
			addressMedia = str(parametersList.takeFirst())
			portMedia = str(parametersList.takeFirst())
			statusMedia = str(parametersList.takeFirst())
			infoMedia = (addressMedia, portMedia, statusMedia)
			self.readMediaList[jidMedia] = infoMedia
			self.readMedia(jidMedia)
			
	
	def readMedia(self, jidMedia):
				print "readMedia ", jidMedia	
				if self.usersList.has_key(jidMedia):
					userBox = self.usersList[jidMedia]
					userSlot = userBox.userSlot
					if userBox.info.has_key("onGuiShow"):
						if userBox.info["onGuiShow"]:
							if self.readMediaList.has_key(jidMedia):
								infoMedia = self.readMediaList[jidMedia]
								addressMedia = infoMedia[0]
								portMedia = infoMedia[1]
								statusMedia = infoMedia[2]
								if statusMedia == "play":					
									userSlot.ui.showMedia.setEnabled(True)
									userSlot.streamLink = "http://" + addressMedia + ":" + portMedia
									if jidMedia != self.userJid:	
										userSlot.ui.showMedia.setChecked(True)
								elif statusMedia == "stop":
									userSlot.ui.showMedia.click()
									userSlot.ui.showMedia.setChecked(False)
									userSlot.ui.showMedia.setEnabled(False)
					else:
						print "prematuro ReadMedia"
		
		
		
	def userRoomSubscriptionRequest(self, jid):
		if jid:
			print "subscriptionRequest from: " + jid 
			if jid == self.clientParameters["jidServer"]:
				print "subscriptionRequest from server"
				self.jabberUser.jidSubscribe(jid, True)		
				
			else:	
				msgCheckJid = "/checkUserRoom " + jid
				print "send to chair checkUserRoom of " + jid
				self.localUserBox.sendMsg(msgCheckJid, True, self.clientParameters["jidChair"])
			if self.chairModeStatus:
				if self.usersRoomList.has_key(jid):
					self.jabberUser.jidSubscribe(jid, True)
				
				
	def chairMode(self, status):
		self.chairModeStatus = status
		if self.chairModeStatus:
			for jidUser, userBox in self.usersList.iteritems():		
				if jidUser != self.userJid:
					print "deleteJidBeforeChair: " + jidUser
					self.interfaceGui.delWindow(userBox)
					self.interfaceGui.boxActivatedNumber = -1
					userBox.info["onGuiShow"] = False
					userBox.hide()
			# aggiunge alla room il chair stesso
			self.manageRoomUser(self.userJid, True)
			self.localUserBox.userSlot.pushButtonActiveMedia.setChecked(True)
			self.localUserBox.userSlot.pushButtonToken.setEnabled(True)
			self.interfaceGui.ui.actionNew.setEnabled(True)
			self.interfaceGui.ui.actionDelete.setEnabled(True)
			self.interfaceGui.webWidget.actionSpreadLink.setEnabled(True)
			msgActiveRemoteDesktop = "/activeRemoteDesktop True KM"
			self.localUserBox.sendMsg(msgActiveRemoteDesktop, True, self.clientParameters["jidServer"])			
			md5PasswdCheckRequest = str(QtCore.QCryptographicHash.hash(self.clientParameters["passwdUser"], 1).toHex())
			self.clientParameters["checkRiunioneRequest"] = "/sackstuff/index.py?userid=" + self.clientParameters["user"] + "&password=" + md5PasswdCheckRequest
			print "Request HTTP GET: ", self.clientParameters["checkRiunioneRequest"]
			self.httpRequestCheckRiunioni.get(self.clientParameters["checkRiunioneRequest"])
			
		else:
			if self.jabberUser.connected:
				self.localUserBox.roomMode(False)	
			self.interfaceGui.ui.actionNew.setEnabled(False)
			self.interfaceGui.ui.actionDelete.setEnabled(False)
			self.interfaceGui.webWidget.actionSpreadLink.setEnabled(False)
			for jidUser, userBox in self.usersRoomList.iteritems():
				print "delSlot in chairMode" + jidUser
				self.interfaceGui.delWindow(userBox)
				self.interfaceGui.boxActivatedNumber = -1
			self.usersRoomList = {}
			for jidUser, userBox in self.usersList.iteritems():		
				if jidUser != self.userJid:
					print "addJidAfterChair: " + jidUser
					self.interfaceGui.newWindow(userBox)
					userBox.info["onGuiShow"] = True
					userBox.show()
			

	def 	httpCheckRiunioniRead(self):
		partecipantsRiunione = QtCore.QString(self.httpRequestCheckRiunioni.readAll())
		listPartecipantsRiunione = partecipantsRiunione.split(",")
		print "read from http:", listPartecipantsRiunione
		for partecipant in listPartecipantsRiunione:
			if partecipant.length() < self.clientParameters["jidMaxLenght"] and not partecipant.contains(" "):
				userJid = str(partecipant + "@" + self.clientParameters["urlServer"])
				self.manageRoomUser(userJid, True)
				userBox = self.usersRoomList[userJid]			
				self.interfaceGui.newWindow(userBox)
				userBox.info["onGuiShow"] = True
				userBox.show()
				if self.clientParameters["ipRemoteScreen"] and self.clientParameters["passwdCtrlRemoteScreen"] and self.clientParameters["passwdViewRemoteScreen"]:
					userBox.initializeRemoteDesktop(self.clientParameters["ipRemoteScreen"], self.clientParameters["passwdCtrlRemoteScreen"], self.clientParameters["passwdViewRemoteScreen"])


	def addRoomUser(self):
		jid, ok = QtGui.QInputDialog.getText(self, self.tr("Input"), self.tr("Add User:"), QtGui.QLineEdit.Normal)	
		userJid = str(jid)		
		if ok and not jid.isEmpty():
			self.manageRoomUser(userJid, True)
			userBox = self.usersRoomList[userJid]
			userBox.initializeRemoteDesktop(self.clientParameters["ipRemoteScreen"], self.clientParameters["passwdCtrlRemoteScreen"], self.clientParameters["passwdViewRemoteScreen"])
			self.interfaceGui.newWindow(userBox)
			userBox.info["onGuiShow"] = True
			userBox.show()

	def delRoomUser(self):
		userBox = self.interfaceGui.ui.toolBox.currentWidget()
		if userBox:
			jidDelUser = userBox.nameSlot
			self.manageRoomUser(jidDelUser, False)
			self.interfaceGui.delWindow(userBox)
			userBox.info["onGuiShow"] = False

	def focusRequestUser(self):
		if self.jabberUser:
				if self.jabberUser.connected > 0:
					msgFocusRequest = "/focusRequest"
					self.localUserBox.sendMsg(msgFocusRequest, True, self.clientParameters["jidChair"])
		

	def manageRoomUser(self, userJid, presence):
		if presence:
			if not self.usersRoomList.has_key(userJid):
				if self.usersList.has_key(userJid):
					userBox = self.usersList[userJid]
				else:
					userBox = pyuserBox(userJid, self.clientParameters["jidServer"], self.jabberUser, self.interfaceGui)

				self.usersRoomList[userJid] = userBox
			else:
				userBox = self.usersRoomList[userJid]	
			userBox.roomMode(True)	
			
			if userJid != self.userJid:
				userBox.presenceServer(True)
		else:
			userBox = self.usersRoomList[userJid]
			userBox.presenceServer(False)
			userBox.roomMode(False)
			for userBox in self.usersRoomList.iteritems():
				if userBox.online:
					msgDelRoomUser = "/delRoomUser " + userJid
					userBox.sendMsg(msgDelRoomUser, True)
			
			
	def elaborateCommandForChair(self, jid, msg):
		msgCommand = QtCore.QString(unicode(msg))
		commandList = msgCommand.split(" ")
		command = commandList.first()
		parametersList = commandList.mid(1)
		print "command for Chair"
		
		if command == "/checkUserRoom":
			userCheckJid = str(parametersList.first())
			if self.usersRoomList.has_key(userCheckJid):
				userBox = self.usersRoomList[userCheckJid]
				print "userBox.online " + str(userBox.online)
				if userBox.online:
					msgAnswerCommand = "/userRoomChecked " + userCheckJid
					print "/userRoomChecked " + userCheckJid + " for Jid: " + jid
					self.localUserBox.sendMsg(msgAnswerCommand, True, jid)
		
		if command == "/setupChair":
			setupChairStatus = str(parametersList.first())
			if setupChairStatus == "True":
				if self.usersRoomList.has_key(jid):
					self.usersRoomCheck(jid)
					
		if command == "/msgToRoom":
			msgRoom = parametersList.join(" ")
			jidMsgReceived = QtCore.QString(jid)
			jidMsgReceivedName = jidMsgReceived.left(jidMsgReceived.indexOf("@"))
			stringMsgShow = "/msgRoom " + jidMsgReceivedName + ": " + msgRoom
			for userBox in self.usersRoomList.iteritems():
				userBox.sendMsg(stringMsgShow, True)
		
		if command == "/focusRequest":
			if self.usersRoomList.has_key(jid):
				userBox = self.usersRoomList[jid]
				userBox.focusRequest(True)
		
# da fare qualora e' sicuro che l'utente jid abbia settato la variabile self.clientParameters["jidChair"]
	def usersRoomCheck(self, jid):
# manda a tutti gli utenti l'avviso che si e' aggiunto alla Room l'utente jid
		for jidUserRoom, userBox in self.usersRoomList.iteritems():
# DA TESTARE EFFETT			
			if userBox.online:
				msgUserConnected = "/newRoomUser " + jid
				userBox.sendMsg(msgUserConnected, True)

# manda all'utente che si e' aggiunto la lista degli utenti attualmente in Room
		for jidUserRoom, userBox in self.usersRoomList.iteritems():
			print "jidCheck " + jidUserRoom + ": " + str(userBox.online)
			if (jidUserRoom != jid) and userBox.online:
				msgAddRoomUser = "/addRoomUser " + jidUserRoom
				self.localUserBox.sendMsg(msgAddRoomUser, True, jid)
			
	def showAbout(self):
		self.aboutBox = QtGui.QMessageBox()
		self.aboutBox.setFixedSize(800, 600)
		self.aboutBox.setText(self.tr("     Sacks, video conference-meeting system, version: 0.6.6        \n\nAuthors: Marcello Di Guglielmo, Daniel Donato           \n\nLicense: GNU public license\nShow details for license            "))
		self.aboutBox.setWindowTitle(self.tr("About Sacks"))
		self.aboutBox.setDetailedText (self.licenseText)
		self.aboutBox.exec_()
	def closeEvent(self, closeEvent):
		print "close"		
		

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	locale = QtCore.QLocale()
	country = locale.system().name()
	print locale
	qtTranslator = QtCore.QTranslator()
	if qtTranslator.load("qt_" + country, ":/"):
		app.installTranslator(qtTranslator)
	appTranslator = QtCore.QTranslator()	
	if appTranslator.load("sacks_" + country, ":/"):
		app.installTranslator(appTranslator)	
	riunione = pyriunioni()

	# riunione.show()
	sys.exit(app.exec_())
