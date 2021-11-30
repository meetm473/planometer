#!/usr/bin/env python3

import logging
import sys
import signal
import threading
import math

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem

import numpy as np
import gui.gui as gui
from communication import Comm
from queue import Queue


def sigint_handler(*args):
	QApplication.quit()

class ControlStation(QMainWindow, gui.Ui_main_window):

	def __init__(self, parent=None):
		super().__init__(parent)

		logging.basicConfig(level=logging.DEBUG)

		self.queue = Queue()
		self.pts = []

		self.comm = Comm("192.168.12.59", self.queue)
		self.comm.setupComm()

		self.left_velocity = 0
		self.right_velocity = 0
		self.gps_pts = []

		self.setupUi(self)
		self.connect_signals()

		self.listener = threading.Thread(target=self.listenForGpsData)
		self.listener.daemon = True
		self.listener.start()

	def listenForGpsData(self):
		"""
			Runs in the background and listens if GPS data is obtained in the background
			communication thread.
		"""
		while True:
			coords = self.queue.get()
			self.pts.append(coords)
			rowPosition = self.point_loc_tab.rowCount()
			self.point_loc_tab.insertRow(rowPosition)

			self.point_loc_tab.setItem(rowPosition, 0, QTableWidgetItem(str(coords[0])))
			self.point_loc_tab.setItem(rowPosition, 1, QTableWidgetItem(str(coords[1])))
			self.point_loc_tab.setItem(rowPosition, 2, QTableWidgetItem(str(coords[2])))
			
			print("Coords received: " + str(coords))

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
		area = self.calcArea(self.pts)
		self.area_lb.setText(str(area))
		print("Area estimated")

	def onSendBtnClicked(self):
		if(self.cmd_tf.text() == ""):
			self.sendInstructions(instruction="PING")
		else:
			self.sendInstructions(instruction=self.cmd_tf.text())

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

	def gpsToEcef(self, lat, lon, alt):
		"""
			Converts GPS coordinates into ECEF coordinate frame

			Parameters
			----------
			* lat: float: Latitude of the point in degs
			* lon: float: Longitude of the point in degs
			* alt: float: Altitude of the point in degs

			Returns
			-------
			x,y,z coordinates of the point in ECEF coordinate frame
		"""
		rad_lat = lat * (math.pi / 180.0)
		rad_lon = lon * (math.pi / 180.0)

		a = 6378137.0
		finv = 298.257223563
		f = 1 / finv
		e2 = 1 - (1 - f) * (1 - f)
		v = a / math.sqrt(1 - e2 * math.sin(rad_lat) * math.sin(rad_lat))

		x = (v + alt) * math.cos(rad_lat) * math.cos(rad_lon)
		y = (v + alt) * math.cos(rad_lat) * math.sin(rad_lon)
		z = (v * (1 - e2) + alt) * math.sin(rad_lat)

		return x, y, z

	def gpsToEnu(self, ref_coords, point_coords):
		"""
			Converts GPS coordinates into ENU coordinate frame

			Parameters
			----------

			* ref_coords: tuple: 1x3 size tuple consisting of the GPS coordinates (deg,deg,m) of reference point.
			* point_coords: tuple: 1x3 size tuple consisting of GPS coordinates (deg,deg,m) of the point of interest.

			Returns
			-------
			x,y,z coordinates of the point wrt reference point in ENU coordinate frame
		"""
		rad_lat = ref_coords[0] * (math.pi / 180.0)
		rad_lon = ref_coords[1] * (math.pi / 180.0)

		rot_mat = np.array([[-math.sin(rad_lon), math.cos(rad_lon), 0],
							[-math.sin(rad_lat)*math.cos(rad_lon), -math.sin(rad_lat)*math.sin(rad_lon), math.cos(rad_lat)],
							[math.cos(rad_lat)*math.cos(rad_lon), math.cos(rad_lat)*math.sin(rad_lon), math.sin(rad_lat)]])

		ref_ecef = np.array(self.gpsToEcef(ref_coords[0], ref_coords[1], ref_coords[2]))
		point_ecef = np.array(self.gpsToEcef(point_coords[0], point_coords[1], point_coords[2]))

		return rot_mat @ (point_ecef - ref_ecef)

	def calcArea(self, pts):
		"""
			Calculates the area defined by a convex polygon formed by the points in the clockwise direction.

			Parameters
			----------

			* pts : list of tuples : List of GPS coordinates (lat-deg, lon-deg, alt-m) of the points forming the polygon in
			a list. The first point is considered as the reference point. 

			Returns
			--------

			Area enclosed by the polygon in sq. m.
		"""
		triangle_coords = []

		for i in range(1, len(pts)):
			triangle_coords.append(tuple(self.gpsToEnu(pts[0], pts[i])))

		area = 0

		for i in range(0, len(triangle_coords)-1):
			area = area + 0.5*np.linalg.norm(np.cross(triangle_coords[i], triangle_coords[i+1]))
		
		return area

if __name__ == "__main__":
	signal.signal(signal.SIGINT, sigint_handler)

	app = QtWidgets.QApplication(sys.argv)
	win = ControlStation()

	timer = QTimer()
	timer.start(100)
	timer.timeout.connect(lambda : None)

	win.show()
	app.exec_()