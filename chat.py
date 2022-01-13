from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QCursor
import sys
import socket

app = QtWidgets.QApplication(sys.argv)
app.setStyleSheet(open("assets/style.css").read()); # Reading external stylesheet

username = '' # The username i selected
chat_open = False # A logical flag that will be used later

# Socket Configuration
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = '127.0.0.1'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
for port in range(1024, 65433):
	try:
		s.connect((HOST, port))
		print('Connected Successfully')
	except:
		pass

class Ui_MainWindow(QMainWindow): # Intro window
	def setupUi(self):
		self.setObjectName("MainWindow")
		self.resize(600, 500)
		self.setWindowTitle("Chatting App")

		self.centralwidget = QtWidgets.QWidget(self)
		self.centralwidget.setObjectName("centralwidget")
		self.setCentralWidget(self.centralwidget)

		self.frame = QtWidgets.QFrame(self)
		self.frame.setGeometry(QtCore.QRect(80, 25, 440, 430))
		self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
		self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
		self.frame.setObjectName("frame")

		self.title = QtWidgets.QLabel(self.frame)
		self.title.setGeometry(QtCore.QRect(0, 50, 440, 40))
		self.title.setText("Live Chat")
		self.title.setObjectName("title")
		self.title.setProperty("class","title")
		self.title.setAlignment(QtCore.Qt.AlignCenter)

		self.label = QtWidgets.QLabel(self.frame)
		self.label.setGeometry(QtCore.QRect(0, 210, 440, 16))
		self.label.setObjectName("label")
		self.label.setProperty("class", "txt");
		self.label.setText("Enter Your Username")
		self.label.setAlignment(QtCore.Qt.AlignCenter)

		self.input = QtWidgets.QTextEdit(self.frame)
		self.input.setGeometry(QtCore.QRect(100, 250, 240, 31))
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.input.sizePolicy().hasHeightForWidth())
		self.input.setSizePolicy(sizePolicy)
		self.input.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.input.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.input.setObjectName("input")
		self.input.setPlaceholderText("e.g. Lawaty") 


		<button>
			<geometry>
				<x></x>
				<y></y>
			</geometry>
		</button>

		self.btn = QtWidgets.QPushButton(self.frame)
		self.btn.setGeometry(QtCore.QRect(170, 350, 112, 31))
		self.btn.setProperty("class", "btn")
		self.btn.setObjectName("btn")
		self.btn.setText("Continue")
		self.btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor));

		self.warning_label = QtWidgets.QLabel(self) #hidden warning pop up
		self.warning_label.setAlignment(QtCore.Qt.AlignCenter)

class users_win(QMainWindow): # The window that manages the communication with the server
	def setupUi(self):
		global username
		global s

		self.setObjectName("MainWindow")
		self.resize(360, 480)
		self.setWindowTitle(username)
		self.centralwidget = QtWidgets.QWidget(self)
		self.centralwidget.setObjectName("centralwidget")
		self.title = QtWidgets.QLabel(self.centralwidget)
		self.title.setText("Available Users")
		self.title.setGeometry(QtCore.QRect(0, 10, 360, 49))
		self.title.setAlignment(QtCore.Qt.AlignCenter)
		self.title.setObjectName("fol")
		self.title.setProperty("class","title")
		self.setCentralWidget(self.centralwidget)

		# Capturing signals from a slot running in another thread which is responsible for the communication with the server
		self.lol_thread = handle_connection()
		self.lol_thread.new.connect(lambda new: show_new(new))
		self.lol_thread.update.connect(lambda users: update_users(users))
		self.lol_thread.request.connect(lambda to: show_dialog(to))
		self.lol_thread.busy.connect(lambda who: construct_warning(users, who+' is busy'))
		self.lol_thread.accept.connect(lambda to: show_chat(to))
		self.lol_thread.msg.connect(lambda msg: append_msg(msg))

		self.warning_label = QtWidgets.QLabel(self) # hidden warning pop up
		self.warning_label.setAlignment(QtCore.Qt.AlignCenter)

	def resetUi(self): # clears all previously read users to be loaded again
		try:
			self.pushButton.deleteLater()
		except:
			pass

	def closeEvent(self, event): # inform the user that we are leaving to forward this to the other clients
		global s
		msg = "leaving-:setting:-"+username
		s.sendall(msg.encode())
		print('left')
		event.accept()
		home.show()

class dialogUi(QMainWindow): # permission window
	def setupUi(self):
		global username
		self.setObjectName("MainWindow")
		self.resize(500, 140)
		self.setWindowTitle("Chatting Request ("+username+")")
		self.centralwidget = QtWidgets.QWidget(self)
		self.centralwidget.setObjectName("centralwidget")
		self.title = QtWidgets.QLabel(self.centralwidget)
		self.title.setGeometry(QtCore.QRect(150, 10, 200, 20))
		self.title.setAlignment(QtCore.Qt.AlignCenter)
		self.title.setObjectName("title")
		self.title.setText("Request From")
		self.title.setProperty("class", "txt")
		self.label = QtWidgets.QLabel(self.centralwidget)
		self.label.setGeometry(QtCore.QRect(0, 49, 500, 50))
		self.label.setAlignment(QtCore.Qt.AlignCenter)
		self.label.setObjectName("label")
		self.label.setProperty("class", "title")
		self.accept = QtWidgets.QPushButton(self.centralwidget)
		self.accept.setGeometry(QtCore.QRect(260, 100, 112, 31))
		self.accept.setObjectName("accept")
		self.accept.setText("Accept")
		self.accept.clicked.connect(accept)
		self.ignore = QtWidgets.QPushButton(self.centralwidget)
		self.ignore.setGeometry(QtCore.QRect(380, 100, 112, 31))
		self.ignore.setObjectName("ignore")
		self.ignore.setText("ignore")
		self.ignore.clicked.connect(dialog.hide)
		self.setCentralWidget(self.centralwidget)


class Ui_Chat(QMainWindow): # Chatting window
	def setupUi(self):
		global username
		self.setObjectName("Chat")
		self.resize(360, 420)
		self.setWindowTitle("Chat dialog ("+username+")")
		self.centralwidget = QtWidgets.QWidget(self)
		self.centralwidget.setObjectName("centralwidget")
		self.title = QtWidgets.QLabel(self.centralwidget)
		self.title.setGeometry(QtCore.QRect(0, 15, 360, 20))
		self.title.setObjectName("lol")
		# self.title.setText(user)
		self.title.setProperty("class", "txt")
		self.title.setAlignment(QtCore.Qt.AlignCenter)
		self.message = QtWidgets.QTextEdit(self.centralwidget)
		self.message.setGeometry(QtCore.QRect(13, 370, 291, 30))
		self.message.setObjectName("textEdit")
		# self.message.setText(user)
		self.send = QtWidgets.QPushButton(self.centralwidget)
		self.send.setGeometry(QtCore.QRect(310, 370, 40, 30))
		self.send.setObjectName("send")
		self.send.setAutoFillBackground(True)
		self.send.clicked.connect(send_msg)
		self.History = QtWidgets.QTextBrowser(self.centralwidget)
		self.History.setGeometry(QtCore.QRect(13, 51, 335, 301))
		self.History.setObjectName("History")
		# self.History.setHtml("<p>lol</p><p>lol</p>")
		self.setCentralWidget(self.centralwidget)

	def closeEvent(self, event): # update the chat_open flag on close
		global chat_open
		chat_open = False


# Logic Section
# Arranged according to the working scenario

def connect(): # Connect to socket server once i choose a username
	global username
	username = home.input.toPlainText()
	users.setupUi() # users window setup must be after username initialization
	init = 'new-:setting:-'+username # Send my username to the server
	s.sendall(init.encode())
	print('sent', init)

	data = s.recv(1024).decode()
	print('received', data)
	if data == 'Username Already Exists': # if Error
		construct_warning(home, data)
	else: 
		update_users(data.split('-:updtAv:-')[1]) # Display Available users in the users window
		home.close()
		users.show()

		users.lol_thread.start() # Now the server added us. let's communicate :D

def update_users(data):
	clients = data.split(',')
	users.resetUi() # delete all pushbuttons if exist
	users.y = 100
	for client in clients:
		show_new(client)

def show_new(client): # Set Single pushbutton that requests for a chat with a specific user
	global username
	print("adding new client", client)
	users.pushButton = QtWidgets.QPushButton(users)
	users.pushButton.setGeometry(QtCore.QRect(85, users.y, 190, 30))
	users.pushButton.setObjectName("pushButton")
	users.pushButton.setText(client)
	if client == username:
		users.pushButton.setEnabled(False)
	users.pushButton.clicked.connect(lambda: request(client))
	users.pushButton.show()
	users.y += 50

class handle_connection(QThread): # thread communicates with the socket server
	global s
	global username

	# The Necessary signals
	new = pyqtSignal(object)
	update = pyqtSignal(object)
	request = pyqtSignal(object)
	busy = pyqtSignal(object)
	accept = pyqtSignal(object)
	msg = pyqtSignal(object)

	def __init__(self):
		QThread.__init__(self)

	def run(self):
		while True:
			data = s.recv(1024).decode()
			print("received", data)
			if '-:updtAv:-' in data: # update all available users
				self.update.emit(data.split('-:updtAv:-')[1])

			elif 'request-:setting:-' in data: # someone asks to open a chat
				self.request.emit(data.split('-:setting:-')[1])

			elif 'accept-:setting:-' in data: # someone accepted my request to open a chat
				self.accept.emit(data.split('-:setting:-')[1])

			elif 'busy-:setting:-' in data:
				self.busy.emit(data.split('-:setting:-')[1])

			elif 'new-:setting:-' in data: # Add a new comer to the available users
				self.new.emit(data.split('-:setting:-')[1])

			elif '-:msg:-' in data: # the other end sends a msg
				self.msg.emit(data.split('-:msg:-')[2])


def request(client): # send request to show dialog at the other instance
	global chat_open
	if chat_open and chat.title.text() == client: # if i am currently chatting with that one
		chat.activateWindow() # just bring the chatting window to front and focus on it
		return
	elif chat_open: # if i am current chatting with someone else
		construct_warning(users, "Close the current chat \n to open another one")
		return

	#otherwise
	global s
	msg = 'request-:setting:-'+client
	s.sendall(msg.encode()) # send a chatting requests
	print('sent', msg)

def show_dialog(to): # whenever someone requests a permission to open a chat with me
	global chat_open
	global s
	if chat_open: # if you are currently chatting with someone
		msg = 'busy-:setting:-'+to
		s.sendall(msg.encode()) # send to the requesting person busy message
		print(to, 'tried to contact with you')
		return
	dialog.setupUi()
	dialog.label.setText(to)
	dialog.show()


def accept(): # when you accept a request, send acception to open the chat at the other instance
	global chat_open
	client = dialog.label.text()
	msg = 'accept-:setting:-'+client # send the acception
	s.sendall(msg.encode())
	dialog.close()
	chat.setupUi()
	chat.title.setText(client)
	chat.show() # open the chat for me
	chat_open = True

def show_chat(to): # whenever I receive someone's acception to my request
	global chat_open
	chat.setupUi()
	chat.title.setText(to)
	chat.show()
	chat_open = True

def append_msg(msg): # whenever a msg is received
	sender = chat.title.text()
	history = chat.History.toHtml()
	chat.History.setHtml(history+"<p>"+sender+': '+msg+"</p>")

def send_msg(): # when i send a message
	global s
	global username
	content = username+'-:msg:-'+chat.title.text()+'-:msg:-'+chat.message.toPlainText()
	s.sendall(content.encode())

	history = chat.History.toHtml()
	chat.History.setHtml(history+"<p>"+username+': '+chat.message.toPlainText()+"</p>")
	chat.message.setText("")


def construct_warning(window,warn): # takes the window and the message to be displayed in that window
	window.warning_label.setGeometry(QtCore.QRect(0, 190, window.frameGeometry().width(), 151))
	window.warning_label.setStyleSheet("color:red;background-color:black;font-size:18pt")
	window.warning_timer = QtCore.QTimer()
	window.warning_timer.start(1400)
	#Remove warning
	window.warning_timer.timeout.connect(lambda: remove_warning(window))
	window.warning_label.setText(warn)
	window.warning_label.raise_()
    
def remove_warning(window):
  window.warning_label.setGeometry(QtCore.QRect(0, 0, 0, 0))
  window.warning_label.setStyleSheet("")
  window.warning_label.setText("")


home = Ui_MainWindow();
users = users_win()
dialog = dialogUi()
chat = Ui_Chat()

home.setupUi()
home.show()
home.btn.clicked.connect(connect)

sys.exit(app.exec_())