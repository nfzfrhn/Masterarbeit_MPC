import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtSql as qts
# from secondWindow_ui_1 import Ui_Gui_Secondary                # This is QWidget class
from secondWindow_ui_2 import Ui_Gui_Secondary                # This is QWidget class
#from secondWindowDialog_ui import Ui_secondaryWindow       # This is QDialog class
# from Database_Handler import Database                     # This is not working
# from dbHandler_Battery import DatabaseBattery             # This is not finish but probably not working


class SecondaryWindow(qtw.QWidget):

    def __init__(self, initial_tab, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Your code will go here
        self.ui = Ui_Gui_Secondary()
        self.ui.setupUi(self)

        self.setWindowTitle("Setting Parameters")

        # Allow only float as input
        self.ui.cw_LEdit.setValidator(qtg.QDoubleValidator())
        self.ui.cz_LEdit.setValidator(qtg.QDoubleValidator())
        self.ui.cf_LEdit.setValidator(qtg.QDoubleValidator())
        self.ui.cpip_LEdit.setValidator(qtg.QDoubleValidator())
        self.ui.cwat_LEdit.setValidator(qtg.QDoubleValidator())
        self.ui.kwoa_LEdit.setValidator(qtg.QDoubleValidator())
        self.ui.kwz_LEdit.setValidator(qtg.QDoubleValidator())
        self.ui.kfz_LEdit.setValidator(qtg.QDoubleValidator())
        self.ui.kfpip_LEdit.setValidator(qtg.QDoubleValidator())
        self.ui.m_LEdit.setValidator(qtg.QDoubleValidator())
        self.ui.kwt_LEdit.setValidator(qtg.QDoubleValidator())
        self.ui.kt_LEdit.setValidator(qtg.QDoubleValidator())
        self.ui.w_LEdit.setValidator(qtg.QDoubleValidator())
        self.ui.mhp_dot_LEdit.setValidator(qtg.QDoubleValidator())
        self.ui.alpha_LEdit.setValidator(qtg.QDoubleValidator())
        self.ui.a1_LEdit.setValidator(qtg.QDoubleValidator())
        self.ui.a2_LEdit.setValidator(qtg.QDoubleValidator())
        self.ui.a3_LEdit.setValidator(qtg.QDoubleValidator())
        self.ui.b1_LEdit.setValidator(qtg.QDoubleValidator())
        self.ui.b2_LEdit.setValidator(qtg.QDoubleValidator())
        self.ui.tau_LEdit.setValidator(qtg.QDoubleValidator())
        self.ui.G_PV_NOCT_LE.setValidator(qtg.QDoubleValidator())         # G_PV_NOCT
        self.ui.T_PV_NOCT_LE.setValidator(qtg.QDoubleValidator())
        self.ui.P_PV_STC.setValidator(qtg.QDoubleValidator())
        self.ui.gamma_PV.setValidator(qtg.QDoubleValidator())
        self.ui.G_PV_STC.setValidator(qtg.QDoubleValidator())
        self.ui.T_PV_STC.setValidator(qtg.QDoubleValidator())
        self.ui.predHrznLE.setValidator(qtg.QIntValidator())
        self.ui.cotrlHrznLE.setValidator(qtg.QIntValidator())
        self.ui.samplingTimeLE.setValidator(qtg.QIntValidator())
        self.ui.daysOfSimLE.setValidator(qtg.QIntValidator())
        self.ui.weightQ.setValidator(qtg.QDoubleValidator())
        self.ui.weightR.setValidator(qtg.QDoubleValidator())
        self.ui.initTw_LE.setValidator(qtg.QIntValidator())
        self.ui.initTz_LE.setValidator(qtg.QIntValidator())
        self.ui.initTf_LE.setValidator(qtg.QIntValidator())
        self.ui.initTpip_LE.setValidator(qtg.QIntValidator())
        self.ui.initT1_LE.setValidator(qtg.QIntValidator())
        self.ui.initT2_LE.setValidator(qtg.QIntValidator())
        self.ui.initT3_LE.setValidator(qtg.QIntValidator())
        self.ui.initT4_LE.setValidator(qtg.QIntValidator())
        self.ui.initCOP_LE.setValidator(qtg.QDoubleValidator())
        self.ui.refTz_LE.setValidator(qtg.QDoubleValidator())
        self.ui.refT1_LE.setValidator(qtg.QDoubleValidator())
        self.ui.refTe_LE.setValidator(qtg.QDoubleValidator())


        # Set up the battery table
        self.ui.batTable.setColumnCount(5)
        self.ui.batTable.setHorizontalHeaderLabels(
            ['ID', 'Initial Value', 'Efficiency Coefficient', 'Min Energy', 'Max Energy'])
        self.ui.batTable.horizontalHeader().setStretchLastSection(True)
        self.ui.batTable.horizontalHeader().setSectionResizeMode(qtw.QHeaderView.Stretch)
        self.ui.batTable.resizeColumnsToContents()
        self.ui.batTable.setEditTriggers(qtw.QAbstractItemView.NoEditTriggers)
        # Change the color of the header
        self.ui.batTable.horizontalHeader().setStyleSheet("QHeaderView::section {background-color: #f0f0f0;}")
        # Remove the vertical header
        self.ui.batTable.verticalHeader().setVisible(False)
        # center the alignment of the content
        self.ui.batTable.horizontalHeaderItem(0).setTextAlignment(qtc.Qt.AlignCenter)

        # Set up the Electrical Vehicle table
        self.ui.evTable.setColumnCount(6)
        self.ui.evTable.setHorizontalHeaderLabels(
            ['ID', 'Initial Value', 'Efficiency Coefficient', 'Min Energy', 'Max Energy', 'Discharging Capability'])
        self.ui.evTable.horizontalHeader().setStretchLastSection(True)
        self.ui.evTable.horizontalHeader().setSectionResizeMode(qtw.QHeaderView.Stretch)
        self.ui.evTable.resizeColumnsToContents()
        self.ui.evTable.setEditTriggers(qtw.QAbstractItemView.NoEditTriggers)
        # Change the color of the header
        self.ui.evTable.horizontalHeader().setStyleSheet("QHeaderView::section {background-color: #f0f0f0;}")
        # Remove the vertical header
        self.ui.evTable.verticalHeader().setVisible(False)
        # center the alignment of the content
        self.ui.evTable.horizontalHeaderItem(0).setTextAlignment(qtc.Qt.AlignCenter)

        db = qts.QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("database/DatabaseParameter.db")

        if db.open():
            query = qts.QSqlQuery()
            print(db.tables())
            if "Building" not in db.tables():
                query.exec_("""CREATE TABLE IF NOT EXISTS Building (
                                buildingId INTEGER PRIMARY KEY AUTOINCREMENT,                                                        
                                cw REAL,                            
                                cz REAL,                                                                                    
                                cf REAL,                                                                                                                                                                                    
                                cpip REAL,
                                cwat REAL,
                                w_capacity REAL,
                                kwt REAL,
                                kt REAL,
                                w REAL,
                                m_hp_dot REAL,
                                alpha REAL,
                                a1 REAL,
                                a2 REAL,
                                a3 REAL,
                                b1 REAL,
                                b2 REAL,
                                tau INTEGER                                                                                                                                                                                                           
                                )""")
                db.commit()
            if "Battery" not in db.tables():
                query.exec_("""CREATE TABLE IF NOT EXISTS Battery (
                                batteryId INTEGER PRIMARY KEY AUTOINCREMENT,                                                        
                                batteryInitialValue INTEGER,                            
                                batteryEfficiencyCoefficient REAL,                                                                                    
                                batteryMinEnergy INTEGER,                                                                                                                                                                                    
                                batteryMaxEnergy INTEGER                                                                                                                                                                                    
                                )""")
                db.commit()
            if "ElectricVehicle" not in db.tables():
                query.exec_("""CREATE TABLE IF NOT EXISTS ElectricVehicle (
                                evId INTEGER PRIMARY KEY AUTOINCREMENT,                                                        
                                evInitialValue INTEGER,                            
                                evEfficiencyCoefficient REAL,                                                                                    
                                evMinEnergy INTEGER,                                                                                                                                                                                    
                                evMaxEnergy INTEGER,
                                evDischargingCapability INTEGER                                                                                                                                                                                    
                                )""")
                db.commit()
            if "SolarPanel" not in db.tables():
                query.exec_("""CREATE TABLE IF NOT EXISTS SolarPanel (
                                solarId INTEGER PRIMARY KEY AUTOINCREMENT,
                                solar_module_type TEXT,                                                        
                                solar_n_PV_mod INTEGER,                            
                                solar_G_PV_NOCT REAL,                                                                                    
                                solar_T_PV_NOCT REAL,                                                                                                                                                                                    
                                solar_P_PV_STC REAL,
                                solar_gamma_PV REAL,
                                solar_G_PV_STC REAL,
                                solar_T_PV_STC REAL,                                                                                                                                                                                    
                                )""")
                db.commit()
            if "Controller" not in db.tables():
                query.exec_("""CREATE TABLE IF NOT EXISTS Controller (
                                controllerId INTEGER PRIMARY KEY AUTOINCREMENT,
                                predictionHorizon_N INTEGER                                                        
                                controlHorizon_m INTEGER,                            
                                samplingTime INTEGER,                                                                                    
                                daySimulation INTEGER                                                                                                                                                                                    
                                coeff_Q REAL,
                                coeff_R REAL,
                                ref_roomTemperature REAL,
                                ref_T1 REAL,
                                ref_Te REAL,
                                ref_PV_sold REAL,
                                initVal_Tw REAL,
                                initVal_Tz REAL,
                                initVal_Tf REAL,
                                initVal_Tpip REAL,
                                initVal_T1 REAL,
                                initVal_T2 REAL,
                                initVal_T3 REAL,
                                initVal_T4 REAL,
                                initVal_COP REAL,                                                                                                                                                                                    
                                )""")
                db.commit()
            self.populateBatteryTable()
            self.populateEVTable()
            self.populateSolarTable()
        else:
            qtw.QMessageBox.warning(self, "Database Error", "Could not open database")

        # Configure the add buttons
        self.ui.batAddBtn.clicked.connect(self.addBattery)
        self.ui.evAddBtn.clicked.connect(self.addEV)
        self.ui.pvSaveBtn.clicked.connect(self.updateSolar)       # TODO: Add the save button function

        # Configure the edit buttons
        self.ui.batEditBtn.clicked.connect(self.editBattery)
        self.ui.evEditBtn.clicked.connect(self.editEV)

        # Enable/Disable the edit buttons and delete buttons
        # self.ui.batEditBtn.setEnabled(False)
        # self.ui.batDelBtn.setEnabled(False)
        # self.ui.evEditBtn.setEnabled(False)
        # self.ui.evDelBtn.setEnabled(False)
        # self.ui.pvEditBtn.setEnabled(False)
        # self.ui.pvDelBtn.setEnabled(False)

        self.ui.batTable.itemSelectionChanged.connect(self.enableBatBtn)
        self.ui.evTable.itemSelectionChanged.connect(self.enableEVBtn)
        # self.ui.tableWidget.itemSelectionChanged.connect(self.enablePVBtn) # TODO: Fill the QLineEdit

        # Configure the delete buttons
        self.ui.batDelBtn.clicked.connect(self.deleteBattery)
        self.ui.evDelBtn.clicked.connect(self.deleteEV)

        self.ui.tabWidget.setCurrentIndex(initial_tab)

        # Your code ends here
        self.show()

    def populateBatteryTable(self):
        query = qts.QSqlQuery()
        bOk = query.exec_("SELECT * FROM Battery")
        if bOk:
            self.ui.batTable.clear()
            self.ui.batTable.setRowCount(0)
            self.ui.batTable.setColumnCount(5)
            self.ui.batTable.setHorizontalHeaderLabels(['ID', 'Initial Value', 'Efficiency Coefficient', 'Min Energy', 'Max Energy'])
            # self.ui.batTable.setColumnWidth(0, 50)
            # self.ui.batTable.setColumnWidth(1, 80)
            # self.ui.batTable.setColumnWidth(2, 80)
            # self.ui.batTable.setColumnWidth(3, 80)
            # self.ui.batTable.setColumnWidth(4, 80)
            # self.ui.batTable.horizontalHeader().setStretchLastSection(True)
            # self.ui.batTable.horizontalHeader().setSectionResizeMode(qtw.QHeaderView.Stretch)

            while query.next():
                rowPosition = self.ui.batTable.rowCount()
                self.ui.batTable.insertRow(rowPosition)
                self.ui.batTable.setItem(rowPosition, 0, qtw.QTableWidgetItem(str(query.value(0))))
                self.ui.batTable.setItem(rowPosition, 1, qtw.QTableWidgetItem(str(query.value(1))))
                self.ui.batTable.setItem(rowPosition, 2, qtw.QTableWidgetItem(str(query.value(2))))
                self.ui.batTable.setItem(rowPosition, 3, qtw.QTableWidgetItem(str(query.value(3))))
                self.ui.batTable.setItem(rowPosition, 4, qtw.QTableWidgetItem(str(query.value(4))))
                rowPosition += 1
            # self.ui.batTable.resizeColumnsToContents()
        else:
            qtw.QMessageBox.warning(self, "Database Error", "Database error\n\n{}".format(query.lastError().text()))

    def populateEVTable(self):
        query = qts.QSqlQuery()
        bOk = query.exec_("SELECT * FROM ElectricVehicle")
        if bOk:
            self.ui.evTable.clear()
            self.ui.evTable.setRowCount(0)
            self.ui.evTable.setColumnCount(5)
            self.ui.evTable.setHorizontalHeaderLabels(
                ['ID', 'Initial Value', 'Efficiency Coefficient', 'Min Energy', 'Max Energy', 'Discharging Capability'])

            while query.next():
                rowPosition = self.ui.evTable.rowCount()
                self.ui.evTable.insertRow(rowPosition)
                self.ui.evTable.setItem(rowPosition, 0, qtw.QTableWidgetItem(str(query.value(0))))
                self.ui.evTable.setItem(rowPosition, 1, qtw.QTableWidgetItem(str(query.value(1))))
                self.ui.evTable.setItem(rowPosition, 2, qtw.QTableWidgetItem(str(query.value(2))))
                self.ui.evTable.setItem(rowPosition, 3, qtw.QTableWidgetItem(str(query.value(3))))
                self.ui.evTable.setItem(rowPosition, 4, qtw.QTableWidgetItem(str(query.value(4))))
                rowPosition += 1
            # self.ui.evTable.resizeColumnsToContents()

    def populateSolarTable(self):
        pass

    def addBattery(self):
        # dlgBattery = DlgBattery()
        dlgBattery = DlgAdd()
        dlgBattery.setWindowTitle("Input Battery Information")
        dlgBattery.saveBtn.clicked.connect(dlgBattery.evt_saveBatteryBtn)
        dlgBattery.show()
        dlgBattery.exec_()
        self.populateBatteryTable()

    def addEV(self):
        dlgEV = DlgAdd()
        dlgEV.setWindowTitle("Input Electric Vehicle Information")
        dlgEV.saveBtn.clicked.connect(dlgEV.evt_saveEVBtn)
        dlgEV.show()
        dlgEV.exec_()
        self.populateEVTable()

    def updateSolar(self):
        pass

    # Callback functions for the edit buttons
    def editBattery(self):
        dlgUpdate = DlgAdd()
        dlgUpdate.setWindowTitle("Update Battery Information")
        row = self.ui.batTable.currentRow()
        idBat = self.ui.batTable.item(row, 0).text()
        # print(idBat)
        dlgUpdate.initValue.setText(self.ui.batTable.item(row, 1).text())
        dlgUpdate.effCoeff.setText(self.ui.batTable.item(row, 2).text())
        dlgUpdate.minEnergy.setText(self.ui.batTable.item(row, 3).text())
        dlgUpdate.maxEnergy.setText(self.ui.batTable.item(row, 4).text())
        dlgUpdate.saveBtn.clicked.connect(lambda: dlgUpdate.evt_editBatteryBtn(idBat))
        dlgUpdate.show()
        dlgUpdate.exec_()
        self.populateBatteryTable()

    def editEV(self):
        dlgUpdate = DlgAdd()
        dlgUpdate.setWindowTitle("Update Electric Vehicle Information")
        row = self.ui.evTable.currentRow()
        idEV = self.ui.evTable.item(row, 0).text()
        # print(idEV)
        dlgUpdate.initValue.setText(self.ui.evTable.item(row, 1).text())
        dlgUpdate.effCoeff.setText(self.ui.evTable.item(row, 2).text())
        dlgUpdate.minEnergy.setText(self.ui.evTable.item(row, 3).text())
        dlgUpdate.maxEnergy.setText(self.ui.evTable.item(row, 4).text())
        dlgUpdate.saveBtn.clicked.connect(lambda: dlgUpdate.evt_editEVBtn(idEV))
        dlgUpdate.show()
        dlgUpdate.exec_()
        self.populateEVTable()

    def editSolar(self):
        pass

    def deleteBattery(self):
        row = self.ui.batTable.currentRow()
        idBat = self.ui.batTable.item(row, 0).text()
        res = qtw.QMessageBox.question(self, "Delete Battery", "Are you sure you want to delete this battery?", qtw.QMessageBox.Yes | qtw.QMessageBox.No)
        if res == qtw.QMessageBox.Yes:
            query = qts.QSqlQuery()
            bOk = query.exec_("DELETE FROM Battery WHERE batteryId = {}".format(idBat))
            if bOk:
                qtw.QMessageBox.information(self, "Battery Deleted", "Battery deleted successfully")
                self.populateBatteryTable()
            else:
                qtw.QMessageBox.warning(self, "Database Error", "Database error\n\n{}".format(query.lastError().text()))

    def deleteEV(self):
        pass

    def deleteSolar(self):
        pass

    def enableBatBtn(self):
        row = self.ui.batTable.currentRow()
        if row < 0:
            self.ui.batEditBtn.setEnabled(False)
            self.ui.batDelBtn.setEnabled(False)
        else:
            self.ui.batEditBtn.setEnabled(True)
            self.ui.batDelBtn.setEnabled(True)

    def enableEVBtn(self):
        row = self.ui.evTable.currentRow()
        if row < 0:
            self.ui.evEditBtn.setEnabled(False)
            self.ui.evDelBtn.setEnabled(False)
        else:
            self.ui.evEditBtn.setEnabled(True)
            self.ui.evDelBtn.setEnabled(True)


# Create a class to handle battery and EV information. Tertiary window
class DlgAdd(qtw.QDialog):
    def __init__(self):
        super().__init__()
        self.resize(400, 300)
        self.mainLayout = qtw.QVBoxLayout()
        self.formLayout = qtw.QFormLayout()
        self.hboxLayout = qtw.QHBoxLayout()
        self.setLayout(self.mainLayout)

        # if not qts.QSqlDatabase.connectionName():
        #     db = qts.QSqlDatabase.addDatabase("QSQLITE")
        #     db.setDatabaseName("database/DatabaseParameter.db")

        self.saveBtn = qtw.QPushButton("Save")
        self.cancelBtn = qtw.QPushButton("Cancel")
        self.hboxLayout.addWidget(self.saveBtn)
        self.hboxLayout.addWidget(self.cancelBtn)

        self.initValue = qtw.QLineEdit()
        self.effCoeff = qtw.QLineEdit()
        self.minEnergy = qtw.QLineEdit()
        self.maxEnergy = qtw.QLineEdit()

        self.initValue.setPlaceholderText("Initial Energy")
        self.effCoeff.setPlaceholderText("Efficiency Coefficient")
        self.minEnergy.setPlaceholderText("Minimum Allowed Charging State in kWh")
        self.maxEnergy.setPlaceholderText("Maximum Allowed Charging State in kWh")

        self.initValue.setValidator(qtg.QDoubleValidator())
        self.effCoeff.setValidator(qtg.QDoubleValidator())
        self.minEnergy.setValidator(qtg.QDoubleValidator())
        self.maxEnergy.setValidator(qtg.QDoubleValidator())

        self.formLayout.addRow("Initial Energy [kWh]", self.initValue)
        self.formLayout.addRow("Efficiency Coefficient", self.effCoeff)
        self.formLayout.addRow("Minimum Energy [kWh]", self.minEnergy)
        self.formLayout.addRow("Maximum Energy [kWh]", self.maxEnergy)

        self.mainLayout.addLayout(self.formLayout)
        self.mainLayout.addLayout(self.hboxLayout)

    def evt_saveBatteryBtn(self):
        initValue = float(self.initValue.text())
        effCoeff = float(self.effCoeff.text())
        minEnergy = float(self.minEnergy.text())
        maxEnergy = float(self.maxEnergy.text())
        query = qts.QSqlQuery()
        query.prepare("INSERT INTO Battery (batteryInitialValue, batteryEfficiencyCoefficient, batteryMinEnergy, batteryMaxEnergy) VALUES (:initValue, :effCoeff, :minEnergy, :maxEnergy)")
        query.bindValue(":initValue", initValue)
        query.bindValue(":effCoeff", effCoeff)
        query.bindValue(":minEnergy", minEnergy)
        query.bindValue(":maxEnergy", maxEnergy)
        status = query.exec_()
        if status:
            qtw.QMessageBox.information(self, "Success", "Battery information saved successfully")
            self.close()
        else:
            # qtw.QMessageBox.warning(self, "Database Error", "Database error\n\n{}".format(self.dbBattery.lastError().text()))
            qtw.QMessageBox.warning(self, "Database Error", "Database error")

    def evt_editBatteryBtn(self, idBat):
        initValue = float(self.initValue.text())
        effCoeff = float(self.effCoeff.text())
        minEnergy = float(self.minEnergy.text())
        maxEnergy = float(self.maxEnergy.text())
        query = qts.QSqlQuery()
        query.prepare(
            """UPDATE Battery SET 
            batteryInitialValue=:initValue, 
            batteryEfficiencyCoefficient=:effCoeff, 
            batteryMinEnergy=:minEnergy, 
            batteryMaxEnergy=:maxEnergy 
            WHERE batteryId=:idBat""")
        query.bindValue(":initValue", initValue)
        query.bindValue(":effCoeff", effCoeff)
        query.bindValue(":minEnergy", minEnergy)
        query.bindValue(":maxEnergy", maxEnergy)
        query.bindValue(":idBat", idBat)
        status = query.exec_()
        if status:
            qtw.QMessageBox.information(self, "Success", "Battery information saved successfully")
            self.close()
        else:
            # qtw.QMessageBox.warning(self, "Database Error", "Database error\n\n{}".format(self.dbBattery.lastError().text()))
            qtw.QMessageBox.warning(self, "Database Error", "Database error")

    def evt_saveEVBtn(self):
        initValue = float(self.initValue.text())
        effCoeff = float(self.effCoeff.text())
        minEnergy = float(self.minEnergy.text())
        maxEnergy = float(self.maxEnergy.text())
        query = qts.QSqlQuery()
        query.prepare("INSERT INTO ElectricVehicle (evInitialValue, evEfficiencyCoefficient, evMinEnergy, evMaxEnergy) VALUES (:initValue, :effCoeff, :minEnergy, :maxEnergy)")
        query.bindValue(":initValue", initValue)
        query.bindValue(":effCoeff", effCoeff)
        query.bindValue(":minEnergy", minEnergy)
        query.bindValue(":maxEnergy", maxEnergy)
        status = query.exec_()
        if status:
            qtw.QMessageBox.information(self, "Success", "EV information saved successfully")
            self.close()
        else:
            # qtw.QMessageBox.warning(self, "Database Error", "Database error\n\n{}".format(self.dbBattery.lastError().text()))
            qtw.QMessageBox.warning(self, "Database Error", "Database error")

    def evt_editEVBtn(self, idEV):
        initValue = float(self.initValue.text())
        effCoeff = float(self.effCoeff.text())
        minEnergy = float(self.minEnergy.text())
        maxEnergy = float(self.maxEnergy.text())
        query = qts.QSqlQuery()
        query.prepare(
            """UPDATE ElectricVehicle SET 
            evInitialValue=:initValue, 
            evEfficiencyCoefficient=:effCoeff, 
            evMinEnergy=:minEnergy, 
            evMaxEnergy=:maxEnergy 
            WHERE evId=:idEV""")
        query.bindValue(":initValue", initValue)
        query.bindValue(":effCoeff", effCoeff)
        query.bindValue(":minEnergy", minEnergy)
        query.bindValue(":maxEnergy", maxEnergy)
        query.bindValue(":idEV", idEV)
        status = query.exec_()
        if status:
            qtw.QMessageBox.information(self, "Success", "Electric Vehicle information saved successfully")
            self.close()
        else:
            # qtw.QMessageBox.warning(self, "Database Error", "Database error\n\n{}".format(self.dbBattery.lastError().text()))
            qtw.QMessageBox.warning(self, "Database Error", "Database error")

if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    w=SecondaryWindow(0)
    sys.exit(app.exec_())
