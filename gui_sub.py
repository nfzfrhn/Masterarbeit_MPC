# This is the the second layer of GUI that will be called from the main GUI.


import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtSql as qts
# from secondWindow_ui_1 import Ui_Gui_Secondary                # This is QWidget class
# from secondWindow_ui_2 import Ui_Gui_Secondary                # This is QWidget class
from secondWindow_ui_8 import Ui_Gui_Secondary                # This is QWidget class
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
        self.setWindowIcon(qtg.QIcon("icon/settings.svg"))
        self.resize(1300, 573)

        self.ui.checkBox.setEnabled(False)
        self.ui.checkBox_2.setEnabled(False)
        self.ui.checkBox_2.setChecked(True)
        self.ui.checkBox_3.setEnabled(False)
        self.ui.checkBox_3.setChecked(True)
        # self.ui.num_bat_LE.setText("2")
        # self.ui.num_ev_LE.setText("2")

        # Allow only float as input
        # self.ui.cw_LEdit.setValidator(qtg.QDoubleValidator())
        # self.ui.cz_LEdit.setValidator(qtg.QDoubleValidator())
        # self.ui.cf_LEdit.setValidator(qtg.QDoubleValidator())
        # self.ui.cpip_LEdit.setValidator(qtg.QDoubleValidator())
        # self.ui.kwoa_LEdit.setValidator(qtg.QDoubleValidator())
        # self.ui.kwz_LEdit.setValidator(qtg.QDoubleValidator())
        # self.ui.kfz_LEdit.setValidator(qtg.QDoubleValidator())
        # self.ui.kfpip_LEdit.setValidator(qtg.QDoubleValidator())
        self.ui.m_LEdit.setValidator(qtg.QDoubleValidator())
        self.ui.kwt_LEdit.setValidator(qtg.QDoubleValidator())
        self.ui.kt_LEdit.setValidator(qtg.QDoubleValidator())
        self.ui.mhp_dot_LEdit.setValidator(qtg.QDoubleValidator())
        self.ui.cwat_LEdit.setValidator(qtg.QDoubleValidator())
        self.ui.HP_Power_min_LEdit.setValidator(qtg.QDoubleValidator())
        self.ui.HP_Power_max_LEdit.setValidator(qtg.QDoubleValidator())
        # self.ui.alpha_LEdit.setValidator(qtg.QDoubleValidator())
        # self.ui.a1_LEdit.setValidator(qtg.QDoubleValidator())
        # self.ui.a2_LEdit.setValidator(qtg.QDoubleValidator())
        # self.ui.a3_LEdit.setValidator(qtg.QDoubleValidator())
        # self.ui.b1_LEdit.setValidator(qtg.QDoubleValidator())
        # self.ui.b2_LEdit.setValidator(qtg.QDoubleValidator())
        # self.ui.tau_LEdit.setValidator(qtg.QDoubleValidator())
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
        self.ui.weightA.setValidator(qtg.QDoubleValidator())
        self.ui.weightB.setValidator(qtg.QDoubleValidator())
        self.ui.weightC.setValidator(qtg.QDoubleValidator())
        # self.ui.initTw_LE.setValidator(qtg.QIntValidator())
        # self.ui.initTz_LE.setValidator(qtg.QIntValidator())
        # self.ui.initTf_LE.setValidator(qtg.QIntValidator())
        # self.ui.initTpip_LE.setValidator(qtg.QIntValidator())
        self.ui.initT1_LE.setValidator(qtg.QDoubleValidator())
        self.ui.initT2_LE.setValidator(qtg.QDoubleValidator())
        self.ui.initT3_LE.setValidator(qtg.QDoubleValidator())
        self.ui.initT4_LE.setValidator(qtg.QDoubleValidator())
        # self.ui.initCOP_LE.setValidator(qtg.QDoubleValidator())
        self.ui.refTz_LE.setValidator(qtg.QDoubleValidator())
        # self.ui.refT1_LE.setValidator(qtg.QDoubleValidator())
        # self.ui.refTe_LE.setValidator(qtg.QDoubleValidator())

        # Set the maximum value of the spin box
        self.ui.num_pv_2.setMaximum(1000)

        # Set up the battery table
        self.ui.batTable.setColumnCount(7)
        self.ui.batTable.setHorizontalHeaderLabels(
            ['ID', 'Initial Value[kWh]', 'Efficiency Coefficient', 'Min Energy[kWh]', 'Max Energy[kWh]', 'Max Discharging Power[kW]', 'Max Discharging Power[kW]'])
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
        self.ui.evTable.setColumnCount(7)
        self.ui.evTable.setHorizontalHeaderLabels(
            ['ID', 'Initial Value[kWh]', 'Efficiency Coefficient', 'Min Energy[kWh]', 'Max Energy[kWh]', 'Max Charging Power[kW]', 'Max Discharging Power[kW]'])
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

        # Set the default value of the controller mode
        self.controllerMode = None  # Default mode

        # Set up the database
        db = qts.QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("database/DatabaseParameter.db")

        if db.open():
            query = qts.QSqlQuery()
            print(db.tables())
            if "HeatPump" not in db.tables():
                query.exec_("""CREATE TABLE IF NOT EXISTS HeatPump (
                                heatPumpId INTEGER PRIMARY KEY,                                                        
                                m REAL,
                                kwt REAL,
                                kt REAL,
                                mhp_dot REAL,
                                cwat REAL,                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
                                HP_Power_min REAL,
                                HP_Power_max REAL                                                                                                                                                                                                                    
                                )""")
                db.commit()
            if "Battery" not in db.tables():
                query.exec_("""CREATE TABLE IF NOT EXISTS Battery (
                                batteryId INTEGER PRIMARY KEY AUTOINCREMENT,                                                        
                                batteryInitialValue INTEGER,                            
                                batteryEfficiencyCoefficient REAL,                                                                                    
                                batteryMinEnergy REAL,                                                                                                                                                                                    
                                batteryMaxEnergy REAL,
                                batteryMinPower REAL,
                                batteryMaxPower REAL                                                                                                                                                                                   
                                )""")
                db.commit()
            if "ElectricVehicle" not in db.tables():
                query.exec_("""CREATE TABLE IF NOT EXISTS ElectricVehicle (
                                evId INTEGER PRIMARY KEY AUTOINCREMENT,                                                        
                                evInitialValue INTEGER,                            
                                evEfficiencyCoefficient REAL,                                                                                    
                                evMinEnergy REAL,                                                                                                                                                                                    
                                evMaxEnergy REAL,
                                evMinChargingPower REAL,
                                evMaxChargingPower REAL                                                                                                                                                                                                                    
                                )""")
                db.commit()
            if "SolarPanel" not in db.tables():
                query.exec_("""CREATE TABLE IF NOT EXISTS SolarPanel (
                                solarId INTEGER PRIMARY KEY,
                                solar_module_type TEXT,                                                        
                                solar_n_PV_mod INTEGER,                            
                                solar_G_PV_NOCT REAL,                                                                                    
                                solar_T_PV_NOCT REAL,                                                                                                                                                                                    
                                solar_P_PV_STC REAL,
                                solar_gamma_PV REAL,
                                solar_G_PV_STC REAL,
                                solar_T_PV_STC REAL                                                                                                                                                                                    
                                )""")
                db.commit()
            if "Controller" not in db.tables():
                query.exec_("""CREATE TABLE IF NOT EXISTS Controller (
                                controllerId INTEGER PRIMARY KEY,
                                predictionHorizon_N INTEGER,                                                        
                                controlHorizon_m INTEGER,                            
                                samplingTime INTEGER,                                                                                    
                                daySimulation INTEGER,                                                                                                                                                                                    
                                coeff_A REAL,
                                coeff_B REAL,
                                coeff_C REAL,
                                ref_roomTemperature REAL,
                                rangeTemp REAL,                                
                                initVal_T1 REAL,
                                initVal_T2 REAL,
                                initVal_T3 REAL,
                                initVal_T4 REAL,
                                mode INTEGER                                                                                                                                                                                                               
                                )""")                                   # Should add column for modes
                db.commit()
            self.initHeatPump()
            self.initSolarPanel()
            self.initController()
            # self.populateHeatPumpTab()
            self.populateBatteryTable()
            self.populateEVTable()
            # self.populateSolarTab()
            # self.populateControllerTab()
        else:
            qtw.QMessageBox.warning(self, "Database Error", "Could not open database")

        # Configure the save button
        self.ui.HPSaveBtn.clicked.connect(self.saveHeatPump)
        self.ui.pvSaveBtn.clicked.connect(self.savePV)
        self.ui.ctrlSaveBtn.clicked.connect(self.saveController)

        # Configure the add buttons
        self.ui.batAddBtn.clicked.connect(self.addBattery)
        self.ui.evAddBtn.clicked.connect(self.addEV)
        # self.ui.pvAddBtn.clicked.connect(self.addSolar)       # TODO: Add the save button function

        # Configure the edit buttons
        self.ui.batEditBtn.clicked.connect(self.editBattery)
        self.ui.evEditBtn.clicked.connect(self.editEV)

        self.ui.batTable.itemSelectionChanged.connect(self.enableBatBtn)
        self.ui.evTable.itemSelectionChanged.connect(self.enableEVBtn)
        # self.ui.tableWidget.itemSelectionChanged.connect(self.enablePVBtn) # TODO: Fill the QLineEdit

        # Enable/Disable the edit buttons and delete buttons
        self.ui.batEditBtn.setEnabled(False)
        self.ui.batDelBtn.setEnabled(False)
        self.ui.evEditBtn.setEnabled(False)
        self.ui.evDelBtn.setEnabled(False)
        # self.ui.pvEditBtn.setEnabled(False)
        # self.ui.pvDelBtn.setEnabled(False)

        # Configure the delete buttons
        self.ui.batDelBtn.clicked.connect(self.deleteBattery)
        self.ui.evDelBtn.clicked.connect(self.deleteEV)


        self.ui.defaultMode_radBtn.toggled.connect(lambda: self.btnState(self.ui.defaultMode_radBtn))
        self.ui.energySavingMode_radBtn.toggled.connect(lambda: self.btnState(self.ui.energySavingMode_radBtn))
        self.ui.economicMode_radBtn.toggled.connect(lambda: self.btnState(self.ui.economicMode_radBtn))
        self.ui.advanceMode_radBtn.toggled.connect(self.advanceMode)

        self.ui.tabWidget.currentChanged.connect(self.tabChanged)

        self.ui.tabWidget.setCurrentIndex(initial_tab)

        # Your code ends here
        self.show()

    def advanceMode(self):
        if self.ui.advanceMode_radBtn.isChecked():
            self.ui.mpcParamBox.setEnabled(True)
            self.ui.refTempValue_Box.setEnabled(True)
            self.ui.initValueGBox.setEnabled(True)
        else:
            self.ui.mpcParamBox.setEnabled(False)
            self.ui.refTempValue_Box.setEnabled(False)
            self.ui.initValueGBox.setEnabled(False)

    def btnState(self, btn):
        if btn.text() == "Default Mode":
            if btn.isChecked():
                self.controllerMode = 1
        elif btn.text() == "Energy Saving Mode":
            if btn.isChecked():
                self.controllerMode = 2
        elif btn.text() == "Economic Mode":
            if btn.isChecked():
                self.controllerMode = 3
        print(f"self.controllerMode = {self.controllerMode}")


    def tabChanged(self):
        query = qts.QSqlQuery()
        query.exec_("SELECT COUNT(*) FROM Battery")
        query.next()
        num_bat = query.value(0)

        query.exec_("SELECT COUNT(*) FROM ElectricVehicle")
        query.next()
        num_ev = query.value(0)

        self.ui.num_bat_LE.setText(str(num_bat))
        self.ui.num_ev_LE.setText(str(num_ev))


    def initHeatPump(self):
        # These values are only for initializations. They will be changed by the user, if needed.
        query = qts.QSqlQuery()
        query.exec_("SELECT COUNT(*) FROM HeatPump")
        query.next()
        count = query.value(0)
        if count == 0:
            # Insert default values if the table is empty
            mValue = 720/4
            kwtValue = 0.99
            ktValue = 18.8
            mhp_dotValue = 1.3611
            cwatValue = 4180.0
            HP_Power_minValue = 2.5
            HP_Power_maxValue = 10

            query = qts.QSqlQuery()
            query.prepare("INSERT INTO HeatPump (m, kwt, kt, mhp_dot, cwat, HP_Power_min, HP_Power_max) VALUES (:mValue, :kwtValue, :ktValue, :mhp_dotValue, :cwatValue, :HP_Power_minValue, :HP_Power_maxValue)")
            query.bindValue(":mValue", mValue)
            query.bindValue(":kwtValue", kwtValue)
            query.bindValue(":ktValue", ktValue)
            query.bindValue(":mhp_dotValue", mhp_dotValue)
            query.bindValue(":cwatValue", cwatValue)
            query.bindValue(":HP_Power_minValue", HP_Power_minValue)
            query.bindValue(":HP_Power_maxValue", HP_Power_maxValue)
            query.exec_()
            self.populateHeatPumpTab()
        else:
            self.populateHeatPumpTab()

    def initSolarPanel(self):

        query = qts.QSqlQuery()
        query.exec_("SELECT COUNT(*) FROM SolarPanel")
        query.next()
        count = query.value(0)
        if count == 0:
            solar_module_typeValue = "Globo Brasil Ind. GBR320p"
            solar_n_PV_modValue = 156
            solar_G_PV_NOCTValue = 0.8
            solar_T_PV_NOCTValue = 45
            solar_P_PV_STCValue = 0.32
            solar_gamma_PVValue = -0.43/100
            solar_G_PV_STCValue = 1
            solar_T_PV_STCValue = 25

            query = qts.QSqlQuery()
            query.prepare("INSERT INTO SolarPanel (solar_module_type, solar_n_PV_mod, solar_G_PV_NOCT, solar_T_PV_NOCT, solar_P_PV_STC, solar_gamma_PV, solar_G_PV_STC, solar_T_PV_STC) VALUES (:solar_module_typeValue, :solar_n_PV_modValue, :solar_G_PV_NOCTValue, :solar_T_PV_NOCTValue, :solar_P_PV_STCValue, :solar_gamma_PVValue, :solar_G_PV_STCValue, :solar_T_PV_STCValue)")
            query.bindValue(":solar_module_typeValue", solar_module_typeValue)
            query.bindValue(":solar_n_PV_modValue", solar_n_PV_modValue)
            query.bindValue(":solar_G_PV_NOCTValue", solar_G_PV_NOCTValue)
            query.bindValue(":solar_T_PV_NOCTValue", solar_T_PV_NOCTValue)
            query.bindValue(":solar_P_PV_STCValue", solar_P_PV_STCValue)
            query.bindValue(":solar_gamma_PVValue", solar_gamma_PVValue)
            query.bindValue(":solar_G_PV_STCValue", solar_G_PV_STCValue)
            query.bindValue(":solar_T_PV_STCValue", solar_T_PV_STCValue)
            query.exec_()
            self.populateSolarTab()
        else:
            self.populateSolarTab()

    def initController(self):
        query = qts.QSqlQuery()
        query.exec_("SELECT COUNT(*) FROM Controller")
        query.next()
        count = query.value(0)
        if count == 0:
            prediction_horizonValue = 24
            control_horizonValue = 1
            samplingTimeValue = 15
            daySimulationValue = 6
            coeffW1Value = 10
            coeffW2Value = 0.06
            coeffW3Value = 1
            refRoomTempValue = 23
            rangeTempValue = 2
            init_T1_Value = 50
            init_T2_Value = 50
            init_T3_Value = 50
            init_T4_Value = 50
            ctrlMode = 1 # 1 = Default, 2 = Energy Saving, 3 = Economic

            query = qts.QSqlQuery()
            query.prepare("""INSERT INTO Controller 
                        (predictionHorizon_N, 
                        controlHorizon_m, 
                        samplingTime, 
                        daySimulation, 
                        coeff_A, 
                        coeff_B, 
                        coeff_C, 
                        ref_roomTemperature, 
                        rangeTemp, 
                        initVal_T1, 
                        initVal_T2, 
                        initVal_T3, 
                        initVal_T4,
                        mode)
                VALUES (:prediction_horizonValue, 
                        :control_horizonValue, 
                        :samplingTimeValue, 
                        :daySimulationValue, 
                        :coeffW1Value, 
                        :coeffW2Value, 
                        :coeffW3Value, 
                        :refRoomTempValue, 
                        :rangeTempValue, 
                        :init_T1_Value, 
                        :init_T2_Value, 
                        :init_T3_Value, 
                        :init_T4_Value,
                        :ctrlMode)""")                                         #Need to add mode
            query.bindValue(":prediction_horizonValue", prediction_horizonValue)
            query.bindValue(":control_horizonValue", control_horizonValue)
            query.bindValue(":samplingTimeValue", samplingTimeValue)
            query.bindValue(":daySimulationValue", daySimulationValue)
            query.bindValue(":coeffW1Value", coeffW1Value)
            query.bindValue(":coeffW2Value", coeffW2Value)
            query.bindValue(":coeffW3Value", coeffW3Value)
            query.bindValue(":refRoomTempValue", refRoomTempValue)
            query.bindValue(":rangeTempValue", rangeTempValue)
            query.bindValue(":init_T1_Value", init_T1_Value)
            query.bindValue(":init_T2_Value", init_T2_Value)
            query.bindValue(":init_T3_Value", init_T3_Value)
            query.bindValue(":init_T4_Value", init_T4_Value)
            query.bindValue(":ctrlMode", ctrlMode)
            bOk = query.exec_()
            if bOk:
                print("Controller initialized")
                self.populateControllerTab()
            else:
                print("Controller not initialized {}".format(query.lastError().text()))
        else:
            self.populateControllerTab()

    def populateHeatPumpTab(self):
        query = qts.QSqlQuery()
        bOk = query.exec_("SELECT * FROM HeatPump")
        if bOk:
            while query.next():
                #print(query.value(0))
                self.ui.m_LEdit.setText(str(query.value(1)))
                self.ui.kwt_LEdit.setText(str(query.value(2)))
                self.ui.kt_LEdit.setText(str(query.value(3)))
                self.ui.mhp_dot_LEdit.setText(str(query.value(4)))
                self.ui.cwat_LEdit.setText(str(query.value(5)))
                self.ui.HP_Power_min_LEdit.setText(str(query.value(6)))
                self.ui.HP_Power_max_LEdit.setText(str(query.value(7)))
        else:
            qtw.QMessageBox.warning(self, "HP Database Error", "Could not open database")

    def populateBatteryTable(self):
        query = qts.QSqlQuery()
        bOk = query.exec_("SELECT * FROM Battery")
        if bOk:
            self.ui.batTable.clear()
            self.ui.batTable.setRowCount(0)
            self.ui.batTable.setColumnCount(7)
            self.ui.batTable.setHorizontalHeaderLabels(['ID', 'Initial Value[kWh]', 'Efficiency Coefficient', 'Min Energy[kWh]', 'Max Energy[kWh]', 'Max Discharging Power[kW]', 'Max Charging Power[kW]'])
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
                self.ui.batTable.setItem(rowPosition, 5, qtw.QTableWidgetItem(str(query.value(5))))
                self.ui.batTable.setItem(rowPosition, 6, qtw.QTableWidgetItem(str(query.value(6))))
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
            self.ui.evTable.setColumnCount(7)
            self.ui.evTable.setHorizontalHeaderLabels(
                ['ID', 'Initial Value[kWh]', 'Efficiency Coefficient', 'Min Energy[kWh]', 'Max Energy[kWh]', 'Min Charging Power[kW]', 'Max Charging Power[kW]'])

            while query.next():
                rowPosition = self.ui.evTable.rowCount()
                self.ui.evTable.insertRow(rowPosition)
                self.ui.evTable.setItem(rowPosition, 0, qtw.QTableWidgetItem(str(query.value(0))))
                self.ui.evTable.setItem(rowPosition, 1, qtw.QTableWidgetItem(str(query.value(1))))
                self.ui.evTable.setItem(rowPosition, 2, qtw.QTableWidgetItem(str(query.value(2))))
                self.ui.evTable.setItem(rowPosition, 3, qtw.QTableWidgetItem(str(query.value(3))))
                self.ui.evTable.setItem(rowPosition, 4, qtw.QTableWidgetItem(str(query.value(4))))
                self.ui.evTable.setItem(rowPosition, 5, qtw.QTableWidgetItem(str(query.value(5))))
                self.ui.evTable.setItem(rowPosition, 6, qtw.QTableWidgetItem(str(query.value(6))))
                rowPosition += 1
            # self.ui.evTable.resizeColumnsToContents()

    def populateSolarTab(self):
        query = qts.QSqlQuery()
        bOk = query.exec_("SELECT * FROM SolarPanel")
        if bOk:
            while query.next():
                self.ui.moduleType_LE.setText(str(query.value(1)))
                self.ui.num_pv_2.setValue(int(query.value(2)))
                self.ui.G_PV_NOCT_LE.setText(str(query.value(3)))
                self.ui.T_PV_NOCT_LE.setText(str(query.value(4)))
                self.ui.P_PV_STC.setText(str(query.value(5)))
                self.ui.gamma_PV.setText(str(query.value(6)))
                self.ui.G_PV_STC.setText(str(query.value(7)))
                self.ui.T_PV_STC.setText(str(query.value(8)))
        else:
            qtw.QMessageBox.warning(self, "Solar Database Error", "Database error\n\n{}".format(query.lastError().text()))

    def populateControllerTab(self):
        query = qts.QSqlQuery()
        bOk = query.exec_("SELECT * FROM Controller")
        if bOk:
            while query.next():
                self.ui.predHrznLE.setText(str(query.value(1)))
                #self.ui.cotrlHrznLE.setValue(int(query.value(2)))
                self.ui.cotrlHrznLE.setText(str(query.value(2)))
                self.ui.samplingTimeLE.setText(str(query.value(3)))
                self.ui.daysOfSimLE.setText(str(query.value(4)))
                self.ui.weightA.setText(str(query.value(5)))
                self.ui.weightB.setText(str(query.value(6)))
                self.ui.weightC.setText(str(query.value(7)))
                self.ui.refTz_LE.setText(str(query.value(8)))
                self.ui.rangeTemp_LE.setValue((query.value(9)))
                self.ui.initT1_LE.setText(str(query.value(10)))
                self.ui.initT2_LE.setText(str(query.value(11)))
                self.ui.initT3_LE.setText(str(query.value(12)))
                self.ui.initT4_LE.setText(str(query.value(13)))
                print(f"controller mode is {query.value(14)}")
                self.controllerMode = int(query.value(14))
                if self.controllerMode == 1:
                    self.ui.defaultMode_radBtn.setChecked(True)
                elif self.controllerMode == 2:
                    self.ui.energySavingMode_radBtn.setChecked(True)
                elif self.controllerMode == 3:
                    self.ui.economicMode_radBtn.setChecked(True)
        else:
            qtw.QMessageBox.warning(self, "MPC Database Error", "Database error\n\n{}".format(query.lastError().text()))


    def addBattery(self):
        # dlgBattery = DlgBattery()
        dlgBattery = DlgAddBat()
        dlgBattery.setWindowTitle("Input Battery Information")
        dlgBattery.saveBtn.clicked.connect(dlgBattery.evt_saveBatteryBtn)
        dlgBattery.cancelBtn.clicked.connect(dlgBattery.close)
        dlgBattery.show()
        dlgBattery.exec_()
        self.populateBatteryTable()

    def addEV(self):
        dlgEV = DlgAddEV()
        dlgEV.setWindowTitle("Input Electric Vehicle Information")
        dlgEV.saveBtn.clicked.connect(dlgEV.evt_saveEVBtn)
        dlgEV.cancelBtn.clicked.connect(dlgEV.close)
        dlgEV.show()
        dlgEV.exec_()
        self.populateEVTable()

    def saveHeatPump(self):
        m_value = float(self.ui.m_LEdit.text())
        kwt_value = float(self.ui.kwt_LEdit.text())
        kt_value = float(self.ui.kt_LEdit.text())
        mhp_dot_value = float(self.ui.mhp_dot_LEdit.text())
        cwat_value = float(self.ui.cwat_LEdit.text())
        HP_Power_min_value = float(self.ui.HP_Power_min_LEdit.text())
        HP_Power_max_value = float(self.ui.HP_Power_max_LEdit.text())

        hp_id = 1      # Set just id to 1 to allow only one configuration of heat pump
        # query = qts.QSqlQuery(f"SELECT * FROM HeatPump WHERE id = 1")
        query = qts.QSqlQuery(f"SELECT * FROM HeatPump WHERE heatPumpId = {hp_id}")
        if query.next():
            # if row exists, update the values
            query.prepare("UPDATE HeatPump SET m = :m, kwt = :kwt, kt = :kt, mhp_dot = :mhp_dot, cwat = :cwat, HP_Power_min = :HP_Power_min, HP_Power_max = :HP_Power_max WHERE heatPumpId = :id")
        else:
            # if row doesn't exist, insert the values
            query.prepare("INSERT INTO HeatPump (heatPumpId, m, kwt, kt, mhp_dot, cwat, HP_Power_min, HP_Power_max) VALUES (:id, :m, :kwt, :kt, :mhp_dot, :cwat, :HP_Power_min, :HP_Power_max)")

        query.bindValue(":id", hp_id)
        query.bindValue(":m", m_value)
        query.bindValue(":kwt", kwt_value)
        query.bindValue(":kt", kt_value)
        query.bindValue(":mhp_dot", mhp_dot_value)
        query.bindValue(":cwat", cwat_value)
        query.bindValue(":HP_Power_min", HP_Power_min_value)
        query.bindValue(":HP_Power_max", HP_Power_max_value)

        query.exec_()

        if query.lastInsertId() != -1:
            qtw.QMessageBox.information(self, "Heat Pump Database", "Heat Pump data saved successfully")
        else:
            qtw.QMessageBox.warning(self, "Heat Pump Database Error", "Database error\n\n{}".format(query.lastError().text()))

    def savePV(self):
        moduleName = str(self.ui.moduleType_LE.text())
        num_pv = int(self.ui.num_pv_2.text())
        G_PV_NOCT = float(self.ui.G_PV_NOCT_LE.text())
        T_PV_NOCT = float(self.ui.T_PV_NOCT_LE.text())
        P_PV_STC = float(self.ui.P_PV_STC.text())
        gamma_PV = float(self.ui.gamma_PV.text())
        G_PV_STC = float(self.ui.G_PV_STC.text())
        T_PV_STC = float(self.ui.T_PV_STC.text())

        print(f"module name is {moduleName}")
        pv_id = 1      # Set just id to 1 to allow only one configuration of PV
        query = qts.QSqlQuery(f"SELECT * FROM SolarPanel WHERE solarId = {pv_id}")
        if query.next():
            # if row exists, update the values
            query.prepare("""UPDATE SolarPanel SET 
                solar_module_type = :moduleName, 
                solar_n_PV_mod = :num_pv, 
                solar_G_PV_NOCT = :G_PV_NOCT, 
                solar_T_PV_NOCT = :T_PV_NOCT, 
                solar_P_PV_STC = :P_PV_STC, 
                solar_gamma_PV = :gamma_PV, 
                solar_G_PV_STC = :G_PV_STC, 
                solar_T_PV_STC = :T_PV_STC WHERE solarId = :id""")
        else:
            # if row didnt exist, then create value
            query.prepare("""INSERT INTO SolarPanel 
                (solarId,solar_module_type,solar_n_PV_mod,solar_G_PV_NOCT,solar_T_PV_NOCT,solar_P_PV_STC,solar_gamma_PV,solar_G_PV_STC,solar_T_PV_STC) 
                VALUES(:id, :moduleName, :num_pv, :G_PV_NOCT, :T_PV_NOCT, :P_PV_STC, :gamma_PV, :G_PV_STC, :T_PV_STC)""")

        query.bindValue(":id", pv_id)
        query.bindValue(":moduleName", moduleName)
        query.bindValue(":num_pv", num_pv)
        query.bindValue(":G_PV_NOCT", G_PV_NOCT)
        query.bindValue(":T_PV_NOCT", T_PV_NOCT)
        query.bindValue(":P_PV_STC", P_PV_STC)
        query.bindValue(":gamma_PV", gamma_PV)
        query.bindValue(":G_PV_STC", G_PV_STC)
        query.bindValue(":T_PV_STC", T_PV_STC)

        query.exec_()

        if query.lastInsertId() != -1:
            qtw.QMessageBox.information(self, "PV Database", "PV data saved successfully")
        else:
            qtw.QMessageBox.warning(self, "PV Database Error", "Database error\n\n{}".format(query.lastError().text()))

    def saveController(self):
        pred_N = int(self.ui.predHrznLE.text())
        ctrl_m = int(self.ui.cotrlHrznLE.text())
        samplingTime = int(self.ui.samplingTimeLE.text())
        daySim = int(self.ui.daysOfSimLE.text())
        coeff_A = float(self.ui.weightA.text())
        coeff_B = float(self.ui.weightB.text())
        coeff_C = float(self.ui.weightC.text())
        refRoomTemp = float(self.ui.refTz_LE.text())
        rangeTemp = float(self.ui.rangeTemp_LE.value())
        initVal_T1 = float(self.ui.initT1_LE.text())
        initVal_T2 = float(self.ui.initT2_LE.text())
        initVal_T3 = float(self.ui.initT3_LE.text())
        initVal_T4 = float(self.ui.initT4_LE.text())
        ctrlMode = self.controllerMode

        mpc_id = 1                                              # Make sure only one configuration of MPC is allowed
        query = qts.QSqlQuery(f"SELECT * FROM Controller WHERE controllerId = {mpc_id}")
        if query.next():
            query.prepare("""UPDATE Controller SET
                predictionHorizon_N = :pred_N,
                controlHorizon_m = :ctrl_m,
                samplingTime = :samplingTime,
                daySimulation = :daySim,
                coeff_A = :coeff_A,
                coeff_B = :coeff_B,
                coeff_C = :coeff_C,
                ref_roomTemperature = :refRoomTemp,
                rangeTemp = :rangeTemp,
                initVal_T1 = :initVal_T1,
                initVal_T2 = :initVal_T2,
                initVal_T3 = :initVal_T3,
                initVal_T4 = :initVal_T4,
                mode = :ctrlMode 
                    WHERE controllerId = :id""")
        else:
            query.prepare("""INSERT INTO Controller 
                (controllerId, predictionHorizon_N, controlHorizon_m, samplingTime, daySimulation, coeff_A, coeff_B, coeff_C, ref_roomTemperature, rangeTemp, initVal_T1, initVal_T2, initVal_T3, initVal_T4, mode) 
                VALUES(:id, :pred_N, :ctrl_m, :samplingTime, :daySim, :coeff_A, :coeff_B, :coeff_C, :refRoomTemp, :rangeTemp, :initVal_T1, :initVal_T2, :initVal_T3, :initVal_T4, :ctrlMode)""")
        query.bindValue(":id", mpc_id)
        query.bindValue(":pred_N", pred_N)
        query.bindValue(":ctrl_m", ctrl_m)
        query.bindValue(":samplingTime", samplingTime)
        query.bindValue(":daySim", daySim)
        query.bindValue(":coeff_A", coeff_A)
        query.bindValue(":coeff_B", coeff_B)
        query.bindValue(":coeff_C", coeff_C)
        query.bindValue(":refRoomTemp", refRoomTemp)
        query.bindValue(":rangeTemp", rangeTemp)
        query.bindValue(":initVal_T1", initVal_T1)
        query.bindValue(":initVal_T2", initVal_T2)
        query.bindValue(":initVal_T3", initVal_T3)
        query.bindValue(":initVal_T4", initVal_T4)
        query.bindValue(":ctrlMode", ctrlMode)

        query.exec_()

        if query.lastInsertId() != -1:
            qtw.QMessageBox.information(self, "Controller Database", "Controller data saved successfully")
        else:
            qtw.QMessageBox.warning(self, "Controller Database Error", "Database error\n\n{}".format(query.lastError().text()))


    # Callback functions for the edit buttons
    def editBattery(self):
        dlgUpdate = DlgAddBat()
        dlgUpdate.setWindowTitle("Update Battery Information")
        row = self.ui.batTable.currentRow()
        idBat = self.ui.batTable.item(row, 0).text()
        # print(idBat)
        dlgUpdate.initValue.setText(self.ui.batTable.item(row, 1).text())
        dlgUpdate.effCoeff.setText(self.ui.batTable.item(row, 2).text())
        dlgUpdate.minEnergy.setText(self.ui.batTable.item(row, 3).text())
        dlgUpdate.maxEnergy.setText(self.ui.batTable.item(row, 4).text())
        dlgUpdate.minPower.setText(self.ui.batTable.item(row, 5).text())
        dlgUpdate.maxPower.setText(self.ui.batTable.item(row, 6).text())
        dlgUpdate.saveBtn.clicked.connect(lambda: dlgUpdate.evt_editBatteryBtn(idBat))
        dlgUpdate.cancelBtn.clicked.connect(dlgUpdate.close)
        dlgUpdate.show()
        dlgUpdate.exec_()
        self.populateBatteryTable()

    def editEV(self):
        dlgUpdate = DlgAddEV()
        dlgUpdate.setWindowTitle("Update Electric Vehicle Information")
        row = self.ui.evTable.currentRow()
        idEV = self.ui.evTable.item(row, 0).text()
        # print(idEV)
        dlgUpdate.initValue.setText(self.ui.evTable.item(row, 1).text())
        dlgUpdate.effCoeff.setText(self.ui.evTable.item(row, 2).text())
        dlgUpdate.minEnergy.setText(self.ui.evTable.item(row, 3).text())
        dlgUpdate.maxEnergy.setText(self.ui.evTable.item(row, 4).text())
        dlgUpdate.minPower.setText(self.ui.evTable.item(row, 5).text())
        dlgUpdate.maxPower.setText(self.ui.evTable.item(row, 6).text())
        dlgUpdate.saveBtn.clicked.connect(lambda: dlgUpdate.evt_editEVBtn(idEV))
        dlgUpdate.cancelBtn.clicked.connect(dlgUpdate.close)
        dlgUpdate.show()
        dlgUpdate.exec_()
        self.populateEVTable()

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
        row = self.ui.evTable.currentRow()
        idEV = self.ui.evTable.item(row, 0).text()
        res = qtw.QMessageBox.question(self, "Delete Electric Vehicle", "Are you sure you want to delete this electric vehicle?", qtw.QMessageBox.Yes | qtw.QMessageBox.No)
        if res == qtw.QMessageBox.Yes:
            query = qts.QSqlQuery()
            bOk = query.exec_("DELETE FROM ElectricVehicle WHERE evId = {}".format(idEV))
            if bOk:
                qtw.QMessageBox.information(self, "Electric Vehicle Deleted", "Electric vehicle deleted successfully")
                self.populateEVTable()
            else:
                qtw.QMessageBox.warning(self, "Database Error", "Database error\n\n{}".format(query.lastError().text()))

    # def deleteSolar(self):
    #     pass

    def enableBatBtn(self):
        if self.ui.batTable.selectedItems():
            self.ui.batEditBtn.setEnabled(True)
            self.ui.batDelBtn.setEnabled(True)
        else:
            self.ui.batEditBtn.setEnabled(False)
            self.ui.batDelBtn.setEnabled(False)

    def enableEVBtn(self):
        if self.ui.evTable.selectedItems():
            self.ui.evEditBtn.setEnabled(True)
            self.ui.evDelBtn.setEnabled(True)
        else:
            self.ui.evEditBtn.setEnabled(False)
            self.ui.evDelBtn.setEnabled(False)


# Create a class to handle battery information. Tertiary window
class DlgAddBat(qtw.QDialog):
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
        self.minPower = qtw.QLineEdit()
        self.maxPower = qtw.QLineEdit()

        self.initValue.setPlaceholderText("Initial Energy")
        self.effCoeff.setPlaceholderText("Efficiency Coefficient")
        self.minEnergy.setPlaceholderText("Minimum Allowed Charging State in kWh")
        self.maxEnergy.setPlaceholderText("Maximum Allowed Charging State in kWh")
        self.minPower.setPlaceholderText("Maximum Allowed Discharging Power in kW")
        self.maxPower.setPlaceholderText("Maximum Allowed Charging Power in kW")

        self.initValue.setValidator(qtg.QDoubleValidator())
        self.effCoeff.setValidator(qtg.QDoubleValidator())
        self.minEnergy.setValidator(qtg.QDoubleValidator())
        self.maxEnergy.setValidator(qtg.QDoubleValidator())
        self.minPower.setValidator(qtg.QDoubleValidator())
        self.maxPower.setValidator(qtg.QDoubleValidator())

        self.formLayout.addRow("Initial Energy [kWh]", self.initValue)
        self.formLayout.addRow("Efficiency Coefficient", self.effCoeff)
        self.formLayout.addRow("Minimum Energy [kWh]", self.minEnergy)
        self.formLayout.addRow("Maximum Energy [kWh]", self.maxEnergy)
        self.formLayout.addRow("Maximum Discharging Power [kW]", self.minPower)
        self.formLayout.addRow("Maximum Charging Power [kW]", self.maxPower)

        self.mainLayout.addLayout(self.formLayout)
        self.mainLayout.addLayout(self.hboxLayout)

    def evt_saveBatteryBtn(self):
        initValue = float(self.initValue.text())
        effCoeff = float(self.effCoeff.text())
        minEnergy = float(self.minEnergy.text())
        maxEnergy = float(self.maxEnergy.text())
        minPower = abs(float(self.minPower.text()))*-1
        maxPower = float(self.maxPower.text())

        if minEnergy > maxEnergy or minPower > maxPower:
            qtw.QMessageBox.warning(self, "Error", "Minimum value cannot be greater than maximum value")
            return

        query = qts.QSqlQuery()
        query.prepare("INSERT INTO Battery (batteryInitialValue, batteryEfficiencyCoefficient, batteryMinEnergy, batteryMaxEnergy, batteryMinPower, batteryMaxPower) VALUES (:initValue, :effCoeff, :minEnergy, :maxEnergy, :minPower, :maxPower)")
        query.bindValue(":initValue", initValue)
        query.bindValue(":effCoeff", effCoeff)
        query.bindValue(":minEnergy", minEnergy)
        query.bindValue(":maxEnergy", maxEnergy)
        query.bindValue(":minPower", minPower)
        query.bindValue(":maxPower", maxPower)
        status = query.exec_()
        if status:
            qtw.QMessageBox.information(self, "Success", "Battery information saved successfully")
            self.close()
        else:
            error = query.lastError()
            qtw.QMessageBox.warning(self, "Database Error", "Database error\n\n{}".format(error))
            # qtw.QMessageBox.warning(self, "Database Error", "Database error")

    def evt_editBatteryBtn(self, idBat):
        initValue = float(self.initValue.text())
        effCoeff = float(self.effCoeff.text())
        minEnergy = float(self.minEnergy.text())
        maxEnergy = float(self.maxEnergy.text())
        minPower = abs(float(self.minPower.text()))*-1
        maxPower = float(self.maxPower.text())

        if minEnergy > maxEnergy or minPower > maxPower:
            qtw.QMessageBox.warning(self, "Error", "Minimum value cannot be greater than maximum value")
            return

        #print(initValue, effCoeff, minEnergy, maxEnergy, minPower, maxPower, idBat)

        query = qts.QSqlQuery()
        query.prepare(
            """UPDATE Battery SET 
            batteryInitialValue=:initValue, 
            batteryEfficiencyCoefficient=:effCoeff, 
            batteryMinEnergy=:minEnergy, 
            batteryMaxEnergy=:maxEnergy, 
            batteryMinPower=:minPower,
            batteryMaxPower=:maxPower
            WHERE batteryId=:idBat""")
        query.bindValue(":initValue", initValue)
        query.bindValue(":effCoeff", effCoeff)
        query.bindValue(":minEnergy", minEnergy)
        query.bindValue(":maxEnergy", maxEnergy)
        query.bindValue(":minPower", minPower)
        query.bindValue(":maxPower", maxPower)
        query.bindValue(":idBat", idBat)
        status = query.exec_()
        if status:
            qtw.QMessageBox.information(self, "Success", "Battery information saved successfully")
            self.close()
        else:
            error = query.lastError()
            qtw.QMessageBox.warning(self, "Database Error", "Database error\n\n{}".format(error.text()))
            # qtw.QMessageBox.warning(self, "Database Error", "Database error")

# Create a class to handle EV information. Tertiary window
class DlgAddEV(qtw.QDialog):
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
        self.minPower = qtw.QLineEdit()
        self.maxPower = qtw.QLineEdit()

        self.initValue.setPlaceholderText("Initial Energy")
        self.effCoeff.setPlaceholderText("Efficiency Coefficient")
        self.minEnergy.setPlaceholderText("Minimum Allowed Charging State in kWh")
        self.maxEnergy.setPlaceholderText("Maximum Allowed Charging State in kWh")
        self.minPower.setPlaceholderText("Minimum Allowed Charging Power in kW")
        self.maxPower.setPlaceholderText("Maximum Allowed Charging Power in kW")

        self.initValue.setValidator(qtg.QDoubleValidator())
        self.effCoeff.setValidator(qtg.QDoubleValidator())
        self.minEnergy.setValidator(qtg.QDoubleValidator())
        self.maxEnergy.setValidator(qtg.QDoubleValidator())
        self.minPower.setValidator(qtg.QDoubleValidator())
        self.maxPower.setValidator(qtg.QDoubleValidator())

        self.formLayout.addRow("Initial Energy [kWh]", self.initValue)
        self.formLayout.addRow("Efficiency Coefficient", self.effCoeff)
        self.formLayout.addRow("Minimum Energy [kWh]", self.minEnergy)
        self.formLayout.addRow("Maximum Energy [kWh]", self.maxEnergy)
        self.formLayout.addRow("Minimum Power [kW]", self.minPower)
        self.formLayout.addRow("Maximum Power [kW]", self.maxPower)

        self.mainLayout.addLayout(self.formLayout)
        self.mainLayout.addLayout(self.hboxLayout)

    def evt_saveEVBtn(self):
        initValue = float(self.initValue.text())
        effCoeff = float(self.effCoeff.text())
        minEnergy = float(self.minEnergy.text())
        maxEnergy = float(self.maxEnergy.text())
        minPower = abs(float(self.minPower.text()))*-1
        maxPower = float(self.maxPower.text())

        if minEnergy > maxEnergy or minPower > maxPower:
            qtw.QMessageBox.warning(self, "Error", "Minimum value cannot be greater than maximum value")
            return

        query = qts.QSqlQuery()
        query.prepare("INSERT INTO ElectricVehicle (evInitialValue, evEfficiencyCoefficient, evMinEnergy, evMaxEnergy, evMinChargingPower, evMaxChargingPower) VALUES (:initValue, :effCoeff, :minEnergy, :maxEnergy, :minPower, :maxPower)")
        query.bindValue(":initValue", initValue)
        query.bindValue(":effCoeff", effCoeff)
        query.bindValue(":minEnergy", minEnergy)
        query.bindValue(":maxEnergy", maxEnergy)
        query.bindValue(":minPower", minPower)
        query.bindValue(":maxPower", maxPower)
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
        minPower = abs(float(self.minPower.text()))*-1
        maxPower = float(self.maxPower.text())

        if minEnergy > maxEnergy or minPower > maxPower:
            qtw.QMessageBox.warning(self, "Error", "Minimum value cannot be greater than maximum value")
            return

        query = qts.QSqlQuery()
        query.prepare(
            """UPDATE ElectricVehicle SET 
            evInitialValue=:initValue, 
            evEfficiencyCoefficient=:effCoeff, 
            evMinEnergy=:minEnergy, 
            evMaxEnergy=:maxEnergy, 
            evMinChargingPower=:minPower,
            evMaxChargingPower=:maxPower
            WHERE evId=:idEV""")
        query.bindValue(":initValue", initValue)
        query.bindValue(":effCoeff", effCoeff)
        query.bindValue(":minEnergy", minEnergy)
        query.bindValue(":maxEnergy", maxEnergy)
        query.bindValue(":minPower", minPower)
        query.bindValue(":maxPower", maxPower)
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
