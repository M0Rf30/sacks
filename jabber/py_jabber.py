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
"""This module provides jabber XMPP-client support, based on Xmppy Python library.

You can find documentation on Xmppy at http://xmpppy.sourceforge.net/ .

The class is "pyjaber", which is used to create a connection to a xmpp server. It realize authentication,  manage sending and incoming messages, organize subscribing request. 

"""


# -*- coding: iso-8859-1 -*-
import sys
import xmpp
# import md5
from PyQt4 import QtCore

class pyjabber(QtCore.QObject):
	
	def __init__(self, parent=None):
		QtCore.QObject.__init__(self, parent)		
		self.connected = 0
		self.listPresence = {}
		self.xmpp = None
# 		self.show()
	def auth(self, connJidParams):
		self.xmpp = pyjabberCore(connJidParams, self)
		QtCore.QObject.connect(self.xmpp, QtCore.SIGNAL("xmpp"), self.xmppSlot)
		self.xmpp.startThread()
		self.jid = connJidParams["jid"]
	def xmppDisconnect(self):
		self.listPresence = {}
		if self.xmpp:
			self.xmpp.xmppDisconnect()		
			xmpp = self.xmpp
			del self.xmpp
	
	def sendMessage(self, destJid, message):
		self.xmpp.sendMessage(destJid, message)
	
	def jidSubscribe(self, jid, value):
		if value:
			self.xmpp.xmppJidSubscribe(jid)
		else:
			self.xmpp.xmppJidUnsubscribe(jid)
			
	def subscriptionRequestSend(self, jid, confirmed=True):		
		self.xmpp.subscriptionRequestSend(jid, confirmed)
			
			
			
	def xmppSlot(self, connectiontype, event):
		self.event = event
		if connectiontype == "connection":
			self.connected = self.event["connection"]		
			self.emit(QtCore.SIGNAL('connection'), self.connected)
			
# 			self.subscriptionRequestSend("laura@intellicom.eushells.net")
		if connectiontype == "jabberMessage":
			receiveFromJid = self.event["jidFrom"]
			receiveType = self.event["typeFrom"]
			msgIncoming = self.event["msgReceive"]
			self.emit(QtCore.SIGNAL('jabberMessage'), receiveFromJid, receiveType, msgIncoming)
		if connectiontype == "presence":
			jid = self.event["jidPresence"]
			jidInfo = self.event["jidInfoPresence"]		
			jidStatusInfo = self.event["jidStatusInfoPresence"]
			self.listPresence[jid] = self.event["userPresence"]
			self.emit(QtCore.SIGNAL("presence"), jid, jidInfo, jidStatusInfo)
		if connectiontype == "subscriptionRequest":
			jid = self.event["subscriptionRequest"]
			self.emit(QtCore.SIGNAL("subscriptionRequest"), jid)
			

class pyjabberCore(QtCore.QThread):
	
	def __init__(self, connJidParams, parent=None):
		QtCore.QThread.__init__(self, parent)
		self.connJidParams = connJidParams
		self.connected = 0
		self.connectionXmpp = 0
		self.userListPresence = {}
		self.transferListFile = {}
		self.acceptedFile = {}
	def startThread(self):
		self.start()
	def run(self):	
		self.connJid = xmpp.protocol.JID(self.connJidParams['jid'])
		self.clientXmpp = xmpp.Client(self.connJid.getDomain(), debug=[])
		self.xmppConnect()
		if self.connected == 1:
			while 1:
				print "elaborate"
				self.clientXmpp.Process(1)	
				
				
	def xmppConnect(self):
		# per una connessione in ssl inserire come parametro di connect: 
		#  server=(self.connJid.getDomain(), 5223)
		# assicurarsi che il server abbia supporto ssl
		self.connectionXmpp = self.clientXmpp.connect()
		if not self.connectionXmpp:
			sys.stderr.write('could not connect!\n')
			self.connected = -2
			event = {}
			event["connection"] = self.connected
			self.emit(QtCore.SIGNAL('xmpp'), "connection", event)
			return False
		sys.stderr.write('connected with %s\n' % self.connectionXmpp)
		# print "********************************"
		# print "********************************"
		# print self.connJid.getNode()
		# print self.connJidParams['password']
		# print self.connJidParams
		# print self.connJid.getResource()
		# print "********************************"
		# print "********************************"
# 		self.authXmpp=self.clientXmpp.auth(self.connJid.getNode(),self.connJidParams['password'],resource=self.connJid.getResource())
		# md5JidPasswd=str(QtCore.QCryptographicHash.hash(self.connJidParams['password'],QtCore.QCryptographicHash.Md5).toHex())
		self.authXmpp = self.clientXmpp.auth(self.connJid.getNode(), self.connJidParams['password'], resource=self.connJid.getResource())  # self.authXmpp=self.clientXmpp.auth(self.connJid.getNode(),md5.new().hexdigest(),resource=self.connJid.getResource())
		if not self.authXmpp:
			sys.stderr.write('could not authenticate!\n')
			self.connected = -1
			event = {}
			event["connection"] = self.connected
			self.emit(QtCore.SIGNAL('xmpp'), "connection", event)
			# self.emit(QtCore.SIGNAL('connection'), self.connected)
			return False
		sys.stderr.write('authenticated using %s\n' % self.authXmpp)
		self.clientXmpp.RegisterHandler('message', self.xmpp_message)
		self.clientXmpp.RegisterHandler("presence", self.presence)
		self.clientXmpp.RegisterHandler("presence", self.subscriptionRequestReceive, typ="subscribe")
		
		self.clientXmpp.sendInitPresence(requestRoster=1)
		self.connected = 1
		event = {}
		event["connection"] = self.connected
		self.emit(QtCore.SIGNAL('xmpp'), "connection", event)
# 		self.xmppJidSubscribe("john@intellicom.eushells.net")
# 		QtCore.QObject.connect(self, QtCore.SIGNAL("subscriptionRequest"), self.xmppJidSubscribe)
# 		QtCore.QObject.connect(self, QtCore.SIGNAL("fileIncomingRequest"), self.acceptFile)
# 		self.subscriptionRequestSend("john@intellicom.eushells.net")
# 		file=QtCore.QFile("jabber.e4p")
# 		self.sendFile("john@intellicom.eushells.net", file)

	def xmppDisconnect(self):
		self.terminate()
		print "self.connected: " + str(self.connected)
		if self.connected == 1:
			self.clientXmpp.disconnect()
			clientXmpp = self.clientXmpp
			del clientXmpp
		self.quit()
# 		self.exit()
		self.connected = 0
		# self.emit(QtCore.SIGNAL('connection'), self.connected)
		event = {}
		event["connection"] = self.connected
		self.emit(QtCore.SIGNAL('xmpp'), "connection", event)
		
	def sendMessage(self, destJid, message):
		if self.connected == 1:
			messXmpp = xmpp.protocol.Message(to=destJid, body=message, typ='chat')
			self.clientXmpp.send(messXmpp)
			pass
		
# 	def sendFile(self, destJid,  file):	
# 		#inserire procedura di sicurezza, numero casuale md5
# 		self.transferListFile[destJid]=file
# 		fileInfo=QtCore.QFileInfo(file)
# 		fileName=str(fileInfo.fileName ())
# 		fileDim=str(file.size())
# 		msgRequestSendFile="<command>/requestSendFile "+fileName+" "+fileDim
# 		self.sendMessage(destJid, msgRequestSendFile)
	
		
		
	def xmpp_message(self, con, event):
		receiveType = event.getType()
		receiveFromJid = event.getFrom().getStripped()
		msgIncoming = event.getBody()		
		event = {}
		if msgIncoming:
			if msgIncoming[0:9] == "<command>":
				msgCommand = msgIncoming[9 :]
				self.elaborateCommand(receiveFromJid, msgCommand)
			else:	
				event["jidFrom"] = receiveFromJid
				event["typeFrom"] = receiveType
				event["msgReceive"] = msgIncoming
				self.emit(QtCore.SIGNAL('xmpp'), "jabberMessage", event)
				
		else:
			event["jidFrom"] = receiveFromJid
			event["typeFrom"] = receiveType
			event["msgReceive"] = msgIncoming
			self.emit(QtCore.SIGNAL('xmpp'), "jabberMessage", event)
			# self.emit(QtCore.SIGNAL('jabberMessage'), receiveFromJid, receiveType, msgIncoming)		
		
		# if receiveType in ['message', 'chat', None] :
			

	def presence(self, con, presence):
		
		jid = presence.getFrom().getStripped()
		jidTypeInfo = presence.getType()
		jidShowInfo = presence.getShow()
		jidStatusInfo = presence.getStatus()
		event = {}
		if  jidTypeInfo == "unavailable":
			jidInfo = jidTypeInfo
			self.userListPresence[jid] = 0
			event["jidPresence"] = jid
			event["jidInfoPresence"] = jidInfo
			event["jidStatusInfoPresence"] = jidStatusInfo
			event["userPresence"] = False			
			self.emit(QtCore.SIGNAL('xmpp'), "presence", event)
			# self.emit(QtCore.SIGNAL("presence"), jid, jidInfo, jidStatusInfo)
		if not jidTypeInfo:
# quando c'e' None in presence.getType() significa che e' disponibile			
			if not presence.getShow():
				jidInfo = "available"
			# vari casi di stato (occupato, non disponibile, ecc)	
				if self.userListPresence.has_key(jid):
					if not self.userListPresence[jid]:
						self.userListPresence[jid] = 1
						event["jidPresence"] = jid
						event["jidInfoPresence"] = jidInfo
						event["jidStatusInfoPresence"] = jidStatusInfo
						event["userPresence"] = True
						self.emit(QtCore.SIGNAL('xmpp'), "presence", event)
						
						
				else:
					self.userListPresence[jid] = 1
					event["jidPresence"] = jid
					event["jidInfoPresence"] = jidInfo
					event["jidStatusInfoPresence"] = jidStatusInfo
					event["userPresence"] = True
					self.emit(QtCore.SIGNAL('xmpp'), "presence", event)
					# self.emit(QtCore.SIGNAL("presence"), jid, jidInfo, jidStatusInfo)
					
# caso in cui l'utente e' occupato					
			else:
				jidInfo = jidShowInfo
				self.userListPresence[jid] = 1
				event["jidPresence"] = jid
				event["jidInfoPresence"] = jidInfo
				event["jidStatusInfoPresence"] = jidStatusInfo
				event["userPresence"] = True
				self.emit(QtCore.SIGNAL('xmpp'), "presence", event)

				# self.emit(QtCore.SIGNAL("presence"), jid, jidInfo, jidStatusInfo)

		
		
	def subscriptionRequestReceive(self, con, presence):	
		print "con: " + str(con)
		print "presence: " + str(presence)
		event = {}
		jid = presence.getFrom().getStripped()
		event["subscriptionRequest"] = jid
		self.emit(QtCore.SIGNAL('xmpp'), "subscriptionRequest", event)
# 		if jid=="laura@intellicom.eushells.net":
# 			self.xmppJidSubscribe(jid)
		
		if self.userListPresence.has_key(jid) and self.userListPresence[jid] == -1:
			self.xmppJidSubscribe(jid)
			self.userListPresence[jid] = 1
		



	def xmppJidSubscribe(self, jid):
		reply = xmpp.protocol.Presence(to=jid, typ="subscribed")

		self.clientXmpp.send(reply)
		presence = xmpp.protocol.Presence(to=str(jid), typ="subscribe")
		self.clientXmpp.send(presence)

		
	def xmppJidUnsubscribe(self, jid):
		reply = xmpp.protocol.Presence(to=jid, typ="unsubscribed")

		self.clientXmpp.send(reply)




	def subscriptionRequestSend(self, jid, confirmed):
		result = xmpp.protocol.Iq(typ='set')
		result.setQueryNS(xmpp.NS_ROSTER)

		item = xmpp.simplexml.Node(tag="item", attrs={"jid": jid})
#        item.addChild(name="group", payload=self.group.currentText())
		result.T.query.addChild(node=item)
		self.clientXmpp.send(result)
		
		presence = xmpp.protocol.Presence(to=str(jid), typ="subscribe")
		self.clientXmpp.send(presence)
#
# 		reply = xmpp.protocol.Presence(to=str(jid),  typ="subscribed")
# 		self.clientXmpp.send(reply)
		
		self.xmppJidSubscribe(str(jid))
		if confirmed:
			self.userListPresence[str(jid)] = -1
		else:	
			self.userListPresence[str(jid)] = 0




# 	def elaborteCommand(self, fromJid, msg):
# 		msgCommand=QtCore.QString(unicode(msg))
# 		commandList=msgCommand.split(" ")
# 		command=commandList.first()
# 		parametersList=commandList.mid(1)
# 		print "jabber command from "+ fromJid + " " + msgCommand
# # lato sender		
# 		if command=="/requestSendFile":
# 			fileName=parametersList.takeFirst()
# 			fileDim=parametersList.takeFirst()
# 			self.emit(QtCore.SIGNAL("fileIncomingRequest"), fromJid, fileName, fileDim)
# 		if command=="/fileTransferFromJid":
# 			fileName=parametersList.takeFirst()
# 			fileDim=parametersList.takeFirst()
# 			if self.acceptedFile.has_key(fromJid):
# 				fileIncoming=self.acceptedFile[fromJid]
# 				if fileIncoming.checkName==fileName and fileIncoming.checkDim==fileDim:
# 					trunkIndex=parametersList.takeFirst()
# 					numberOfTrunks=parametersList.takeFirst()
# 					trunkString=parametersList.takeFirst()
# 					trunk=trunkString.toAscii()
# 					fileIncoming.byteArrayBase64.append(trunk)
# 					
# 					if trunkIndex==numberOfTrunks:
# 						fileByteArrayBase64=fileIncoming.byteArrayBase64
# 						fileByteArray=QtCore.QByteArray.fromBase64 (fileByteArrayBase64)
# 						fileIncoming.open(QtCore.QIODevice.WriteOnly)
# 						fileIncoming.write(fileByteArray)
# 						fileIncoming.close()
# 						del self.acceptedFile[fromJid]
# 				else:
# 					print "check file incoming errato"
# 			else:
# 				print "file non atteso"
# #lato receiver		
# 		if command=="/acceptFile":
# 			destJid=fromJid
# 			fileName=parametersList.takeFirst()
# 			fileDim=parametersList.takeFirst()
# 			self.transferFile(destJid, fileName,  fileDim)
# 		if command=="/refusedFile":
# 			fileName=parametersList.takeFirst()
# 			msgRefusedFile="The file "+ fileName+ " has been refused by " + fromJid
# 			print msgRefusedFile
		
# 	def acceptFile(self, acceptedFile, acceptJid, fileName, fileDim):
# 		if acceptedFile:
# 			msgAcceptFile="<command>/acceptFile "+fileName+" "+fileDim
# 			fileAccepted=QtCore.QFile()
# 			fileAccepted.setFileName(fileName)
# 			fileAccepted.checkName=fileName
# 			fileAccepted.checkDim=fileDim
# 			fileAccepted.byteArrayBase64=QtCore.QByteArray()		
# 			self.acceptedFile[acceptJid]=fileAccepted		
# 			self.sendMessage(acceptJid,msgAcceptFile)
# 		else:
# 			print "file rifiutato"
# 			msgRefusedFile="<command>/refusedFile "+fileName
# 			self.sendMessage(acceptJid,msgRefusedFile)
#
# 	def transferFile(self, destJid, fileNameCheck,  fileDimCheck):
# 		print destJid
# 		file=self.transferListFile[destJid]
# 		fileInfo=QtCore.QFileInfo(file)
# 		
# 		fileName=str(fileInfo.fileName ())
# 		fileDim=str(file.size())
# 		if fileName==fileNameCheck and fileDim==fileDimCheck:
# 			print "check file -->"+ file.fileName() + "OK"
# 			if not (file.open(QtCore.QIODevice.ReadOnly)):
# 				print "Error opening File"
# 			else:
# 				print "FileOpen"
# 				fileByteArray=file.readAll()
# 				fileByteArrayBase64=fileByteArray.toBase64()
# 				fileByteArrayBase64Size=fileByteArrayBase64.size()
# 				
# 				trunkLenght=3000
# 				numberOfTrunks=(fileByteArrayBase64Size/trunkLenght)+1
# 				trunkIndex=0
# 				while fileByteArrayBase64:
# 					trunkIndex+=1
# 					trunk=fileByteArrayBase64.left(trunkLenght)
# 					fileByteArrayBase64.remove(0, trunkLenght)
# 					msgFileTransfer="<command>/fileTransferFromJid "+fileName+" "+fileDim+" "+str(trunkIndex) +" " +str(numberOfTrunks)+" "+trunk
# 					percentage=int((float(trunkIndex)/float(numberOfTrunks))*100)
# 					self.emit(QtCore.SIGNAL('userInterface'),destJid, "percentage", percentage)
# 					self.sendMessage(destJid,msgFileTransfer)
# 				
# 											
# 				del self.transferListFile[destJid]
# 		else:
# 			print "Error sending File"	
# 			
			
			
if __name__ == "__main__":
	app = QtCore.QCoreApplication(sys.argv)
	mittJidParams = {}
	mittJidParams["jid"] = "john@intellicom.eushells.net"
	mittJidParams["password"] = "123456"
	
	jab = pyjabber()	
	jab.auth(mittJidParams)
	
	sys.exit(app.exec_())
		

