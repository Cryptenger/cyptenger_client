import sys, random, os, functools, datetime, json

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *
#from importlib import reload
#root directory
MAINDIR = os.path.dirname(os.path.realpath(__file__))

class connectionWidgetOBJ(QWidget):
    """docstring for connectionWidgetOBJ."""

    def __init__(self, *args, **kwargs):
        super(connectionWidgetOBJ, self).__init__(*args, **kwargs)
        self.buildWidget()
        self.setStyleSheet('''QWidget{margin-left: 20em; margin-right: 20em}''')

    def buildWidget(self):
        #******************
        #layout
        #******************
        self.main_V_lyt = QVBoxLayout()
        self.main_V_lyt.setAlignment(QtCore.Qt.AlignVCenter)
        self.setLayout(self.main_V_lyt)

        #******************
        #objects
        #******************
        self.main_V_lyt.addStretch()

        #flag
        cryptenger_flag_lyt = QHBoxLayout()
        cryptenger_flag_lyt.setAlignment(QtCore.Qt.AlignCenter)

        cryptenger_logo = QLabel("Cryptenger")
        pixmap = QtGui.QPixmap(MAINDIR + "/assets/img/cryptenger_flag.jpg")
        pixmap = pixmap.scaled(1000, 200, aspectRatioMode=QtCore.Qt.KeepAspectRatioByExpanding)
        # cryptenger_logo.setObjectName('Pixmap')
        cryptenger_logo.setPixmap(pixmap)
        cryptenger_flag_lyt.addWidget(cryptenger_logo)

        cryptenger_flag = QWidget()
        cryptenger_flag.setLayout(cryptenger_flag_lyt)
        cryptenger_flag.setFixedHeight(170)
        cryptenger_flag.setStyleSheet("""border-color: transparent""")
        self.main_V_lyt.addWidget(cryptenger_flag)

        self.main_V_lyt.addStretch()

        #input
        name1_lb = QLabel('First name : ')
        self.firstName_lne = QLineEdit()
        self.firstName_lne.setPlaceholderText('Boby')
        self.main_V_lyt.addWidget(name1_lb)
        self.main_V_lyt.addWidget(self.firstName_lne)

        name2_lb = QLabel('\nSecond name : ')
        self.secondName_lne = QLineEdit()
        self.secondName_lne.setPlaceholderText('Bob')
        self.main_V_lyt.addWidget(name2_lb)
        self.main_V_lyt.addWidget(self.secondName_lne)

        name3_lb = QLabel('\nThird name : ')
        self.thirdName_lne = QLineEdit()
        self.thirdName_lne.setPlaceholderText('Bobu')
        self.main_V_lyt.addWidget(name3_lb)
        self.main_V_lyt.addWidget(self.thirdName_lne)

        adresse_lb = QLabel('\nAdress : ')
        self.adresse_lne = QLineEdit()
        self.adresse_lne.setPlaceholderText('localhost')
        self.main_V_lyt.addWidget(adresse_lb)
        self.main_V_lyt.addWidget(self.adresse_lne)

        port_lb = QLabel('\nPort : ')
        self.port_lne = QLineEdit()
        self.port_lne.setPlaceholderText('25565')
        self.main_V_lyt.addWidget(port_lb)
        self.main_V_lyt.addWidget(self.port_lne)

        space_lb = QLabel('\n')
        self.start_btn = QPushButton('Connection')
        #self.start_btn.setStyleSheet("align-item: center")
        self.main_V_lyt.addWidget(space_lb)
        self.main_V_lyt.addWidget(self.start_btn)

        self.main_V_lyt.addStretch()


class mainWidgetOBJ(QWidget):
    """docstring for mainWidgetOBJ."""

    def __init__(self, parentObject, Username, serverName, *args, **kwargs):
        super(mainWidgetOBJ, self).__init__(*args, **kwargs)
        #variables
        self.leftColumnWidth = 300
        self.hudHeight = 65
        self.serverHeight = 150
        self.serverName = serverName
        self.username = Username
        self.channels = []  #objects
        self.historics = ['msg1', 'msg2', 'msg3'] #text
        self.channelsNames=['salon 1', 'salon 2', 'salon 3']
        #
        self.buildWidget()

        #the shortcut to close Cryptenger
        self.quit_action = QAction(self)
        self.quit_action.triggered.connect(functools.partial(self.quitCryptenger, toClose=parentObject))
        self.quit_action.setShortcut('Ctrl+Q')
        self.addAction(self.quit_action)


    def buildWidget(self):

        self.buildChannels()

        #layout
        self.main_grid_lyt = QGridLayout()
        self.setLayout(self.main_grid_lyt)


        self.serverUI = serverUI_OBJ(parent=self)
        self.channelsList = channelsListOBJ(parent=self, channels=self.channelsNames)


        self.userUI = userUI_OBJ(parent = self)
        self.inputUI = inputOBJ(parent = self)

        #objects settings
        self.CHANNEL_lyt = QVBoxLayout()
        self.main_grid_lyt.addLayout(self.CHANNEL_lyt, 0, 1, 2, 1)
        self.channelsList.itemClicked.connect(functools.partial(self.setChannels, listWidget=self.channelsList))

        self.setChannels(channelClicked='0')
    #***************************************************************************
    #       EVENTS
    #***************************************************************************

    def buildChannels(self):        #on initialise tous les channels au lancement de Cryptenger (on rajoute tous les messages)
        for i in range(len(self.channelsNames)):
            channel = channelOBJ(text=str(i))
            self.channels.append(channel)
            self.channels[i].messages = self.historics[i]


    def setChannels(self,  listWidget=None, channelClicked=''):          #on switch de channel des qu'on clique sur un item de la liste des channels
        if channelClicked == '':        #pour mettre le channel 0 par defaut
            channelToSet_index = self.getCurrrentIndex(listWidget)
        else:               #toutes les autres fois (a partir du moment ou on a changé de channel au moins une fois)
            channelToSet_index = int(channelClicked)
        for i in reversed(range(self.CHANNEL_lyt.count())):
            self.CHANNEL_lyt.itemAt(i).widget().setParent(None)

        index = self.main_grid_lyt.indexOf(self.channels[channelToSet_index])
        # print('INDEX ' + str(index))
        self.CHANNEL_lyt.addWidget(self.channels[channelToSet_index])


    def getCurrrentIndex(self, listWidget):
        #return 0; # COSISUS !!! ICII !!! HÉHOOOOO !!!
        return int(listWidget.currentItem().text())


    def addMessageToAChannel(self, msg, channel):
        self.channels[channel].addMessageToTheChannel(msg)


    def openSettings(self):
        """open the settings window creating an object defined in the class settingsOBJ"""
        print(('Hello world'))
        print(self.pos().x())
        print(self.pos().y())
        print(str(self.size()))
        print(self.height())
        self.settings = settingsOBJ(location=[self.pos().x(), self.pos().y()], scale=[self.width(), self.height()])

    def quitCryptenger(self, toClose):
        """ to close Cryptenger """
        toClose.close()



class serverUI_OBJ(QGroupBox):
    """docstring for serverUI_OBJ."""

    def __init__(self, parent):                     #parent : mainWidgetOBJ (d'ou cette classe est appelée)
        super(serverUI_OBJ, self).__init__()
        self.parent = parent
        self.serverWidget()

    def serverWidget(self):
        """
        this is the widget located on the top left and corner displaying the server's informations
        """
        #objects
        self.serverName_lb = QLabel(str(self.parent.serverName))
        #layout
        self.serverInf_lyt = QGridLayout()
        self.serverInf_lyt.addWidget(self.serverName_lb)
        #widget

        self.setLayout(self.serverInf_lyt)
        self.setFixedWidth(self.parent.leftColumnWidth)
        self.setFixedHeight(self.parent.serverHeight)

        #add widget to main layout
        self.parent.main_grid_lyt.addWidget(self, 0, 0)




class userUI_OBJ(QWidget):
    """docstring for userUI_OBJ."""

    def __init__(self, parent):
        super(userUI_OBJ, self).__init__()
        self.parent = parent
        self.buildUserUI()

    def buildUserUI(self):
        #objects
        self.settings_btn = QPushButton(QtGui.QIcon(MAINDIR+"/assets/img/settings_icon.png"), '')
        self.settings_btn.clicked.connect(self.parent.openSettings)
        lb = QLabel(self.parent.username)

        #layout
        self.hud_lyt = QHBoxLayout()
        self.hud_lyt.addWidget(self.settings_btn)
        self.hud_lyt.addWidget(lb)

        #widget
        self.setLayout(self.hud_lyt)
        self.setFixedWidth(self.parent.leftColumnWidth)
        self.setFixedHeight(self.parent.hudHeight)

        #add widget to main layout
        self.parent.main_grid_lyt.addWidget(self, 2, 0, 1, 1)



class channelsListOBJ(QListWidget):
    """docstring for channelsListOBJ."""

    def __init__(self, parent, channels = []):
        super(channelsListOBJ, self).__init__()

        self.parent = parent
        self.channelsSENT = channels    #liste contenant toutes les infos à entrer dans les channels
        self.selectChannelsWidgetList = []       #liste contenant tous les item pour sélectionner les channels
        self.buildChannelsList()

    def buildChannelsList(self):

        for i in range(len(self.channelsSENT)):
            # print(self.channelsSENT[i])
            #item
            item = QListWidgetItem(str(i))  #le i est pour avoir un index pour sélectionner plus tard le bon channel quand on cliquera dessus
            #widget
            widget = QWidget()
            lyt = QHBoxLayout()
            widget.setLayout(lyt)
            lb = QLabel(self.channelsSENT[i])
            lyt.addWidget(lb)

            item.setSizeHint(widget.sizeHint())

            self.setFixedWidth(self.parent.leftColumnWidth)

            self.selectChannelsWidgetList.append(widget)
            self.addItem(item)
            self.setItemWidget(item, widget)


        self.parent.main_grid_lyt.addWidget(self, 1, 0)



class channelOBJ(QScrollArea):
    """docstring for channelOBJ."""

    def __init__(self, text, *args, **kwargs):
        super(channelOBJ, self).__init__(*args, **kwargs)
        self.messages = []

        #layout
        self.channel_lyt = QVBoxLayout()
        #self.setLayout(self.channel_lyt)

        #widget
        widget = QWidget()
        widget.setLayout(self.channel_lyt)

        #scroll widget
        self.setWidget(widget)
        self.setWidgetResizable(True)

        #debug label
        lb = QLabel(str(text))
        self.channel_lyt.addWidget(lb)



    #add message to the channel
    def addMessageToTheChannel(self, message):
        message = messagesOBJ(message=message)                                  #on déclare l'objet messagesOBJ  (on ajoute le message à l'UI)
        self.channel_lyt.addWidget(message)




class messagesOBJ(QGroupBox):
    """docstring for messagesOBJ."""

    def __init__(self, message, *args, **kwargs):
        super(messagesOBJ, self).__init__(*args, **kwargs)
        #layout
        self.lyt = QHBoxLayout()
        self.setLayout(self.lyt)
        self.setFixedHeight(50)

        #messageProcessing
        messageJSON = json.loads(message)
        # print(type(messageJSON))
        messageJSON =  messageJSON["messageType"]

        #colors
        color = [random.randint(0, 255), random.randint(100, 190), random.randint(200, 255)]
        values = "{h}, {s}, {v}".format(
        h = color[0],
        s = color[1],
        v = color[2],
        )

        #hour
        hour_lb = QLabel(messageJSON["date"]["hour"])
        hour_lb.setFixedWidth(50)
        self.lyt.addWidget(hour_lb)

        #pseudo
        pseudo_lb = QLabel(messageJSON["username"])
        pseudo_lb.setFixedWidth(100)
        pseudo_lb.setAutoFillBackground(True)
        pseudo_lb.setStyleSheet("QLabel{color: hsv("+values+")}")
        self.lyt.addWidget(pseudo_lb)

        #circle
        circle = QLabel()
        circle.setStyleSheet("QLabel{border: 2px solid transparent;border-radius: 25px;min-height: 20px;min-width: 20px;background-color: hsv("+values+");}")
        circle.setFixedWidth(50)
        circle.setFixedHeight(50)
        self.lyt.addWidget(circle)

        #message
        message_lb = QLabel(messageJSON["message"])
        self.lyt.addWidget(message_lb)


class inputOBJ(QWidget):
    """docstring for inputOBJ."""

    def __init__(self, parent):
        super(inputOBJ, self).__init__()
        self.parent = parent
        self.buildInput()

    def buildInput(self):
        """
        the input line where we hit the message
        """
        #objects
        self.input_lne = QLineEdit()
        self.input_lne.setPlaceholderText('Hit your message here ;-)')
        #layout
        self.input_lyt = QHBoxLayout()
        self.input_lyt.addWidget(self.input_lne)

        #widget
        self.input_widget = QWidget()
        self.input_widget.setLayout(self.input_lyt)

        #add widget to main layout
        self.parent.main_grid_lyt.addWidget(self.input_widget, 2, 1, 1, 1)



class settingsOBJ(QDialog):
    """docstring for settingsOBJ."""

    def __init__(self, scale, location=[100, 100], *args, **kwargs):
        super(settingsOBJ, self).__init__(*args, **kwargs)

        self.setGeometry(location[0]+100, location[1]+100, scale[0]/2, scale[1]/2)
        self.setWindowTitle('Settings')
        self.show()

#
