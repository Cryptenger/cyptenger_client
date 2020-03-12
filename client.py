import sys
import random

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
                                                    
#Connexion au serveur
import socket
import select

host = 'localhost'
port = 25565

server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_connection.connect((host, port))
print("La connexion avec le serveur a été établie sur le port", port)
#Fin de la connexion

class WorkerSignals(QObject):
    result = pyqtSignal(object)


class Worker(QRunnable):
    '''
    Worker thread
    '''
    def __init__(self):
        super(Worker, self).__init__()

        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        while True:
            server_message, wlist, xlist = select.select([server_connection], [], [], 0.05)
            #print(MainWindow().history)
            if len(server_message) != 0:
                # Client est de type socket
                msg_received = server_message[0].recv(1024)
                # Peut planter si le message contient des caractères spéciaux
                msg_received = msg_received.decode()

                print(msg_received)
                
                #appli.history = appli.history + msg_received + '\n'
                #appli.messages.setPlainText(appli.history) 

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.history = ''
        
        self.button = QPushButton("Send Message")
        self.dialog = QLineEdit()
        self.messages = QTextEdit()
        
        self.button.clicked.connect(self.msgSend)
        self.messages.setReadOnly(True)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.messages)
        self.layout.addWidget(self.dialog)
        self.layout.addWidget(self.button)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)
        self.show()

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        
        worker = Worker()
        self.threadpool.start(worker)


    def msgSend(self):
        if self.dialog.text() != '':
            #self.history = self.history + '\n' + self.dialog.text()
            #self.messages.setPlainText(self.history)
            server_connection.send(self.dialog.text().encode())
            self.dialog.setText('')

            if self.dialog.text() == "fin":
                QCoreApplication.instance().quit

    def msgRecv(self, msg):
        print("Signal reçu")
        


if __name__ == "__main__":



    app = QApplication([])
    window = MainWindow()
    app.exec_()