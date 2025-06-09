import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("tkagg")

print(plt.style.available)

plt.style.use('seaborn-poster')

with open('log_u_array.txt', 'r') as f:
    log_u_array = np.loadtxt(f)

with open ('log_xx_array.txt', 'r') as f:
    log_xx_array = np.loadtxt(f)

with open ('log_yy_array.txt', 'r') as f:
    log_yy_array = np.loadtxt(f)

P_wp = log_u_array[:, 0]
P_pv_used = log_u_array[:, 1]
mt_dot = log_u_array[:, 2]
Toa = log_u_array[:, 3]
P_pv_sold = log_u_array[:, 4]
QBedarf = log_u_array[:, 5]
COP = log_u_array[:, 6]
P_cost = log_u_array[:, 7]
P_bat = log_u_array[:, 8]
P_ev = log_u_array[:, 9]

P_ev1 = log_u_array[:, 10]
P_ev2 = log_u_array[:, 11]

T1 = log_xx_array[:, 0]
T2 = log_xx_array[:, 1]
T3 = log_xx_array[:, 2]
T4 = log_xx_array[:, 3]
time_it = log_xx_array[:, 4]
SOC_Bat = log_xx_array[:, 5]
SOC_EV = log_xx_array[:, 6]

PV_sold_y = log_yy_array

t = np.arange(len(P_wp))
print(f"length of t: {len(t)}")

# fig, (ax1, ax2, ax3) = plt.subplots(3)
# ax1.plot(t/3600, P_pv_used+P_pv_sold, label="PV_total")    # PV total
# ax1.plot(t/3600, mt_dot, label="P_pv_used")    # PV total
# ax1.plot(t/3600, P_pv_sold, label="P_pv_sold")    # PV total
# ax1.plot(t/3600, PV_sold_y, label="PV_sold_y")    # PV_sold_y
# ax2.plot(t/3600, SOC_Bat, label="SOC_Bat")        # Toa
# ax3.plot(t/3600, P_bat, label="P_bat")    # QBedarf
# ax1.legend()
# ax2.legend()
# ax3.legend()

# plt.plot(t/96, (P_pv_used+P_pv_sold)/1000, label="Solar Power")
plt.plot(t/96, P_cost, label="Heat Demand")
plt.ylabel("Electricty Price [Cents/kWh]")
plt.xlabel("Days [d]")
# Make the xticks (0, 12, 24, 36, 48, 60)
#plt.xticks(np.arange(0, 120, 12))
plt.grid()
plt.title("Energy Price over Time")
plt.tight_layout()
plt.show()