import sys, random, os

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *
from gui import mainWidgetOBJ, connectionWidgetOBJ

#Connexion au serveur
import socket
import select

host = 'localhost'
port = 25565

server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_connection.connect((host, port))
print("La connexion avec le serveur a été établie sur le port", port)
#Fin de la connexion

#root directory
MAINDIR = os.path.dirname(os.path.realpath(__file__))

class WorkerSignals(QtCore.QObject):
    result = QtCore.pyqtSignal(object)


class Worker(QtCore.QRunnable):
    '''
    Worker thread
    '''
    def __init__(self):
        super(Worker, self).__init__()

        self.signals = WorkerSignals()

    @QtCore.pyqtSlot()
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
        self.connection_widget.firstName_lne.setText('Cosius')
        self.connection_widget.secondName_lne.setText('KTN')
        self.connection_widget.thirdName_lne.setText('Moi')
        self.connection_widget.port_lne.setText('25565')
        self.connection_widget.adresse_lne.setText('localhost')





        self.history = ''

        self.button = QPushButton("Send Message")
        self.dialog = QLineEdit()
        self.messages = QTextEdit()

        self.button.clicked.connect(self.msgSend)
        self.dialog.returnPressed.connect(self.msgSend)
        self.messages.setReadOnly(True)

        #test = mainWidgetOBJ()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.messages)
        self.layout.addWidget(self.dialog)
        self.layout.addWidget(self.button)
        #self.layout.addWidget(test)

        widget = QWidget()
        widget.setLayout(self.main_V_lyt)
        self.setCentralWidget(widget)
        self.show()

        self.threadpool = QtCore.QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        worker = Worker()
        self.threadpool.start(worker)

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

            self.cryptenger_win = mainWidgetOBJ(serverName=settings['adress'], Username=settings['firstName'])
            self.main_V_lyt.addWidget(self.cryptenger_win)




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
