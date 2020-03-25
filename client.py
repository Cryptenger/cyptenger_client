#les modules faisant parti de la librairie standard de python :
import sys, random, os, functools, datetime, json, time, socket, select
#nous utilison la librairie graphiqye PyQt5
try:
    from PyQt5 import QtGui, QtCore
    from PyQt5.QtWidgets import *
except:
    print('You must install the PyQt5 library')
    print('You can do it with the following command on your Commands Prompt')
    print('pip install PyQt5')
    quit = input('press a key to quit')
    exit()
#nos propres modules
from gui import mainWidgetOBJ, connectionWidgetOBJ

#les commentaires d'explications sont disposés dans les déclarations de fonctions principalement. Les pararmètres ne sont pas forcément expliqués lors des appels de fonctions.

#le serveur n'envoieque des strings pures et par paquets de 1 Ko
#nous utilisons le json pour dialoguer avec le serveur
#Donc si l'historique est trop long il n'est pas envoyé d'un seul coup.
#Tant qu'il n'est pas entier on stoque l'historique dans la variable history


class WorkerSignals(QtCore.QObject):
    """
    Worker signal
    """
    result = QtCore.pyqtSignal(object)

class Worker(QtCore.QObject):#QRunnable):
    '''
    Worker thread    ben le truc qui recoit le message
    '''
    received_message = QtCore.pyqtSignal(str)


    def __init__(self, parent):
        super(Worker, self).__init__()
        self.parent = parent

        self.signals = WorkerSignals()

        self.history = ''

    @QtCore.pyqtSlot()
    def run(self):
        # global history
        while True:
            server_message, wlist, xlist = select.select([self.parent.server_connection], [], [], 0.05)

            if len(server_message) != 0:
                # Client est de type socket
                msg_received = server_message[0].recv(1024)
                # Peut planter si le message contient des caractères spéciaux
                msg_received = msg_received.decode()


                try:    #si le message n'est pas en entier ca fail (= si on peut pas le convertir en json)
                    json.loads(msg_received)       #conversion JSON to PYTHON
                    self.received_message.emit(msg_received)       #ON NE PEUT PAS ENVOYER  UN DICTIONNAIRE DONC ON VA TRICHER MAIS CE SERA PLUS LOURD
                except:     #PREMIERE FOIS SI CA MARCHE PAS : A CAUSE DE LA LISTE DES CHANNELS
                    if "channelList" in msg_received:
                        channelsListReceived = msg_received.split("<KTN>")[0]          #on fait passer d'abord la liste des channels
                        self.received_message.emit(channelsListReceived)

                        rest_of_the_message = msg_received.split("<KTN>")[1]      #puis l'historique

                        print(type(self.history))
                        self.history = self.checkIfMsgIsInCorrectFormat(checked_msg=rest_of_the_message, store_in_var=str(self.history))

                    else:                   #maintenant si ca marche pas c'est que le message n'est pas entier : on le stique dans var global history
                        self.history = self.checkIfMsgIsInCorrectFormat(checked_msg=msg_received, store_in_var=str(self.history))


    def checkIfMsgIsInCorrectFormat(self, checked_msg, store_in_var):
        """si checked_msg n'a pas un format json correct, on store checked_msg dans store_in_var pour que la suite du json soit ajouté au prochain paquet envoyé par le serveur"""
        new = store_in_var + checked_msg

        try:
            json.loads(new)
            self.received_message.emit(new)
            return new

        except:
            return new
            pass


class MainWindow(QMainWindow):
    """Ben, tout Cryptenger"""
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.initWindow()
        self.buildWindow()

    def closeEvent(self, event):
        """fonction appelée (toute seule) quand l'utilisateur ferme cryptenger"""
        print("Cryptenger closed")
        try:    #on mettra ici toutes les fenêtres à fermer
            self.cryptenger_win.settings.close()
        except:
            pass

    def initWindow(self):                                                       #les self.settings de la fenêtre principale
        self.setGeometry(0, 0, 1280, 720)
        self.setWindowTitle('Cryptenger')
        self.setWindowIcon(QtGui.QIcon('./assets/ico/cryptenger_icon.ico'))

        with open('./assets/css/style.css') as style:
            self.setStyleSheet(style.read())

    def buildWindow(self):                                                      #le contenu de la fenêtre principale
        #fenêtre de connection
        self.connection_widget = connectionWidgetOBJ()      #on appelle la fenêtre de connection
        self.connection_widget.start_btn.clicked.connect(self.connectAndRunSever)

        #layout de la fenêtre principale
        self.main_V_lyt = QVBoxLayout()
        self.main_V_lyt.addWidget(self.connection_widget)

        """TEMP PARCE QUE RELOU"""
        self.connection_widget.firstName_lne.setText('Cosius')
        self.connection_widget.adresse_lne.setText('localhost')
        self.connection_widget.port_lne.setText('25565')

        #widget
        widget = QWidget()
        widget.setLayout(self.main_V_lyt)

        #QMainWindow
        self.setCentralWidget(widget)
        self.show()


    def connectAndRunSever(self):
        self.settings = {
            "firstName" : self.connection_widget.firstName_lne.text(),
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


            try:        #si la connection est impossible, on affiche un message d'erreur et on attend
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

                self.connection_widget.close()
            except:
                print("Couldn't establish network communication with server")
                print("Something's wrong. Maybe the server is not started. Check the port, the adress. ")



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

            # #met notif a 0
            # self.cryptenger_win.changeNotif(channel, reset=True)

            """ADD THE TEXT TO THE UI"""
            #self.cryptenger_win.addMessageToAChannel(msg = message, channel = channel)




    def msgRecv(self, msg):
        message_in_python = json.loads(msg)       #conversion JSON to PYTHON

        try:                                                                        #récupère le channel actuel depuis le current item sélectionné de la QListWidget des channels
            current_channel = self.cryptenger_win.channelsList.currentItem().text()
            current_channel = int(current_channel)
        except:                                                                     #si on a pas encore sélectionné de channel (qu'on utilise le channel par défaut, après le lancement) on utilise le channel 0 lancé par défaut. Car la ligne du dessus a besoin qu'un item de la liste ait été sélectionné au moins une fois.
            current_channel = 0

        print(message_in_python)

        #si la string envoyée par le serveur est la liste des channels
        #fait parti des informations que le client doit recevoi AVANT de lancer la connection ET l'interface utilisateur principale
        if "channelList" in message_in_python:      #NE SE LIRA QU 1 SEULE FOIS       LA PREMIERE FOIS
            print("server : Channel list recieved")

            self.channelList = message_in_python["channelList"]

            #maintenant qu'on a TOUTES les informations nécessaires à la création de l'interface utilisateur finale on la crée
            self.cryptenger_win = mainWidgetOBJ(
                parentObject=self,
                serverName=self.settings['adress'],
                Username=self.settings['firstName'],
                channelsNames = self.channelList,
            )

            self.main_V_lyt.addWidget(self.cryptenger_win)
            self.cryptenger_win.inputUI.input_lne.returnPressed.connect(self.msgSend)

            #initialisation des notifications (on cache le label et remet le compteur à 0)
            for j in range(len(self.channelList)):
                self.cryptenger_win.changeNotif(channel=int(j), reset=True)


        #si la string envoyée par le serveur est l'historique
        elif "history" in message_in_python:
            print("server : History recieved")

            #pour chaque message
            for i in range(0, len(message_in_python["history"])):

                message = message_in_python["history"][i]
                channel = json.loads(message)           #json to python     JE SAIS PAS POURQUOI JE SUIS OBLIG2 DE LE REFAIRE
                channel = channel["messageType"]['channel']     #récupère le channel

                #ajout du message
                self.cryptenger_win.addMessageToAChannel(msg=message, channel=int(channel))

        #si la string envoyé par le serveur est un message
        elif "messageType" in message_in_python:
            print("server : message received")

            channel = message_in_python["messageType"]["channel"]
            username = message_in_python["messageType"]["username"]

            #on ajoute une notification seulement si le message vient d'un autre utilisateur et qu'il est affiché dans un autre channel que celui actuellement sélectionné
            addNotif = False
            if username != self.settings["firstName"] and not channel == current_channel :          #ET SI CURRENT CHANNEL DIFFERENT DE CHANNEL DU MESSAGE ENVOYE
                addNotif=True

            #ajout du message
            self.cryptenger_win.addMessageToAChannel(msg = msg, channel=channel, addNotif=addNotif)





"""Lancement de L'application Cryptenger"""
if __name__ == "__main__":

    app = QApplication([])
    window = MainWindow()
    app.exec_()
