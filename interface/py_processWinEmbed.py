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
from PyQt5 import QtCore, QtGui
from .Ui_processWinEmbed import Ui_ProcessWinEmbed

class pyprocessWinEmbed(QtGui.QWidget):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.ui = Ui_ProcessWinEmbed()
		self.ui.setupUi(self)
		self.widgetScreen = QtGui.QWidget(self)
		self.widgetScreen.setFixedSize(800, 600)
# 		self.containerScreen=QtGui.QX11EmbedContainer()
# 		self.containerScreen=QtGui.QX11EmbedContainer(self.widgetScreen)
# 		self.containerScreen.embedClient(77594642)
# 		self.containerScreen.setFixedSize(800, 600)
		self.commandProcessWin = ""
		self.winIdCatchProcessOutput = ""
		self.containerScreen = None
		# QtCore.QTimer.singleShot(10000, self.discardWinProcess)
		# self.a.show()
		# self.tabWidget.addTab(self.b, 'RemoteDesktop')
		self.ui.scrollAreaScreen.setWidget(self.widgetScreen)
		self.winIdCatchProcess = QtCore.QProcess()
		QtCore.QObject.connect(self.winIdCatchProcess, QtCore.SIGNAL("readyReadStandardOutput()"), self.manageWinIdCatchOutput)
		QtCore.QObject.connect(self.winIdCatchProcess, QtCore.SIGNAL("readyReadStandardError()"), self.manageWinIdCatchError)
		QtCore.QObject.connect(self.winIdCatchProcess, QtCore.SIGNAL("finished (int)"), self.winIdCatchFinish)
		self.winId = None
		self.catchProcess = None
		self.numCatch = 0
		self.maxNumCatch = 50
# 		self.show()
		
	def embedWinProcess(self, process):	
		if hasattr(process, "program"):
			self.catchProcess = process
			if hasattr(process, "args"):
				self.commandProcessWin = process.program + " " + process.args
			else:
				self.commandProcessWin = process.program
			# print "self.commandProcessWin " , self.commandProcessWin
			
			self.winIdCatchProcessOutput = ""
			self.winIdCatchProcess.start("xlsclients -al")
			
			
	def closeEvent(self, closeEvent):
		self.discardWinProcess()
	def discardWinProcess(self):
		if self.containerScreen:
			self.containerScreen.discardClient()
			self.containerScreen = None
			self.winId = None
			self.catchProcess = None
			self.numCatch = 0
		
	def manageWinIdCatchOutput(self):
		if not self.winId:
			winIdCatchProcessOutput = self.winIdCatchProcess.readAllStandardOutput()	
			# print "output: "+winIdCatchProcessOutput
			self.winIdCatchProcessOutput = self.winIdCatchProcessOutput + winIdCatchProcessOutput
			startWinIDPos = self.winIdCatchProcessOutput.indexOf(self.commandProcessWin)
			if startWinIDPos > 0:
				print("startWinIDPos", startWinIDPos)
				startWinIDPos = self.winIdCatchProcessOutput.lastIndexOf("Window", startWinIDPos)
				print("startWinIDPos", startWinIDPos)
				startWinIDPos = startWinIDPos + len("Window ")
				print("startWinIDPos", startWinIDPos)	
				endWinIDPos = self.winIdCatchProcessOutput.indexOf(":", startWinIDPos)
				if endWinIDPos > 0:
					self.winIdStrHex = self.winIdCatchProcessOutput.mid(startWinIDPos, endWinIDPos - startWinIDPos)
					# print "self.winId:", self.winId
					self.winId
					print("winIdInt:", self.winId)
# 		if winIdCatchProcessOutput.contains
					containerScreen = QtGui.QX11EmbedContainer(self.widgetScreen)
				# self.containerScreen.setParent(self.widgetScreen)
					containerScreen.embedClient(self.winId)
					containerScreen.setFixedSize(800, 600)
					containerScreen.show()
					self.containerScreen = containerScreen
				# 		self.show()
# 		
	def manageWinIdCatchError(self):
		winIdCatchProcessError = self.winIdCatchProcess.readAllStandardError()	
		print("error: " + winIdCatchProcessError)

	def winIdCatchFinish(self):
		if self.numCatch < self.maxNumCatch:
			if not self.winId:
				if self.catchProcess:
					QtCore.QTimer.singleShot(300, lambda:self.embedWinProcess(self.catchProcess))
					self.numCatch += 1
					print("self.numCatch:", self.numCatch)
		
		
if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	mainpymplayer = pyprocessWinEmbed()
	proc = QtCore.QProcess()
	
	
	proc.program = "vncviewer"
	proc.args = "localhost:0"
	procArgsList = proc.args.split(" ")
	proc.start(proc.program, procArgsList)
	proc.waitForStarted()
	mainpymplayer.embedWinProcess(proc)
	# QtCore.QTimer.singleShot(300, lambda: mainpymplayer.embedWinProcess(proc))
	# mainpymplayer.embedWinProcess(proc)
	
	mainpymplayer.show()
	sys.exit(app.exec_())



	
