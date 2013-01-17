# Sacks: a video conference-meeting system
# Copyright (C) 2009 Associazione Intellicom team
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
"""This module provides web browser support, realized with QtWebKit Module based on WebKit engine.

You can find documentation on WebKit at http://webkit.org/ .

The class is "webWidget", which is used to create an interface to web pages navigation. It imports an interface gui for manage URL page changes, has trace of load progress, print page contents.

"""


import sys

from PyQt4 import QtCore, QtGui, QtWebKit
from Ui_web import Ui_webForm



class webWidget(QtGui.QMainWindow):
	def __init__(self, parent=None):
		super(webWidget, self).__init__(parent)
		self.ui = Ui_webForm()
		self.ui.setupUi(self)
		self.webPage = self.ui.webView.page()
		self.webSettings = self.webPage.settings()
		self.webSettings.setAttribute(QtWebKit.QWebSettings.PluginsEnabled, True)
		self.webSettings.setAttribute(QtWebKit.QWebSettings.JavascriptEnabled, True)
		self.webSettings.setAttribute(QtWebKit.QWebSettings.JavaEnabled, True)

		self.webMainFrame = self.webPage.mainFrame()
		self.printer = QtGui.QPrinter()
		self.menuWeb = self.ui.menuWeb
		self.menuBar = self.ui.menuBar
		self.toolBar = self.ui.toolBar
		self.actionSpreadLink = self.ui.actionSpreadLink
		self.urlWeb = self.ui.urlWeb
		
		# set the default page
		url = 'http://www.google.it'
		self.ui.urlWeb.setText(url)
		
		# load page
		# history buttons:
		self.ui.webView.setUrl(QtCore.QUrl(url))
		self.ui.actionBack.setEnabled(False)
		self.ui.actionNext.setEnabled(False)

		QtCore.QObject.connect(self.ui.actionBack, QtCore.SIGNAL("triggered()"), self.back)
		QtCore.QObject.connect(self.ui.actionNext, QtCore.SIGNAL("triggered()"), self.next)
		QtCore.QObject.connect(self.ui.actionPrint, QtCore.SIGNAL("triggered()"), self.webPrint)
		QtCore.QObject.connect(self.ui.actionPrintPreview, QtCore.SIGNAL("triggered()"), self.webPrintPreview)
		QtCore.QObject.connect(self.ui.urlWeb, QtCore.SIGNAL("returnPressed()"), self.urlChanged)
		QtCore.QObject.connect(self.ui.webView, QtCore.SIGNAL("linkClicked (const QUrl&)"), self.linkClicked)
		QtCore.QObject.connect(self.ui.webView, QtCore.SIGNAL("urlChanged (const QUrl&)"), self.linkClicked)
		QtCore.QObject.connect(self.ui.webView, QtCore.SIGNAL("loadProgress (int)"), self.loadProgress)
		QtCore.QObject.connect(self.ui.actionReload, QtCore.SIGNAL("triggered()"), self.reloadPage)
		QtCore.QObject.connect(self.ui.actionStop, QtCore.SIGNAL("triggered()"), self.stopPage)
		
		QtCore.QMetaObject.connectSlotsByName(self)
	
	def urlChanged(self):
# 		"""
# 		Url have been changed by user
# 		"""
		page = self.ui.webView.page()
		history = page.history()
		if history.canGoBack():
			self.ui.actionBack.setEnabled(True)
		else:
			self.ui.actionBack.setEnabled(False)
		if history.canGoForward():
			self.ui.actionNext.setEnabled(True)
		else:
			self.ui.actionNext.setEnabled(False)
		
		url = self.ui.urlWeb.text()
		if not str(url).startswith('http://'):
			url = "http://" + url 
		self.ui.webView.setUrl(QtCore.QUrl(url))
	def stopPage(self):
# 		"""
# 		Stop loading the page
# 		"""
		print "stop"
		self.ui.webView.stop()
	
# 	def title_changed(self, title):
# 		"""
# 		Web page title changed - change the tab name
# 		"""
# 		self.setWindowTitle(title)
	def webPrint(self):
		printDialog = QtGui.QPrintDialog(self.printer, self)
		if printDialog.exec_() == QtGui.QDialog.Accepted:
			self.ui.webView.print_(self.printer)

	def webPrintPreview(self):
		printPreviewDialog = QtGui.QPrintPreviewDialog(self.printer, self)
		QtCore.QObject.connect(printPreviewDialog, QtCore.SIGNAL("paintRequested (QPrinter *)"), self.ui.webView.print_)
		printPreviewDialog.exec_()

	def reloadPage(self):
# 		"""
# 		Reload the web page
# 		"""
		self.ui.webView.setUrl(QtCore.QUrl(self.ui.urlWeb.text()))
	
	def linkClicked(self, url):
# 		"""
# 		Update the URL if a link on a web page is clicked
# 		"""
		page = self.ui.webView.page()
		history = page.history()
		if history.canGoBack():
			self.ui.actionBack.setEnabled(True)
		else:
			self.ui.actionBack.setEnabled(False)
		if history.canGoForward():
			self.ui.actionNext.setEnabled(True)
		else:
			self.ui.actionNext.setEnabled(False)
		
		self.ui.urlWeb.setText(url.toString())
	
	def loadProgress(self, load):
		"""
#		Page load progress
#		"""
		if load == 100:
			self.ui.actionStop.setEnabled(False)
		else:
			self.ui.actionStop.setEnabled(True)
		
	def back(self):
# 		"""
# 		Back button clicked, go one page back
# 		"""
		page = self.ui.webView.page()
		history = page.history()
		history.back()
		if history.canGoBack():
			self.ui.actionBack.setEnabled(True)
		else:
			self.ui.actionBack.setEnabled(False)
	
	def next(self):
# 		"""
# 		Next button clicked, go to next page
# 		"""
		page = self.ui.webView.page()
		history = page.history()
		history.forward()
		if history.canGoForward():
			self.ui.actionNext.setEnabled(True)
		else:
			self.ui.actionNext.setEnabled(False)
			
	def spreadLink(self):
		linkPath = self.ui.urlWeb.text()
		self.emit(QtCore.SIGNAL('spreadLink'), linkPath)
		
	def closeEvent(self, closeEvent):
		self.ui.webView.setUrl(QtCore.QUrl(""))
		print "webClose"
if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	myapp = webWidget()
	myapp.show()
	sys.exit(app.exec_())
