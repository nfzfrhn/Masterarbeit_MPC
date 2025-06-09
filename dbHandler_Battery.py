from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtSql as qts


class DatabaseBattery:
    def __init__(self):
        self.db = qts.QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("database/db_Battery")
        # Open the database
        if not self.db.open():
            qtw.QMessageBox.critical(None, "Cannot open database",
                                        "Unable to establish a database connection.\n"                                                 
                                        "Click Cancel to exit.",
                                        qtw.QMessageBox.Cancel)

        # Create a query object
        # self.query = qts.QSqlQuery()
        # Create a table
        self.createBatteryTable()

    def createBatteryTable(self):
        self.query = qts.QSqlQuery(self.db)
        # Create a table
        self.query.exec_("""CREATE TABLE IF NOT EXISTS Battery (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,                                                        
                            batteryInitialValue INTEGER,                            
                            batteryEfficiencyCoefficient REAL,                                                                                    
                            batteryMinEnergy INTEGER,                                                                                                                                                                                    
                            batteryMaxEnergy INTEGER,                                                                                                                                                                                    
                            )""")
        self.db.commit()

    def getBatteryTable(self):
        # Get the table
        bOk = self.query.exec_("""SELECT * FROM Battery""")
        return bOk, self.query

    def insertBatteryData(self, batteryInitialValue, batteryEfficiencyCoefficient, batteryMinEnergy, batteryMaxEnergy):
        self.query = qts.QSqlQuery(self.db)
        self.query.prepare("""INSERT INTO Battery (batteryInitialValue, batteryEfficiencyCoefficient, batteryMinEnergy, batteryMaxEnergy)
                                 VALUES (:batteryInitialValue, :batteryEfficiencyCoefficient, :batteryMinEnergy, :batteryMaxEnergy)""")
        self.query.bindValue(":batteryInitialValue", batteryInitialValue)
        self.query.bindValue(":batteryEfficiencyCoefficient", batteryEfficiencyCoefficient)
        self.query.bindValue(":batteryMinEnergy", batteryMinEnergy)
        self.query.bindValue(":batteryMaxEnergy", batteryMaxEnergy)
        self.query.exec_()
        self.db.commit()

        if self.query.isActive():
            return True
        else:
            return False