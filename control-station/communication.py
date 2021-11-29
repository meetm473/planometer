import socket
import threading
import logging
import re

class Comm:

	def __init__(self, vehicle_ip):

		self.vehicle_ip  = vehicle_ip
		self.TALKING_PORT = 1621
		self.LISTENING_PORT = 1620
		self.MSG_FORMAT = 'utf-8'               
		self.shutdown = False

	def setupComm(self):
		"""
			Setup objects that aid in communication.
		"""

		self.sock = []        # Socket object [serverSocket, clientSocket]
		self.clientFlag = True

		try:
			self.sock.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
			self.sock.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
		except socket.error as msg:
			logging.error("Socket creation error: " + str(msg))

		if (self.bindSocket()):
			# Creating a thread to listen to requests
			self.listener = threading.Thread(target=self.listenRqsts)
			self.listener.daemon = True
			self.listener.start()
		else:
			self.close()

	def bindSocket(self):
		''' 
			Binds a socket to port.

			Returns
			-------
			success : bool
				True if the socket is successfully binded to given port number; else False 
		'''
		try:
			logging.debug("[PORT BINDED] Binding the Port: " + str(self.LISTENING_PORT))
			self.sock[0].bind(('', self.LISTENING_PORT))
			self.sock[0].listen(2)
			return True

		except socket.error as msg:
			logging.error("[ERROR] Socket binding error: " + str(msg))
			logging.info("Cannot bind to port number: " + str(self.LISTENING_PORT) + " | Exiting node...")
			return False

	def listenRqsts(self):
		'''
			Accept connection from other nodes in the network.
			Makes 5 attempts to check and accept a connection
		'''

		allConn = []
		allAddr = []


		while not self.shutdown:
			try:
				del allConn[:]
				del allAddr[:]
				conn, address = self.sock[0].accept()
				logging.debug("here")
				self.sock[0].setblocking(1)  # prevents timeout

				allConn.append(conn)
				allAddr.append(address)
				
				logging.debug("[NEW CONNECTION] Connection has been established to :" + address[0])

				for i in range(len(allConn)):
					data = allConn[i].recv(1024)
					if len(data) > 0:
						logging.debug("[NEW MESSAGE] Message received from: " + str(allAddr[i]) + " | " + str(data))
						self.processRqst(str(data))

			except KeyboardInterrupt:
				logging.error("[ERROR] accepting connections. Trying again...")

			except socket.error as msg:
				if not bool(re.search(".WinError 10038.", str(msg))):
					logging.error("[ERROR] Cannot accept any connections: " + str(msg))
					self.close()

		self.sock[0].close()
		logging.debug("Socket closed")

	def send(self, msg, waitReply=False):
		'''
			Connect to a node and send message. (Low level function)

			Parameters
			----------
			msg : str
				Message to send
			waitReply : bool
				To wait or not to wait for the reply. Default: False
			
			Returns
			-------
			success : bool
				True if message was sent successfully; else False
		'''
		try:    
			if not self.clientFlag:
				self.sock[1] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				self.clientFlag = True

			self.sock[1].connect((self.vehicle_ip, self.TALKING_PORT))
			self.sock[1].send(msg.encode(self.MSG_FORMAT))

			if waitReply:
				print(self.sock[1].recv(1024).decode(self.MSG_FORMAT))

			return True

		except KeyboardInterrupt:
			logging.error("[ERROR] Keyboard interrupt detected")
			return False
		
		except socket.error as msg:
			logging.error("[ERROR] Cannot send message to the target node: " + str(self.TALKING_PORT) + str(msg))
			return False
		
		finally:
			self.sock[1].close()
			self.clientFlag = False

	def close(self):
		'''
			Closes all the sockets 
		'''
		self.shutdown = True
		self.sock[0].close()
		if self.clientFlag:
			self.sock[1].close()
			self.clientFlag = False

	def processRqst(self, msg):
		"""
			Processes the request messages obtained by the node. Should only be called from within
			listenRqsts function.

			Parameters
			----------
			msg : str
				Message string received by the node.
		"""
		pass
