# The core system of my application

# Import XML module
from xml.etree.ElementTree import ElementTree
import xml.parsers.expat as expat
import xml.etree.ElementTree as Xml

# Import sql alchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy import desc
from sqlalchemy import asc

#we import the logger
import logging

#Import Database class
import databaseClass

#Configure the session
Session = sessionmaker()

class systemApp():
    def __init__(self):
        #self.__filename = ""
        self.__filename = "/home/dario/Documents/FichierXml/Exemple de raccordement.xml"
        self.__tree = None
        self.__session = None
        
        self.__logger = logging.getLogger("Convert XML Database")
        self.__logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(levelname)s] %(message)s')
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.__logger.addHandler(handler)
        
        
        # Errors Constants
        self.OK = 0
        self.ERROR_OPEN_FILE = 1
        self.ERR0R_PARSE_XML = 2
        self.OPERATIONAL_ERROR = 3
        self.ADDING_ERROR = 4
        self.ERROR = 5
        
    # PRECONDITIONS : filename doit etre un fichier XML
    def loadFile(self, filename):
        # In oder to conserve the file
        self.__tree = ElementTree()
        
        #Logging info
        self.__logger.info("Chargement du fichier...")
        
        #self.__tree.parse(filename)
        try:
            self.__tree.parse(filename)
            self.__filename = filename
            
        except IOError:
            self.__logger.critical("Impossible d ouvrir le fichier...")
            return self.ERROR_OPEN_FILE
        except expat.ExpatError:
            self.__logger.critical("Erreur de parsage du fichier...")
            return self.ERR0R_PARSE_XML
        except:
            self.__logger.critical("Erreur de traitement fichier...")
            return self.ERROR
        
        #Logging info
        self.__logger.info("Chargement du fichier effectue...")
        
        return self.OK
        
        
    #RETOUR : le nom d un fichier XML
    def getFilename(self):
        return self.__filename
    
    # Transform XML Element  to text
    def getContentFile(self):
        
        #Logging info
        self.__logger.info("Obtention du contenu du fichier...")
        
        contenu = None
        if (self.__tree == None):
            contenu = ""
        else:
            contenu = Xml.tostring(self.__tree.getroot())
            
        #Logging info
        self.__logger.info("Obtention du contenu du fichier effectuee...")    
        return contenu
    
    def __logDatabase(self, user, password, host, port, database):
        
        #Logging info
        self.__logger.info("Connexion a la base de donnee...")
        
        # We create the engine
        urlPostgres = "postgresql+psycopg2://"+user+":"+password+"@"+host+":"+port+"/"+database
        engine = create_engine(urlPostgres)
       
        try:
            connection = engine.connect()
        except OperationalError, e:
            # logging critical
            self.__logger.critical("Impossible de se connecter a la base de donnee...")
            return {'state':self.OPERATIONAL_ERROR, 'message': str(e)}
        
        self.__session = Session(bind = connection)
        
        #Logging info
        self.__logger.info("Connexion a la base de donnee effectuee...")
        
        return {'state':self.OK, 'message': 'Connection established'}
        
    
    def __logoutDatabase(self):
        
        #Logging info
        self.__logger.info("Deconnexion de la base de donnee...")
        
        # We logout of the database
        try:
            self.__session.close()
        except:
            return {'state':self.CLOSE_ERROR , 'message':'Can not close session'}
        
        #Logging info
        self.__logger.info("Deconnexion de la base de donnee effectuee...")
        
        return {'state':self.OK , 'message':'Session closed'}
        
    def __write(self):
        
        #Logging info
        self.__logger.info("Ecriture dans la base de donnee...")
        
        # We populate the database
        try:
            if (self.__tree != None):  # A file has been loaded
            
                #tabProject = self.__tree.getiterator("project")
                tabProject = self.__tree.getiterator("project")
                
                for project in tabProject:
                    
                    nameProject = project.attrib['name']
                    
                    objProject = databaseClass.project(nameProject)
                    idObjProject = None
                    
                    # We insert in tHe database the project
                    self.__session.add(objProject)
                    
                    
                    # We get the id of the objProject
                    for idproject,  in self.__session.query(databaseClass.project.idproject).order_by(desc(databaseClass.project.idproject)).limit(1):
                        idObjProject = idproject
                    
                    
                        
                    # We get the data model
                    tabDataModel = project.getiterator("datamodel")
                    
                    
                    # We insert the data model
                    #for dataModel in tabDataModel:
                    dataModel = tabDataModel[0]
                    nameDataModel = dataModel.attrib["name"]
                    try:
                        idDataModel = int(dataModel.attrib["idmodel"])
                    except:
                        idDataModel = -1
                        
                    try:
                        idRefDataModel = int(dataModel.attrib["idref"])
                    except:
                        idRefDataModel = -1
                    
                    objDataModel = databaseClass.dataModel(idObjProject, idDataModel, nameDataModel, idRefDataModel)
                    self.__session.add(objDataModel)
                    
                    #To avoid Foreign Key Problem
                    self.__session.commit()
                    
                    
                    # We get the tables
                    tabTable = dataModel.getiterator("table")
                    
                    for table in tabTable:
                    
                        nameTable = table.attrib["name"]
                        if (nameTable == None):
                            nameTable = ""
                        aliasTable = table.attrib["alias"]
                        if (aliasTable == None):
                            aliasTable = ""
                        physicalName = table.attrib["physicalName"]
                        if (physicalName == None):
                            physicalName = ""
                        superTable = table.attrib["superTable"]
                        if (superTable == None):
                            superTable = ""
                        
                        
                            
                        objTable = databaseClass.tableu(idObjProject, idDataModel, nameTable, aliasTable, physicalName, superTable)
                        self.__session.add(objTable)
                        
                        # To avoid Foreign Key Problem
                        self.__session.commit()
                        
                        # We get the id of the objTable
                        for idtable,  in self.__session.query(databaseClass.tableu.idtable).filter(databaseClass.tableu.idproject==idObjProject and databaseClass.tableu.idmodel ==idDataModel).order_by(desc(databaseClass.tableu.idtable)).limit(1):
                            idObjTable = idtable
                            
                       
                        
                        # We get the column
                        tabColumn = table.getiterator("column")
                       
                        for column in tabColumn:
                            nameColumn = column.attrib["name"]
                            tabTypeColumn = column.getiterator("type")
                            if (len(tabTypeColumn)>0):
                                typeColumn = tabTypeColumn[0].text
                            else:
                                typeColumn = ""
                            tabNullAlowed = column.getiterator("nullAllowed")
                            if (len(tabNullAlowed)>0):
                                if (tabNullAlowed[0].text == "True"):
                                    nullAllowed = True
                                elif(tabNullAlowed[0].text == "False"):
                                    nullAllowed = False
                                else:
                                    nullAllowed = False
                            else:
                                nullAllowed = False
                            tabFullDisplayName = column.getiterator("fullDisplayName")
                            if (len(tabFullDisplayName)):
                                fullDisplayName = tabFullDisplayName[0].text
                            else:
                                fullDisplayName = ""
                             
                            tabLengthColumn = column.getiterator("LengthColumn")
                            try:
                                LengthColumn = int(tabLengthColumn[0].text)
                            except:
                                LengthColumn = None
                            
                            tabLengthNbDecimal = column.getiterator("LengthNbDecimal")
                            if (len(tabLengthNbDecimal)>0):
                                LengthNbDecimal = tabLengthNbDecimal[0].text
                            else:
                                LengthNbDecimal = ""
                            
                            objColumn = databaseClass.columm(idObjProject, idDataModel, idObjTable, nameColumn, typeColumn, nullAllowed, fullDisplayName, LengthColumn, LengthNbDecimal)
                            
                            self.__session.add(objColumn)
                            
                self.__session.commit()
        except KeyError, e:
            #Logging critical
            self.__logger.critical("Erreur d attribut.")
            return {'state':self.ADDING_ERROR, 'message': 'Erreur attribut :'+str(e)} 
                         
        except Exception, e:
            #Logging critical
            self.__logger.critical("Impossible d ecrire dans la base de donnee.")
            return {'state':self.ADDING_ERROR, 'message': str(e)} 
        
        #Logging info
        self.__logger.info("Ecriture dans la base de donnee effectuee...")
        
        return {'state':self.OK, 'message': 'Ecriture effectuee'}
    
    def writeDatabase(self, user, password, host, port, database): 
   
        # We connect to the database
        dictLog = self.__logDatabase(user, password, host, port, database)
        if (dictLog['state'] != self.OK):
            return dictLog
        
        # We write in the database
        dictWrite = self.__write()
        if (dictWrite['state'] != self.OK):
            return dictWrite
                
        # We get out of the database
        dictOut = self.__logoutDatabase()
        if (dictOut['state'] != self.OK):
            return dictOut
                
        return {'state':self.OK, 'message': 'Ecriture effectuee base donnee'}
    
    def getLastInsertedRow(self, user, password, host, port, database):
        
        # We connect the database
        self.__logDatabase(user, password, host, port, database)
        
        # We get the string inserted
        stringInserted = ""
        # We get the id of the objProject
        for idproject, nameProject  in self.__session.query(databaseClass.project.idproject, databaseClass.project.name).order_by(desc(databaseClass.project.idproject)).limit(1):
            stringInserted += "projet " + str(nameProject) +"\n"
            for idmodel, nameModel, idref in self.__session.query(databaseClass.dataModel.idmodel, databaseClass.dataModel.name, databaseClass.dataModel.idref).order_by(asc(databaseClass.dataModel.idmodel)).filter(databaseClass.dataModel.idproject == idproject):
                stringInserted += "datamodel "+str(idmodel)+", "+str(nameModel)+", "+str(idref)+"\n"
                for idtable, nameTable, alias, physicalName, superTable in self.__session.query(databaseClass.tableu.idtable, databaseClass.tableu.name, databaseClass.tableu.alias, databaseClass.tableu.physicalname, databaseClass.tableu.supertable).filter(databaseClass.tableu.idproject==idproject and databaseClass.tableu.idmodel == idmodel):
                    stringInserted += "table "+str(nameTable)+", "+str(alias)+", "+str(physicalName)+", "+str(superTable)+"\n"
                    for idcolumn, nameColumn, type, nullAllowed, fullDisplayName, LengthColumn, LengthNbDecimal in self.__session.query(databaseClass.columm.idcolumn, databaseClass.columm.name, databaseClass.columm.type, databaseClass.columm.nullallowed, databaseClass.columm.fulldisplayname, databaseClass.columm.lengthcolumn, databaseClass.columm.lengthnbdecimal).filter(databaseClass.columm.idproject == idproject and databaseClass.columm.idmodel == idmodel and databaseClass.columm.idtable == idtable):
                        if (nullAllowed):
                            nullAllowedStr = "True"
                        else:
                            nullAllowedStr = "False"
                        stringInserted += "column "+str(nameColumn)+", "+str(type)+", "+str(nullAllowedStr)+", "+str(fullDisplayName)+", "+str(LengthColumn)+", "+str(LengthNbDecimal)+"\n" 
         
        #We get out of the database
        self.__logoutDatabase()
        
        return stringInserted
                
                
            
       