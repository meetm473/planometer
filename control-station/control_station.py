import logging
import sys
import signal

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow

import gui.gui as gui
from communication import Comm


def sigint_handler(*args):
	QApplication.quit()

class ControlStation(QMainWindow, gui.Ui_main_window):
	def __init__(self, parent=None):
		super().__init__(parent)

		logging.basicConfig(level=logging.DEBUG)

		self.comm = Comm("192.168.103.70")
		self.comm.setupComm()

		self.left_velocity = 0
		self.right_velocity = 0

		self.setupUi(self)
		self.connect_signals()

	def connect_signals(self):
		"""
			Connect signals/shortcuts to methods
		"""

		self.up_btn.clicked.connect(self.moveForward)
		self.down_btn.clicked.connect(self.moveBackward)
		self.right_btn.clicked.connect(self.moveRight)
		self.left_btn.clicked.connect(self.moveLeft)
		self.stop_btn.clicked.connect(self.stop)
		self.process_btn.clicked.connect(self.estimateArea)
		self.gps_btn.clicked.connect(self.getGnssData)
		self.send_btn.clicked.connect(self.onSendBtnClicked)

	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key.Key_W:
			self.moveForward()
		elif event.key() == QtCore.Qt.Key.Key_S:
			self.moveBackward()
		elif event.key() == QtCore.Qt.Key.Key_A:
			self.moveLeft()
		elif event.key() == QtCore.Qt.Key.Key_D:
			self.moveRight()
		elif event.key() == QtCore.Qt.Key.Key_Q:
			self.stop()
		elif event.key() == QtCore.Qt.Key.Key_G:
			self.getGnssData()
		elif event.key() == QtCore.Qt.Key.Key_P:
			self.estimateArea()
	
	def moveForward(self):
		self.left_velocity = (self.left_velocity + 5)
		self.right_velocity = (self.right_velocity + 5)

		self.sendInstructions(is_velocity=True)

	def moveBackward(self):
		self.left_velocity = (self.left_velocity - 5) 
		self.right_velocity = (self.right_velocity - 5)

		self.sendInstructions(is_velocity=True)

	def moveRight(self):
		self.left_velocity = (self.left_velocity + 5)
		self.right_velocity = (self.right_velocity - 5)
		self.sendInstructions(is_velocity=True)

	def moveLeft(self):
		self.left_velocity = (self.left_velocity - 5)
		self.right_velocity = (self.right_velocity + 5)
		self.sendInstructions(is_velocity=True)

	def stop(self):
		self.left_velocity = 0
		self.right_velocity = 0
		self.sendInstructions(is_velocity=True)

	def getGnssData(self):
		self.sendInstructions(instruction="@gps")

	def estimateArea(self):
		print("Estimating area...")
	
	def onSendBtnClicked(self):
		self.sendInstructions(instruction="PING")

	def sendInstructions(self, instruction="!", is_velocity=False):
		data = instruction
		if is_velocity:
			if self.left_velocity < 0:
				self.left_velocity = 0
			elif self.left_velocity > 256:
				self.left_velocity = 255

			if self.right_velocity < 0:
				self.right_velocity = 0
			elif self.right_velocity > 256:
				self.right_velocity = 255

			data = "@" + str(self.left_velocity) + "," + str(self.right_velocity)
		
		self.comm.send(msg=data)
		logging.debug("[DATA SENT]: " + data)

if __name__ == "__main__":
	signal.signal(signal.SIGINT, sigint_handler)

	app = QtWidgets.QApplication(sys.argv)
	win = ControlStation()

	timer = QTimer()
	timer.start(100)
	timer.timeout.connect(lambda : None)

	win.show()
	app.exec_()