import sys
from PyQt5 import QtCore, QtGui, QtNetwork


class pyslotVlc(QtGui.QWidget):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)
		print("number")
		
		self.a = QtGui.QWidget()
		self.a.show()	
		self.tcpSocket = QtNetwork.QTcpSocket()
		self.tcpSocket.connectToHost("192.168.0.3", 4212)
		QtCore.QObject.connect(self.tcpSocket, QtCore.SIGNAL("readyRead()"), self.socketManage)
		self.vlcStreamName = "stream "
		self.stremPort = str(1234)
		self.vlcStreamInput = "udp://@:" + self.stremPort
		self.vlcStreamOutput = "#duplicate{dst=std{access=http,mux=ASF,dst=:" + self.stremPort + "}}"
		self.listCommands = []
		self.listCommands.append("test\n")
		self.listCommands.append("new " + self.vlcStreamName + "broadcast enabled\n")
		self.listCommands.append("setup " + self.vlcStreamName + "input " + self.vlcStreamInput + "\n")
		self.listCommands.append("setup " + self.vlcStreamName + "output " + self.vlcStreamOutput + "\n")
		self.listCommands.append("control stream play \n")
		# QtCore.QTimer.singleShot(7000, self.socketManage)
		
		
		
	def socketManage(self):	
		print("ciao")
		readMsg = self.tcpSocket.readAll()
		print(readMsg)
		print("len " + str(len(self.listCommands)))
		if len(self.listCommands):
			commandVlc = self.listCommands.pop(0)
			if readMsg[0:8] == "Password":
				print(self.tcpSocket.writeData(commandVlc))
			else:
				print(commandVlc)
				print(self.tcpSocket.writeData(commandVlc))
				
			
			
if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	vlcCommand = pyslotVlc()
	sys.exit(app.exec_())
