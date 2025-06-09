from scipy import interpolate
import numpy as np
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import logging

# logging.basicConfig(filename='logging_temperature2.log', level=logging.INFO)


def timeConvert(x):
    return 60 * int(x)

def powerConvert(x):
    return 1000*float(x)

def HeizConvert(x):
    g = float(x)
    if g < 0:
        g = 0
    return 1000*g

def priceConvert(x):
    return float(x)/1000

def forceFloat(x):
    return float(x)

def forceInt(x):
    return int(x)

# Length of minutes in a year: 525600
def temperatureData():
    minuten = 15
    yearMinuten = 365*24*60
    newTime = np.arange(0, yearMinuten, minuten)
    # print(type(newTime))

    df1 = pd.read_csv('data/Rembrandt_Saniert_Prognosedaten.CSV', sep=',', decimal=',')
    T = df1["Temperatur [°C]"].to_numpy()
    t1 = df1["Zeit [h]"].to_numpy()
    t2 = df1["Zeit [h]"].apply(timeConvert).to_numpy()

    f = interpolate.interp1d(t2, T, kind='linear', bounds_error=False, fill_value=(T[0], T[-1]))

    Temperature = f(newTime)

    Temperature[0] = T[0]
    Temperature[1] = T[1]

    return newTime, Temperature

# Length of minutes in a year: 525600
def solarData():
    minuten = 15
    yearMinuten = 365*24*60
    newTime = np.arange(0, yearMinuten, minuten)
    #print(newTime)

    df1 = pd.read_csv('data/Rembrandt_Saniert_Prognosedaten.CSV', sep=',', decimal=',')
    # S = df1["Globalstrahlung [kWh/m²]"].apply(powerConvert).to_numpy()
    S = df1["Globalstrahlung [kWh/m²]"].to_numpy()
    t1 = df1["Zeit [h]"].to_numpy()
    t2 = df1["Zeit [h]"].apply(timeConvert).to_numpy()

    f = interpolate.interp1d(t2, S, kind='linear', bounds_error=False, fill_value=(S[0], S[-1]))

    Solar = f(newTime)

    Solar[0] = S[0]
    Solar[1] = S[1]

    return newTime, Solar

# Length of minutes in a year: 525600
def HeizWarmeBedarfData():
    minuten = 15
    yearMinuten = 365*24*60
    newTime = np.arange(0, yearMinuten, minuten)
    #print(newTime)

    df1 = pd.read_csv('data/Rembrandt_Saniert_Prognosedaten.CSV', sep=',', decimal=',')
    H = df1["Heizwärmebedarf [kWh]"].apply(HeizConvert).to_numpy()
    # H = df1["Heizwärmebedarf [kWh]"].apply(powerConvert).to_numpy()
    t1 = df1["Zeit [h]"].to_numpy()
    t2 = df1["Zeit [h]"].apply(timeConvert).to_numpy()

    f = interpolate.interp1d(t2, H, kind='linear', bounds_error=False, fill_value=(H[0], H[-1]))

    HeizWarmeBedarf = f(newTime)

    HeizWarmeBedarf[0] = H[0]
    HeizWarmeBedarf[1] = H[1]

    return newTime, HeizWarmeBedarf

# Length of minutes in a year: 525600
def COP_data():
    minuten = 15
    yearMinuten = 365 * 24 * 60
    newTime = np.arange(0, yearMinuten, minuten)

    df1 = pd.read_csv('data/COP.CSV', sep=',', decimal=',')
    C = df1["COP"].astype(float).to_numpy()
    t2 = df1["T"].astype(float).to_numpy()
    #t2 = df1["T"].apply(timeConvert).to_numpy()

    local_t, local_toa = temperatureData()

    f = interpolate.interp1d(t2, C, kind='linear', bounds_error=False, fill_value=(C[0], C[-1]))
    # f = interpolate.interp1d(t2, C, fill_value="extrapolate")

    local_toa = local_toa.astype(float)
    COP = f(local_toa)

    COP[0] = C[0]
    COP[1] = C[1]

    return newTime, COP

# Length of a minute in 6 days: 6*24*60 = 8640
def priceData():
    minuten = 15
    weekMinuten = 6 * 24 * 60
    newTime = np.arange(0, weekMinuten, minuten)
    print(newTime)

    df1 = pd.read_csv('data/Boersenstrompreise_in_Deutschland_2022.csv', sep=';', decimal=',')
    Price = df1["Strompreis"].apply(priceConvert).to_numpy()
    df_datetime = pd.to_datetime(df1["Datum (GMT+1)"], format='%d.%m.%Y %H:%M')
    df_date = df_datetime.dt.date
    df_hour = df_datetime.dt.hour
    df_minute = df_datetime.dt.minute

    df_elapsedMinutes = (df_datetime - df_datetime[0]).dt.total_seconds() / 60
    df_dayOffset = (df_date - df_date[0]).dt.days * 24 * 60
    df_totalMinutes = df_elapsedMinutes + df_dayOffset

    f = interpolate.interp1d(df_totalMinutes, Price, fill_value="extrapolate")
    # f = interpolate.interp1d(t2, H, kind='linear', bounds_error=False, fill_value=(H[0], H[-1]))

    Price = f(newTime)

    # HeizWarmeBedarf[0] = H[0]
    # HeizWarmeBedarf[1] = H[1]

    # print(len(Price))
    newTime = np.arange(len(Price))

    return newTime, Price

if __name__ == "__main__":
    t_temperature, temperature_outside = temperatureData()
    t_solar, pv_power_raw = solarData()
    t_heiz, heiz_warme_bedarf = HeizWarmeBedarfData()
    t_cop, cop = COP_data()
    t_price, price = priceData()

    # Solar Plant - TODO:Implement using database
    n_PV_mod = 156           # Number of PV modules
    G_PV_NOCT = 0.8          # in 1 W/m^2, STC reference solar irradiance
    T_PV_NOCT = 45           # in 1 °C, NOCT module temperature
    P_PV_STC = 0.32          # in 1 W, STC power per module
    gamma_PV = -0.43/100     # in 1 / °C, STC temperature coefficient of module
    G_PV_STC = 1          # in 1 W/m^2, STC reference solar irradiance
    T_PV_STC = 25            # in 1 °C, STC reference cell temperature

    T_PV_mod = temperature_outside + (T_PV_NOCT - 20) * pv_power_raw / G_PV_NOCT    # in 1 °C, module temperature
    pv_power = 1000*n_PV_mod * P_PV_STC * (pv_power_raw / G_PV_STC) * (1 + gamma_PV * (T_PV_mod - T_PV_STC))  # in 1 kW, PV power

    print("Length of temperature is {}".format(len(t_temperature)))             # Length of minutes in a year: 525600
    print("Length of solar is {}".format(len(t_solar)))                         # Length of minutes in a year: 525600
    print("Length of heiz is {}".format(len(t_heiz)))                           # Length of minutes in a year: 525600
    print("Length of cop is {}".format(len(t_cop)))                             # Length of minutes in a year: 525600
    print("Length of price is {}".format(len(t_price)))                         # Length of minutes in a week: 10080

    T_mpc = 900
    controlHorizon = 1
    mpc_iter = 0
    T_sim = 60
    N = 96

    # startVal = int(T_mpc * controlHorizon * mpc_iter / T_sim)
    startVal = int(T_mpc * controlHorizon * mpc_iter / T_mpc)
    # stepVal = int(T_mpc / T_sim)
    stepVal = int(T_mpc / T_mpc)
    # stopVal = startVal + int(365*(N - 1) * T_mpc / T_sim) + stepVal
    stopVal = startVal + int(365 * (N - 1) * T_mpc / T_mpc) + stepVal
    timeFrame_local = slice(startVal, stopVal, stepVal)

    slice_temp = temperature_outside[timeFrame_local]
    slice_solar = pv_power[timeFrame_local]
    slice_heiz = heiz_warme_bedarf[timeFrame_local]
    slice_cop = cop[timeFrame_local]
    slice_price = price[timeFrame_local]

    print("Length of slice_temp is {}".format(len(slice_temp)))                 # Length of minutes in a year: 35040. 35040/96 = 365
    print("Length of slice_solar is {}".format(len(slice_solar)))               # Length of minutes in a year: 35040. 35040/96 = 365
    print("Length of slice_heiz is {}".format(len(slice_heiz)))                 # Length of minutes in a year: 35040. 35040/96 = 365
    print("Length of slice_cop is {}".format(len(slice_cop)))                   # Length of minutes in a year: 35040. 35040/96 = 365
    print("Length of slice_price is {}".format(len(slice_price)))               # Length of minutes in a week: 576. 576/6 = 96

    # with open('solar_temp_value.txt', 'w') as f:
    #     for i in range(len(temperature_outside)):
    #         print('temperature_outside: {}'.format(temperature_outside[i]), file=f)
    #
    #     for i in range(len(pv_power)):
    #         print('pv_power: {}'.format(pv_power[i]), file=f)

    #plt.plot(t_time[:8640]/1440, pv_power[:8640], label='Solar')
    #plt.plot(t_solar, pv_power, label='Solar')
    plt.plot(t_solar/1440, temperature_outside, label='Temperature')
    plt.plot(t_solar/1440, T_PV_mod, label='Temperature modified')
    plt.legend()
    plt.ylabel('Solar [W]')
    # fig, (ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8) = plt.subplots(8)
    # ax1.plot(t_price/1440, price, label='Price')
    # ax1.set_title('Price')
    # ax1.set_ylabel('Price [€/kWh]')
    # ax1.legend()
    # ax2.plot(slice_price, label='Sliced Price')
    # ax2.set_title('Price')
    # ax2.set_ylabel('Price [€/kWh]')
    # ax2.legend()
    # ax3.plot(t_solar/1440, pv_power, label='Solar')
    # ax3.set_title('Solar')
    # ax3.set_ylabel('Solar [W]')
    # ax3.legend()
    # ax4.plot(slice_solar, label='Sliced Solar')
    # ax4.set_title('Solar')
    # ax4.set_ylabel('Solar [W]')
    # ax4.legend()
    # ax5.plot(t_heiz/1440, heiz_warme_bedarf, label='Heiz')
    # ax5.set_title('Heiz')
    # ax5.set_ylabel('Heiz [W]')
    # ax5.legend()
    # ax6.plot(slice_heiz, label='Sliced Heiz')
    # ax6.set_title('Heiz')
    # ax6.set_ylabel('Heiz [W]')
    # ax6.legend()
    # ax7.plot(t_cop/1440, cop, label='COP')
    # ax7.set_title('COP')
    # ax7.set_ylabel('COP')
    # ax7.legend()
    # ax8.plot(slice_cop, label='Sliced COP')
    # ax8.set_title('COP')
    # ax8.set_ylabel('COP')
    # ax8.legend()
    plt.show()
