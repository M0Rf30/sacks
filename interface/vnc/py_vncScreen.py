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
"""This module provides remote screen RFB-client support, based on Libvncclient and Python binding Pyvnc.

You can find documentation on Libvncclient at http://libvncserver.sourceforge.net/ and on Pyvnc at http://d-austin.net/pyvnc/ .

The class is "pyvncScreen", which is used to create a connection to a RFB remote desktop server. It realizes authentication, manages  keys and mouse events and elaborate screen updates.

"""

 

# -*- coding: utf-8 -*-
import sys,  platform
import pyvnc	
import py_vncKey as pyvncKey
from PyQt4 import QtCore, QtGui,  QtNetwork

class pyvncScreen(QtGui.QLabel):
	def __init__(self,  parent=None):
		QtGui.QLabel.__init__(self, parent)
		self.show()
		self.vncCore=None
		
		self.mouseButtonPressed=0

	def connect(self, host, display,  passwd):	
		self.vncCore=pyvncCore(str(host), display, str(passwd))
		QtCore.QObject.connect(self.vncCore, QtCore.SIGNAL("imageUpdated(QImage)"), self.elaboratePix)
		if self.vncCore.connected:
			self.setFixedSize(self.vncCore.width,self.vncCore.height)
			self.setMouseTracking(True)
			self.setFocusPolicy(QtCore.Qt.ClickFocus)
			
		return self.vncCore.connected
	def disconnect(self):
		if self.vncCore:
			#QtCore.QObject.disconnect(self.vncCore, QtCore.SIGNAL("imageUpdated()"), self.elaboratePix)
			self.setMouseTracking(False)


			self.vncCore.stop()
			del self.vncCore
			

			self.vncCore=None
			self.clear()
#		for i in range(0x0000, 0xFFFF):
#			print i
#			self.vncCore.sendKeyEvent(i, 0, 1)
#			self.vncCore.sendKeyEvent(i, 0, 0)
	def mouseMoveEvent(self,mouseEvent):
		if self.vncCore and self.vncCore.connected:
			self.vncCore.sendMouseEvent(mouseEvent.x(),mouseEvent.y(),self.mouseButtonPressed)
			

	def mousePressEvent(self,mouseEvent):
		""" Method "mousePressEvent" that receive event from Desktop mouse press
			interaction, recognize it and send the value to the server through the vnc 
			core library.
		"""
		
#"""Method "mousePressEvent" that receive event from Desktop mouse press interaction, recognize it and send the value to the server through the vnc core library.
#"""
		button=mouseEvent.button()
		if button==QtCore.Qt.LeftButton:
			self.mouseButtonPressed=1
		elif button==QtCore.Qt.RightButton:
			self.mouseButtonPressed=4
		elif button==QtCore.Qt.MidButton:
			self.mouseButtonPressed=2
		if self.vncCore and self.vncCore.connected:
			self.vncCore.sendMouseEvent(mouseEvent.x(),mouseEvent.y(),self.mouseButtonPressed)
			
		#self.emit(QtCore.SIGNAL('mouseEvent(int,int,bool)'),mouseEvent.x(),mouseEvent.y(),True)
	def mouseReleaseEvent(self,mouseEvent):
		self.mouseButtonPressed=0
		if self.vncCore and self.vncCore.connected:
			print "release event" 
			self.vncCore.sendMouseEvent(mouseEvent.x(),mouseEvent.y(),self.mouseButtonPressed)

	def keyPressEvent(self,keyPressEvent):
		"""Method "keyPressEvent" that receive event from keyboard interaction, 
		recognize the characther and send the value to the server through 
		the vnc core library.  
		"""
		self.keyPressed= keyPressEvent.key()
		self.keyModifier=keyPressEvent.modifiers()
		#print "keyText: ",keyPressEvent.text()
		#print "modifiers: ", int(keyPressEvent.modifiers())
		#print "native modifiers", keyPressEvent.nativeModifiers()
		if self.vncCore and self.vncCore.connected:
			self.vncCore.sendKeyEvent(self.keyPressed, self.keyModifier, 1)

	def keyReleaseEvent(self,keyPressEvent): 
		self.keyPressed= keyPressEvent.key()
		self.keyModifier=keyPressEvent.modifiers()
		if self.vncCore and self.vncCore.connected:
			self.vncCore.sendKeyEvent(self.keyPressed, self.keyModifier, 0)
			
			
	def event(self, event):
		if (event.type()==QtCore.QEvent.KeyPress) and (event.key()==QtCore.Qt.Key_Tab):
			self.vncCore.sendKeyEvent(QtCore.Qt.Key_Tab, None,  1)
			return True
#			
		return QtGui.QLabel.event(self, event)
		
#	def elaboratePix(self):
	def elaboratePix(self, image):	
		"""Method "elaboratePix" that sect the updated frame received from VNC server 
		as parameter 
		"""
		if self.vncCore:
			pix=QtGui.QPixmap.fromImage(image)
			#pix=QtGui.QPixmap.fromImage(self.vncCore.image)
			self.setPixmap(pix)
		#self.vncCore.clientVnc.clearupdates()


	def closeEvent(self, closeEvent):
		self.disconnect()




class pyvncCore(QtCore.QThread):
	def __init__(self,  host, display, passwd, parent=None):
		QtCore.QThread.__init__(self, parent)
		self.clientVnc = pyvnc.pyvncclient()
		self.connected=False
		connectionVnc=self.clientVnc.connect(host,display,passwd)
		print "Connect return %d" % connectionVnc
		if connectionVnc==0:
			self.connected=True
			self.running=True
			print "Connected to: '%s'" % (self.clientVnc.servername)
			print "Fileno is %d" % (self.clientVnc.fileno())
			print "Checkforupdates returned %d" % self.clientVnc.checkforupdates(1.0)
			print "Updatedarea = ", self.clientVnc.updatedarea()
			self.width=self.clientVnc.width
			self.height=self.clientVnc.height
			self.image=QtGui.QImage()
			self.numImage=0
			self.start(QtCore.QThread.IdlePriority)
			#self.start()
			#QtCore.QTimer.singleShot(11000, self.terminate)
			#QtCore.QTimer.singleShot(20000, self.start)
	def stop(self):
		print "del vncCore"
		self.running=False
#		self.terminate()
		self.wait()
		del self.clientVnc
	def run(self):
		i=0
		while self.running:
			#print "while"
			checkUpdates=self.clientVnc.checkforupdates(0)
			#print "updatedarea: ", self.clientVnc.updatedarea()
		#	print "getbuffer"
			buf=self.clientVnc.getbuffer()
#			confronto rispetto al buffer precedente
		#	print "image"
			
			img=QtGui.QImage(buf,self.width,self.height,QtGui.QImage.Format_RGB32)
			#print "confronto"
			
			if img != self.image:
				#image=img.rgbSwapped()
				image=img.copy(0, 0, self.width, self.height)
			#	print self.clientVnc.state
				self.emit(QtCore.SIGNAL('imageUpdated(QImage)'), image)		
				
				if self.numImage>0:
					self.image=image
				self.numImage+=1	
			self.clientVnc.clearupdates()
			#self.wait(200)
			QtCore.QThread.msleep(150)
			
	
	def sendMouseEvent(self, posX, posY, press):
		#print "manageMouseEvent ", posX, " ", posY, " ", press
		self.clientVnc.sendmouseevent(posX, posY, press)
		
		
	def sendKeyEvent(self, key,keyModifier, down):
		print "pyvncKey"
#		print pyvncKey.key[30]
		print "key: ", key, " keyModifier: ", keyModifier, " down: ", down
		keyElaborated=None
		if pyvncKey.key.has_key(key):
			if pyvncKey.key[key]:
				keyElaborated=pyvncKey.key[key]
				if QtCore.Qt.Key_A<=key<=QtCore.Qt.Key_Z  and  keyModifier==QtCore.Qt.ShiftModifier:
					keyElaborated=keyElaborated-0x20

#			if keyModifier==QtCore.Qt.ShiftModifier:
#				keyElaborated=key
#			else:
#				keyElaborated=key+0x20	
		#elif key==
		if keyElaborated:
			print "keyElaborated: ", keyElaborated, "down: ", down
			self.clientVnc.sendkeyevent(keyElaborated, down)


		
			




if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	vnc = pyvncScreen()
	vnc.connect("193.205.171.97", 1, "g3n3r1c0")
	QtCore.QTimer.singleShot(11000, vnc.disconnect)
	QtCore.QTimer.singleShot(16000, lambda:vnc.connect("193.205.171.97", 1, "g3n3r1c0"))
	QtCore.QTimer.singleShot(25000, vnc.disconnect)
	sys.exit(app.exec_())
		

