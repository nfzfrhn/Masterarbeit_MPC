import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("tkagg")

# from dummy_uploadData import temperatureData, solarData
#
# t_temperature, temperature_outside = temperatureData()
# t_solar, pv_power_raw = solarData()
#
# # Solar Plant - TODO:Implement using database
# n_PV_mod = 156           # Number of PV modules
# G_PV_NOCT = 800          # in 1 W/m^2, STC reference solar irradiance
# T_PV_NOCT = 45           # in 1 °C, NOCT module temperature
# P_PV_STC = 0.32          # in 1 W, STC power per module
# gamma_PV = -0.43/100     # in 1 / °C, STC temperature coefficient of module
# G_PV_STC = 1000          # in 1 W/m^2, STC reference solar irradiance
# T_PV_STC = 25            # in 1 °C, STC reference cell temperature
#
# T_sim = 60
# T_mpc = 900
# sim_day = 7  # TODO: replace with the one from OpenFileDialog
# daySec = 24 * 3600
# sim_tim = sim_day * daySec
# N = int(24 * 3600 / T_mpc)
# controlHorizon = 1
#
# T_PV_mod = temperature_outside + (T_PV_NOCT - 20) * pv_power_raw / G_PV_NOCT    # in 1 °C, module temperature
# pv_power = n_PV_mod * P_PV_STC * (pv_power_raw / G_PV_STC) * (1 + gamma_PV * (T_PV_mod - T_PV_STC))*T_sim  # in 1 kW, PV power

total_pv = np.array([])
i = 0
j = 0
k = 0
with open('log_u_array.txt', 'r') as f:
    log_u_array = np.loadtxt(f)
    total_pv = np.append(total_pv, log_u_array[:,1]+log_u_array[:,4])
    i += 1

with open('log_xx_array.txt', 'r') as f:
    log_xx_array = np.loadtxt(f)
    j += 1

with open ('log_yy_array.txt', 'r') as f:
    log_yy_array = np.loadtxt(f)
    k += 1

with open('log_soc_lower.txt', 'r') as f:
    log_soc_lower = np.loadtxt(f)

with open('log_soc_upper.txt', 'r') as f:
    log_soc_upper = np.loadtxt(f)

# iter = 0
# startVal = int(T_mpc * controlHorizon * iter / T_sim)
# stepVal = int(T_mpc / T_sim)
# stopVal = startVal + int((N - 1) * T_mpc / T_sim) + stepVal
# timeFrame_local = slice(startVal, stopVal, stepVal)
# pv_slice_raw = pv_power_raw[timeFrame_local]
# pv_slice = pv_power[timeFrame_local]
# pv_slice_time = np.arange(len(pv_slice))
# print(pv_slice.shape)

P_wp = log_u_array[:, 0]
P_pv_used = log_u_array[:, 1]
mt_dot = log_u_array[:, 2]
Toa = log_u_array[:, 3]
P_pv_sold = log_u_array[:, 4]
QBedarf = log_u_array[:, 5]
COP = log_u_array[:, 6]
P_cost = log_u_array[:, 7]
P_bat1 = log_u_array[:, 8]
P_bat2 = log_u_array[:, 9]
P_ev1 = log_u_array[:, 10]
P_ev2 = log_u_array[:, 11]

T1 = log_xx_array[:, 0]
T2 = log_xx_array[:, 1]
T3 = log_xx_array[:, 2]
T4 = log_xx_array[:, 3]
time_it = log_xx_array[:, 4]
SOC_Bat1 = log_xx_array[:, 5]
SOC_Bat2 = log_xx_array[:, 6]
SOC_EV1 = log_xx_array[:, 7]
SOC_EV2 = log_xx_array[:, 8]

soc_upper1 = log_soc_upper[0, :]
soc_upper2 = log_soc_upper[1, :]
soc_lower1 = log_soc_lower[0, :]
soc_lower2 = log_soc_lower[1, :]

PV_sold = log_yy_array

t = np.arange(len(P_wp))
len_pwp = len(P_wp)
t_soc_upper_lower = np.arange(len(soc_lower1))
print(f"length of t: {len(t)}")
print(f"length of t_soc_upper_lower: {len(t_soc_upper_lower)}")
# fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True)
# pv_total = P_pv_used + P_pv_sold
# len_pv_total = np.arange(len(pv_total))
# ax1.plot(len_pv_total, pv_total, label="PV_total")
# ax1.set_title("PV_total from mpc reading")
# ax2.plot(pv_slice_time, pv_slice_raw, label="PV slice_raw")
# ax2.set_title("PV_raw")
# ax3.plot(pv_slice_time, pv_slice, label="PV slice modified")
# ax3.set_title("PV modified PV variables")
# ax1.legend()

fig, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(6, sharex=True)
ax1.plot(t, P_wp, label="P_wp")       # P_wp
ax1.plot(t, P_pv_used+P_pv_sold, label="PV_total")    # PV total
# ax1.plot(t, P_pv_sold, label="PV_sold")    # PV_sold
#ax1.plot(t, total_pv, label="PV_total")    # PV_total
ax1.plot(t, QBedarf, label="QBedarf")      # QBedarf
ax1.set_ylabel("Power [W]")
ax1.legend()
ax2.plot(t, P_bat1, label="P_bat")          # P_bat
ax2.plot(t, P_bat2, label="P_bat")          # P_bat
ax2.plot(t, P_ev1, label="P_ev")            # P_ev
ax2.plot(t, P_ev2, label="P_ev")            # P_ev
ax2.set_ylabel("Power [W]")
ax2.legend()
ax3.plot(t, Toa, label="Toa")        # Toa
ax3.plot(t, T1, label="T1")   # T1
ax3.plot(t, T2, label="T2")   # T2
ax3.plot(t, T3, label="T3")   # T3
ax3.plot(t, T4, label="T4")   # T4
ax3.set_ylabel("Temperature [°C]")
ax3.legend()
ax4.plot(t, COP, label="COP")   # COP
ax4.set_ylabel("COP")
ax4.legend()
ax5.plot(t, SOC_Bat1, label="SOC_Bat")   # SOC_Car
ax5.plot(t, SOC_Bat2, label="SOC_Bat")   # SOC_Car
ax5.plot(t, SOC_EV1, label="SOC_EV")   # SOC_EV
ax5.plot(t, SOC_EV2, label="SOC_EV")   # SOC_EV
ax5.plot(t, soc_lower1[:len_pwp], label="SOC_lower1")   # SOC_lower
ax5.plot(t, soc_upper1[:len_pwp], label="SOC_upper1")   # SOC_upper
ax5.plot(t, soc_lower2[:len_pwp], label="SOC_lower2")   # SOC_lower
ax5.plot(t, soc_upper2[:len_pwp], label="SOC_upper2")   # SOC_upper
ax5.set_ylabel("SOC [%]")
ax5.legend()
ax6.plot(t, P_cost, label="P_cost")  # P_cost
ax6.set_ylabel("Strompreis [Euro/kWh]")
ax6.legend()
plt.show()