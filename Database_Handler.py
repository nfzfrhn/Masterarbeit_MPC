# This file is not a correct implementation. See dbHandler_Battery.py, dbHandler_EV.py, dbHandler_Solar.py for correct
# implementation
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtSql as qts


# Create a class to handle the database. This database class will be used to handle 3 different databases
class Database:
    def __init__(self, dbName):
        self.dbName = dbName
        self.db = qts.QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("database/" + self.dbName)
        # Open the database
        if not self.db.open():
            qtw.QMessageBox.critical(None, qtw.qApp.tr("Cannot open database"),
                                     qtw.qApp.tr("Unable to establish a database connection.\n"
                                                 "This example needs SQLite support. Please read "
                                                 "the Qt SQL driver documentation for information "
                                                 "how to build it.\n\n"
                                                 "Click Cancel to exit."),
                                     qtw.QMessageBox.Cancel)

        # Create a query object
        self.query = qts.QSqlQuery()
        # Create a table depending on the database name
        if self.dbName == "DatabaseBattery.db":
            self.createBatteryTable()
        elif self.dbName == "DatabaseEV.db":
            self.createEVTable()
        elif self.dbName == "DatabaseSolar.db":
            self.createSolarTable()
        else:
            qtw.QMessageBox.critical(None, qtw.qApp.tr("Cannot open database"))

    def createBatteryTable(self):
        # Create a table
        self.query.exec_("""CREATE TABLE IF NOT EXISTS Battery (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,                                                        
                            batteryInitialValue INTEGER,                            
                            batteryEfficiencyCoefficient REAL,                                                                                    
                            batteryMinEnergy INTEGER,                                                                                                                                                                                    
                            batteryMaxEnergy INTEGER,                                                                                                                                                                                    
                            )""")
        self.db.commit()

    def createEVTable(self):
        # Create a table
        self.query.exec_("""CREATE TABLE IF NOT EXISTS EV (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,                                                        
                            evInitialValue INTEGER,                            
                            evEfficiencyCoefficient REAL,                                                                                    
                            evMinEnergy INTEGER,                                                                                                                                                                                    
                            evMaxEnergy INTEGER,                                                                                                                                                                                    
                            )""")
        self.db.commit()

    def createSolarTable(self):
        # Create a table
        self.query.exec_("""CREATE TABLE IF NOT EXISTS Solar (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,                                                        
                            solarNumberOfModules INTEGER,                            
                            solarSTC_ReferenceSolarIrradiance REAL,                                                                                    
                            solarNOCT_ModuleTemperature INTEGER,                                                                                                                                                                                    
                            solarSTC_PowerPerModule INTEGER,
                            solarSTC_TemperatureCoefficient REAL,
                            solarSTC_ReferenceIrradianceCoefficient_TestCond REAL,
                            solarSTC_ReferenceCellTemperature INTEGER                                                                                                                                                                                    
                            )""")
        self.db.commit()

    def insertBatteryData(self, batteryInitialValue, batteryEfficiencyCoefficient, batteryMinEnergy, batteryMaxEnergy):
        # Insert data into the table
        query = qts.QSqlQuery()
        query.prepare("""INSERT INTO Battery (batteryInitialValue, batteryEfficiencyCoefficient, batteryMinEnergy, batteryMaxEnergy)
                         VALUES (:batteryInitialValue, :batteryEfficiencyCoefficient, :batteryMinEnergy, :batteryMaxEnergy)""")
        query.bindValue(":batteryInitialValue", batteryInitialValue)
        query.bindValue(":batteryEfficiencyCoefficient", batteryEfficiencyCoefficient)
        query.bindValue(":batteryMinEnergy", batteryMinEnergy)
        query.bindValue(":batteryMaxEnergy", batteryMaxEnergy)
        query.exec_()
        self.db.commit()

        if query.isActive():
            return True
        else:
            return False


    def insertEVData(self, evInitialValue, evEfficiencyCoefficient, evMinEnergy, evMaxEnergy):
        # Insert data into the table
        self.query.prepare("""INSERT INTO EV (evInitialValue, evEfficiencyCoefficient, evMinEnergy, evMaxEnergy)
                              VALUES (:evInitialValue, :evEfficiencyCoefficient, :evMinEnergy, :evMaxEnergy)""")
        self.query.bindValue(":evInitialValue", evInitialValue)
        self.query.bindValue(":evEfficiencyCoefficient", evEfficiencyCoefficient)
        self.query.bindValue(":evMinEnergy", evMinEnergy)
        self.query.bindValue(":evMaxEnergy", evMaxEnergy)
        self.query.exec_()
        self.db.commit()

    def insertSolarData(self, solarNumberOfModules, solarSTC_ReferenceSolarIrradiance, solarNOCT_ModuleTemperature, solarSTC_PowerPerModule, solarSTC_TemperatureCoefficient, solarSTC_ReferenceIrradianceCoefficient_TestCond, solarSTC_ReferenceCellTemperature):
        # Insert data into the table
        self.query.prepare("""INSERT INTO Solar (solarNumberOfModules, solarSTC_ReferenceSolarIrradiance, solarNOCT_ModuleTemperature, solarSTC_PowerPerModule, solarSTC_TemperatureCoefficient, solarSTC_ReferenceIrradianceCoefficient_TestCond, solarSTC_ReferenceCellTemperature)
                              VALUES (:solarNumberOfModules, :solarSTC_ReferenceSolarIrradiance, :solarNOCT_ModuleTemperature, :solarSTC_PowerPerModule, :solarSTC_TemperatureCoefficient, :solarSTC_ReferenceIrradianceCoefficient_TestCond, :solarSTC_ReferenceCellTemperature)""")
        self.query.bindValue(":solarNumberOfModules", solarNumberOfModules)
        self.query.bindValue(":solarSTC_ReferenceSolarIrradiance", solarSTC_ReferenceSolarIrradiance)
        self.query.bindValue(":solarNOCT_ModuleTemperature", solarNOCT_ModuleTemperature)
        self.query.bindValue(":solarSTC_PowerPerModule", solarSTC_PowerPerModule)
        self.query.bindValue(":solarSTC_TemperatureCoefficient", solarSTC_TemperatureCoefficient)
        self.query.bindValue(":solarSTC_ReferenceIrradianceCoefficient_TestCond", solarSTC_ReferenceIrradianceCoefficient_TestCond)
        self.query.bindValue(":solarSTC_ReferenceCellTemperature", solarSTC_ReferenceCellTemperature)
        self.query.exec_()
        self.db.commit()

    def getBatteryData(self):
        # Select data from the table
        self.query.exec_("SELECT * FROM Battery")
        # Get the data
        #return bOk, self.query
        return self.query



