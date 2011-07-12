from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Boolean

Base = declarative_base()
class project(Base):
    __tablename__ = 'project'
    
    idproject = Column(Integer, primary_key=True, nullable = False, unique=True)
    name = Column(String(250), nullable = False)
    
    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return "<project("+self.name+")>"
    
    
class dataModel(Base):
    __tablename__ = 'datamodel'
    
    idproject = Column(Integer, ForeignKey('project.idproject'), primary_key = True, nullable=False)
    idmodel = Column(Integer, primary_key = True, nullable=False)
    name = Column(String(250), nullable=False)
    idref = Column(Integer, nullable=False)
    
    def __init__(self, idproject, idmodel, name, idref):
        self.idproject = idproject
        self.idmodel = idmodel
        self.name = name
        self.idref = idref
        
    def __repr__(self):
        return "<datamodel("+str(self.idproject)+","+str(self.idmodel)+","+str(self.name)+","+str(self.idref)+")>"
    
class tableu(Base):
    __tablename__ = 'tableu'
    
    idtable = Column(Integer, primary_key = True, nullable=False, unique=True)
    idproject = Column(Integer, ForeignKey('datamodel.idproject'), nullable=False)
    idmodel = Column(Integer, ForeignKey('datamodel.idmodel'), nullable=False)
    name = Column(String(250), nullable=True)
    alias = Column(String(250), nullable=True)
    physicalname = Column(String(250), nullable=True)
    supertable = Column(String(250), nullable=True)
    
    # idproject, idmodel foreignKey de dataModel
    def __init__(self, idproject, idmodel, name, alias, physicalname, supertable):
        self.idmodel = idmodel
        self.idproject = idproject
        self.name = name
        self.alias = alias
        self.physicalname = physicalname
        self.supertable = supertable
        
    def __repr__(self):
        return "<tableu("+str(self.idproject)+","+str(self.idmodel)+","+","+str(self.name)+","+str(self.alias)+","+str(self.physicalname)+","+str(self.supertable)+")>"
    
    
class columm(Base):
    __tablename__ = 'columm'
    
    idcolumn = Column(Integer, primary_key=True, nullable=False, unique=True)
    idtable = Column(Integer, ForeignKey('tableu.idtable'), nullable=False)
    idmodel = Column(Integer, ForeignKey('datamodel.idmodel'), nullable=False)
    idproject = Column(Integer, ForeignKey('datamodel.idproject'), nullable=False)
    name = Column(String(250), nullable=True)
    type = Column(String(250), nullable=True)
    nullallowed = Column(Boolean, nullable=False)
    fulldisplayname = Column(String(500), nullable=True)
    lengthcolumn = Column(Integer, nullable=True)
    lengthnbdecimal = Column(String(250), nullable=True)
    
    # idproject, idmodel foreignKey de dataModel
    def __init__(self, idproject, idmodel, idtable, name, type, nullallowed, fulldisplayname, lengthcolumn, lengthnbdecimal):
        self.idtable = idtable
        self.idmodel = idmodel
        self.idproject = idproject
        self.name = name
        self.type = type
        self.nullallowed = nullallowed
        self.fulldisplayname = fulldisplayname
        self.lengthcolumn = lengthcolumn
        self.lengthnbdecimal = lengthnbdecimal
        
    def __repr__(self):
        return "<columm("+str(self.idproject)+","+str(self.idmodel)+","+str(self.idtable)+","+str(self.name)+","+str(self.type)+","+str(self.nullallowed)+","+str(self.fulldisplayname)+","+str(self.lengthcolumn)+","+str(self.lengthnbdecimal)+")>"
    