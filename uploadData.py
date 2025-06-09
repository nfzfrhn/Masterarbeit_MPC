from scipy import interpolate
import numpy as np
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import logging

# logging.basicConfig(filename='logging_temperature2.log', level=logging.INFO)

def timeConvert(x):
    times = x.split(":")
    return 3600 * int(times[0]) + 60 * int(times[1]) + int(times[2])


def temperatureData():
    minuten = 60
    daySec = 3600*24
    # a = np.arange(0,daySec+minuten, minuten)
    a = np.arange(0, daySec, minuten)
    #print(a)

    # df1 = pd.read_csv('data/Temperature_2020/20200103_temperature.CSV', sep=';', decimal=',')
    # df2 = pd.read_csv('data/Temperature_2020/20200104_temperature.CSV', sep=';', decimal=',')
    # df3 = pd.read_csv('data/Temperature_2020/20200105_temperature.CSV', sep=';', decimal=',')
    # df1 = pd.read_csv('data/Temperature_2020/20220101_temperature.CSV', sep=';', decimal=',')   # This works fine but we use the file outside
    # df2 = pd.read_csv('data/Temperature_2020/20220102_temperature.CSV', sep=';', decimal=',')   # This works fine but we use the file outside
    # df3 = pd.read_csv('data/Temperature_2020/20220103_temperature.CSV', sep=';', decimal=',')   # This works fine but we use the file outside
    df1 = pd.read_csv('data/20220101_temperature.CSV', sep=';', decimal=',')
    df2 = pd.read_csv('data/20220102_temperature.CSV', sep=';', decimal=',')
    df3 = pd.read_csv('data/20220103_temperature.CSV', sep=';', decimal=',')
    df4 = pd.read_csv('data/20220104_temperature.CSV', sep=';', decimal=',')
    df5 = pd.read_csv('data/20220105_temperature.CSV', sep=';', decimal=',')
    df6 = pd.read_csv('data/20220106_temperature.CSV', sep=';', decimal=',')
    df7 = pd.read_csv('data/20220107_temperature.CSV', sep=';', decimal=',')
    t1 = df1["time"].apply(timeConvert).to_numpy()
    t2 = df2["time"].apply(timeConvert).to_numpy()
    t3 = df3["time"].apply(timeConvert).to_numpy()
    t4 = df4["time"].apply(timeConvert).to_numpy()
    t5 = df5["time"].apply(timeConvert).to_numpy()
    t6 = df6["time"].apply(timeConvert).to_numpy()
    t7 = df7["time"].apply(timeConvert).to_numpy()
    T1 = df1["aussen"].to_numpy()
    T2 = df2["aussen"].to_numpy()
    T3 = df3["aussen"].to_numpy()
    T4 = df4["aussen"].to_numpy()
    T5 = df5["aussen"].to_numpy()
    T6 = df6["aussen"].to_numpy()
    T7 = df7["aussen"].to_numpy()

    # print(type(df1))

    ff1 = interpolate.interp1d(t1,T1,fill_value="extrapolate")
    ff2 = interpolate.interp1d(t2,T2,fill_value="extrapolate")
    ff3 = interpolate.interp1d(t3,T3,fill_value="extrapolate")
    ff4 = interpolate.interp1d(t4,T4,fill_value="extrapolate")
    ff5 = interpolate.interp1d(t5,T5,fill_value="extrapolate")
    ff6 = interpolate.interp1d(t6,T6,fill_value="extrapolate")
    ff7 = interpolate.interp1d(t7,T7,fill_value="extrapolate")

    days = 7
    daysSec = days*daySec
    t_total = np.arange(0,daysSec, minuten)

    yy1=ff1(a)
    yy2=ff2(a)
    yy3=ff3(a)
    yy4=ff4(a)
    yy5=ff5(a)
    yy6=ff6(a)
    yy7=ff7(a)

    # with open('t_temp_value.txt', 'w') as f:
    #     for i in range(len(t1)):
    #         print('index:{}, time: {} and Temperature: {}'.format(i, t1[i], T1[i]), file=f)
    #
    # with open('t_temp_value_extrapolate.txt', 'w') as f:
    #     for i in range(len(a)):
    #         print('index:{}, time: {} and Temperature: {}'.format(i, a[i], yy1[i]), file=f)

    # yy_total = np.concatenate((yy1,yy2[1:],yy3[1:]))
    yy_total = np.concatenate((yy1, yy2, yy3, yy4, yy5, yy6, yy7))
    #plt.plot(t_total, yy_total)
    #plt.show()

    #logging.info('t_total:{} yy_total:{}'.format(t_total, yy_total))

    return t_total, yy_total


def solarData():
    minuten = 60
    daySec = 3600*24
    # a = np.arange(0, daySec + minuten, minuten)
    a = np.arange(0,daySec, minuten)
    # print(a)

    # df1 = pd.read_csv('data/Solar_2020/20200103_sn.CSV', sep=';', decimal=',')
    # df2 = pd.read_csv('data/Solar_2020/20200104_sn.CSV', sep=';', decimal=',')
    # df3 = pd.read_csv('data/Solar_2020/20200105_sn.CSV', sep=';', decimal=',')
    # df1 = pd.read_csv('data/Solar_2020/20200101_sn.CSV', sep=';', decimal=',')  # This has extreme negative 1st point
    # df2 = pd.read_csv('data/Solar_2020/20200102_sn.CSV', sep=';', decimal=',')  # This has extreme negative 1st point
    # df3 = pd.read_csv('data/Solar_2020/20200103_sn.CSV', sep=';', decimal=',')  # This has extreme negative 1st point
    df1 = pd.read_csv('data/20200101_sn.CSV', sep=';', decimal=',')
    df2 = pd.read_csv('data/20200102_sn.CSV', sep=';', decimal=',')
    df3 = pd.read_csv('data/20200103_sn.CSV', sep=';', decimal=',')
    df4 = pd.read_csv('data/20200104_sn.CSV', sep=';', decimal=',')
    df5 = pd.read_csv('data/20200105_sn.CSV', sep=';', decimal=',')
    df6 = pd.read_csv('data/20200106_sn.CSV', sep=';', decimal=',')
    df7 = pd.read_csv('data/20200107_sn.CSV', sep=';', decimal=',')
    t1 = df1["time"].apply(timeConvert).to_numpy()
    t2 = df2["time"].apply(timeConvert).to_numpy()
    t3 = df3["time"].apply(timeConvert).to_numpy()
    t4 = df4["time"].apply(timeConvert).to_numpy()
    t5 = df5["time"].apply(timeConvert).to_numpy()
    t6 = df6["time"].apply(timeConvert).to_numpy()
    t7 = df7["time"].apply(timeConvert).to_numpy()
    T1 = df1["pac"].to_numpy()
    T2 = df2["pac"].to_numpy()
    T3 = df3["pac"].to_numpy()
    T4 = df4["pac"].to_numpy()
    T5 = df5["pac"].to_numpy()
    T6 = df6["pac"].to_numpy()
    T7 = df7["pac"].to_numpy()

    # print(type(df1))

    ff1 = interpolate.interp1d(t1,T1,fill_value="extrapolate")
    ff2 = interpolate.interp1d(t2,T2,fill_value="extrapolate")
    ff3 = interpolate.interp1d(t3,T3,fill_value="extrapolate")
    ff4 = interpolate.interp1d(t4,T4,fill_value="extrapolate")
    ff5 = interpolate.interp1d(t5,T5,fill_value="extrapolate")
    ff6 = interpolate.interp1d(t6,T6,fill_value="extrapolate")
    ff7 = interpolate.interp1d(t7,T7,fill_value="extrapolate")

    days = 7
    daysSec = days*daySec
    t_total = np.arange(0,daysSec, minuten)

    yy1=ff1(a)
    yy2=ff2(a)
    yy3=ff3(a)
    yy4=ff4(a)
    yy5=ff5(a)
    yy6=ff6(a)
    yy7=ff7(a)

    yy_total = np.concatenate((yy1,yy2,yy3,yy4,yy5,yy6,yy7))
    #plt.plot(t_total, yy_total)
    # plt.show()

    # logging.info('t_total:{} yy_total:{}'.format(t_total, yy_total))

    return t_total, yy_total


if __name__ == "__main__":
    t_temperature, temperature_outside = temperatureData()
    t_solar, pv_power = solarData()

    print(len(temperature_outside))
    print(len(pv_power))

    T_mpc = 900
    controlHorizon = 1
    mpc_iter = 0
    T_sim = 60
    N = 96

    startVal = int(T_mpc * controlHorizon * mpc_iter / T_sim)
    stepVal = int(T_mpc / T_sim)
    stopVal = startVal + int((N - 1) * T_mpc / T_sim) + stepVal
    timeFrame_local = slice(startVal, stopVal, stepVal)

    slice_temperature = temperature_outside[timeFrame_local]
    slice_pv_power = pv_power[timeFrame_local]

    ti = np.arange(len(slice_temperature))
    tj = np.arange(len(slice_pv_power))

    np.savetxt('z_temperature_slice.txt', slice_temperature, fmt='%0.5f')
    np.savetxt('z_solar_slice.txt', slice_pv_power, fmt='%0.5f')

    # with open('solar_temp_value.txt', 'w') as f:
    #     for i in range(len(temperature_outside)):
    #         print('temperature_outside: {}'.format(temperature_outside[i]), file=f)
    #
    #     for i in range(len(pv_power)):
    #         print('pv_power: {}'.format(pv_power[i]), file=f)

    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4)
    ax1.plot(t_temperature, temperature_outside)
    ax2.plot(ti, slice_temperature)
    ax3.plot(t_solar, pv_power)
    ax4.plot(tj, slice_pv_power)
    plt.show()
