import sys, random, os, functools, datetime, json
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *
#notifications
from plyer import notification
#identicon
from identicon import Identicon
from PIL.ImageQt import ImageQt

class connectionWidgetOBJ(QWidget):
    """docstring for connectionWidgetOBJ."""

    def __init__(self, *args, **kwargs):
        super(connectionWidgetOBJ, self).__init__(*args, **kwargs)
        self.buildWidget()
        self.setStyleSheet('''QLabel#user, QLineEdit, QPushButton{margin-left: 15em; margin-right: 15em}''')

    def buildWidget(self):
        #flag
        pixmap = QtGui.QPixmap("./assets/img/cryptenger_flag.jpg")
        cryptenger_logo = QLabel()
        cryptenger_logo.setPixmap(pixmap)

        cryptenger_flag_lyt = QHBoxLayout()
        cryptenger_flag_lyt.setAlignment(QtCore.Qt.AlignCenter)
        cryptenger_flag_lyt.addWidget(cryptenger_logo)

        #input
        name1_lb = QLabel('Username : ')
        name1_lb.setObjectName("user")
        self.firstName_lne = QLineEdit()
        self.firstName_lne.setPlaceholderText('Boby')

        adresse_lb = QLabel('\nAdress : ')
        adresse_lb.setObjectName("user")
        self.adresse_lne = QLineEdit()
        self.adresse_lne.setPlaceholderText('localhost')

        port_lb = QLabel('\nPort : ')
        port_lb.setObjectName("user")
        self.port_lne = QLineEdit()
        self.port_lne.setPlaceholderText('25565')

        space_lb = QLabel('\n')
        space_lb.setObjectName("user")
        self.start_btn = QPushButton('Connection')
        self.start_btn.setFixedWidth(1000)
        self.start_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.connection_lyt = QHBoxLayout()
        self.connection_lyt.addWidget(self.start_btn)

        self.main_V_lyt = QVBoxLayout()
        self.main_V_lyt.setAlignment(QtCore.Qt.AlignVCenter)
        self.main_V_lyt.addStretch()
        self.main_V_lyt.addLayout(cryptenger_flag_lyt)
        self.main_V_lyt.addStretch()
        self.main_V_lyt.addWidget(name1_lb)
        self.main_V_lyt.addWidget(self.firstName_lne)
        self.main_V_lyt.addWidget(adresse_lb)
        self.main_V_lyt.addWidget(self.adresse_lne)
        self.main_V_lyt.addWidget(port_lb)
        self.main_V_lyt.addWidget(self.port_lne)
        self.main_V_lyt.addWidget(space_lb)
        self.main_V_lyt.addLayout(self.connection_lyt)
        self.main_V_lyt.addStretch()
        self.setLayout(self.main_V_lyt)




class mainWidgetOBJ(QWidget):
    """docstring for mainWidgetOBJ."""

    def __init__(self, parentObject, Username, serverName, channelsNames, *args, **kwargs):
        super(mainWidgetOBJ, self).__init__(*args, **kwargs)
        #variables
        self.app_settings = parentObject.app_settings
        self.parentObject = parentObject
        self.serverName = serverName
        self.username = Username
        self.channels = []  #channelOBJ objects : QScrollArea : les objets channels contenant les messages
        self.channelsNames= channelsNames   #seulement le nom des channels dans une liste de strings

        self.buildWidget()

        #the shortcut to close Cryptenger
        self.quit_action = QAction(self)
        self.quit_action.triggered.connect(functools.partial(self.quitCryptenger, toClose=parentObject))
        self.quit_action.setShortcut(self.app_settings["shortcuts"]["quit_cryptenger"])
        self.addAction(self.quit_action)

        self.restart_action = QAction(self)
        self.restart_action.triggered.connect(functools.partial(self.restartCryptenger))
        self.restart_action.setShortcut(self.app_settings["shortcuts"]["restart_cryptenger"])
        self.addAction(self.restart_action)



    def buildWidget(self):

        #layout
        self.main_grid_lyt = QGridLayout()
        # self.main_grid_lyt.setHorizontalSpacing(2)      #STYLE
        # self.main_grid_lyt.setVerticalSpacing(2)
        self.setLayout(self.main_grid_lyt)

        #left column
        self.serverUI = serverUI_OBJ(parent=self)
        self.channelsList = channelsListOBJ(parent=self, channels=self.channelsNames)
        self.userUI = userUI_OBJ(parent = self)

        #middle column
        #on crée tous les channels (QScrollArea) contenant les messages et on les ajoute à la liste self.channels
        self.buildChannels()
        self.inputUI = inputOBJ(parent = self)

        #right column
        self.userList = usersListOBJ(parent = self)

        #objects settings
        self.CHANNEL_lyt = QVBoxLayout()
        self.main_grid_lyt.addLayout(self.CHANNEL_lyt, 0, 1, 2, 1)
        #slot : chaque fois qu'on clique sur un channel ca change le channelOBJ actuel
        self.channelsList.channel_list_widget.itemClicked.connect(functools.partial(self.setChannels, listWidget=self.channelsList))
        #pour activer le premier channel lors du lancement de cryptenger
        self.setChannels(channelClicked='0')


    #***************************************************************************
    #       EVENTS
    #***************************************************************************

    def buildChannels(self):
        """on crée tous les channels (channelOBJ -> QScrollArea) au lancement de Cryptenger"""
        #autant de fois qu'il y a de channels, la liste (contenant les noms) a été envoyée par le serveur
        for i in range(len(self.channelsNames)):
            channel = channelOBJ(parent=self, text=str(i))
            self.channels.append(channel)


    def setChannels(self,  listWidget=None, channelClicked=''):
        """on switch de channel des qu'on clique sur un item de la liste des channels"""
        if channelClicked == '':        #pour mettre le channel 0 par defaut
            channelToSet_index = self.getCurrrentIndex(listWidget)
            self.channels[channelToSet_index].scrollDown()
                          #A VOIR
        else:               #toutes les autres fois (a partir du moment ou on a changé de channel au moins une fois)
            channelToSet_index = int(channelClicked)
        #set current channel label infos
        self.channelsList.current_channel_lb.setText(self.channelsNames[channelToSet_index])
        #change the place holder text in the input line edit
        self.inputUI.input_lne.setPlaceholderText("Hit your message in #" + self.channelsNames[channelToSet_index])

        self.channels[channelToSet_index].scrollDown()                      #A VOIR

        for i in reversed(range(self.CHANNEL_lyt.count())):
            self.CHANNEL_lyt.itemAt(i).widget().setParent(None)

        index = self.main_grid_lyt.indexOf(self.channels[channelToSet_index])
        # print('INDEX ' + str(index))
        self.CHANNEL_lyt.addWidget(self.channels[channelToSet_index])

        self.changeNotif(channelToSet_index, reset=True)




    def getCurrrentIndex(self, listWidget):
        """on récupère l'index du channel actuellement sélectionné"""
        return int(listWidget.channel_list_widget.currentItem().text())


    def addMessageToAChannel(self, msg, channel, isHistory = False, addNotif=False):
        """dit au channel de s'ajouter son message ;-)"""
        self.channels[channel].addMessageToTheChannel(msg)

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

    def setIdenticon(self, string, background):     #could be used for channels and server too
        string_id = 0
        for i in string:
            string_id += ord(i)

        icon = Identicon(user_id = string_id, background = background)
        identicon_lb = QLabel()

        icon_img = icon.give_me_my_image()
        imageq = ImageQt(icon_img)
        qimage = QtGui.QImage(imageq)
        identicon_px = QtGui.QPixmap(qimage)
        identicon_px = identicon_px.scaled(32, 32)
        identicon_lb.setPixmap(identicon_px)

        return identicon_lb, icon.color

    # def setStyleSheetForAllWindows(self):
    #     with open(self.app_settings["default_style"]) as style_file:
    #         style = style_file.read()
    #         print(type(self.parent))
    #         self.parentObject.setStyleSheet(style)

    def openSettings(self):
        """open the settings window creating an object defined in the class settingsOBJ"""
        print(self.pos().x())
        print(self.pos().y())
        print(str(self.size()))
        print(self.height())
        self.settings = settingsOBJ(parent=self, location=[self.pos().x(), self.pos().y()], scale=[self.width(), self.height()])


    def quitCryptenger(self, toClose):
        """ to close Cryptenger """
        toClose.close()


    def restartCryptenger(self, toClose):
        """ to close Cryptenger """
        os.startfile(os.path.dirname(os.path.realpath(__file__)) +"/client.py")
        self.quitCryptenger(toClose=self.parentObject)



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

        self.total_connected_users = QLabel("Logged users : " + str(len(self.connected_users)))
        self.total_connected_users.setObjectName("groupbox_title")

        for i in self.connected_users:
            self.add_user_to_list(username=i)


        self.user_list_lyt = QVBoxLayout(self)
        self.user_list_lyt.addWidget(connected_members_lb)
        self.user_list_lyt.addWidget(self.user_list)
        self.user_list_lyt.addStretch()
        self.user_list_lyt.addWidget(self.total_connected_users)
        self.setLayout(self.user_list_lyt)

        self.parent.main_grid_lyt.addWidget(self, 0, 2, 3, 1)

    def add_user_to_list(self, username):
        if username not in self.connected_users:
            item = QListWidgetItem()

            widget = channelItemOBJ(parent=self.parent, channelName = username, is_a_channel=False)
            item.setSizeHint(widget.sizeHint())
            widget.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))   #ne fonctionne pas pour les channels

            self.user_list.addItem(item)
            self.user_list.setItemWidget(item, widget)
            self.connected_users.append(username)

            self.total_connected_users.setText("Logged users : " + str(len(self.connected_users)))

            self.total_connected_users.setText("Logged users : " + str(len(self.connected_users)))


class channelsListOBJ(QGroupBox):
    """La liste des boutons sur lesquels on clique pour sélectionner un channel"""

    def __init__(self, parent, channels = []):
        super(channelsListOBJ, self).__init__()

        self.parent = parent
        self.channelsSENT = channels    #liste contenant toutes les infos à entrer dans les channels
        self.selectChannelsWidgetList = []       #liste contenant tous les item pour sélectionner les channels
        self.buildChannelsList()
        self.setMaximumWidth(self.parent.app_settings["cryptenger_win"]["left_column_width"])

    def buildChannelsList(self):
        self.channel_list_widget = QListWidget()
        for i in range(len(self.channelsSENT)):

            widget = channelItemOBJ(parent=self.parent, channelName = self.channelsSENT[i])
            item = QListWidgetItem(str(i))  #le i est pour avoir un index pour sélectionner plus tard le bon channel quand on cliquera dessus
            font = QtGui.QFont('SansSerif', 1)
            item.setFont(font)       #loul le 1 c'est pour cacherr cet index
            item.setSizeHint(widget.sizeHint())

            self.selectChannelsWidgetList.append(widget)
            self.channel_list_widget.addItem(item)
            self.channel_list_widget.setItemWidget(item, widget)



        channels_lb = QLabel('Channels')
        channels_lb.setObjectName("groupbox_title")

        self.current_channel_lb = QLabel('current')
        self.current_channel_lb.setStyleSheet("QLabel{font-weight: bold}")

        top_infos_widget = QWidget()
        top_infos_lyt = QHBoxLayout(top_infos_widget)
        top_infos_lyt.addWidget(channels_lb)
        top_infos_lyt.addStretch()
        top_infos_lyt.addWidget(self.current_channel_lb)






        self.channel_list_lyt = QVBoxLayout(self)
        self.channel_list_lyt.addWidget(top_infos_widget)
        self.channel_list_lyt.addWidget(self.channel_list_widget)
        self.setLayout(self.channel_list_lyt)

        self.parent.main_grid_lyt.addWidget(self, 1, 0)

class channelItemOBJ(QWidget):
    """Le bouton sur lequel on clique quand on sélectionne un channel."""

    def __init__(self, parent, channelName, is_a_channel=True):
        super(channelItemOBJ, self).__init__()
        self.parent = parent
        self.newMsg = 0

        self.setStyleSheet('border: 0px')

        self.channelsListOBJ_layout = QHBoxLayout()

        if is_a_channel == True:
            color = self.parent.app_settings["cryptenger_win"]["channels_icon_color"]#"orange"
        else:
            color = self.parent.app_settings["cryptenger_win"]["users_icon_color"] #F6F6F6"

        identicon_lb, icon_color = self.parent.setIdenticon(string=channelName, background=color)
        self.channelsListOBJ_layout.addWidget(identicon_lb)

        channel_name = QLabel(channelName)
        channel_name.setStyleSheet("""
            text-align: left;
            padding-left: 1em;
            background: transparent;
            """)

        self.channelsListOBJ_layout.addWidget(channel_name)

        self.channelsListOBJ_layout.addStretch()

        if is_a_channel == True:
            self.notif = QLabel(str(self.newMsg))
            self.notif.setStyleSheet("background: #7f7f7f; border-radius: 5px; max-height: 1.2em")
            self.channelsListOBJ_layout.addWidget(self.notif)

        self.setLayout(self.channelsListOBJ_layout)

class channelOBJ(QScrollArea):
    """Le channel lui même contenant les messages"""

    def __init__(self,parent,  text, *args, **kwargs):
        super(channelOBJ, self).__init__(*args, **kwargs)
        self.parent = parent
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
    def addMessageToTheChannel(self, message):
        message = messagesOBJ(parent=self.parent, message=message)                                  #on déclare l'objet messagesOBJ  (on ajoute le message à l'UI)
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

    def __init__(self, parent, message, *args, **kwargs):
        super(messagesOBJ, self).__init__(*args, **kwargs)
        self.parent = parent
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

        #hour
        hour_lb = QLabel(messageJSON["date"]["hour"])
        hour_lb.setFixedWidth(50)
        self.lyt.addWidget(hour_lb)

        #identicon
        identicon_lb, icon_color = self.parent.setIdenticon(string=messageJSON["username"], background= self.parent.app_settings["cryptenger_win"]["users_icon_color"])
        self.lyt.addWidget(identicon_lb)

        #pseudo
        pseudo_lb = QLabel(messageJSON["username"])
        pseudo_lb.setFixedWidth(100)
        pseudo_lb.setAutoFillBackground(True)
        pseudo_lb.setStyleSheet("QLabel{color: "+icon_color+"; font-weight: bold}")
        # pseudo_lb.setStyleSheet("")
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
        # self.input_lne.setPlaceholderText('Hit your message here ;-)')

        #layout
        self.input_lyt = QHBoxLayout()
        self.input_lyt.addWidget(self.input_lne)

        #widget
        self.input_widget = QWidget()
        self.input_widget.setLayout(self.input_lyt)

        #add widget to main layout
        self.parent.main_grid_lyt.addWidget(self.input_widget, 2, 1, 1, 1)



class settingsOBJ(QScrollArea):
    """Ben les settings quoi..."""

    def __init__(self, parent, scale, location=[100, 100], *args, **kwargs):
        super(settingsOBJ, self).__init__(*args, **kwargs)
        #variables
        self.parent = parent
        self.location = location
        self.scale = scale
        self.initWindow()
        self.buildSettings()

    def initWindow(self):
        self.setGeometry(self.location[0]+100, self.location[1]+100, self.scale[0]/2, self.scale[1]/2)
        self.setWindowIcon(QtGui.QIcon('./assets/ico/cryptenger_icon.ico'))
        self.setWindowTitle('Settings')
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        # self.setFixedHeight(100)
        # self.setWidgetResizable(True)

        with open(self.parent.app_settings["default_style"]) as style_file:
            style = style_file.read()
            self.setStyleSheet(style)
        self.show()

    def buildSettings(self):
        #st = settings namespace
        #gb = groupbox namespace
        settings_lb = QLabel("Settings\n\n /!\\ Some settings require the restart of the application /!\\ ")

        display_settings_gb = QGroupBox("Display settings")
        display_settings_gb.setStyleSheet("margin: 15px 5px 5px 5px")

        style_combo_st = QComboBox()
        style_combo_st.addItem("Dark theme")
        style_combo_st.addItem("Light theme")
        style_combo_st.activated[str].connect(self.setStyleSheetC)

        server_icon_color_st = QPushButton("pick color")
        server_icon_color_st.clicked.connect(functools.partial(self.colorPicker, "server_icon_color"))

        channels_icon_color_st = QPushButton("pick color")
        channels_icon_color_st.clicked.connect(functools.partial(self.colorPicker, "channels_icon_color"))

        users_icon_color_st = QPushButton("pick color")
        users_icon_color_st.clicked.connect(functools.partial(self.colorPicker, "users_icon_color"))

        display_settings_form_lyt = QFormLayout(display_settings_gb)
        display_settings_form_lyt.setHorizontalSpacing(15)
        display_settings_form_lyt.setVerticalSpacing(5)
        display_settings_form_lyt.addRow("Style", style_combo_st)
        display_settings_form_lyt.addRow("Server icon color", server_icon_color_st)
        display_settings_form_lyt.addRow("Channel icon color", channels_icon_color_st)
        display_settings_form_lyt.addRow("Users icon color", users_icon_color_st)


        advanced_settings_gb = QGroupBox("Advanced settings")



        main_settings_lyt = QGridLayout(self)
        main_settings_lyt.setAlignment(QtCore.Qt.AlignTop)
        main_settings_lyt.addWidget(settings_lb)
        main_settings_lyt.addWidget(display_settings_gb)
        main_settings_lyt.addWidget(advanced_settings_gb)


    def colorPicker(self, setting):
        color = QColorDialog.getColor()
        self.parent.app_settings["cryptenger_win"][setting] = str(color.name())

        self.write_a_setting_in_json_settings_file()

    def setStyleSheetC(self, str):
        # print(self.parent.app_settings)
        # self.parent.parentObject.setStyleSheetForAllWindows()
        print(str)
        if str == "Dark theme":
            self.parent.app_settings["default_style"] = "./assets/css/dark_style.css"

        if str == "Light theme":
            self.parent.app_settings["default_style"] = "./assets/css/light_style.css"
        # new_settings = json.dumps
        self.write_a_setting_in_json_settings_file()

        # self.parent.setStyleSheet(self.parent.app_settings["cryptenger_win"]["default_style"])
        with open(self.parent.app_settings["default_style"], "r") as style:
            # styleSheet =
            new_style = style.read()
            self.setStyleSheet(new_style)
            self.parent.parentObject.setStyleSheet(new_style)

    def write_a_setting_in_json_settings_file(self):
        new_settings = json.dumps(self.parent.app_settings, indent=1)
        with open("./settings.json", "w") as app_settings:
            app_settings.write(new_settings)


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
        identicon_lb, icon_color = self.parent.setIdenticon(
            string=self.parent.serverName,
            background=self.parent.app_settings["cryptenger_win"]["server_icon_color"])
        serverInfos = QLabel("About server\n")
        serverInfos.setObjectName("groupbox_title")
        self.serverName_lb = QLabel(str(self.parent.serverName))
        #layout
        self.serverInf_lyt = QGridLayout()
        self.serverInf_lyt.addWidget(identicon_lb, 0, 0, 2, 1)
        self.serverInf_lyt.addWidget(serverInfos, 0, 1)
        self.serverInf_lyt.addWidget(self.serverName_lb, 1, 1)
        self.serverInf_lyt.setColumnStretch(2, 1)
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
        identicon_lb, icon_color = self.parent.setIdenticon(
            string=self.parent.username,
            background=self.parent.app_settings["cryptenger_win"]["users_icon_color"]
        )
        username = QLabel(self.parent.username)
        username.setStyleSheet("QLabel{color: "+icon_color+"; font-weight: bold}")
        self.settings_btn = QPushButton(QtGui.QIcon("./assets/img/settings_icon.png"), '')
        self.settings_btn.setStyleSheet('border: 0px solid transparent')
        self.settings_btn.clicked.connect(self.parent.openSettings)
        self.settings_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        #layout
        self.hud_lyt = QHBoxLayout()
        self.hud_lyt.addWidget(identicon_lb)
        self.hud_lyt.addWidget(username)
        self.hud_lyt.addStretch()
        self.hud_lyt.addWidget(self.settings_btn)

        #widget
        self.setLayout(self.hud_lyt)
        self.setFixedWidth(self.parent.app_settings["cryptenger_win"]["left_column_width"])
        self.setFixedHeight(self.parent.app_settings["cryptenger_win"]["user_ui_height"])

        #add widget to main layout
        self.parent.main_grid_lyt.addWidget(self, 2, 0, 1, 1)

class warningOBG(QMessageBox):
    """docstring for WarningOBG."""

    def __init__(self, parent, windowTitle, h1text, informativeText, pythonError, sizeX=800, sizeY=100):
        super(warningOBG, self).__init__()
        self.setIcon(QMessageBox.Warning)
        self.setWindowTitle('WARNING - ' + windowTitle)
        self.setText(h1text)
        self.setInformativeText(informativeText)
        self.setDetailedText("Details : \n" + pythonError)
        with open(parent.app_settings["default_style"], "r") as style:
            self.setStyleSheet(style.read())
        self.resize(sizeX, sizeY)
        self.exec_()
