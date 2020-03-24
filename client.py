import sys, random, os, functools, datetime, json
import time
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *
from gui import mainWidgetOBJ, connectionWidgetOBJ

#Connexion au serveur
import socket, select

history = ''
historyAdded = False
#root directory
MAINDIR = os.path.dirname(os.path.realpath(__file__))

class WorkerSignals(QtCore.QObject):
    result = QtCore.pyqtSignal(object)

class Worker(QtCore.QObject):#QRunnable):
    '''
    Worker thread
    '''
    received_message = QtCore.pyqtSignal(str)


    def __init__(self, parent):
        super(Worker, self).__init__()
        self.parent = parent

        self.signals = WorkerSignals()

    @QtCore.pyqtSlot()
    def run(self):
        global history, historyAdded
        while True:
            server_message, wlist, xlist = select.select([self.parent.server_connection], [], [], 0.05)
            #print(MainWindow().history)
            if len(server_message) != 0:
                # Client est de type socket
                msg_received = server_message[0].recv(1024)
                # Peut planter si le message contient des caractères spéciaux
                msg_received = msg_received.decode()


                if msg_received.startswith('<history') and msg_received.endswith('</history>'):
                    print('HOURRAAAAAA')

                if historyAdded == False:
                    try:    #si le message n'est pas en entie ca crash (= si on peut pas le convertir en json)
                        json.loads(msg_received)       #conversion JSON to PYTHON
                        print('lolilol')
                        self.received_message.emit(msg_received)       #ON NE PEUT PAS ENVOYER  UN DICTIONNAIRE DONC ON VA TRICHER MAIS CE SERA PLUS LOURD
                    except:     #PREMIERE FOIS SI CA MARCHE PAS : A CAUSE DE LA LISTE DES CHANNELS
                        if "channelList" in msg_received:
                            print("H1")
                            part1 = msg_received.split("<KTN>")[0]          #on fait passer d'abord la liste des channels
                            self.received_message.emit(part1)

                            part2 = msg_received.split("<KTN>")[1]      #puis l'historique

                            history = history + part2

                        else:                   #maintenant si ca marche pas c'est que le message n'est pas entier : on le stique dans var global history
                            print('H2')
                            history = history + msg_received
                            try:
                                print('H4')
                                json.loads(history)             #teste si l'historique est complet = si le json n'a pas d'errreur
                                self.received_message.emit(history)
                            except:
                                print('H3')
                                pass




class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.initWindow()
        self.buildWindow()

    def initWindow(self):                                                       #les self.settings de la fenêtre principale
        self.setGeometry(0, 0, 1280, 720)
        self.setWindowTitle('Cryptenger')
        self.setWindowIcon(QtGui.QIcon(MAINDIR + '/assets/ico/cryptenger_icon.ico'))

        with open(MAINDIR + '/assets/css/style.css') as style:
            self.setStyleSheet(style.read())

    def buildWindow(self):                                                      #le contenu de la fenêtre principale
        #layout de la fenêtre principale
        self.main_V_lyt = QVBoxLayout()

        #fenêtre de connection
        self.connection_widget = connectionWidgetOBJ()
        self.connection_widget.start_btn.clicked.connect(self.connectAndRunSever)
        self.main_V_lyt.addWidget(self.connection_widget)

        """TEMP PARCE QUE RELOU"""
        self.connection_widget.firstName_lne.setText('Alfiory')
        self.connection_widget.secondName_lne.setText('Samper')
        self.connection_widget.thirdName_lne.setText('Cosius')
        self.connection_widget.port_lne.setText('25565')
        self.connection_widget.adresse_lne.setText('localhost')


        widget = QWidget()
        widget.setLayout(self.main_V_lyt)
        self.setCentralWidget(widget)
        self.show()


    def connectAndRunSever(self):
        self.settings = {
            "firstName" : self.connection_widget.firstName_lne.text(),
            "secondName" : self.connection_widget.secondName_lne.text(),
            "thirdName" : self.connection_widget.thirdName_lne.text(),
            "port" : self.connection_widget.port_lne.text(),
            "adress" : self.connection_widget.adresse_lne.text(),
            }

        #check if the user have given all the required informations
        itIsOK = True
        for i in self.settings:
            if self.settings[i]=='':
                print('You must give a ' + i)
                itIsOK = False


        #if the user have given all the required informations the client starts
        if itIsOK == True:
            #close connection widget
            self.connection_widget.close()

            #BUILD SERVER
            #creating a connection
            self.server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_connection.connect((self.settings['adress'], int(self.settings['port'])))
            print("Connection established on the port", self.settings['port'])

            #starting server
            self.threadpool = QtCore.QThreadPool()
            print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

            self.worker = Worker(parent = self)
            self.workerThread = QtCore.QThread()
            self.workerThread.started.connect(self.worker.run) #r Start the Run function
            self.worker.received_message.connect(self.msgRecv)  # Connect your signals/slots
            self.worker.moveToThread(self.workerThread)  # Move the Worker object to the Thread object
            self.workerThread.start()

            #BUILD MAIN WIDGET
            self.cryptenger_win = mainWidgetOBJ(
            parentObject=self,                                              #pour fermer toute la mainWindow
            serverName=self.settings['adress'],
            Username=self.settings['firstName'],
            )
            self.main_V_lyt.addWidget(self.cryptenger_win)
            self.cryptenger_win.inputUI.input_lne.returnPressed.connect(self.msgSend)   #send message signal

    def msgSend(self):
        #message
        message = self.cryptenger_win.inputUI.input_lne.text()

        if message != '':
            #channel
            try:                                                                #PARCE QU IL FAUT SELECTIONNER UN CHANNEK D ABORD (plutard on le setera parr default)
                channel = self.cryptenger_win.getCurrrentIndex(listWidget=self.cryptenger_win.channelsList)
            except:
                channel = 0     #si on a pas encorer changé de channel en cliquant sur la listWidget

            #date
            date = datetime.datetime.now()
            date = {
            "day": date.strftime("%F"),
            "hour": date.strftime("%X")
            }

            #message metadata
            messageDict = {
                "messageType":{
                    "message": message,
                    "username": self.settings["firstName"],
                    "channel": channel,
                    "date": date,
                }
            }

            message = json.dumps(messageDict)

            #send message
            self.server_connection.send(message.encode())

            #reset input line
            self.cryptenger_win.inputUI.input_lne.setText('')   #c'est peut etre de la que vient le bug d'atom des multiples messages

            """ADD THE TEXT TO THE UI"""
            #self.cryptenger_win.addMessageToAChannel(msg = message, channel = channel)


    def msgRecv(self, msg):
        message_in_python = json.loads(msg)       #conversion JSON to PYTHON

        try:                                                                        #récupère le channel actuel depuis le current item sélectionné de la QListWidget des channels
            channel = self.cryptenger_win.channelsList.currentItem().text()
            channel = int(channel)
        except:                                                                     #si on a pas encore sélectionné de channel (qu'on utilise le channel par défaut, après le lancement) on utilise le channel 0 lancé par défaut. Car la ligne du dessus a besoin qu'un item de la liste ait été sélectionné au moins une fois.
            channel = 0

        if "channelList" in message_in_python:
            print("on a ici la liste des channels !")
            print(message_in_python["channelList"][0])
            self.channelList = message_in_python["channelList"]

        elif "history" in message_in_python:
            print("on a ici l'historique")

            for i in range(0, len(message_in_python["history"])):
                message = message_in_python["history"][i]
                channel = message_in_python["history"][i]
                channel = json.loads(channel)           #json to python
                channel = channel["messageType"]['channel']     #récupèr le channel
                self.cryptenger_win.addMessageToAChannel(message, int(channel))
            print("scroll down")
            # self.cryptenger_win.channels[channel].scrollDownFar()
            print("scroll down")
        elif "messageType" in message_in_python:
            print("on a ici un message !")

            channel = message_in_python["messageType"]["channel"]   #pour envoyer dans le bon channel

            self.cryptenger_win.addMessageToAChannel(msg, channel)                  #ajoute le message à l'UI






if __name__ == "__main__":

    app = QApplication([])
    window = MainWindow()
    app.exec_()
