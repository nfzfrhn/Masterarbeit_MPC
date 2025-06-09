import numpy as np
import pandas as pd
from scipy import interpolate


def timeConvert(x):
    times = x.split(":")
    return 3600 * int(times[0]) + 60 * int(times[1]) + int(times[2])


def loadingData(days):
    minuten = 60
    daySec = 3600 * 24
    sec = np.arange(0, daySec + minuten, minuten)

    daysSec = days * daySec
    t_total = np.arange(0, daysSec + minuten, minuten)

    df1 = pd.read_csv("data/20220101_temperature.csv", sep=";")
    df2 = pd.read_csv("data/20220101_temperature.csv", sep=";")
    df3 = pd.read_csv("data/20220101_temperature.csv", sep=";")
    t1 = df1["time"].apply(timeConvert).to_numpy()
    t2 = df2["time"].apply(timeConvert).to_numpy()
    t3 = df3["time"].apply(timeConvert).to_numpy()
    T1 = df1["aussen"].to_numpy()
    T2 = df2["aussen"].to_numpy()
    T3 = df3["aussen"].to_numpy()

    ff1 = interpolate.interp1d(t1, T1, fill_value="extrapolate")
    ff2 = interpolate.interp1d(t2, T2, fill_value="extrapolate")
    ff3 = interpolate.interp1d(t3, T3, fill_value="extrapolate")

    yy1 = ff1(a)
    yy2 = ff2(a)
    yy3 = ff3(a)

    temperature_total = np.concatenate((yy1, yy2[1:], yy3[1:]))
    # plt.plot(t_total,Temperature_total)
    # plt.show()

    sol1 = pd.read_csv('data/20200101_sn.csv', sep=';')
    sol2 = pd.read_csv('data/20200102_sn.csv', sep=';')
    sol3 = pd.read_csv('data/20200103_sn.csv', sep=';')
    t1_sol = sol1["time"].apply(timeConvert).to_numpy()
    t2_sol = sol2["time"].apply(timeConvert).to_numpy()
    t3_sol = sol3["time"].apply(timeConvert).to_numpy()
    Sol1 = sol1["pac"].to_numpy()
    Sol2 = sol2["pac"].to_numpy()
    Sol3 = sol3["pac"].to_numpy()

    gg1 = interpolate.interp1d(t1_sol, Sol1, fill_value="extrapolate")
    gg2 = interpolate.interp1d(t2_sol, Sol2, fill_value="extrapolate")
    gg3 = interpolate.interp1d(t3_sol, Sol3, fill_value="extrapolate")

    qq1 = gg1(a)
    qq2 = gg2(a)
    qq3 = gg3(a)

    solar_total = np.concatenate((qq1, qq2[1:], qq3[1:]))
    # plt.plot(t_total,Solar_total)
    # plt.show()

    return temperature_total, solar_total
