import sys
import random

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

class Cryptenger(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.historique = ''
 
        self.button = QPushButton("Send Message")
        self.refresh = QPushButton("Rafraîchir")
        self.dialogue = QLineEdit()
        self.messages = QTextEdit()
        
        self.button.clicked.connect(self.msgSend)
        self.refresh.clicked.connect(self.msgRecv)
        self.messages.setReadOnly(True)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.messages)
        self.layout.addWidget(self.dialogue)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.refresh)
        self.setLayout(self.layout)

    def msgSend(self):
        if self.dialogue.text() != '':
            #self.historique = self.historique + '\n' + self.dialogue.text()
            #self.messages.setPlainText(self.historique)
            connexion_avec_serveur.send(self.dialogue.text().encode())
            self.dialogue.setText('')

            if self.dialogue.text() == "fin":
                QCoreApplication.instance().quit

    def msgRecv(self):
        message_serveur, wlist, xlist = select.select([connexion_avec_serveur], [], [], 0.05)

        if len(message_serveur) != 0:
            # Client est de type socket
            msg_recu = message_serveur[0].recv(1024)
            # Peut planter si le message contient des caractères spéciaux
            msg_recu = msg_recu.decode()
            self.historique = self.historique + msg_recu + '\n'
            self.messages.setPlainText(self.historique)



if __name__ == "__main__":

    app = QApplication(sys.argv)
    
    widget = Cryptenger()
    widget.show()



    sys.exit(app.exec())
