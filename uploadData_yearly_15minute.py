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

def temperatureData():
    # df = pd.read_csv('data/Rembrandt_Saniert_Prognosedaten.CSV', sep=',', decimal=',')
    df = pd.read_excel('data/Rembrandt_Saniert_Prognosedaten.xlsx')

    interval = 0.25
    # totalLength = 6 * 24 * 60
    t = df['Zeit [h]'].to_numpy()
    time = np.arange(0, len(t), interval)

    T = df['Temperatur [°C]'].apply(forceFloat).to_numpy()
    f = interpolate.interp1d(t, T, kind='linear', bounds_error=False, fill_value=(T[0], T[-1]))

    Temperature = f(time)

    # To avoid NaN values at the beginning
    Temperature[0] = T[0]
    Temperature[1] = T[1]

    return time, Temperature

def solarData():
    # df = pd.read_csv('data/Rembrandt_Saniert_Prognosedaten.CSV', sep=',', decimal=',')
    df = pd.read_excel('data/Rembrandt_Saniert_Prognosedaten.xlsx')

    interval = 0.25
    # totalLength = 6 * 24 * 60
    t = df['Zeit [h]'].to_numpy()
    time = np.arange(0, len(t), interval)

    S = df['Globalstrahlung [kWh/m²]'].apply(forceFloat).to_numpy()
    f = interpolate.interp1d(t, S, kind='linear', bounds_error=False, fill_value=(S[0], S[-1]))

    Solar = f(time)

    # To avoid NaN values at the beginning
    Solar[0] = S[0]
    Solar[1] = S[1]

    return time, Solar

def HeizWarmeBedarfData():
    # df = pd.read_csv('data/Rembrandt_Saniert_Prognosedaten.CSV', sep=',', decimal=',')
    df = pd.read_excel('data/Rembrandt_Saniert_Prognosedaten.xlsx')

    interval = 0.25
    # totalLength = 6 * 24 * 60
    t = df['Zeit [h]'].to_numpy()
    time = np.arange(0, len(t), interval)

    H = df['Heizwärmebedarf [kWh]'].apply(HeizConvert).to_numpy()
    f = interpolate.interp1d(t, H, kind='linear', bounds_error=False, fill_value=(H[0], H[-1]))

    Heat = f(time)

    # To avoid NaN values at the beginning
    Heat[0] = H[0]
    Heat[1] = H[1]

    return time, Heat

# Length of minutes in a year: 525600
def COP_data():
    df1 = pd.read_csv('data/COP.CSV', sep=',', decimal=',')
    C = df1["COP"].astype(float).to_numpy()
    t2 = df1["T"].astype(float).to_numpy()
    #t2 = df1["T"].apply(timeConvert).to_numpy()

    local_t, local_toa = temperatureData()

    f = interpolate.interp1d(t2, C, kind='linear', bounds_error=False, fill_value=(C[0], C[-1]))
    # f = interpolate.interp1d(t2, C, fill_value="extrapolate")

    local_toa = local_toa.astype(float)
    COP = f(local_toa)

    # To avoid NaN values at the beginning
    COP[0] = C[0]
    COP[1] = C[1]

    time = np.arange(len(COP))

    return time, COP

# Length of a minute in 6 days: 6*24*60 = 8640
# We just need the y-axis values: Price. Done!
def priceData():
    minuten = 1
    weekMinuten = 6 * 24 * 60
    newTime = np.arange(0, weekMinuten, minuten)
    # print(newTime)

    df1 = pd.read_csv('data/Boersenstrompreise_in_Deutschland_2022.csv', sep=';', decimal=',')
    Price = df1["Strompreis"].apply(priceConvert).to_numpy()
    df_datetime = pd.to_datetime(df1["Datum (GMT+1)"], format='%d.%m.%Y %H:%M')
    df_date = df_datetime.dt.date
    df_hour = df_datetime.dt.hour
    df_minute = df_datetime.dt.minute
    # print(f"df_minute is {df_minute}")

    df_elapsedMinutes = (df_datetime - df_datetime[0]).dt.total_seconds() / 60
    df_dayOffset = (df_date - df_date[0]).dt.days * 24 * 60
    df_totalMinutes = df_elapsedMinutes + df_dayOffset

    f = interpolate.interp1d(df_totalMinutes, Price, fill_value="extrapolate")
    # f = interpolate.interp1d(t2, H, kind='linear', bounds_error=False, fill_value=(H[0], H[-1]))

    #Price = f(newTime)

    # HeizWarmeBedarf[0] = H[0]
    # HeizWarmeBedarf[1] = H[1]

    # print(len(Price))
    newTime = np.arange(len(Price))
    a = np.arange(len(Price))
    return a, Price

if __name__ == "__main__":
    t_cop, cop = COP_data()
    t_price, price = priceData()
    t_temperature, temperature_outside = temperatureData()
    t_solar, pv_power_raw = solarData()
    t_heiz, heiz_warme_bedarf = HeizWarmeBedarfData()

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

    np.savetxt('z_solar.txt', pv_power, fmt='%.5f')
    np.savetxt('z_temperature.txt', temperature_outside, fmt='%.5f')

    print("Length of temperature is {}".format(len(temperature_outside)))             # Length of minutes in a year: 525600
    # print("Length of solar is {}".format(len(t_solar)))                         # Length of minutes in a year: 525600
    # print("Length of heiz is {}".format(len(t_heiz)))                           # Length of minutes in a year: 525600
    # print("Length of cop is {}".format(len(t_cop)))                             # Length of minutes in a year: 525600
    # print("Length of price is {}".format(len(t_price)))                         # Length of minutes in a week: 10080

    T_mpc = 900
    controlHorizon = 1
    mpc_iter = 0
    T_sim = 60
    N = 96*6

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

    # print("Length of slice_temp is {}".format(len(slice_temp)))                 # Length of minutes in a year: 35040. 35040/96 = 365
    # print("Length of slice_solar is {}".format(len(slice_solar)))               # Length of minutes in a year: 35040. 35040/96 = 365
    # print("Length of slice_heiz is {}".format(len(slice_heiz)))                 # Length of minutes in a year: 35040. 35040/96 = 365
    # print("Length of slice_cop is {}".format(len(slice_cop)))                   # Length of minutes in a year: 35040. 35040/96 = 365
    # print("Length of slice_price is {}".format(len(slice_price)))               # Length of minutes in a week: 576. 576/6 = 96

    # with open('solar_temp_value.txt', 'w') as f:
    #     for i in range(len(temperature_outside)):
    #         print('temperature_outside: {}'.format(temperature_outside[i]), file=f)
    #
    #     for i in range(len(pv_power)):
    #         print('pv_power: {}'.format(pv_power[i]), file=f)

    #plt.plot(t_time[:8640]/1440, pv_power[:8640], label='Solar')
    fig, (ax1, ax2, ax3) = plt.subplots(3)
    # plt.plot(t_time, temperature_outside, label='Temperature')
    # plt.legend()
    ax1.plot(t_temperature[:576], temperature_outside[:576], label='Temperature')
    ax1.legend()
    ax2.plot(t_solar[:576], pv_power[:576], label='Solar')
    ax2.legend()
    ax3.plot(t_heiz[:576], heiz_warme_bedarf[:576], label='HeizWarmeBedarf')
    ax3.legend()
    plt.show()
