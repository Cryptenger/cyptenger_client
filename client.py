import sys, random, os, functools

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *
from gui import mainWidgetOBJ, connectionWidgetOBJ

#Connexion au serveur
import socket
import select


#Fin de la connexion

#root directory
MAINDIR = os.path.dirname(os.path.realpath(__file__))

class WorkerSignals(QtCore.QObject):
    result = QtCore.pyqtSignal(object)


class Worker(QtCore.QRunnable):
    '''
    Worker thread
    '''
    def __init__(self, parent):
        super(Worker, self).__init__()
        self.parent = parent

        self.signals = WorkerSignals()

    @QtCore.pyqtSlot()
    def run(self):
        while True:
            server_message, wlist, xlist = select.select([self.parent.server_connection], [], [], 0.05)
            #print(MainWindow().history)
            if len(server_message) != 0:
                # Client est de type socket
                msg_received = server_message[0].recv(1024)
                # Peut planter si le message contient des caractères spéciaux
                msg_received = msg_received.decode()

                # print(msg_received)

                #pour envoyer la liste des channels à mainWidgetOBJ
                # print(msg_received == "['salon1', 'salon2', 'salon3']")
                #
                # if msg_received.startswith('<') != True:
                #     print(msg_received.replace('\n', ' ') + 'TADATATATA')

                if msg_received.startswith('<history') and msg_received.endswith('</history>'):
                    print('HOURRAAAAAA')

                try:
                    self.parent.msgRecv(msg = msg_received)
                except:
                    print('FAILED')




class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.initWindow()
        self.buildWindow()



    def initWindow(self):
        self.setGeometry(0, 0, 1280, 720)
        self.setWindowTitle('Cryptenger')
        self.setWindowIcon(QtGui.QIcon(MAINDIR + '/assets/ico/cryptenger_icon.ico'))

        with open(MAINDIR + '/assets/css/style.css') as style:
            self.setStyleSheet(style.read())

    def buildWindow(self):
        #layout
        self.main_V_lyt = QVBoxLayout()

        #connection
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
        settings = {
            "firstName" : self.connection_widget.firstName_lne.text(),
            "secondName" : self.connection_widget.secondName_lne.text(),
            "thirdName" : self.connection_widget.thirdName_lne.text(),
            "port" : self.connection_widget.port_lne.text(),
            "adress" : self.connection_widget.adresse_lne.text(),
            }

        #check if the user have given all the required informations
        itIsOK = True
        for i in settings:
            if settings[i]=='':
                print('You must give a ' + i)
                itIsOK = False


        #if the user have given all the required informations the client starts
        if itIsOK == True:
            #close connection widget
            self.connection_widget.close()

            self.cryptenger_win = mainWidgetOBJ(
                parentObject=self,  #to close all the mainWindow
                serverName=settings['adress'],
                Username=settings['firstName']
                )
            self.main_V_lyt.addWidget(self.cryptenger_win)
            self.cryptenger_win.inputUI.input_lne.returnPressed.connect(self.msgSend)   #send message signal

            #creating a connection
            self.server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_connection.connect((settings['adress'], int(settings['port'])))
            print("Connection established on the port", settings['port'])

            #starting server
            self.threadpool = QtCore.QThreadPool()
            print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

            worker = Worker(parent = self)
            self.threadpool.start(worker)


    def msgSend(self):
        message = self.cryptenger_win.inputUI.input_lne.text()
        if message != '':
            """select channel"""
            try:        #PARCE QU IL FAUT SELECTIONNER UN CHANNEK D ABORD (plutard on le setera parr default)
                channel = self.cryptenger_win.getCurrrentIndex(listWidget=self.cryptenger_win.channelsList)
                # print("CHANNEL", +channel)
            except:
                channel = 0     #si on a pas encorer changé de channel en cliquant sur la listWidget
            message = "<channel>" + str(channel) + "<channel>" + message
            self.server_connection.send(message.encode())
            #add the message to the channel object
            """a rajouter : """
            #self.cryptenger_win.addMessage(msgToAdd=message, channel=0) #TEMP CHANNEL PR L INSTANT ON LE SET A LA MAIN
            self.cryptenger_win.inputUI.input_lne.setText('')   #c'est peut etre de la que vient le bug d'atom des multiples messages

            if message == "fin":
                QCoreApplication.instance().quit



            """ADD THE TEXT TO THE UI"""
            self.cryptenger_win.addMessageToAChannel(msg = message, channel = channel)


    def msgRecv(self, msg):
        print("Signal reçu")
        print(msg)

        # test pour l'historique
        if '<history>' in msg:
            print('GAGNE\n')
            list = msg.split('history')
            # print(list)
            # list.remove(list[0])
            # list.remove(list[-1])
            # print(list)
            history = list[1]
            # print('history : : : : : ' + history)


            self.cryptenger_win.historics.append(history)
            #le nouvel historique
            print(self.cryptenger_win.historics)


        channel = self.cryptenger_win.getCurrrentIndex(listWidget=self.cryptenger_win.channelsList)
        # print("channel --> " + str(channel))
        #self.cryptenger_win.addMessageToAChannel(msg = msg, channel = channel)
        self.cryptenger_win.channels[channel].addMessageToTheChannel(msg)







if __name__ == "__main__":

    app = QApplication([])
    window = MainWindow()
    app.exec_()
