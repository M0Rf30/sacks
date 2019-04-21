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


# -*- coding: iso-8859-1 -*-
import sys
from .web.web import webWidget
# from .vnc.py_vncInterface import pyvncInterface
from PyQt5 import QtCore, QtGui, QtWidgets
from .Ui_mainwindow import Ui_MainWindow
from .py_dialogsContainer import pydialogsContainer

class pymainWindow(QtWidgets.QMainWindow):
	def __init__(self, media, parent=None):
		QtWidgets.QMainWindow.__init__(self, parent)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		# self.tabifyDockWidget(self.ui.dockWidgetUser, self.ui.dockWidgetRoom)
		self.tabifyDockWidget(self.ui.dockWidgetUser, self.ui.dockWidgetVoip)
		self.tabifyDockWidget(self.ui.dockWidgetVoip, self.ui.dockWidgetRoom)
		# self.voipInterface = media["voip"]
		# self.ui.dockWidgetVoip.resize(self.ui.dockWidgetVoip.height(), 200)
		# self.voipInterface.setParent(self.ui.widgetVoip)
		# self.ui.layoutVoip.addWidget(self.voipInterface)
		# self.ui.dockWidgetUser.show()
		self.mdi = QtWidgets.QMdiArea()
		#self.addToolBar(self.voipInterface.ui.toolBar)
		#self.ui.menuBar.addMenu(self.voipInterface.ui.menuVoip)
		#self.voipInterface.ui.menuBar.setVisible(False)
		self.webWidget = webWidget(self)
		self.addToolBar(self.webWidget.toolBar)
		self.webWidget.toolBar.setVisible(False)
		self.ui.menuBar.addMenu(self.webWidget.menuWeb)
		self.webWidget.menuBar.setVisible(False)
		self.deleteMdiWin = 1				
		self.tabWidget = QtWidgets.QTabWidget()
		self.setCentralWidget(self.tabWidget)
# 		self.tabWidget.addTab(self.mdi, 'VideoSlots')
# 		self.tabWidget.addTab(self.webWidget, 'Web')
		# self.remoteDesktopWinEmbed=pyprocessWinEmbed()
		# self.remoteDesktopInterface = pyvncInterface()
		# self.addToolBar(self.remoteDesktopInterface.toolBar)
		# self.remoteDesktopInterface.toolBar.setVisible(False)
		# self.ui.menuBar.addMenu(self.remoteDesktopInterface.menuRemoteScreen)
		# self.remoteDesktopInterface.menuBar.setVisible(False)
		# jid che detiente attualmente il remote desktop
		

		self.tabWidget.addTab(self.mdi, 'VideoSlots')
		self.tabWidget.addTab(self.webWidget, 'Web')
		# self.tabWidget.addTab(self.remoteDesktopInterface, 'RemoteScreen')
		# self.streamSession = media["streamSession"]
		# self.streamSession.numWin = -1
		# self.mdi.addWindow(self.streamSession)
		# self.streamSession.hide()
		# Definizione del dialog container di configurazioni
		self.configContainer = pydialogsContainer(self)
		self.configContainer.addDialog(self.streamSession.streamDialog)
		self.configContainer.addDialog(self.voipInterface.voipDialog)
		QtCore.QObject.connect(self.configContainer.closeButton, QtCore.SIGNAL("clicked()"), lambda:self.ui.actionConfigure.setChecked(False))
		QtCore.QObject.connect(self.voipInterface, QtCore.SIGNAL("configureRequest()"), lambda:self.configContainer.setCurrentDialog(self.voipInterface.voipDialog))
		QtCore.QObject.connect(self.voipInterface, QtCore.SIGNAL("configureRequest()"), self.configContainer.show)
# 		self.show()
		self.numPlayer = 0
		self.boxActivatedNumber = -1
		self.boxActivatedUser = None
		# QtCore.QObject.connect(self.ui.actionNew, QtCore.SIGNAL("triggered()"), self.newWindow)
		QtCore.QObject.connect(self.ui.actionTile, QtCore.SIGNAL("triggered()"), self.tile)
		QtCore.QObject.connect(self.ui.actionCascade, QtCore.SIGNAL("triggered()"), self.mdi, QtCore.SLOT("cascade()"))
# 		QtCore.QObject.connect(self.ui.actionDelete, QtCore.SIGNAL("triggered()"), self.mdi, QtCore.SLOT("closeActiveWindow()"))
		QtCore.QObject.connect(self.ui.actionSendVideo, QtCore.SIGNAL("toggled(bool)"), self.sendVideo)
		QtCore.QObject.connect(self.ui.actionSendDesktop, QtCore.SIGNAL("toggled(bool)"), self.sendDesktop)
		QtCore.QObject.connect(self.ui.actionConfigure, QtCore.SIGNAL("toggled(bool)"), self.configureManage)
		QtCore.QObject.connect(self.ui.actionVideoStream, QtCore.SIGNAL("toggled (bool)"), self.showStream)
		QtCore.QObject.connect(self.ui.lineEditRoomMsg, QtCore.SIGNAL("returnPressed()"), self.sendMsg)
		QtCore.QObject.connect(self.tabWidget, QtCore.SIGNAL("currentChanged (int)"), self.tabActivate)
		QtCore.QObject.connect(self.ui.toolBox, QtCore.SIGNAL("currentChanged (int)"), self.boxActivated)
		QtCore.QObject.connect(self.ui.listWidgetRoomBox, QtCore.SIGNAL("itemChanged (QListWidgetItem *)"), self.setRightMsgItem)
		QtCore.QObject.connect(self.ui.dockWidgetRoom, QtCore.SIGNAL("dockLocationChanged (Qt::DockWidgetArea)"), self.location)
		QtCore.QObject.connect(self.ui.dockWidgetRoom, QtCore.SIGNAL("void topLevelChanged (bool)"), self.location)
		
		self.iconConnected = QtGui.QIcon(self.ui.actionConnection.icon())		
		self.iconConnected.addPixmap(QtGui.QPixmap(":/new/prefix2/images/actions/connect_established.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
		self.iconDisconnected = QtGui.QIcon(self.ui.actionConnection.icon())		
		self.iconDisconnected.addPixmap(QtGui.QPixmap(":/new/prefix2/images/actions/connect_creating.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
		self.timer = QtCore.QTimer()
		self.timer.start(2000)
		self.lineEditRoomMsg = self.ui.lineEditRoomMsg
		self.sysTrayIcon = None
		if QtGui.QSystemTrayIcon.isSystemTrayAvailable():
			self.sysTrayMenu = QtGui.QMenu(self)
			self.sysTrayMenu.addAction(self.ui.actionExit)
			self.sysTrayIcon = QtGui.QSystemTrayIcon(self)
			self.sysTrayIcon.setIcon(self.windowIcon())
			self.sysTrayIcon.setContextMenu(self.sysTrayMenu)
			sysTrayToolTipMsg = QtCore.QString(self.tr("Sacks - Disconnected"))
			self.sysTrayIcon.setToolTip(sysTrayToolTipMsg)
			self.sysTrayIcon.show()
			QtCore.QObject.connect(self.sysTrayIcon, QtCore.SIGNAL("activated(QSystemTrayIcon::ActivationReason)"), self.trayIconClick)
			
	def location(self, location):
		print(location)
		
		
		
	def trayIconClick(self, trayActivation):
		if trayActivation == QtGui.QSystemTrayIcon.Trigger:
			if self.isHidden():
				self.show()
			else:
				self.hide()
		
	def streamSessionInit(self, streamDestination):
		self.streamDestination = streamDestination
		
	def tabActivate(self, tabNumber):
		print(tabNumber)
		if tabNumber == 1:
			self.webWidget.toolBar.setVisible(True)
		else:
			self.webWidget.toolBar.setVisible(False)
# 		if tabNumber==2:
# 			self.remoteDesktopInterface.toolBar.setVisible(True)
# 		else:	
# 			self.remoteDesktopInterface.toolBar.setVisible(False)

	def boxActivated(self, boxNumber):
		print("boxActivated number: ", boxNumber)
		for mdiWin in self.mdi.windowList():
			if mdiWin.numWin == boxNumber:
				self.mdi.setActiveWindow(mdiWin)
				
		if self.boxActivatedUser and (self.boxActivatedNumber != -1):
			self.ui.toolBox.setItemIcon(self.boxActivatedNumber, self.boxActivatedUser.iconUser)
		
		
		
		if boxNumber >= 0:
			boxActivatedUser = self.ui.toolBox.widget(boxNumber)
			boxActivatedUser.focusRequest(False)
			if boxNumber > 0:
				self.ui.toolBox.setItemIcon(boxNumber, boxActivatedUser.iconUser)				
				self.boxActivatedNumber = boxNumber
				self.boxActivatedUser = boxActivatedUser
		
	def tile(self):
		self.mdi.tile()
		self.mdi.exactHeight = 0
		for mdiWin in self.mdi.windowList():
			print(mdiWin.height(), mdiWin.width())
			if mdiWin.height() < 1.1 * mdiWin.width() :
				self.mdi.exactHeight = mdiWin.height()
		
		for mdiWin in self.mdi.windowList():
			if mdiWin.height() > 1.1 * mdiWin.width() :
				if self.mdi.exactHeight:
					mdiWin.resize(mdiWin.width(), self.mdi.exactHeight)
				else:
					mdiWin.resize(mdiWin.width(), mdiWin.height() * 0.6)
		
	
	def sendVideo(self, streamChecked):
		
		if self.streamSession and self.streamDestination:
			print("streamChecked" + str(streamChecked))
			if streamChecked:
				streamInfoDict = {}
				print('sendVideo')
				self.streamSession.stop()
				self.ui.actionSendDesktop.setChecked(False)
				self.streamSession.numWin = -1
			
				print("streamDestination" + str(self.streamDestination))
				streamInfoDict['streamDestination'] = self.streamDestination
				streamInfoDict['streamContent'] = "acquisitionVideo"
				self.streamSession.initialize(streamInfoDict)
				self.streamSession.start()
				self.ui.actionVideoStream.setChecked(True)
				self.streamSession.setWindowTitle('My Stream Video')
			else:
				self.streamSession.stop()
	

		
	def sendDesktop(self, streamChecked):
		if self.streamSession and self.streamDestination:
			if streamChecked:
				print('sendDesktop')
				streamInfoDict = {}
				self.streamSession.stop()
				self.ui.actionSendVideo.setChecked(False)
				self.streamSession.numWin = -1
				print("streamDestination" + str(self.streamDestination))
				streamInfoDict['streamDestination'] = self.streamDestination
			# "intellicom.eushells.net"
				streamInfoDict['streamContent'] = "acquisitionDesktop"
			
				self.streamSession.initialize(streamInfoDict)
				print("in mezzo")
				self.streamSession.start()

				self.ui.actionVideoStream.setChecked(True)
				
				self.streamSession.setWindowTitle('My Stream Desktop')
			else:
				self.streamSession.stop()	
	
	def showStream(self, showStreamStatus):
		if showStreamStatus:
			self.streamSession.show()
		else:
			self.streamSession.hide()

	def activeStream(self, streamEnable):
		if streamEnable:
			self.ui.actionSendVideo.setEnabled(True)
			self.ui.actionSendDesktop.setEnabled(True)
		else:
			self.ui.actionSendVideo.setChecked(False)
			self.ui.actionSendDesktop.setChecked(False)
			self.ui.actionSendVideo.setEnabled(False)
			self.ui.actionSendDesktop.setEnabled(False)	


	def configureManage(self, configureEnable):
		if configureEnable:
			self.configContainer.show()
		else:
			self.configContainer.hide()
			
	
	def newWindow(self, userBox):
		if userBox:
			print("presenceUserBox" + str(self.ui.toolBox.indexOf(userBox)))
			# verifica per controllare se il widget percaso era gia' nel toolbox
			if self.ui.toolBox.indexOf(userBox) == -1:
				userBox.boxIndex = self.ui.toolBox.addItem(userBox, userBox.nameSlot)
				self.ui.toolBox.setItemIcon(userBox.boxIndex, userBox.iconUser)
				userBoxMdiWin = userBox.mdiWin
				userBoxMdiWin.numWin = userBox.boxIndex
				userBoxMdiWin.setWindowTitle(userBox.nameSlot)
				self.numPlayer = self.numPlayer + 1
			else: 
				print("il toolBox era stato gia' occupato dal widget")


	def delWindow(self, userBox):
		if userBox:
			userBoxIndex = self.ui.toolBox.indexOf(userBox)
			self.ui.toolBox.removeItem(userBoxIndex)

	def sendMsg(self):
		msg = self.ui.lineEditRoomMsg.text()
		self.emit(QtCore.SIGNAL('msgOut'), msg)
		self.ui.lineEditRoomMsg.clear()
		
	def showMsg(self, msg):
		itemListWidget = QtGui.QListWidgetItem(msg)
		itemListWidget.msgText = msg
		itemListWidget.setFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)
		
		self.ui.listWidgetRoomBox.addItem(itemListWidget)
		self.ui.listWidgetRoomBox.scrollToBottom() 
		
		
	def setRightMsgItem(self, itemListWidget):
		itemListWidget.setText(itemListWidget.msgText)
	

# metodo per rendere corrente il dockwidget passato
	def setCurrentDock(self, dockWidget):
		dockWidgetTitle = dockWidget.windowTitle()
		dockWidgetKeyPosition = dockWidgetTitle.indexOf("&")
		print("dockWidgetKeyPosition ", dockWidgetKeyPosition)
		if dockWidgetKeyPosition >= 0:
			dockWidgetKey = dockWidgetTitle[dockWidgetKeyPosition + 1]
			print("dockWidgetKey ", dockWidgetKey)
			# genera come evento il digitare la lettera scorciatoia nel titolo del dockWidget
			keyEvent = QtGui.QKeyEvent(QtCore.QEvent.KeyPress, 0, QtCore.Qt.AltModifier, dockWidgetKey)
			QtGui.QApplication.sendEvent(self, keyEvent)
			
	def closeEvent(self, closeEvent):
# 		self.mdi.closeAllWindows()	
		print("closeEvent MainWindow")
		self.streamSession.close()
		self.voipInterface.close()
		self.webWidget.close()
		self.sysTrayIcon.hide()
		numTotalUserBox = self.ui.toolBox.count()
		for userBoxIndex in range(numTotalUserBox):
			userBox = self.ui.toolBox.widget(userBoxIndex)
			userBox.closeEvent(0)
		
from .stream.py_stream import pystream
# from stream.py_userSlot import pyuserSlot		
if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	a = pystream()
	MainWindow = pymainWindow(a)
	hal = QtGui.QListWidgetItem("ciao")
	MainWindow.showMsg("34")
	MainWindow.streamSession.streamDialog.show()
	MainWindow.streamDestination = "192.168.0.4:1222"
	MainWindow.activeStream(True)
	MainWindow.show()
	sys.exit(app.exec_())
