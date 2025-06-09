# This is the main file for the GUI of MPC Energy Management System
# _author_ = "Nafiz Farhan Bin Zainurin"
# Master thesis: Design of Modular Model Predictive Controller for Building Automation

import sys
import numpy as np
import scipy as sc
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtSql as qts
from PyQt5 import uic
import random as rd
from pathlib import Path

from primaryWindow_ui_6 import Ui_MainWindow
from gui_sub import SecondaryWindow
from controller import mpc_controller

# Ui_GUI_Main, baseClass = uic.loadUiType("form2.ui")
Ui_LoginForm, baseClass = uic.loadUiType("primaryWindow_ui_4.ui")

matplotlib.use("tkagg")
plt.style.use('seaborn-v0_8-whitegrid')

class MainWindow(baseClass):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("Energy Management System")
        self.setWindowIcon(qtg.QIcon("icon/building.png"))

        #Set window to maximized
        self.showMaximized()

        self.ui.stackedWidget.setCurrentIndex(0)

        self.ui.startBtn.clicked.connect(self.callMPC)
        self.ui.settingBtn.clicked.connect(self.callSetting)
        self.ui.energyBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.buildingBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.batteryBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))
        self.ui.evBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(3))
        self.ui.weatherBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(4))
        self.ui.energyPriceBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(5))

        #Disable SpinBox
        self.ui.setTemp_SpinBox.setEnabled(False)

        # Disable QCheckBox
        self.ui.hp_chkBox.setEnabled(False)
        self.ui.battery_chkBox.setEnabled(False)
        self.ui.ev_chkBox.setEnabled(False)
        # Set QCheckBox to checked
        self.ui.hp_chkBox.setChecked(True)
        self.ui.battery_chkBox.setChecked(True)
        self.ui.ev_chkBox.setChecked(True)

        self.ui.hp_chkBox.stateChanged.connect(self.updateCheckBox)
        self.ui.battery_chkBox.stateChanged.connect(self.updateCheckBox)
        self.ui.ev_chkBox.stateChanged.connect(self.updateCheckBox)

        # TODO: This date functionality can be added later
        date = qtc.QDate(2020, 1, 6)
        self.ui.endDateEV.setDate(date)
        self.ui.endDatePrice.setDate(date)
        self.ui.endDateWeather.setDate(date)
        self.ui.endDateBuilding.setDate(date)
        self.ui.endDateBattery.setDate(date)
        self.ui.endDateEnergy.setDate(date)

        self.ui.startDateEV.setEnabled(False)
        self.ui.startDatePrice.setEnabled(False)
        self.ui.startDateWeather.setEnabled(False)
        self.ui.startDateBuilding.setEnabled(False)
        self.ui.startDateBattery.setEnabled(False)
        self.ui.startDateEnergy.setEnabled(False)

        self.ui.endDateEV.setEnabled(False)
        self.ui.endDatePrice.setEnabled(False)
        self.ui.endDateWeather.setEnabled(False)
        self.ui.endDateBuilding.setEnabled(False)
        self.ui.endDateBattery.setEnabled(False)
        self.ui.endDateEnergy.setEnabled(False)

        # # Set up the battery status table
        # self.ui.batStatusTable.setColumnCount(2)
        # self.ui.batStatusTable.setHorizontalHeaderLabels(["Battery", "Status[%]"])
        # self.ui.batStatusTable.horizontalHeader().setStretchLastSection(True)
        # self.ui.batStatusTable.horizontalHeader().setSectionResizeMode(qtw.QHeaderView.Stretch)
        # self.ui.batStatusTable.resizeColumnsToContents()
        # self.ui.batStatusTable.setEditTriggers(qtw.QAbstractItemView.NoEditTriggers)
        # self.ui.batStatusTable.horizontalHeader().setStyleSheet("QHeaderView::section {background-color: #f0f0f0;}")
        # self.ui.batStatusTable.verticalHeader().setVisible(False)
        # self.ui.batStatusTable.horizontalHeaderItem(0).setTextAlignment(qtc.Qt.AlignCenter)

        # # Set up the EV status table
        # self.ui.evStatusTable.setColumnCount(2)
        # self.ui.evStatusTable.setHorizontalHeaderLabels(["EV", "Status[%]"])
        # self.ui.evStatusTable.horizontalHeader().setStretchLastSection(True)
        # self.ui.evStatusTable.horizontalHeader().setSectionResizeMode(qtw.QHeaderView.Stretch)
        # self.ui.evStatusTable.resizeColumnsToContents()
        # self.ui.evStatusTable.setEditTriggers(qtw.QAbstractItemView.NoEditTriggers)
        # self.ui.evStatusTable.horizontalHeader().setStyleSheet("QHeaderView::section {background-color: #f0f0f0;}")
        # self.ui.evStatusTable.verticalHeader().setVisible(False)
        # self.ui.evStatusTable.horizontalHeaderItem(0).setTextAlignment(qtc.Qt.AlignCenter)

        self.total_pv = np.array([])

        with open('log_u_array.txt', 'r') as f:
            log_u_array = np.loadtxt(f)
            total_pv = np.append(self.total_pv, log_u_array[:, 2] + log_u_array[:, 5])

        with open('log_xx_array.txt', 'r') as f:
            log_xx_array = np.loadtxt(f)

        with open('log_yy_array.txt', 'r') as f:
            log_yy_array = np.loadtxt(f)

        with open('log_soc_lower.txt', 'r') as f:
            log_soc_lower = np.loadtxt(f)

        with open('log_soc_upper.txt', 'r') as f:
            log_soc_upper = np.loadtxt(f)

        self.n_states = log_xx_array.shape[1]
        self.n_controls = log_u_array.shape[1]
        # self.n_outputs = log_yy_array.shape[1]

        db = qts.QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("database/databaseParameter.db")
        if not db.open():
            print("Error: Failed to connect database.")
            return False

        query = qts.QSqlQuery()
        query.exec_("SELECT COUNT(*) FROM Battery")
        query.next()
        self.num_bat = query.value(0)

        query.exec_("SELECT COUNT(*) FROM ElectricVehicle")
        query.next()
        self.num_ev = query.value(0)

        self.P_wp = log_u_array[:, 0]
        self.P_pv_used = log_u_array[:, 1]
        self.mt_dot = log_u_array[:, 2]
        self.Toa = log_u_array[:, 3]
        self.P_pv_sold = log_u_array[:, 4]
        self.QBedarf = log_u_array[:, 5]
        self.COP = log_u_array[:, 6]
        self.P_cost = log_u_array[:, 7]

        self.offset_bat_con = self.n_controls - self.num_bat - self.num_ev
        self.offset_ev_con = self.offset_bat_con

        self.P_bat = np.zeros([self.num_bat,log_u_array.shape[0]])
        self.P_ev = np.zeros([self.num_ev,log_u_array.shape[0]])

        index_bat_con = 0
        for i in range(self.offset_bat_con, self.offset_bat_con + self.num_bat):
            if self.num_bat >= 1:
                self.P_bat[index_bat_con,:] = log_u_array[:, i]
                self.offset_ev_con += 1
                index_bat_con += 1

        index_ev_con = 0
        for i in range(self.offset_ev_con, self.offset_ev_con + self.num_ev):
            if self.num_ev >= 1:
                self.P_ev[index_ev_con,:] = log_u_array[:, i]
                index_ev_con += 1

        self.T1 = log_xx_array[:, 0]
        self.T2 = log_xx_array[:, 1]
        self.T3 = log_xx_array[:, 2]
        self.T4 = log_xx_array[:, 3]
        self.time_it = log_xx_array[:, 4]

        self.offset_bat_st = self.n_states - self.num_bat - self.num_ev
        self.offset_ev_st = self.offset_bat_st

        self.SOC_Bat = np.zeros([self.num_bat,log_xx_array.shape[0]])
        self.SOC_EV = np.zeros([self.num_ev,log_xx_array.shape[0]])

        index_bat_st = 0
        for i in range(self.offset_bat_st, self.offset_bat_st + self.num_bat):
            if self.num_bat >= 1:
                self.SOC_Bat[index_bat_st,:] = log_xx_array[:, i]
                self.offset_ev_st += 1
                index_bat_st += 1

        index_ev_st = 0
        for i in range(self.offset_ev_st, self.offset_ev_st + self.num_ev):
            if self.num_ev >= 1:
                self.SOC_EV[index_ev_st,:] = log_xx_array[:, i]
                index_ev_st += 1


        # self.SOC_Bat1 = log_xx_array[:, 5]
        # self.SOC_Bat2 = log_xx_array[:, 6]
        # self.SOC_EV1 = log_xx_array[:, 7]
        # self.SOC_EV2 = log_xx_array[:, 8]

        # self.SOC_EV_lower = log_soc_lower
        # self.SOC_EV_upper = log_soc_upper
        self.soc_upper = np.zeros([self.num_ev,log_soc_upper.shape[1]])
        self.soc_lower = np.zeros([self.num_ev,log_soc_lower.shape[1]])
        for i in range(self.num_ev):
            self.soc_upper[i,:] = log_soc_upper[i, :]
            self.soc_lower[i,:] = log_soc_lower[i, :]
        # self.soc_upper1 = log_soc_upper[0, :]
        # self.soc_upper2 = log_soc_upper[1, :]
        # self.soc_lower1 = log_soc_lower[0, :]
        # self.soc_lower2 = log_soc_lower[1, :]

        self.t_ev_limit = np.arange(len(self.soc_upper[0,:]))/96

        self.PV_sold = self.P_pv_sold

        #self.t = np.arange(len(self.P_wp))/96
        self.T_st = np.arange(log_xx_array.shape[0])/96
        self.T_con = np.arange(log_u_array.shape[0])/96

        self.powerEV_Plot()
        self.socEV_Plot()
        self.solarEnergyPlot()
        self.dailyEnergyConsumptionPlot()
        self.hpTempPlot()
        self.energyPricePlot()
        self.copPlot()
        self.energyGenPlot()
        self.pvSoldPlot()
        self.energyConsumePlot()
        self.socBat_Plot()
        self.powerBat_Plot()
        self.toaPlot()
        self.show()

    def callMPC(self):
        self.ui.startBtn.setEnabled(False)
        states, output, control, lbg, ubg, lbx, ubx, t, times, soc_lower, soc_upper, num_bat, num_ev = mpc_controller()
        self.n_states = states.shape[1]
        self.n_controls = control.shape[1]
        self.num_bat = num_bat
        self.num_ev = num_ev
        np.savetxt('log_xx_array.txt', states, fmt='%.5f')
        np.savetxt('log_yy_array.txt', output, fmt='%.5f')
        np.savetxt('log_u_array.txt', control, fmt='%.5f')
        np.savetxt('log_lbg_array.txt', lbg, fmt='%.5f')
        np.savetxt('log_ubg_array.txt', ubg, fmt='%.5f')
        np.savetxt('log_lbx_array.txt', lbx, fmt='%.5f')
        np.savetxt('log_ubx_array.txt', ubx, fmt='%.5f')
        np.savetxt('log_soc_lower.txt', soc_lower, fmt='%.5f')
        np.savetxt('log_soc_upper.txt', soc_upper, fmt='%.5f')

        self.P_hp = control[:, 0]
        self.P_pv_used = control[:, 1]
        self.mt_dot = control[:, 2]
        self.toa = control[:, 3]
        self.P_pv_sold = control[:, 4]
        self.QBedarf = control[:, 5]
        self.COP = control[:, 6]
        self.P_cost = control[:, 7]

        self.offset_bat_con = self.n_controls - self.num_bat - self.num_ev
        self.offset_ev_con = self.offset_bat_con

        self.P_bat = np.zeros([self.num_bat, control.shape[0]])
        self.P_ev = np.zeros([self.num_ev, control.shape[0]])

        index_bat_con = 0
        for i in range(self.offset_bat_con, self.offset_bat_con + self.num_bat):
            if self.num_bat >= 1:
                self.P_bat[index_bat_con,:] = control[:, i]
                self.offset_ev_con += 1
                index_bat_con += 1

        index_ev_con = 0
        for i in range(self.offset_ev_con, self.offset_ev_con + self.num_ev):
            if self.num_ev >= 1:
                self.P_ev[index_ev_con,:] = control[:, i]
                index_ev_con += 1

        self.T1 = states[:, 0]
        self.T2 = states[:, 1]
        self.T3 = states[:, 2]
        self.T4 = states[:, 3]
        self.time_it = states[:, 4]

        self.offset_bat_st = self.n_states - self.num_bat - self.num_ev
        self.offset_ev_st = self.offset_bat_st

        self.SOC_Bat = np.zeros([self.num_bat, states.shape[0]])
        self.SOC_EV = np.zeros([self.num_ev, states.shape[0]])

        index_bat_st = 0
        for i in range(self.offset_bat_st, self.offset_bat_st + self.num_bat):
            if self.num_bat >= 1:
                self.SOC_Bat[index_bat_st,:] = states[:, i]
                self.offset_ev_st += 1
                index_bat_st += 1

        index_ev_st = 0
        for i in range(self.offset_ev_st, self.offset_ev_st + self.num_ev):
            if self.num_ev >= 1:
                self.SOC_EV[index_ev_st,:] = states[:, i]
                index_ev_st += 1

        self.powerEV_Plot()
        self.socEV_Plot()
        self.solarEnergyPlot()
        self.dailyEnergyConsumptionPlot()
        self.hpTempPlot()
        self.energyPricePlot()
        self.copPlot()
        self.energyGenPlot()
        self.pvSoldPlot()
        self.energyConsumePlot()
        self.socBat_Plot()
        self.powerBat_Plot()
        self.toaPlot()

        self.ui.startBtn.setEnabled(True)


    def callSetting(self):
        self.secWindow = SecondaryWindow(0)
        self.secWindow.show()
        #self.secWindow.exec()

    def selectFiles(self):
        res = qtw.QFileDialog.getOpenFileNames(self,"Select solar data", str(Path.cwd()), "CSV File *.csv()")

    def powerEV_Plot(self):
        #data = [rd.random() for i in range(10)]
        layout = qtw.QVBoxLayout()
        figured = plt.figure()
        figured.clear()
        ax = figured.add_subplot(111)
        #t = np.arange(len(self.P_ev[0,:])) / 96
        for i in range(self.num_ev):
            ax.plot(self.T_con, self.P_ev[i,:]/1000, label='Power EV_' + str(i+1))
        # ax.plot(t, self.P_ev1/1000, label='Power EV_1')
        # ax.plot(t, self.P_ev2/1000, label='Power EV_2')
        ax.set_ylabel('Power [kW]')
        ax.set_xlabel('Days')
        ax.legend()
        canvas = FigureCanvas(figured)
        canvas.draw()
        layout.addWidget(canvas)
        self.ui.powerEV_Frame.setLayout(layout)

    def socEV_Plot(self):
        # data = [rd.random() for i in range(10)]
        layout = qtw.QVBoxLayout()
        figured = plt.figure()
        figured.clear()
        ax = figured.add_subplot(111)
        #t = np.arange(len(self.SOC_EV[0,:])) / 96
        len_soc = len(self.SOC_EV[0,:])
        for i in range(self.num_ev):
            ax.plot(self.T_st, self.SOC_EV[i, :] / 1000, label='SOC EV_' + str(i + 1))
            ax.plot(self.T_st, self.soc_lower[i, :len_soc] / 1000, linestyle='--')
            ax.plot(self.T_st, self.soc_upper[i, :len_soc] / 1000, linestyle='--')
        # ax.plot(t,self.SOC_EV1/1000, label='SOC EV')
        # ax.plot(t,self.SOC_EV2/1000, label='SOC EV')
        # ax.plot(t,self.soc_lower1[:len_soc]/1000, linestyle='--')
        # ax.plot(t,self.soc_upper1[:len_soc]/1000, linestyle='--')
        # ax.plot(t,self.soc_lower2[:len_soc]/1000, linestyle='--')
        # ax.plot(t,self.soc_upper2[:len_soc]/1000, linestyle='--')
        ax.set_ylabel('SOC [kWh]')
        ax.set_xlabel('Days')
        ax.legend()
        canvas = FigureCanvas(figured)
        canvas.draw()
        layout.addWidget(canvas)
        self.ui.socEV_Frame.setLayout(layout)

    def solarEnergyPlot(self):
        # data = [rd.random() for i in range(10)]
        layout = qtw.QVBoxLayout()
        figured = plt.figure()
        figured.clear()
        ax = figured.add_subplot(111)
        #t = np.arange(len(self.P_pv_used)) / 96
        ax.plot(self.T_con,(self.P_pv_used+self.P_pv_sold)/1000, label='Solar Energy')
        ax.set_ylabel('Power [kW]')
        ax.set_xlabel('Days')
        ax.legend()
        canvas = FigureCanvas(figured)
        canvas.draw()
        layout.addWidget(canvas)
        self.ui.solarEnergyFrame.setLayout(layout)

    # TODO
    def dailyEnergyConsumptionPlot(self):
        # data = [rd.random() for i in range(10)]
        #t = np.arange(len(self.P_bat1)) / 96
        data = np.random.randint(20, 23, [len(self.T_con)])
        layout = qtw.QVBoxLayout()
        figured = plt.figure()
        figured.clear()
        ax = figured.add_subplot(111)
        #t = np.arange(len(self.P_bat1)) / 96
        ax.plot(self.T_con,data, label='T_room')
        ax.set_ylim(15, 25)
        ax.set_ylabel('Room Temperature [°C]')
        ax.set_xlabel('Days')
        ax.legend()
        canvas = FigureCanvas(figured)
        canvas.draw()
        layout.addWidget(canvas)
        self.ui.indoorTempFrame.setLayout(layout)

    def hpTempPlot(self):
        data = [rd.random() for i in range(10)]
        layout = qtw.QVBoxLayout()
        figured = plt.figure()
        figured.clear()
        ax = figured.add_subplot(111)
        #t = np.arange(len(self.T1)) / 96
        ts = np.arange(len(self.Toa)) / 96
        ax.plot(self.T_st,70*np.ones(len(self.T_st)),'r--')
        ax.plot(self.T_st,self.T1, label='T1', color = '#ff8000')
        ax.plot(self.T_st,self.T2, label='T2',color = '#00cc00')
        ax.plot(self.T_st,self.T3, label='T3',color = '#0066cc')
        ax.plot(self.T_st,self.T4, label='T4',color = '#9933ff')
        ax.plot(ts,40-30/21*self.Toa,'r--')
        ax.set_ylim(0, 80)
        ax.set_ylabel('Temperature [°C]')
        ax.set_xlabel('Days')
        ax.legend()
        canvas = FigureCanvas(figured)
        canvas.draw()
        layout.addWidget(canvas)
        self.ui.hpTempFrame.setLayout(layout)

    def energyPricePlot(self):
        data = [rd.random() for i in range(10)]
        layout = qtw.QVBoxLayout()
        figured = plt.figure()
        figured.clear()
        ax = figured.add_subplot(111)
        #t = np.arange(len(self.P_cost)) / 96
        ax.plot(self.T_con,self.P_cost, label='Energy Price')
        ax.set_ylabel('Price [€/kWh]')
        ax.set_xlabel('Days')
        ax.legend()
        canvas = FigureCanvas(figured)
        canvas.draw()
        layout.addWidget(canvas)
        self.ui.energyPriceFrame.setLayout(layout)

    def copPlot(self):
        data = [rd.random() for i in range(10)]
        layout = qtw.QVBoxLayout()
        figured = plt.figure()
        figured.clear()
        ax = figured.add_subplot(111)
        #t = np.arange(len(self.COP)) / 96
        ax.plot(self.T_con,self.COP, label='COP')
        ax.set_ylabel('COP')
        ax.set_xlabel('Days')
        ax.legend()
        canvas = FigureCanvas(figured)
        canvas.draw()
        layout.addWidget(canvas)
        self.ui.copFrame.setLayout(layout)

    def energyGenPlot(self):
        data = [rd.random() for i in range(10)]
        layout = qtw.QVBoxLayout()
        figured = plt.figure()
        figured.clear()
        ax = figured.add_subplot(111)
        #t = np.arange(len(self.P_pv_used)) / 96
        P_bat_total = 0
        P_bat_discharge = 0
        for i in range(self.num_bat):
            P_bat_total += self.P_bat[i]
            P_bat_discharge += self.P_bat[i]*(self.P_bat[i]<0)
        P_ev_total = 0
        for i in range(self.num_ev):
            P_ev_total += self.P_ev[i]
        # ax.plot(self.T_con, (self.P_wp + self.P_pv_sold + self.P_bat1 + self.P_bat2 + self.P_ev1 + self.P_ev2
        #             - self.P_bat1*(self.P_bat1<0) - self.P_bat2*(self.P_bat2<0))/1000, label='Total Power Generated')
        ax.plot(self.T_con, (self.P_wp + self.P_pv_sold + P_bat_total + P_ev_total
                    - P_bat_discharge)/1000, label='Total Power Generated')
        ax.set_ylabel('Power [kW]')
        ax.set_xlabel('Days')
        ax.legend()
        canvas = FigureCanvas(figured)
        canvas.draw()
        layout.addWidget(canvas)
        self.ui.energyGenFrame.setLayout(layout)

    def pvSoldPlot(self):
        data = [rd.random() for i in range(10)]
        # layout = qtw.QVBoxLayout()
        # figured = plt.figure()
        # figured.clear()
        # ax = figured.add_subplot(111)
        # t = np.arange(len(self.P_pv_sold)) / 96
        # ax.plot(t, self.P_pv_sold, label='P_pv_sold')
        # ax.set_ylabel('Power [W]')
        # ax.set_xlabel('Days')
        # ax.legend()
        # canvas = FigureCanvas(figured)
        # canvas.draw()
        # layout.addWidget(canvas)
        # self.ui.pvSoldFrame.setLayout(layout)

    def energyConsumePlot(self):
        data = [rd.random() for i in range(10)]
        layout = qtw.QVBoxLayout()
        figured = plt.figure()
        figured.clear()
        ax = figured.add_subplot(111)
        # self.line_P_wp = ax.plot(self.T_con, self.P_wp/1000, label='Heat Pump')
        # self.line_QBedarf = ax.plot(self.T_con, self.QBedarf/1000, label='Heat Demand')
        # self.line_P_bat = ax.plot(self.T_con, self.P_bat1*(self.P_bat1>0)/1000, label='Battery')
        # self.line_P_ev1 = ax.plot(self.T_con, self.P_ev1/1000, label='Electric Vehicle')
        ax.plot(self.T_con, self.P_wp / 1000, label='Heat Pump')
        ax_2 = ax.twinx()
        ax_2.plot(self.T_con, self.QBedarf / 1000, label='Heat Demand', linestyle='--', color = 'red')
        for i in range(self.num_bat):
            ax.plot(self.T_con, self.P_bat[i,:]*(self.P_bat[i,:]>0)/1000, label='Battery '+str(i+1))
        for i in range(self.num_ev):
            ax.plot(self.T_con, self.P_ev[i,:]/1000, label='Electric Vehicle '+str(i+1))
        yticks = np.arange(0,30,5)
        ax.set_yticks(yticks)
        ax_2.set_yticks(yticks)
        ax.set_ylabel('Power [kW]')
        ax_2.set_ylabel('Heat Demand [kW]')
        ax.set_xlabel('Days')
        ax.legend()
        canvas = FigureCanvas(figured)
        canvas.draw()
        layout.addWidget(canvas)
        self.ui.energyConsumeFrame.setLayout(layout)

    def socBat_Plot(self):
        data = [rd.random() for i in range(10)]
        layout = qtw.QVBoxLayout()
        figured = plt.figure()
        figured.clear()
        ax = figured.add_subplot(111)
        #t = np.arange(len(self.SOC_Bat1)) / 96
        for i in range(self.num_bat):
            ax.plot(self.T_st,self.SOC_Bat[i,:]/1000, label='SOC_Bat '+str(i+1))
        # ax.plot(t,self.SOC_Bat1/1000, label='SOC_Bat_1')
        # ax.plot(t,self.SOC_Bat2/1000, label='SOC_Bat_2')
        ax.set_ylabel('SOC [kWh]')
        ax.set_xlabel('Days')
        ax.legend()
        canvas = FigureCanvas(figured)
        canvas.draw()
        layout.addWidget(canvas)
        self.ui.socBat_Frame.setLayout(layout)

    def periodReportingPlot(self):
        pass

    def powerBat_Plot(self):
        data = [rd.random() for i in range(10)]
        layout = qtw.QVBoxLayout()
        figured = plt.figure()
        figured.clear()
        ax = figured.add_subplot(111)
        #t = np.arange(len(self.P_bat1)) / 96
        for i in range(self.num_bat):
            ax.plot(self.T_con,self.P_bat[i,:]/1000, label='Charging/Discharging Power of Battery '+str(i+1))
        # ax.plot(self.T_con,self.P_bat1/1000, label='Charging/Discharging Power of Battery 1')
        # ax.plot(self.T_con,self.P_bat2/1000, label='Charging/Discharging Power of Battery 2')
        ax.set_ylabel('Power [kW]')
        ax.set_xlabel('Days')
        ax.legend()
        canvas = FigureCanvas(figured)
        canvas.draw()
        layout.addWidget(canvas)
        self.ui.powerBat_Frame.setLayout(layout)

    def toaPlot(self):
        data = [rd.random() for i in range(10)]
        layout = qtw.QVBoxLayout()
        figured = plt.figure()
        figured.clear()
        ax = figured.add_subplot(111)
        #t = np.arange(len(self.Toa)) / 96
        ax.plot(self.T_con,self.Toa, label='Outside Temperature')
        ax.set_ylabel('Temperature [°C]')
        ax.set_xlabel('Days')
        ax.legend()
        canvas = FigureCanvas(figured)
        canvas.draw()
        layout.addWidget(canvas)
        self.ui.powerBat_Frame.setLayout(layout)
        self.ui.toaFrame.setLayout(layout)

    def updateCheckBox(self):
        # if self.ui.hp_chkBox.isChecked():
        #     self.ui.checkBox.setText("True")
        # else:
        #     self.ui.checkBox.setText("False")
        self.line_P_wp.set_visible(self.ui.hp_chkBox.isChecked())
        self.line_P_bat.set_visible(self.ui.battery_chkBox.isChecked())
        self.line_P_ev.set_visible(self.ui.ev_chkBox.isChecked())
        #self.ui.energyConsumeFrame.canvas.draw()


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)

    #num_bat = 1
    #num_ev = 1
    #states = initState(num_bat, num_ev)
    #controls =initControl(num_bat, num_ev)

    #rhs = states[1]+controls[1]

    #f = Function('f', [states, controls], [rhs])

    w = MainWindow()
    sys.exit(app.exec_())