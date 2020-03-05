import sys
import random

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
                                                    
#Connexion au serveur
import socket
import select

hote = 'localhost'
port = 25565

connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_avec_serveur.connect((hote, port))
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
            message_serveur, wlist, xlist = select.select([connexion_avec_serveur], [], [], 0.05)
            #print(MainWindow().historique)
            if len(message_serveur) != 0:
                # Client est de type socket
                msg_recu = message_serveur[0].recv(1024)
                # Peut planter si le message contient des caractères spéciaux
                msg_recu = msg_recu.decode()

                print(msg_recu)
                
                #appli.historique = appli.historique + msg_recu + '\n'
                #appli.messages.setPlainText(appli.historique) 

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.historique = ''
        
        self.button = QPushButton("Send Message")
        self.dialogue = QLineEdit()
        self.messages = QTextEdit()
        
        self.button.clicked.connect(self.msgSend)
        self.messages.setReadOnly(True)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.messages)
        self.layout.addWidget(self.dialogue)
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
        if self.dialogue.text() != '':
            #self.historique = self.historique + '\n' + self.dialogue.text()
            #self.messages.setPlainText(self.historique)
            connexion_avec_serveur.send(self.dialogue.text().encode())
            self.dialogue.setText('')

            if self.dialogue.text() == "fin":
                QCoreApplication.instance().quit

    def msgRecv(self, msg):
        print("Signal reçu")
        


if __name__ == "__main__":



    app = QApplication([])
    window = MainWindow()
    app.exec_()