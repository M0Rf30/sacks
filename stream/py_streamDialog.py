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
from PyQt5 import QtCore, QtGui, QtWidgets
from .Ui_streamWidget import Ui_streamWidget


class pystreamDialog(QtWidgets.QDialog):
	def __init__(self, settings, parent=None):
		QtWidgets.QDialog.__init__(self, parent)
		self.ui = Ui_streamWidget()
		self.ui.setupUi(self)
		self.okClicked = False
		self.settings = settings
		self.streamParameters = {}
		devVideo = self.settings.value("stream/devVideo", QtCore.QVariant(""))
		self.streamParameters["devVideo"] = str(devVideo)
		self.ui.lineEditDevVideo.setText(self.streamParameters["devVideo"])
# 		self.devVideo=""
		devAudio = self.settings.value("stream/devAudio", QtCore.QVariant(""))
		self.streamParameters["devAudio"] = str(devAudio)
		self.ui.lineEditDevAudio.setText(self.streamParameters["devAudio"])
# 		self.devAudio=""
		audioSamplerate = self.settings.value("stream/audioSamplerate", QtCore.QVariant(0))
		self.streamParameters["audioSamplerate"] = int(audioSamplerate)
	# 	self.audioSamplerate=""
		inputNum = settings.value("stream/inputNum", QtCore.QVariant(""))
		self.streamParameters["inputNum"] = str(inputNum)
		# self.inputNum=""
		
		varVideoBitrate = self.settings.value("stream/videoBitrate", QtCore.QVariant(256))
		videoBitrate = int(varVideoBitrate)
		self.streamParameters["videoBitrate"] = videoBitrate
		if videoBitrate != 256:
			self.ui.checkBoxVideoBitrate.setChecked(True)
		self.ui.spinBoxVideoBitrate.setValue(videoBitrate)	
		# self.videoBitrate=""
		varAudioBitrate = self.settings.value("stream/audioBitrate", QtCore.QVariant(32))
		audioBitrate = int(varAudioBitrate)
		self.streamParameters["audioBitrate"] = audioBitrate
		if audioBitrate != 32:
			self.ui.checkBoxAudioBitrate.setChecked(True)
		self.ui.spinBoxAudioBitrate.setValue(audioBitrate)	
		
	# 	self.audioBitrate=""
		video4linuxType = settings.value("stream/video4linuxType", QtCore.QVariant("v4l2"))
		self.streamParameters["video4linuxType"] = str(video4linuxType)
		# self.video4linuxType=""
		
		self.iconDialog = self.windowIcon()
		self.nameDialog = self.windowTitle()
		self.listWidgetItem = QtWidgets.QListWidgetItem()
		self.listWidgetItem.setIcon(self.iconDialog)
		self.listWidgetItem.setText(self.nameDialog)
		
		if sys.platform == 'win32':
			self.ui.groupBoxAcquisition.hide()
		

		# QtCore.QObject.connect(self.ui.buttonBox, QtCore.SIGNAL("clicked (QAbstractButton *)"), self.buttonClicked)
		# QtCore.QObject.connect(self.ui.checkBoxAudioSamplerate, QtCore.SIGNAL("toggled (bool)"), lambda: self.ui.spinBoxAudioSamplerate.setValue(0))
		# QtCore.QObject.connect(self.ui.checkBoxVideoBitrate, QtCore.SIGNAL("toggled (bool)"), lambda: self.ui.spinBoxVideoBitrate.setValue(256))
		# QtCore.QObject.connect(self.ui.checkBoxAudioBitrate, QtCore.SIGNAL("toggled (bool)"), lambda: self.ui.spinBoxAudioBitrate.setValue(32))

			
	def returnParameters(self):
		return self.streamParameters
	def buttonClicked(self, button):
		buttonClickedRole = self.ui.buttonBox.buttonRole(button)
		
		if buttonClickedRole == QtGui.QDialogButtonBox.ResetRole:
			self.ui.comboBoxV4l.setCurrentIndex(0)
			self.ui.lineEditDevVideo.clear()
			self.ui.lineEditDevAudio.clear()
			self.ui.comboBoxInputNum.setCurrentIndex(0)			
			self.ui.spinBoxAudioSamplerate.setValue(0)
			self.ui.checkBoxAudioSamplerate.setChecked(False)
			self.ui.spinBoxVideoBitrate.setValue(256)
			self.ui.checkBoxVideoBitrate.setChecked(False)
			self.ui.spinBoxAudioBitrate.setValue(32)
			self.ui.checkBoxAudioBitrate.setChecked(False)

		elif buttonClickedRole == QtGui.QDialogButtonBox.AcceptRole:
			v4lType = self.ui.comboBoxV4l.currentText()
			if v4lType == "v4l2":
				self.streamParameters["video4linuxType"] = "v4l2"
			elif v4lType == "v4l":
				self.streamParameters["video4linuxType"] = "v4l"
					
			inputNum = self.ui.comboBoxInputNum.currentText()
			self.streamParameters["inputNum"] = inputNum
				
			
			if self.ui.checkBoxAudioSamplerate.isChecked():
				audioSamplerate = self.ui.spinBoxAudioSamplerate.value()				
				self.streamParameters["audioSamplerate"] = audioSamplerate
				if not audioSamplerate:
					QtGui.QMessageBox.warning(self, self.tr("Alert"), self.tr("Audio samplerate is not a valid value"))
					self.ui.checkBoxAudioSamplerate.setChecked(False)
			else:
				self.streamParameters["audioSamplerate"] = 0
				
			pathDevVideo = self.ui.lineEditDevVideo.text()
			if pathDevVideo:
				if QtCore.QFile.exists (pathDevVideo):
					self.streamParameters["devVideo"] = pathDevVideo
				else:
					QtGui.QMessageBox.warning(self, self.tr("Alert"), self.tr("Video device file not exist"))
					self.ui.lineEditDevVideo.clear()
					self.streamParameters["devVideo"] = ""
			else:
				self.streamParameters["devVideo"] = ""
				
			pathDevAudio = self.ui.lineEditDevAudio.text()
			if pathDevAudio:
				if QtCore.QFile.exists (pathDevAudio):
					self.streamParameters["devAudio"] = pathDevAudio
				else:
					QtGui.QMessageBox.warning(self, self.tr("Alert"), self.tr("Audio device file not exist"))
					self.ui.lineEditDevAudio.clear()
					self.streamParameters["devAudio"] = ""
			else:
				self.streamParameters["devAudio"] = ""
	
			videoBitrate = self.ui.spinBoxVideoBitrate.value()
			if self.ui.checkBoxVideoBitrate.isChecked():
				self.streamParameters["videoBitrate"] = videoBitrate
				if not videoBitrate:
					QtGui.QMessageBox.warning(self, self.tr("Alert"), self.tr("Video bitrate is not a valid value"))
					self.ui.checkBoxVideoBitrate.setChecked(False)
			else:
				self.streamParameters["videoBitrate"] = 256

			audioBitrate = self.ui.spinBoxAudioBitrate.value()
			if self.ui.checkBoxAudioBitrate.isChecked():
				self.streamParameters["audioBitrate"] = audioBitrate
				if not audioBitrate:
					QtGui.QMessageBox.warning(self, self.tr("Alert"), self.tr("Audio bitrate is not a valid value"))
					self.ui.checkBoxAudioBitrate.setChecked(False)
			else:
				self.streamParameters["audioBitrate"] = 32


			self.settings.setValue("stream/devVideo", QtCore.QVariant(self.streamParameters["devVideo"]))
			self.settings.setValue("stream/devAudio", QtCore.QVariant(self.streamParameters["devAudio"]))
			self.settings.setValue("stream/audioSamplerate", QtCore.QVariant(self.streamParameters["audioSamplerate"]))
			self.settings.setValue("stream/inputNum", QtCore.QVariant(self.streamParameters["inputNum"]))
			self.settings.setValue("stream/videoBitrate", QtCore.QVariant(self.streamParameters["videoBitrate"]))
			self.settings.setValue("stream/audioBitrate", QtCore.QVariant(self.streamParameters["audioBitrate"]))
			self.settings.setValue("stream/video4linuxType", QtCore.QVariant(self.streamParameters["video4linuxType"]))
			print("devVideo: " + self.streamParameters["devVideo"])
			print("devAudio: " + self.streamParameters["devAudio"])
			print("audioSamplerate: " + str(self.streamParameters["audioSamplerate"]))
			print("inputNum: " + self.streamParameters["inputNum"])
			print("videoBitrate: " + str(self.streamParameters["videoBitrate"]))
			print("audioBitrate: " + str(self.streamParameters["audioBitrate"]))
			print("v4l type: " + str(self.streamParameters["video4linuxType"]))

# 	def showEvent(self, showEvent):
# 		if self.streamParameters["video4linuxType"]:
# 			indexComboBoxV4l=self.ui.comboBoxV4l.findText(self.streamParameters["video4linuxType"])
# 			self.ui.comboBoxV4l.setCurrentIndex(indexComboBoxV4l)
# 		else:
# 			self.ui.comboBoxV4l.setCurrentIndex(0)
# 		
# 		if self.streamParameters["audioSamplerate"]:
# 			self.ui.checkBoxAudioSamplerate.setChecked(True)
# 			self.ui.spinBoxAudioSamplerate.setValue(self.streamParameters["audioSamplerate"])
# 		else:
# 			self.ui.checkBoxAudioSamplerate.setChecked(False)
# 			
# 		if self.streamParameters["devVideo"]:
# 			self.ui.lineEditDevVideo.setText(self.streamParameters["devVideo"])
# 		else:
# 			self.ui.lineEditDevVideo.clear()
# 			
# 		if self.streamParameters["devAudio"]:
# 			self.ui.lineEditDevAudio.setText(self.streamParameters["devAudio"])
# 		else:
# 			self.ui.lineEditDevAudio.clear()
# 		
# 		if self.streamParameters["inputNum"]:
# 			indexComboBoxInputNum=self.ui.comboBoxInputNum.findText(self.streamParameters["inputNum"])
# 			self.ui.comboBoxInputNum.setCurrentIndex(indexComboBoxInputNum)
# 		else:
# 			self.ui.comboBoxInputNum.setCurrentIndex(0)
#
# 		if self.streamParameters["audioBitrate"]:
# 			self.ui.checkBoxAudioBitrate.setChecked(True)
# 			self.ui.spinBoxAudioBitrate.setValue(self.streamParameters["audioBitrate"])
# 		else:
# 			self.ui.checkBoxAudioBitrate.setChecked(False)
#
# 		if self.streamParameters["videoBitrate"]:
# 			self.ui.checkBoxVideoBitrate.setChecked(True)
# 			self.ui.spinBoxVideoBitrate.setValue(self.streamParameters["videoBitrate"])
# 		else:
# 			self.ui.checkBoxVideoBitrate.setChecked(False)
# 		

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	settings = QtCore.QSettings("Intellicom", "Prove")
	mainpymplayer = pystreamDialog(settings)
	
	mainpymplayer.show()
	
	
	
	sys.exit(app.exec_())
