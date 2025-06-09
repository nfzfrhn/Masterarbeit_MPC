import sys

from PyQt5 import QtSql as qts
import numpy as np
import casadi as cs

def readThemAll():

    db = qts.QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName('database/databaseParameter.db')
    if not db.open():
        print("Error: Failed to connect database.")
        return False

    # Battery initialization
    query = qts.QSqlQuery()
    query.exec_("SELECT COUNT(*) FROM Battery")
    query.next()
    num_bat = query.value(0)
    batInit = cs.DM.zeros((num_bat,1))
    batEff = cs.DM.zeros((num_bat,1))
    batMinEnergy = cs.DM.zeros((num_bat,1))
    batMaxEnergy = cs.DM.zeros((num_bat,1))
    batMinPower = cs.DM.zeros((num_bat,1))
    batMaxPower = cs.DM.zeros((num_bat,1))

    bOk = query.exec_("SELECT * FROM Battery")
    if not bOk:
        print("Error: ", query.lastError().text())
        sys.exit(1)

    # Get the column indices for the columns we want to access
    batRecord = query.record()
    batInitIdx = batRecord.indexOf("batteryInitialValue")
    batEffIdx = batRecord.indexOf("batteryEfficiencyCoefficient")
    batMinEnergyIdx = batRecord.indexOf("batteryMinEnergy")
    batMaxEnergyIdx = batRecord.indexOf("batteryMaxEnergy")
    batMinPowerIdx = batRecord.indexOf("batteryMinPower")
    batMaxPowerIdx = batRecord.indexOf("batteryMaxPower")

    i = 0
    while query.next():
        batInit[i] = query.value(batInitIdx)*1000
        batEff[i] = query.value(batEffIdx)
        batMinEnergy[i] = query.value(batMinEnergyIdx)*1000
        batMaxEnergy[i] = query.value(batMaxEnergyIdx)*1000
        batMinPower[i] = query.value(batMinPowerIdx)*1000
        batMaxPower[i] = query.value(batMaxPowerIdx)*1000
        i += 1

    # EV Initialization
    query.exec_("SELECT COUNT(*) FROM ElectricVehicle")
    query.next()
    num_ev = query.value(0)
    evInit = cs.DM.zeros((num_ev,1))
    evEff = cs.DM.zeros((num_ev,1))
    evMinEnergy = cs.DM.zeros((num_ev,1))
    evMaxEnergy = cs.DM.zeros((num_ev,1))
    evMinPower = cs.DM.zeros((num_ev,1))
    evMaxPower = cs.DM.zeros((num_ev,1))

    bOk = query.exec_("SELECT * FROM ElectricVehicle")

    if not bOk:
        print("Error: ", query.lastError().text())
        sys.exit(1)

    evRecord = query.record()
    evInitIdx = evRecord.indexOf("evInitialValue")
    evEffIdx = evRecord.indexOf("evEfficiencyCoefficient")
    evMinEnergyIdx = evRecord.indexOf("evMinEnergy")
    evMaxEnergyIdx = evRecord.indexOf("evMaxEnergy")
    evMinPowerIdx = evRecord.indexOf("evMinChargingPower")
    evMaxPowerIdx = evRecord.indexOf("evMaxChargingPower")

    i = 0
    while query.next():
        evInit[i] = query.value(evInitIdx)*1000
        evEff[i] = query.value(evEffIdx)
        evMinEnergy[i] = query.value(evMinEnergyIdx)*1000
        evMaxEnergy[i] = query.value(evMaxEnergyIdx)*1000
        evMinPower[i] = query.value(evMinPowerIdx)*1000
        evMaxPower[i] = query.value(evMaxPowerIdx)*1000
        i += 1

    # Heat Pump Initialization
    query.exec_("SELECT * FROM HeatPump")
    query.next()
    m = query.value(1)
    kwt = query.value(2)
    kt = query.value(3)
    mhp_dot = query.value(4)
    cwat = query.value(5)
    HP_Power_min = query.value(6)
    HP_Power_max = query.value(7)

    # Solar Panel Initialization
    query.exec_("SELECT * FROM SolarPanel")
    query.next()
    solarModulType = query.value(1)
    solar_n_PV_mod = query.value(2)
    solar_G_PV_NOCT = query.value(3)
    solar_T_PV_NOCT = query.value(4)
    solar_P_PV_STC = query.value(5)
    solar_gamma_PV = query.value(6)
    solar_G_PV_STC = query.value(7)
    solar_T_PV_STC = query.value(8)

    # Controller Initialization
    query.exec_("SELECT * FROM Controller")
    query.next()
    predictionHorizon = query.value(1)
    controlHorizon = query.value(2)
    samplingTime = query.value(3)
    daySimulation = query.value(4)
    coeffW1 = query.value(5)
    coeffW2 = query.value(6)
    coeffW3 = query.value(7)
    ref_room_temp = query.value(8)
    rangeTemp = query.value(9)
    init_T1 = query.value(10)
    init_T2 = query.value(11)
    init_T3 = query.value(12)
    init_T4 = query.value(13)

    for i in range(num_bat):
        print(f"Battery {i} specification: {batInit[i]}, {batEff[i]}, {batMinEnergy[i]}, {batMaxEnergy[i]}, {batMinPower[i]}, {batMaxPower[i]}")

    for i in range(num_ev):
        print(f"EV {i} specification: {evInit[i]}, {evEff[i]}, {evMinEnergy[i]}, {evMaxEnergy[i]}, {evMinPower[i]}, {evMaxPower[i]}")

    print(f"Solar panel specification: Type of Module:{solarModulType}. Number of Module: {solar_n_PV_mod}")
    print(f"G_PV_NOCT: {solar_G_PV_NOCT}")
    print(f"T_PV_NOCT: {solar_T_PV_NOCT}")
    print(f"P_PV_STC: {solar_P_PV_STC}")
    print(f"gamma_PV: {solar_gamma_PV}")
    print(f"G_PV_STC: {solar_G_PV_STC}")
    print(f"T_PV_STC: {solar_T_PV_STC}")

    print(f"Heat Pump specification: m: {m}, kwt: {kwt}, kt: {kt}, mhp_dot: {mhp_dot}, cwat: {cwat}, HP_Power_min: {HP_Power_min}, HP_Power_max: {HP_Power_max}")
    print(f"Controller specification: predictionHorizon: {predictionHorizon}, controlHorizon: {controlHorizon}, samplingTime: {samplingTime}, daySimulation: {daySimulation}, coeffW1: {coeffW1}, coeffW2: {coeffW2}, coeffW3: {coeffW3}, ref_room_temp: {ref_room_temp}, rangeTemp: {rangeTemp}, init_T1: {init_T1}, init_T2: {init_T2}, init_T3: {init_T3}, init_T4: {init_T4}")

    print(f"Number of bat is {num_bat}")
    print(f"Number of EV is {num_ev}")

    # Print type of variables
    print(f"Type predictionHorizon is {type(predictionHorizon)}")
    print(f"Type of coeffW1 is {type(coeffW1)}")

    print(f"Type of init_T1 is {type(init_T1)}")
    print(f"Type of init_T2 is {type(init_T2)}")
    print(f"Type of init_T3 is {type(init_T3)}")
    print(f"Type of init_T4 is {type(init_T4)}")

    # Initialize the state vector
    state_init = [int(init_T1), int(init_T2), int(init_T3), int(init_T4), int(0)]
    #state_init = [int(x) for x in state_init]
    for i in range(num_bat):
        # state_init.extend([2000])
        # Append state_init with batInit
        # state_init.append(batInit[i].full())
        state_init.append(int(batInit[i]))
        print(f"Type of batInit is {type(batInit[i])}")
        print(f"Type of batInit is {type(int(batInit[i]))}")
        print(f"Type of batInit is {type(batInit[i].full())}")

    for i in range(num_ev):
        # state_init.extend([2000])
        # Append state_init with evInit
        # state_init.append(evInit[i].full())
        state_init.append(int(evInit[i]))
        print(f"Type of evInit is {type(int(evInit[i]))}")
        print(f"Type of evInit is {type(evInit[i].full())}")

    xx = np.array(state_init).reshape(1, -1)  # contains the history of states. And we want to make it row vector
    print(state_init)


if __name__ == "__main__":
    readThemAll()