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
        #
        self.buildWidget()
        #the shortcut to close Cryptenger
        self.quit_action = QAction(self)
        self.quit_action.triggered.connect(functools.partial(self.quitCryptenger, toClose=parentObject))
        self.quit_action.setShortcut('Ctrl+Q')
        self.addAction(self.quit_action)

    def buildWidget(self):
        #layout
        self.main_grid_lyt = QGridLayout()
        self.setLayout(self.main_grid_lyt)


        self.serverWidget()
        self.channelsWidget()
        #self.messagesWidget()

        self.hudWidget()
        self.inputWidget()

        #objects settings

    #***************************************************************************
    #       WIDGETS
    #***************************************************************************
    def serverWidget(self):
        """
        this is the widget located on the top left and corner displaying the server's informations
        """
        #objects
        self.serverName_lb = QLabel(str(self.serverName))
        #layout
        self.serverInf_lyt = QGridLayout()
        self.serverInf_lyt.addWidget(self.serverName_lb)
        #widget
        self.serverInf_widget = QGroupBox()
        self.serverInf_widget.setLayout(self.serverInf_lyt)
        self.serverInf_widget.setFixedWidth(self.leftColumnWidth)
        self.serverInf_widget.setFixedHeight(self.serverHeight)

        #add widget to main layout
        self.main_grid_lyt.addWidget(self.serverInf_widget, 0, 0)

    def channelsWidget(self):
        """
        """
        #layout
        self.channels_lyt = QVBoxLayout()
        self.channels_lyt.setAlignment(QtCore.Qt.AlignTop)
        #objects
        self.channels_list_names = ["general", "presentation", "rank"]
        self.channels_list_widgets = []
        self.channels = []

        for i in range(len(self.channels_list_names)):
            #channel button
            button = QPushButton(str(self.channels_list_names[i]))
            button.clicked.connect(functools.partial(self.setChannel, channel=i))

            lyt = QHBoxLayout()
            lyt.addWidget(button)

            widget = QGroupBox()
            widget.setLayout(lyt)
            widget.setStyleSheet("""QGroupBox{border: 0px}""")
            self.channels_list_widgets.append(widget)
            self.channels_lyt.addWidget(self.channels_list_widgets[i])

            channel = channelMessagesOBJ(text=self.channels_list_names[i])
            self.channels.append(channel)

            """"""


        #set the default channel
        self.setChannel(channel=0)

        #widget
        self.channels_widget = QWidget()
        self.channels_widget.setLayout(self.channels_lyt)
        self.channels_widget.setFixedWidth(self.leftColumnWidth)

        #add widget to main layout
        self.main_grid_lyt.addWidget(self.channels_widget, 1, 0)
        print(self.channels_list_widgets)



    def hudWidget(self):
        """
        """
        #objects
        self.settings_btn = QPushButton(QtGui.QIcon(MAINDIR+"/assets/img/settings_icon.png"), '')
        self.settings_btn.clicked.connect(self.openSettings)
        lb = QLabel(self.username)

        #layout
        self.hud_lyt = QHBoxLayout()
        self.hud_lyt.addWidget(self.settings_btn)
        self.hud_lyt.addWidget(lb)

        #widget
        self.hud_widget = QWidget()
        self.hud_widget.setLayout(self.hud_lyt)
        self.hud_widget.setFixedWidth(self.leftColumnWidth)
        self.hud_widget.setFixedHeight(self.hudHeight)

        #add widget to main layout
        self.main_grid_lyt.addWidget(self.hud_widget, 2, 0, 1, 1)

    def inputWidget(self):
        """
        the input line where we hit the message
        """
        #objects
        self.input_lne = QLineEdit()
        #layout
        self.input_lyt = QHBoxLayout()
        self.input_lyt.addWidget(self.input_lne)

        #widget
        self.input_widget = QWidget()
        self.input_widget.setLayout(self.input_lyt)

        #add widget to main layout
        self.main_grid_lyt.addWidget(self.input_widget, 2, 1, 1, 1)


    #***************************************************************************
    #       EVENTS
    #***************************************************************************

    def openSettings(self):
        """open the settings window creating an object defined in the class settingsOBJ"""
        print(('Hello world'))
        print(self.pos().x())
        print(self.pos().y())
        print(str(self.size()))
        print(self.height())
        self.settings = settingsOBJ(location=[self.pos().x(), self.pos().y()], scale=[self.width(), self.height()])

    def setChannel(self, channel):
        print("channel changed to : " + str(channel))
        # self.currentChannel = channelMessagesOBJ(text=self.channels_list_names[channel])
        # pos = self.main_grid_lyt.getItemPosition(self.channels[0])
        # print(pos)
        # self.main_grid_lyt.itemAt(0, 1, 2, 1).widget().setParent(None)
        self.main_grid_lyt.addWidget(self.channels[channel], 0, 1, 2, 1)

    def addMessage(self, msgToAdd, channel):
        print('loul')
        self.channels[channel].messages.append(msgToAdd)
        message = messagesOBJ(self.channels[channel].messages[channel])

        #self.channels[channel].channel_lyt =
        self.channels[channel].channel_lyt.addWidget(message)


        #c'est le self qui pose pb : mettre l'objet en argument

    def quitCryptenger(self, toClose):
        """ to close Cryptenger """
        toClose.close()

class channelMessagesOBJ(QWidget):
    """docstring for channelMessagesOBJ."""

    def __init__(self, text, *args, **kwargs):
        super(channelMessagesOBJ, self).__init__(*args, **kwargs)
        self.messages = []

        self.channel_lyt = QVBoxLayout()
        self.setLayout(self.channel_lyt)

        lb = QLabel(text)
        self.channel_lyt.addWidget(lb)


class messagesOBJ(QGroupBox):
    """docstring for messagesOBJ."""

    def __init__(self, message, *args, **kwargs):
        super(messagesOBJ, self).__init__(*args, **kwargs)

        self.lyt = QHBoxLayout()
        self.setLayout(self.lyt)

        lb = QLabel(message)
        self.lyt.addWidget(lb)



class settingsOBJ(QDialog):
    """docstring for settingsOBJ."""

    def __init__(self, scale, location=[100, 100], *args, **kwargs):
        super(settingsOBJ, self).__init__(*args, **kwargs)

        self.setGeometry(location[0]+100, location[1]+100, scale[0]/2, scale[1]/2)
        self.setWindowTitle('Settings')
        self.show()








#
