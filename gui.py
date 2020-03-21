import sys, random, os, functools

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *

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
        # cryptenger_flag_lyt.addStretch()

        cryptenger_logo = QLabel()
        cryptenger_logo.setPixmap(QtGui.QPixmap(MAINDIR + "/assets/ico/cryptenger_icon.ico"))
        cryptenger_flag_lyt.addWidget(cryptenger_logo)

        #cryptenger_flag_lyt.addStretch()

        cryptenger_title = QLabel('Cryptenger')
        cryptenger_title.setFont(QtGui.QFont("Times", 20, QtGui.QFont.Bold))
        cryptenger_flag_lyt.addWidget(cryptenger_title)

        # cryptenger_flag_lyt.addStretch()

        cryptenger_flag = QWidget()
        cryptenger_flag.setLayout(cryptenger_flag_lyt)
        cryptenger_flag.setFixedHeight(170)
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


    #***************************************************************************
    #       EVENTS
    #***************************************************************************

    def buildChannels(self):        #on initialise tous les channels au lancement de Cryptenger (on rajoute tous les messages)
        for i in range(len(self.channelsNames)):
            channel = channelOBJ(text=str(i))
            self.channels.append(channel)
            self.channels[i].messages = self.historics[i]


    def setChannels(self,  listWidget, channelClicked=''):          #on switch de channel des qu'on clique sur un item de la liste des channels
        channelToSet_index = self.getCurrrentIndex(listWidget)
        for i in reversed(range(self.CHANNEL_lyt.count())):
            self.CHANNEL_lyt.itemAt(i).widget().setParent(None)

        index = self.main_grid_lyt.indexOf(self.channels[channelToSet_index])
        # print('INDEX ' + str(index))
        self.CHANNEL_lyt.addWidget(self.channels[channelToSet_index])


    def getCurrrentIndex(self, listWidget):
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
        print('hello world ;-)')
        print(self.channelsSENT)

        for i in range(len(self.channelsSENT)):
            print(self.channelsSENT[i])
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



class channelOBJ(QWidget):
    """docstring for channelOBJ."""

    def __init__(self, text, *args, **kwargs):
        super(channelOBJ, self).__init__(*args, **kwargs)
        self.messages = []

        self.channel_lyt = QVBoxLayout()
        self.setLayout(self.channel_lyt)



        lb = QLabel(str(text))
        self.channel_lyt.addWidget(lb)



    def addMessageToTheChannel(self, message):
        label = QLabel(message)
        self.channel_lyt.addWidget(label)

        print(message)


class messagesOBJ(QGroupBox):
    """docstring for messagesOBJ."""

    def __init__(self, message, *args, **kwargs):
        super(messagesOBJ, self).__init__(*args, **kwargs)

        self.lyt = QHBoxLayout()
        self.setLayout(self.lyt)

        lb = QLabel(message)
        self.lyt.addWidget(lb)


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
