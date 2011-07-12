#Import Qt Modules
from PyQt4 import QtGui, QtCore



# In order to get the information connection
class connectDialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        
        # Properties of the window
        self.setWindowTitle('Informations Base Donnee Postgresql')
        self.setModal(True)
        
        # Username
        self.userLabel = QtGui.QLabel('Utilisateur :')
        self.userEdit = QtGui.QLineEdit('hepot10')
        
        hboxUser = QtGui.QHBoxLayout()
        hboxUser.addWidget(self.userLabel)
        hboxUser.addWidget(self.userEdit)
        
        #Password
        self.passwordLabel = QtGui.QLabel('Password :')
        self.passswordEdit = QtGui.QLineEdit('admin13')
        self.passswordEdit.setEchoMode(QtGui.QLineEdit.Password)
        
        hboxPass = QtGui.QHBoxLayout()
        hboxPass.addWidget(self.passwordLabel)
        hboxPass.addWidget(self.passswordEdit)
        
        #host
        self.hostLabel = QtGui.QLabel('Hote :')
        self.hostEdit = QtGui.QLineEdit('localhost')
        
        hboxHost = QtGui.QHBoxLayout()
        hboxHost.addWidget(self.hostLabel)
        hboxHost.addWidget(self.hostEdit)
        
        #Port
        self.portLabel = QtGui.QLabel('Port :')
        self.portEdit = QtGui.QLineEdit('5432')
        
        hboxPort = QtGui.QHBoxLayout()
        hboxPort.addWidget(self.portLabel)
        hboxPort.addWidget(self.portEdit)
        
        #Database
        self.dbLabel = QtGui.QLabel('Base de donnee :')
        self.dbEdit = QtGui.QLineEdit('openmodelxml')
        
        hboxDb = QtGui.QHBoxLayout()
        hboxDb.addWidget(self.dbLabel)
        hboxDb.addWidget(self.dbEdit)
        
        # Accept, Reject button
        self.buttonOkay = QtGui.QPushButton('Confirmer', self)
        self.connect(self.buttonOkay, QtCore.SIGNAL('clicked()'), self.validate)
        
        self.buttonCancel = QtGui.QPushButton('Annuler', self)
        self.connect(self.buttonCancel, QtCore.SIGNAL('clicked()'), self.reject)
        
        hboxConfirm = QtGui.QHBoxLayout()
        hboxConfirm.addWidget(self.buttonOkay)
        hboxConfirm.addWidget(self.buttonCancel) 
        
        vhbox = QtGui.QVBoxLayout()
        vhbox.addLayout(hboxUser)
        vhbox.addLayout(hboxPass)
        vhbox.addLayout(hboxHost)
        vhbox.addLayout(hboxPort)
        vhbox.addLayout(hboxDb)
        vhbox.addLayout(hboxConfirm)
        
        self.setLayout(vhbox)
        
    def getConnectInfos(self):
        dict = {}
        dict['user'] = str(self.userEdit.text())
        dict['password'] = str(self.passswordEdit.text())
        dict['host'] = str(self.hostEdit.text())
        dict['port'] = str(self.portEdit.text())
        dict['db'] = str(self.dbEdit.text())
        return dict
    
    def validate(self):
        accept = True
        try:
            int(self.portEdit.text())
            if (str(self.userEdit.text()) == ''):
                QtGui.QMessageBox.warning(self, self.tr('Valeur incorrecte'), 'L utilisateur ne doit pas etre vide')
                accept = False
            elif(str(self.dbEdit.text()) == ''):
                QtGui.QMessageBox.warning(self, self.tr('Valeur incorrecte'), 'La base de donnee ne doit pas etre vide')
                accept = False          
            
        except ValueError:
            QtGui.QMessageBox.warning(self, self.tr('Valeur incorrecte'), 'Le port doit etre un entier')
            accept = False  
       
        if (accept):
            self.accept()
        

# Graphic interface of my application
class systemGui(QtGui.QMainWindow):
    def __init__(self, systemCore):
        QtGui.QMainWindow.__init__(self);
        
        # Constants
        self.__CHAINE_VIDE = ""
        self.__WEIGHT = 500
        self.__HEIGHT = 500
        
        self.setWindowTitle("Convertir XML Database");
        
        self.setCentralWidget(QtGui.QTextEdit(self))
        self.centralWidget().setReadOnly(True)
        
        self.resize(QtCore.QSize(self.__WEIGHT, self.__HEIGHT))
        
        self.__systemCore = systemCore
        
        self.__setInitialMenu()
        
    def __load(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, "Choisir un fichier XML", self.__systemCore.getFilename(), "Xml(*.xml)")
        if (filename != self.__CHAINE_VIDE):
            status = self.__systemCore.loadFile(str(filename))
            
            if (status == self.__systemCore.OK):
                self.centralWidget().setText(self.__systemCore.getContentFile())
            elif (status == self.__systemCore.ERROR_OPEN_FILE):
                QtGui.QMessageBox.critical(self, self.tr('Erreur Ouverture'), 'Le fichier ne peut pas etre ouvert!')
            elif (status == self.__systemCore.ERR0R_PARSE_XML):
                QtGui.QMessageBox.critical(self, self.tr('Erreur Parsing'), 'La structure du fichier est incorrecte!')
            elif (status == self.__systemCore.ERROR):
                QtGui.QMessageBox.critical(self, self.tr('Erreur'), 'Le fichier n est pas valide!')
                
        
    
    def __convertToDb(self):
        infosConnectDialog = connectDialog()
        
        if (infosConnectDialog.exec_() == QtGui.QDialog.Accepted):
            dict = infosConnectDialog.getConnectInfos()
            dictExecution = self.__systemCore.writeDatabase(dict['user'], dict['password'], dict['host'], dict['port'], dict['db'])
            if (dictExecution['state'] == self.__systemCore.OK):
                QtGui.QMessageBox.information(self, self.tr('BRAVO!'), dictExecution['message'])
            elif(dictExecution['state'] == self.__systemCore.OPERATIONAL_ERROR):
                QtGui.QMessageBox.critical(self, self.tr('Erreur connection base donnee'), dictExecution['message'])
            else:
                QtGui.QMessageBox.critical(self, self.tr('Erreur ecriture base donnee'), dictExecution['message'])
        
        
    def __setInitialMenu(self):
        
        # action quit
        exit = QtGui.QAction(QtGui.QIcon(""), self.tr('&Quitter'), self)
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip('Quitter l'+"'"+'application')
        self.connect(exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
        
        # action load
        load = QtGui.QAction(QtGui.QIcon(""), self.tr('&Ouvrir'), self)
        load.setShortcut('Ctrl+O')
        load.setStatusTip('Ouvrir Fichier Xml')
        self.connect(load, QtCore.SIGNAL('triggered()'), self.__load)
        
        # action convertToDb
        convertToDb = QtGui.QAction(QtGui.QIcon(""), self.tr('&InsererBaseDonnee'), self)
        convertToDb.setShortcut('Ctrl+C')
        convertToDb.setStatusTip('Mettre le fichier dans la base de donnee')
        self.connect(convertToDb, QtCore.SIGNAL('triggered()'), self.__convertToDb)
        
        
        # creation of menu
        menubar = self.menuBar()
        file = menubar.addMenu('&Fichier')
        operation = menubar.addMenu('&Operation')
        
        # menu file 
        file.addAction(load)
        file.addAction(exit)
        
        # menu operation
        operation.addAction(convertToDb)