import sys
import random
import asyncio

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

class Cryptenger(QObject):
    def __init__(self):
        QWidget.__init__(self)

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
        self.setLayout(self.layout)
        
        self.emit(SIGNAL("startWorking()"))

    def msgSend(self):
        if self.dialogue.text() != '':
            self.historique = self.historique + '\n' + self.dialogue.text()
            self.messages.setPlainText(self.historique)
            connexion_avec_serveur.send(self.dialogue.text().encode())
            self.dialogue.setText('')

class Worker(QObject):
    def msgRecv():
        while True:
            print("Working...")
            time.sleep(0.5)



if __name__ == "__main__":

    app = QApplication(sys.argv)
    
    widget = Cryptenger()
    worker = Worker()

    thread = Qthread()
    worker.moveToThread(thread)
    QObject.connect(widget, SIGNAL("startWorking()"), worker.msgRecv)
    
    thread.start()
    widget.show()



    sys.exit(app.exec())