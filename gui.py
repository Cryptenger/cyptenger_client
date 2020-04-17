import sys, random, os, functools, datetime, json
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *
from plyer import notification

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
        pixmap = QtGui.QPixmap("./assets/img/cryptenger_flag.jpg")
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
        name1_lb = QLabel('Username : ')
        self.firstName_lne = QLineEdit()
        self.firstName_lne.setPlaceholderText('Boby')
        self.main_V_lyt.addWidget(name1_lb)
        self.main_V_lyt.addWidget(self.firstName_lne)

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
        self.start_btn.setFixedWidth(1000)
        self.connection_lyt = QHBoxLayout()
        self.connection_lyt.addWidget(self.start_btn)

        self.main_V_lyt.addWidget(space_lb)
        self.main_V_lyt.addLayout(self.connection_lyt)
        self.main_V_lyt.addStretch()


class mainWidgetOBJ(QWidget):
    """docstring for mainWidgetOBJ."""

    def __init__(self, parentObject, Username, serverName, channelsNames, *args, **kwargs):
        super(mainWidgetOBJ, self).__init__(*args, **kwargs)
        #variables
        self.app_settings = parentObject.app_settings
        self.serverName = serverName
        self.username = Username
        self.channels = []  #objects
        self.channelsNames= channelsNames #['salon 1', 'salon 2', 'salon 3']
        #
        self.buildWidget()

        #the shortcut to close Cryptenger
        self.quit_action = QAction(self)
        self.quit_action.triggered.connect(functools.partial(self.quitCryptenger, toClose=parentObject))
        self.quit_action.setShortcut(self.app_settings["shortcuts"]["quit_cryptenger"])
        self.addAction(self.quit_action)


    def buildWidget(self):

        self.buildChannels()

        #layout
        self.main_grid_lyt = QGridLayout()
        # self.main_grid_lyt.setHorizontalSpacing(2)      #STYLE
        # self.main_grid_lyt.setVerticalSpacing(2)
        self.setLayout(self.main_grid_lyt)


        self.serverUI = serverUI_OBJ(parent=self)
        self.channelsList = channelsListOBJ(parent=self, channels=self.channelsNames)


        self.userUI = userUI_OBJ(parent = self)
        self.inputUI = inputOBJ(parent = self)

        self.userList = usersListOBJ(parent = self)

        #objects settings
        self.CHANNEL_lyt = QVBoxLayout()

        self.main_grid_lyt.addLayout(self.CHANNEL_lyt, 0, 1, 2, 1)
        self.channelsList.itemClicked.connect(functools.partial(self.setChannels, listWidget=self.channelsList))


        self.setChannels(channelClicked='0')
    #***************************************************************************
    #       EVENTS
    #***************************************************************************

    def buildChannels(self):
        """on initialise tous les channels au lancement de Cryptenger"""
        for i in range(len(self.channelsNames)):
            channel = channelOBJ(text=str(i))
            self.channels.append(channel)



    def setChannels(self,  listWidget=None, channelClicked=''):          #
        """on switch de channel des qu'on clique sur un item de la liste des channels"""
        if channelClicked == '':        #pour mettre le channel 0 par defaut
            channelToSet_index = self.getCurrrentIndex(listWidget)
            self.channels[channelToSet_index].scrollDown()                  #A VOIR
        else:               #toutes les autres fois (a partir du moment ou on a changé de channel au moins une fois)
            channelToSet_index = int(channelClicked)

        self.channels[channelToSet_index].scrollDown()                      #A VOIR

        for i in reversed(range(self.CHANNEL_lyt.count())):
            self.CHANNEL_lyt.itemAt(i).widget().setParent(None)

        index = self.main_grid_lyt.indexOf(self.channels[channelToSet_index])
        # print('INDEX ' + str(index))
        self.CHANNEL_lyt.addWidget(self.channels[channelToSet_index])

        self.changeNotif(channelToSet_index, reset=True)


    def getCurrrentIndex(self, listWidget):
        """on récupère l'index du channel actuellement sélectionné"""
        return int(listWidget.currentItem().text())


    def addMessageToAChannel(self, msg, channel, coloration, isHistory = False, addNotif=False):
        """dit au channel de s'ajouter son message ;-)"""
        self.channels[channel].addMessageToTheChannel(msg, coloration)

        if self.channelsList.selectChannelsWidgetList[channel].newMsg == 0:
            # print("ONE")
            pass

        if addNotif != False:


            if self.app_settings["notifications"]["cryptenger_notif"] == True:
                self.changeNotif(channel)

            if  self.app_settings["notifications"]["desktop_notif"] == True:
                message = json.loads(msg)

                notification.notify(
                    app_name="Cryptenger",
                    title= message["messageType"]["username"],
                    message= message["messageType"]["message"],
                    app_icon=self.app_settings["cryptenger_icon"],  # e.g. 'C:\\icon_32x32.ico'
                    timeout=5,  # seconds
                )

        #si ce n'est pas l'historique ca veut dier que le message vient de quelqu'un de connecté donc on l'ajoute à la user list
        if isHistory == False:
            # self.cryptenger_win.user_list.add_user_to_list()
            message = json.loads(msg)
            self.userList.add_user_to_list(username=message["messageType"]["username"])


    def changeNotif(self, channel, reset=False):
        """change le nombre de notifications
        reset : True: on remet le compteur à 0; False : on ajoute 1
        """
        if reset :
            self.channelsList.selectChannelsWidgetList[channel].newMsg = 0
            self.channelsList.selectChannelsWidgetList[channel].notif.setText("")
        else:
            self.channelsList.selectChannelsWidgetList[channel].newMsg += 1
            notif_txt = "  " + str(self.channelsList.selectChannelsWidgetList[channel].newMsg) + "  "
            self.channelsList.selectChannelsWidgetList[channel].notif.setText(notif_txt)

    def openSettings(self):
        """open the settings window creating an object defined in the class settingsOBJ"""
        print(('Hello world'))
        print(self.pos().x())
        print(self.pos().y())
        print(str(self.size()))
        print(self.height())
        self.settings = settingsOBJ(parent=self, location=[self.pos().x(), self.pos().y()], scale=[self.width(), self.height()])

    def quitCryptenger(self, toClose):
        """ to close Cryptenger """
        toClose.close()



class usersListOBJ(QGroupBox):
    """La liste des utilisateurs actuellement connectés au serveur"""

    def __init__(self, parent):
        super(usersListOBJ, self).__init__()
        self.parent = parent
        self.connected_users = []

        self.setFixedWidth(self.parent.app_settings["cryptenger_win"]["right_column_width"])

        connected_members_lb = QLabel('Connected members')
        connected_members_lb.setObjectName("groupbox_title")

        self.user_list = QListWidget()
        self.user_list.setStyleSheet('border: 0px')
        for i in self.connected_users:
            item = QListWidgetItem()

            widget = channelItemOBJ(channelName = i, is_a_channel=False)
            item.setSizeHint(widget.sizeHint())

            self.user_list.addItem(item)
            self.user_list.setItemWidget(item, widget)

        self.user_list_lyt = QVBoxLayout(self)
        self.user_list_lyt.addWidget(connected_members_lb)
        self.user_list_lyt.addWidget(self.user_list)
        self.setLayout(self.user_list_lyt)

        self.parent.main_grid_lyt.addWidget(self, 0, 2, 3, 1)

    def add_user_to_list(self, username):
        if username not in self.connected_users:
            item = QListWidgetItem()

            widget = channelItemOBJ(channelName = username, is_a_channel=False)
            item.setSizeHint(widget.sizeHint())

            self.user_list.addItem(item)
            self.user_list.setItemWidget(item, widget)
            self.connected_users.append(username)
        print('hello')

class usersListItemOBJ(QGroupBox):
    """docstring for usersListItemOBJ."""

    def __init__(self):
        super(usersListItemOBJ, self).__init__()
        pass




class channelsListOBJ(QListWidget):
    """La liste des boutons sur lesquels on clique pour sélectionner un channel"""

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
            font = QtGui.QFont('SansSerif', 1)
            # font.setStyleSheet('color: red')
            item.setFont(font)       #loul le 1 c'est pour cacherr cet index
            # item.setPalette()
            #widget

            widget = channelItemOBJ(channelName = self.channelsSENT[i])
            # print(self.channelsSENT[i]) Debug pour afficher les channels

            item.setSizeHint(widget.sizeHint())

            self.setFixedWidth(self.parent.app_settings["cryptenger_win"]["left_column_width"])

            self.selectChannelsWidgetList.append(widget)
            self.addItem(item)
            self.setItemWidget(item, widget)


        self.parent.main_grid_lyt.addWidget(self, 1, 0)

class channelItemOBJ(QWidget):
    """Le bouton sur lequel on clique quand on sélectionne un channel."""

    def __init__(self, channelName, is_a_channel=True):
        super(channelItemOBJ, self).__init__()
        self.newMsg = 0

        self.setStyleSheet('border: 0px')

        self.channelsListOBJ_layout = QHBoxLayout()

        channel_name = QLabel(channelName)
        channel_name.setStyleSheet("""
            text-align: left;
            padding-left: 1em;
            background: transparent;
            """)

        self.channelsListOBJ_layout.addWidget(channel_name)

        self.channelsListOBJ_layout.addStretch()

        if is_a_channel == True:
            channel_name.setStyleSheet("""
                text-align: left;
                padding-left: 1em;
                background: transparent;
                min-width: 10em;
                """)

            self.notif = QLabel(str(self.newMsg))
            self.notif.setStyleSheet("background: #7f7f7f; border-radius: 5px")
            self.channelsListOBJ_layout.addWidget(self.notif)

        self.setLayout(self.channelsListOBJ_layout)

class channelOBJ(QScrollArea):
    """Le channel lui même contenant les messages"""

    def __init__(self, text, *args, **kwargs):
        super(channelOBJ, self).__init__(*args, **kwargs)
        # self.messagesList = []
        #layout
        main_lyt = QVBoxLayout()                                                #layout contenant les deux autres layouts
        #messages layout
        self.channel_lyt = QVBoxLayout()                                        #premier layout : contient les messages
        main_lyt.addLayout(self.channel_lyt)
        #focus_lyt
        focus_lyt = QVBoxLayout()                                               #deuxième layout : on met un label dessus et on focusle label
        main_lyt.addLayout(focus_lyt)
        self.space_lb = QLabel('')
        self.space_lb.setFont(QtGui.QFont('SansSerif', 30))
        focus_lyt.addWidget(self.space_lb)

        #widget
        widget = QWidget()
        widget.setLayout(main_lyt)
        self.setWidget(widget)
        self.setWidgetResizable(True)

        widget.setObjectName('box')
        # self.setObjectName('box')

    #add message to the channel
    def addMessageToTheChannel(self, message, coloration):
        message = messagesOBJ(parent=self, message=message, coloration=coloration)                                  #on déclare l'objet messagesOBJ  (on ajoute le message à l'UI)
        self.channel_lyt.addWidget(message)
        #scroll focus toujours le bas de la liste des messages

        # self.messagesList.append(message)
        # print(self.messagesList)

        self.scrollDown()


    def scrollDown(self):
        self.ensureWidgetVisible(self.space_lb)     #, 500, 200
        # self.ensureWidgetVisible(self.messagesList[-1])
        # self.ensureVisible(0, 50, 0, 0)
        # print("scroll")


    # def scrollDownFar(self):
        # self.ensureWidgetVisible(self.messagesList[-1].message_lb)
        # print(self.messagesList[-1].index())

class messagesOBJ(QGroupBox):
    """Le message qu'on va ajouter au channel"""

    def __init__(self, parent, message, coloration, *args, **kwargs):
        super(messagesOBJ, self).__init__(*args, **kwargs)
        #layout
        self.lyt = QHBoxLayout()
        self.setLayout(self.lyt)
        self.setFixedHeight(50)
        self.setStyleSheet("border: 0px")
        self.setObjectName("messagesOBJ")

        #messageProcessing
        messageJSON = json.loads(message)
        # print(type(messageJSON))
        messageJSON =  messageJSON["messageType"]

        #colors
        # color = [random.randint(0, 255), random.randint(100, 190), random.randint(200, 255)]
        values = "{h}, {s}, {v}".format(
        h = coloration[0],
        s = coloration[1],
        v = coloration[2],
        )

        #hour
        hour_lb = QLabel(messageJSON["date"]["hour"])
        hour_lb.setFixedWidth(50)
        self.lyt.addWidget(hour_lb)

        #circle
        circle = QLabel()

        # painter = QtGui.QPainter(circle)
        # painter.setPen(QtGui.QPen(QtGui.QColor(1, 1, 1), 5, QtCore.Qt.SolidLine))
        # painter.setBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255), QtCore.Qt.SolidPattern))
        # painter.begin(circle)
        # painter.drawRect(200, 200, 200, 200)


        circle.setFixedWidth(30)
        circle.setFixedHeight(30)
        circle.setStyleSheet("QLabel{border: 2px solid transparent;border-radius: 25px;min-height: 20px;min-width: 20px;background-color: hsv("+values+");}")
        self.lyt.addWidget(circle)

        #pseudo
        pseudo_lb = QLabel(messageJSON["username"])
        pseudo_lb.setFixedWidth(100)
        pseudo_lb.setAutoFillBackground(True)
        pseudo_lb.setStyleSheet("QLabel{color: hsv("+values+")}")
        self.lyt.addWidget(pseudo_lb)


        #message
        # self.message_lb = QLabel(messageJSON["message"])
        self.message_lb = QTextEdit(messageJSON["message"])
        self.message_lb.setReadOnly(True)
        self.message_lb.setStyleSheet("border: 0px")
        self.lyt.addWidget(self.message_lb)

        self.setStyleSheet('box')




class inputOBJ(QGroupBox):
    """Là où on entre le message à tapper"""

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
        self.input_lne.setStyleSheet("border: 0px solid transparent")
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
    """Ben les settings quoi..."""

    def __init__(self, parent, scale, location=[100, 100], *args, **kwargs):
        super(settingsOBJ, self).__init__(*args, **kwargs)

        self.setGeometry(location[0]+100, location[1]+100, scale[0]/2, scale[1]/2)
        self.setWindowIcon(QtGui.QIcon('./assets/ico/cryptenger_icon.ico'))
        self.setWindowTitle('Settings')
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.show()

        with open(parent.app_settings["default_style"]) as style:
            self.setStyleSheet(style.read())



class serverUI_OBJ(QGroupBox):
    """Le carré en haut à gauche ou ya des infos sur le serveur"""

    def __init__(self, parent):                     #parent : mainWidgetOBJ (d'ou cette classe est appelée)
        super(serverUI_OBJ, self).__init__()
        self.parent = parent
        self.serverWidget()

    def serverWidget(self):
        """
        this is the widget located on the top left and corner displaying the server's informations
        """
        #objects
        serverInfos = QLabel("About server\n")
        serverInfos.setObjectName("groupbox_title")
        self.serverName_lb = QLabel(str(self.parent.serverName))
        #layout
        self.serverInf_lyt = QGridLayout()
        self.serverInf_lyt.addWidget(serverInfos)
        self.serverInf_lyt.addWidget(self.serverName_lb)
        #widget

        self.setLayout(self.serverInf_lyt)
        self.setFixedWidth(self.parent.app_settings["cryptenger_win"]["left_column_width"])
        self.setFixedHeight(self.parent.app_settings["cryptenger_win"]["server_ui_height"])

        #add widget to main layout
        self.parent.main_grid_lyt.addWidget(self, 0, 0)


class userUI_OBJ(QGroupBox):
    """Le carré en bas à gauche ou ya des infos sur le user et ou on peut ouvrir les settings"""

    def __init__(self, parent):
        super(userUI_OBJ, self).__init__()
        self.parent = parent
        self.buildUserUI()

    def buildUserUI(self):
        #objects
        username = QLabel(self.parent.username)
        self.settings_btn = QPushButton(QtGui.QIcon("./assets/img/settings_icon.png"), '')
        self.settings_btn.setStyleSheet('border: 0px solid transparent')
        self.settings_btn.clicked.connect(self.parent.openSettings)

        #layout
        self.hud_lyt = QHBoxLayout()
        self.hud_lyt.addWidget(username)
        self.hud_lyt.addStretch()
        self.hud_lyt.addWidget(self.settings_btn)

        #widget
        self.setLayout(self.hud_lyt)
        self.setFixedWidth(self.parent.app_settings["cryptenger_win"]["left_column_width"])
        self.setFixedHeight(self.parent.app_settings["cryptenger_win"]["user_ui_height"])

        #add widget to main layout
        self.parent.main_grid_lyt.addWidget(self, 2, 0, 1, 1)
