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
"""This module provides media manager, based on Python binding of VideoLan project



The class is "pystream" that import the module "vlc" and set instances for multimedia operations,  it manage initialization and configurations stream parameters, and player functions.

"""

import sys
from PyQt4 import QtCore, QtGui

import vlc
# from py_streamDialog import pystreamDialog

class pystream(QtGui.QWidget):
	def __init__(self, streamDialog=None, parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.setMinimumSize(160, 120)
		self.statusPlayer = 0
		self.streamDialog = streamDialog
		self.playerInitialized = 0
		vlcVersionString = QtCore.QString(vlc.libvlc_get_version())
		vlcVersion, ok = vlcVersionString[0:3].toFloat()		
		if ok:
			self.vlcVersion = vlcVersion
		else:
			print "vlcVersion not recognized"
			exit()		
		print "vlcVersion: ", self.vlcVersion   
		if self.vlcVersion >= 1:
			if sys.platform == "win32":
				currentPath = QtCore.QDir.toNativeSeparators(QtCore.QDir.currentPath ())
				sessionPlugin = str(currentPath) + "\plugins"
				print "sessionPlugin", sessionPlugin
				self.vlcInstance = vlc.Instance(["--plugin-path", sessionPlugin])
			else:
				self.vlcInstance = vlc.Instance()
# 	def mediaHasVideoOut(self):				
# 		if self.statusPlayer:
# 			if self.mediaPlayer.has_vout():
# 				return True
# 			else:	
# 				
# 				return False

	def initialize(self, streamInfoDict):
		print streamInfoDict
		self.streamInfoDict = streamInfoDict
		# controlla se deve prelevare delle impostazioni dal dialog
		if self.streamDialog:
			dialogStreamParameters = self.streamDialog.returnParameters()
			print "dialogStreamParameters:  ........       ", dialogStreamParameters
		else:
			dialogStreamParameters = None
		if(streamInfoDict['streamContent']):
			parameters = []
			inputVideoDevice = ""
			inputAudioDevice = ""
			inputNum = ""
			audioSamplerate = ""
			if dialogStreamParameters:
				if dialogStreamParameters["inputNum"]:
					inputNum = "--v4l2-input=" + str(dialogStreamParameters["inputNum"])
				if dialogStreamParameters["devVideo"]:
					inputVideoDevice = str(dialogStreamParameters["devVideo"])
				if dialogStreamParameters["devAudio"]:
					inputAudioDevice = str(dialogStreamParameters["devAudio"])
				if dialogStreamParameters["audioSamplerate"]:
					audioSamplerate = str(1000 * dialogStreamParameters["audioSamplerate"])
			
			
			if streamInfoDict['streamContent'] == "acquisitionVideo":
				if sys.platform != 'win32':
					# cache="--v4l2-caching=500"
					# parameters.append(cache)	
					if inputNum:
						parameters.append(inputNum)
					if self.vlcVersion < 1:
						if inputAudioDevice:	
							parameters.append("--v4l2-adev=" + inputAudioDevice)	
	# metodo per l'acquiszione audio a partire alla versione 1.0						
					else:
						parameters.append("--input-slave=oss://" + inputAudioDevice)
					
					if audioSamplerate:		
						if self.vlcVersion < 1:
							parameters.append("--v4l2-samplerate=" + audioSamplerate)
						else:	
							parameters.append("--oss-samplerate=" + audioSamplerate)
			
			if streamInfoDict['streamContent'] == "acquisitionDesktop":
				screenParameters = "--screen-follow-mouse --screen-width=300 --screen-height=200 --screen-fps=5"
				parameters.extend(screenParameters.split())
				if self.vlcVersion >= 1:
						parameters.append("--input-slave=oss://" + inputAudioDevice)
			
			if(streamInfoDict.has_key('streamDestination')):
				if (streamInfoDict['streamDestination']):
					if  dialogStreamParameters:
						videoBitrate = "vb=" + str(dialogStreamParameters["videoBitrate"]) + ", "
						audioBitrate = "ab=" + str(dialogStreamParameters["audioBitrate"]) + ", "	
					else:
						videoBitrate = "vb=256, "
						audioBitrate = "ab=32, "
						
					sessionTranscode = "#transcode{vcodec=WMV2, " + videoBitrate + "width=320, height=240, acodec=mpga, " + audioBitrate + "channels=1}"
					
					sessionDuplicate = ":duplicate{dst=display,dst=std{access=udp,mux=ts,dst=" + streamInfoDict['streamDestination'] + "}}"

					
					parameters.append("--sout=" + sessionTranscode + sessionDuplicate)
				else:
					print "Parametro streaming destinatario mancante"
			else:
# anche per sola lettura di uno stream o di una qualunque cosa e' importante settare il duplicate perche' accade che lui invia a casaccio sui passati duplicate qualunque cosa legge di nuovo;
# pertanto faccio un duplicate che lo inizializza su una porta sicura 1233.
				if self.vlcVersion < 1:
					sessionDuplicate = "#duplicate{dst=display,dst=std{access=udp,mux=ts,dst=:1233}}"
					parameters.append("--sout")
					parameters.append(sessionDuplicate)
			

			print "parameters"
			print parameters
			
# 			self.playerVolume=50
# 			
			
				
			# operazione di cache utile in presenza di alcuni driver
		
			
			
			if(streamInfoDict['streamContent'] == "acquisitionVideo") :
				if sys.platform == 'win32':
					playUrl = ur"dshow:// :dshow-size=320x240"
				else:
					if dialogStreamParameters:
						video4linuxType = str(dialogStreamParameters["video4linuxType"]) + "://"
					else:
						video4linuxType = "v4l2://"
					playUrl = video4linuxType + inputVideoDevice + ":width=320:height=240"
			elif(streamInfoDict['streamContent'] == "acquisitionDesktop"):
				playUrl = ur"screen://"
			else:
				playUrl = streamInfoDict['streamContent']
			
			print "playUrl: ", playUrl
			# casting per supportare il formato in windows
			winId = int(self.winId())
			
			if self.vlcVersion < 1:
				self.player = vlc.MediaControl(parameters)
				self.mediaPlayer = self.player.get_media_player()
				print "####### playUrl: " + playUrl
				self.player.set_mrl(playUrl)
				self.player.set_visual(winId)
			else:
				self.media = self.vlcInstance.media_new(playUrl)
				self.player = self.media.player_new_from_media()
				if sys.platform == "win32":
					self.player.set_hwnd(winId)
				else:	
					self.player.set_xwindow(winId)
					
				for option in parameters:	
					self.media.add_option(option[2:])
					
			self.playerInitialized = 1	

		else:
			print "media to read not found"
			



	def start(self):
		print "inizializer"
		print self.playerInitialized
		if self.playerInitialized:
			if self.vlcVersion < 1:
				self.player.start(0)
			else:
				self.player.play()
			self.statusPlayer = 1
			self.playerInitialized = 0
		else:
			if self.streamInfoDict:
				self.initialize(self.streamInfoDict)
				if self.vlcVersion < 1:
					self.player.start(0)
				else:
					self.player.play()
				self.statusPlayer = 1
				self.playerInitialized = 0
			else:
				print "vlcStream not initialized"

	def stop(self):
		print "stop vlc"
		if self.statusPlayer:
			print "ciao"
# modificato per prova
			self.player.stop()
			print  "dopociao"
			self.statusPlayer = 0
			print "stop" + str(self.statusPlayer)

		
	def setVolume(self, vol):
		if self.playerInitialized:
			self.player.sound_set_volume(vol)
			self.playerVolume = vol
			msgVolumePlayer = "Volume: " + str(vol)
			if self.mediaPlayer.has_vout():
				self.player.display_text(msgVolumePlayer, 0, 1500)
			

	def setMute(self, statusMute):
		
		if self.playerInitialized:
			if statusMute:
				self.playerVolume = self.player.sound_get_volume()
				self.player.sound_set_volume(0)
				if self.mediaPlayer.has_vout():
					self.player.display_text("MuteOn", 0, 2000)
			else:
				print self.playerVolume
				self.playerVolume = self.player.sound_set_volume(self.playerVolume)
				if self.mediaPlayer.has_vout():
					self.player.display_text("MuteOff", 0, 2000)

	def closeEvent(self, closeEvent):
		
		self.stop()
# 			self.player.exit()
		self.emit(QtCore.SIGNAL('closeEmitApp()'))
# 			self.close()
		print "exit VLC"
		

		
	def startMedia(self):
		# self.initialize(streamInfoDict)
		self.start()
		# self.streamDialog.show()
		
if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	mainpymplayer = pystream()
	mainpymplayer.show()
# 	mainpymplayer.streamDialog.show()
	InfoDict = {}
	InfoDict2 = {}
#       streamInfoDict['streamDestination']="192.168.0.4:1223"
#       streamInfoDict['streamContent']="acquisitionVideo"
# 	InfoDict['streamContent']="sounds/Kopete_Received.ogg"
# 	mainpymplayer.initialize(InfoDict)
# 	mainpymplayer.startMedia()
# 	InfoDict['streamContent']="sounds/dialog-information.ogg"
# 	mainpymlayer2.show()
#       InfoDict['streamContent']=ur"http://82.211.18.118:1251"
# 	InfoDict['streamContent']=ur"http://192.168.0.4:8080"
# 	InfoDict['streamContent']=ur"acquisitionVideo"
# 	InfoDict['streamContent']=ur"/home/marcello/fant.mpg"
	InfoDict['streamContent'] = ur"acquisitionDesktop"
# 	InfoDict['streamDestination']="192.168.0.4:1234"
	# InfoDict['streamContent']=ur"acquisitionDesktop"
	mainpymplayer.initialize(InfoDict)
	mainpymplayer.startMedia()
	mainpymplayer2 = pystream()
	mainpymplayer2.show()
# 	InfoDict2['streamContent']=ur"/home/marcello/fant.mpg"
	InfoDict2['streamContent'] = ur"acquisitionVideo"
	InfoDict2['streamDestination'] = "192.168.0.4:1234"
	mainpymplayer2.initialize(InfoDict2)
	
	QtCore.QTimer.singleShot(11000, mainpymplayer2.startMedia)
# 	#streamInfoDict['streamContent']="http://192.168.0.3:1251"
	QtCore.QTimer.singleShot(15000, mainpymplayer.stop)
# 	#QtCore.QTimer.singleShot(17000, lambda:mainpymplayer.initialize(InfoDict))
	QtCore.QTimer.singleShot(19000, mainpymplayer.startMedia)
	sys.exit(app.exec_())




	
