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
"""This module provides voip support, based on Python binding of Pjsip project  

You can find documentation on Pjsip at http://www.pjsip.org/.

Basically, the most important class is "pyvoip", which is used to
create a voip instance. From this instance, you can then register an account, make a call, manage incoming call, receive information on status events.
"""


from PyQt5 import QtCore
import sys
import pjsua as pj



class voipAccountCallback(pj.AccountCallback, QtCore.QObject):
	def __init__(self, account=None, parent=None):
		pj.AccountCallback.__init__(self, account)
# 		self.currentCall=currentCall
		QtCore.QObject.__init__(self, parent)

	def on_incoming_call(self, call):
		print("call ", call)
		callCallBack = voipCallCallback(call)
		call.set_callback(callCallBack)
		call.callCallBack = callCallBack		
		self.emit(QtCore.SIGNAL('incomingCall'), call)
		# callCallBack=voipCallCallback(call)
		
class voipCallCallback(pj.CallCallback, QtCore.QObject):
	def __init__(self, call=None, parent=None):
		pj.CallCallback.__init__(self, call)
		QtCore.QObject.__init__(self, parent)
		print("call :", call)
		print("self.call", self.call)
		self.call = call
		self.callInfo = {}
	# Notification when call state has changed
	def on_state(self):
		currentCallInfo = self.call.info()
		self.callInfo["infoState"] = currentCallInfo.state_text
		self.callInfo["lastCode"] = currentCallInfo.last_code
		self.callInfo["lastReason"] = currentCallInfo.last_reason
		# print "self.currentCall ", self.currentCall
		self.callInfo["urlCall"] = QtCore.QString(currentCallInfo.remote_uri).remove("<").remove("sip:").remove(">")
# 		print "Call with", self.call.info().remote_uri,
# 		print "is", self.call.info().state_text,
# 		print "last code =", self.call.info().last_code, 
# 		print "(" + self.call.info().last_reason + ")"
		self.emit(QtCore.SIGNAL('stateCallChanged()'))
	# Notification when call's media state has changed.
	def on_media_state(self):
		callInfo = self.call.info()
		if callInfo.media_state == pj.MediaState.ACTIVE:
			# Connect the call to sound device
			callSlot = callInfo.conf_slot
			pj.Lib.instance().conf_connect(callSlot, 0)
			pj.Lib.instance().conf_connect(0, callSlot)
			print("Media is now active")
		else:
			print("Media is inactive")

class pyvoip(QtCore.QObject):
	def __init__(self, stunServer="", parent=None):
		QtCore.QObject.__init__(self, parent)
		LOG_LEVEL = 3
		self.hostVoipProvider = ""
		self.voipAccountLogin = ""
		self.voipAccountPasswd = ""
		self.voipStunServer = stunServer
		print("self.voipStunServer", self.voipStunServer)
		self.registered = False
		self.accountVoip = None
		self.currentCall = None
		self.libVoip = pj.Lib()
		self.transportVoip = None
		try:
			if self.voipStunServer:
				userAgentCfg = pj.UAConfig()
				userAgentCfg.stun_host = self.voipStunServer
				# userAgentCfg.stun_host = "stun.voip.eutelia.it"
				# mediaCfg = pj.MediaConfig()
			# mediaCfg.enable_ice = True
				self.libVoip.init(ua_cfg=userAgentCfg, log_cfg=pj.LogConfig(level=LOG_LEVEL, callback=self.logCallBack))
			else:	
				self.libVoip.init(log_cfg=pj.LogConfig(level=LOG_LEVEL, callback=self.logCallBack))
# 			self.libVoip.init( log_cfg = pj.LogConfig(level=LOG_LEVEL,  callback=self.logCallBack))
		# lib.init(ua_cfg=my_ua_cfg, media_cfg=my_media_cfg)
		except pj.Error as err:
			print('Initialization error:', err)

		print("create_transport")
		try:
			self.transportVoip = self.libVoip.create_transport(pj.TransportType.UDP, pj.TransportConfig(5060))
			self.libVoip.start()
			print("\nListening on", self.transportVoip.info().host, end=' ')
			print("port", self.transportVoip.info().port, "\n")
			currentPath = QtCore.QDir.currentPath()
			if sys.platform == "win32":
				ringTonePath = str(currentPath) + "/tools/sounds/phone_incoming_call.wav"    
			else:
				ringTonePath = str(currentPath) + "/tools/sounds/phone_incoming_call.wav"
				print("ringTonePath ", ringTonePath)
			wavId = self.libVoip.create_player(ringTonePath, True)
			print("wav player id ", wavId)
			self.ringSlot = self.libVoip.player_get_slot(wavId)
			print("playerSlot ", self.ringSlot)
		
		except:
			print("Address Voip already in use")
		
		
	def registerVoip(self, hostVoipProvider, voipAccountLogin, voipAccountPasswd):
		print("register: " , hostVoipProvider, " ", voipAccountLogin, " ", voipAccountPasswd)
		if self.transportVoip:
			if not self.registered:
				self.hostVoipProvider = str(hostVoipProvider)
				self.voipAccountLogin = str(voipAccountLogin)
				self.voipAccountPasswd = str(voipAccountPasswd)
				accountParameters = pj.AccountConfig(self.hostVoipProvider, self.voipAccountLogin, self.voipAccountPasswd)
# forse va all'init
				accountCallBack = voipAccountCallback()
				QtCore.QObject.connect(accountCallBack, QtCore.SIGNAL("incomingCall"), self.manageIncomingCall)
				self.accountVoip = self.libVoip.create_account(accountParameters, cb=accountCallBack)
				self.accountVoip.accountCallBack = accountCallBack
			
	
	def unregisterVoip(self):
		if self.accountVoip:
			self.accountVoip.delete()
		self.accountVoip = None
		self.registered = False

	def manageIncomingCall(self, call):
		print("Incoming call from ", call.info().remote_uri)
		if self.currentCall:
			call.answer(486, "Busy")
			return
		# self.currentCall=call
		#
		# QtCore.QTimer.singleShot(10000, self.answer)		
		QtCore.QObject.connect(call.callCallBack, QtCore.SIGNAL("stateCallChanged()"), self.manageStatusChanged)
		self.currentCall = call
		# da il segnale di "ring"
		self.currentCall.answer(180)
# 		self.currentCall.answer(200)
	
	def manageStatusChanged(self):	
		self.currentCallInfo = self.currentCall.callCallBack.callInfo
		infoState = self.currentCall.callCallBack.callInfo["infoState"]
		lastCode = self.currentCall.callCallBack.callInfo["lastCode"]
		lastReason = self.currentCall.callCallBack.callInfo["lastReason"]
		urlCall = self.currentCall.callCallBack.callInfo["urlCall"]
# 		infoState=self.currentCallInfo.state_text
# 		lastCode=self.currentCallInfo.last_code
# 		lastReason=self.currentCallInfo.last_reason
# 		#print "self.currentCall ", self.currentCall
# 		urlCall=QtCore.QString(self.currentCallInfo.remote_uri).remove("<").remove("sip:").remove(">")
		print("infoState ", infoState, "lastCode ", lastCode, "lastReason ", lastReason) 
		if infoState == "DISCONNCTD":
			self.libVoip.conf_disconnect(self.ringSlot, 0)	
			# QtCore.QObject.disconnect(self.currentCall.callCallBack, QtCore.SIGNAL("stateCallChanged"), self.manageStatusChanged)
			self.emit(QtCore.SIGNAL('callDisconnected'), urlCall)
			self.currentCall = None
		if infoState == "CONFIRMED":
			self.libVoip.conf_disconnect(self.ringSlot, 0)
			self.emit(QtCore.SIGNAL('callConfirmed'), urlCall)	
		if infoState == "EARLY" and lastCode == 180:
			self.emit(QtCore.SIGNAL('callRequest'), urlCall)
			self.libVoip.conf_connect(self.ringSlot, 0)
		print("manageStatusChanged")
		
		
	def makeCall(self, voipUrl):
		if not self.currentCall:
			if self.registered:
				try:
					print("Making call to", voipUrl)
					# self.currentCall=self.accountVoip.make_call(voipUrl, cb=MyCallCallback())
					callCallBack = voipCallCallback()
					call = self.accountVoip.make_call(voipUrl, callCallBack)
					call.callCallBack = callCallBack
					QtCore.QObject.connect(call.callCallBack, QtCore.SIGNAL("stateCallChanged()"), self.manageStatusChanged)
					self.currentCall = call
				except pj.Error as e:
					print("Exception: " + str(e))
			else:
				print("voip non registrato")
		else: 
			print("Already have another call")
		return self.currentCall

	def closeSession(self):
		self.transport = None
		if self.registered:
			self.accountVoip.delete()
			self.accountVoip = None
		if self.libVoip:
			self.libVoip.destroy()
			self.libVoip = None

	def hangupCall(self):
		if self.currentCall:
			self.currentCall.hangup()
			# QtCore.QObject.disconnect(self.currentCall.callCallBack, QtCore.SIGNAL("stateCallChanged"), self.manageStatusChanged)
			# self.currentCall=None
		else:
			print("There is no call!")
			
	def answer(self):
		if self.currentCall:
			self.currentCall.answer(200)
			
			
	def logCallBack(self, level, string, lenght):
		print("log_cb:", str, end=' ')
		logVoip = QtCore.QString(str)
		if logVoip.contains("registration success"):
			self.emit(QtCore.SIGNAL("voipRegistrated(bool)"), True)
			self.registered = True
		elif logVoip.contains("Network is unreachable"):
			self.emit(QtCore.SIGNAL("voipRegistrated(bool)"), False)
		elif logVoip.contains("Unregistration sent"):
			self.emit(QtCore.SIGNAL("voipRegistrated(bool)"), False)
			self.registered = False
			


if __name__ == '__main__':
	app = QtCore.QCoreApplication(sys.argv)

	voip = pyvoip()
	sys.exit(app.exec_())
