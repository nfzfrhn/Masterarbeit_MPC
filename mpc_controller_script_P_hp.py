# _author_: Nafiz Farhan Bin Zainurin
"""
cs.DM is for constant variables or parameters
cs.SX is for variables that are going to be optimized
cs.MX is for variables that are going to be optimized
"""
import casadi as cs
import numpy as np
import time
import logging
import random as rd
import matplotlib
import matplotlib.pyplot as plt

from uploadData import temperatureData, solarData
# from dummy_uploadData_yearly import temperatureData, solarData

# Initialization
# TODO: add num_bat and num_ev
num_bat = 1
num_ev = 1
logging.basicConfig(filename='logfile.log', level=logging.INFO)

t_temperature, temperature_outside = temperatureData()
t_solar, pv_power_raw = solarData()
# t_solar, pv_power_raw = solarData()

# MPC configuration
T_sim = cs.DM(60)
T_mpc = cs.DM(900)
sim_day = cs.DM(7)  # TODO: replace with the one from OpenFileDialog
daySec = 24 * 3600
sim_tim = sim_day * daySec
N = int(24 * 3600 / T_mpc)
controlHorizon = 1

# Building - TODO:Implement using database
cw = cs.DM(42e5)
cz = cs.DM(6e6)
cf = cs.DM(18e5)
cpip = cs.DM(1.7e6)
kwoa = cs.DM(86)
kwz = cs.DM(86)
kfz = cs.DM(594)
kfpip = cs.DM(506)
w = cs.DM(0.124)
cwat = cs.DM(4180)
kp = cs.DM(383)
capacity = cs.DM(200e-3)
alpha = cs.DM(0.06)
kt = cs.DM(18.8)
mhp_dot = cs.DM(0.2)
kwt = cs.DM(0.99)
# m = cs.DM(4.18e1)
m = cs.DM(125)
taw = cs.DM(60)
m_dot = cs.DM(0.2)
ts = cs.DM(30)

a1 = cs.DM(6.1189)
a2 = cs.DM(0.0676)
a3 = cs.DM(-0.0632)

# Battery - TODO:Implement using database
eta_Bat = cs.DM(0.96)
n_Bat_mod = cs.DM(8)
E_Bat_nom = 4000 * n_Bat_mod
E_Bat_min = cs.DM(0)
E_Bat_max = E_Bat_nom

# Electric Car - TODO:Implement using database
eta_EV = cs.DM(0.88)
n_EV_mod = cs.DM(6)
E_EV_nom = 3800 * n_EV_mod
E_EV_min = cs.DM(0)
E_EV_max = E_EV_nom

ev_capacity = cs.DM(48000)

t_ev = np.arange(4 * 24 * sim_day + 1)
time_ev = np.random.randint(0, num_ev, [4 * 24 * sim_day])
soc_ev = np.zeros(4 * 24 * sim_day + 1)
soc_upper = np.zeros([num_ev, 4 * 24 * 7])
soc_lower = np.zeros([num_ev, 4 * 24 * 7])

for i in range(num_ev):
    flag = 0
    for j in range(4 * 24 * 7):
        tick_ev = time_ev[i, j]
        if tick_ev == 1:
            soc_ev[i, j] = round(rd.uniform(0, 1), 2)
            flag = j
        elif tick_ev == -1:
            soc_ev[i, j] = soc_ev[i, flag] + 0.7 * round(rd.uniform(0, 1), 2) + 0.3
            if soc_ev[i, j] > 1 or soc_ev[i, j] > 1 / 24 * (j - flag) + soc_ev[i, flag]:
                soc_ev[i, j] = min(1, 1 / 24 * (j - flag) + soc_ev[i, flag])
            for k in range(flag, j):
                soc_upper[i, k] = min(1, soc_ev[i, flag] + 1 / 24 * (k - flag))
                soc_lower[i, k] = max(soc_ev[i, flag], soc_ev[i, j] + 1 / 24 * (k - i))
                if soc_lower[i, k] > soc_upper[i, k]:
                    soc_lower[i, k] = soc_upper[i, k]

soc_ev = ev_capacity*soc_ev
soc_upper = ev_capacity*soc_upper
soc_lower = ev_capacity*soc_lower

# Solar Plant - TODO:Implement using database
n_PV_mod = cs.DM(156)           # Number of PV modules
G_PV_NOCT = cs.DM(800)          # in 1 W/m^2, STC reference solar irradiance
T_PV_NOCT = cs.DM(45)           # in 1 °C, NOCT module temperature
P_PV_STC = cs.DM(0.32)          # in 1 W, STC power per module
gamma_PV = cs.DM(-0.43/100)     # in 1 / °C, STC temperature coefficient of module
G_PV_STC = cs.DM(1000)          # in 1 W/m^2, STC reference solar irradiance
T_PV_STC = cs.DM(25)            # in 1 °C, STC reference cell temperature

T_PV_mod = temperature_outside + (T_PV_NOCT - 20) * pv_power_raw / G_PV_NOCT    # in 1 °C, module temperature
pv_power = n_PV_mod * P_PV_STC * (pv_power_raw / G_PV_STC) * (1 + gamma_PV * (T_PV_mod - T_PV_STC))*T_sim  # in 1 kW, PV power

# Input definition - TODO:Implement using database
p_max = cs.DM(4800)
p_min = cs.DM(4800 * 0.25)
mt_dot_max = cs.DM(0.124)
mt_dot_min = cs.DM(0.124 * 0.25)


def DM2Arr(dm):
    return np.array(dm.full())


#def shift_timestep(t, x, u, f, h):
def shift_timestep(t, x, u, h):
    # The parameter that we receive, u is not casadi type
    # u is casadi.DM type. n_controls * N
    # x is casadi.DM type. n_states * 1
    # print("Variable x is {}".format(type(x)))
    # print("Variable u is {}".format(type(u)))
    # print("Variable x is {}".format(x.shape))
    # print("Variable u is {}".format(u.shape))
    st_local = x
    x0_local = x
    u_local = u[:, 0]
    y0_local = cs.DM()
    t0_local = t + T_mpc*controlHorizon

    con_bat = cs.DM.zeros(num_bat, 1)
    con_ev = cs.DM.zeros(num_ev, 1)

    len_con = u_local.numel()
    offset_con = len_con - num_bat - num_ev
    tot_bat = cs.DM(0)
    tot_ev = cs.DM(0)
    index_con = 0
    i_bat = 0       # Starting index. Matlab was 1 but python start with zero. Let's see if there is a problem
    i_ev = 0        # Starting index. Matlab was 1 but python start with zero. Let's see if there is a problem

    for pp in range(offset_con, offset_con+num_bat):
        tot_bat = tot_bat + u_local[pp]
        con_bat[i_bat] = u_local[pp]
        index_con = pp + 1
        i_bat = i_bat + 1

    for qq in range(index_con, index_con+num_ev):
        tot_ev = tot_ev + u_local[qq]
        con_ev[i_ev] = u_local[qq]
        i_ev = i_ev + 1

    net_power = u_local[1] + u_local[2] - tot_bat - tot_ev
    # local_mt_dot = u_local[3]                                # TODO:Do I really need this?
    # local_mr_dot = w - local_mt_dot                          # TODO: Do I really need this?

    # I am not sure if this should be np.zeroes or cs.DM.zeroes
    # -> Should be np.zeros. Nope
    # -> Should be cs.DM.zeros
    # size1() = query the number of rows
    # size2() = query the number of columns
    u0_local = cs.DM.zeros(u.size1(), u.size2()+controlHorizon)    # What does this line do? u0_local=u+column(controlHorizon)
    # u0_local[:u.shape[0], :] = u                                  # What does this line do? u0_local=u+rows(controlHorizon)
    u0_local[:, :u.size2()] = u                                  # What does this line do? u0_local=u+column(controlHorizon)
    for i in range(u.size2(), u.size2()+controlHorizon):
        u0_local[:, i] = u[:, -1]                                 # u0_local = u + rows(controlHorizon). The rows for the controlHorizon repeat the previous last rows

    #for i in range(controlHorizon):
    for i in range(controlHorizon):
        # y0_local = cs.vertcat(y0_local, h(st_local, u0_local[:, i]))
        y0_local = cs.horzcat(y0_local, h(st_local, u0_local[:, i]))
        # local_con = u0[i, :]                                # Do I even need to redefine everything?
        local_con = u0_local[:, i]                                    # Do I even need to redefine everything?
        local_net_power = local_con[1] + local_con[2] - tot_bat - tot_ev    # Do I even need to redefine everything??
        local_mt_dot = local_con[3]                             # This looks like can be deleted
        local_mr_dot = w - local_mt_dot                         # This looks like can be deleted

        for j in range(int(T_mpc/T_sim)):
            # print("Variable local_con is {}".format(local_con))
            f_value = f_rhs(st_local, local_con)
            st_local = st_local + (f_value*T_sim)

        # st_np = DM2Arr(st)
        # x0 = cs.vertcat(x0, st_np)
        # x0_local = cs.vertcat(x0_local, st)
        x0_local = cs.horzcat(x0_local, st_local)

    # print("Variable x0_local after ch loop is {}".format(x0_local.shape))
    # print("Variable u0_local after ch loop is {}".format(u0_local.shape))
    # print("Variable y0_local after ch loop is {}".format(y0_local.shape))

    # xest = x0_local[controlHorizon+1:, :]               # Need to check this
    # yest = y0_local[controlHorizon + 1:, :]  # Need to check this
    # TODO: Check variation with controlHorizon
    xest = x0_local[:, controlHorizon:]                 # Need to check this
    yest = y0_local[:, controlHorizon:]                 # Need to check this
    x0_return = x0_local[:, controlHorizon:]            # Need to check this
    u0_return = u0_local[:, controlHorizon:]            # Need to check this
    # y0_return = y0_local[:controlHorizon, :]            # Need to check this
    # y0_return = y0_local[controlHorizon:, :]            # Need to check this
    y0_return = y0_local              # Need to check this

    # print("Size of x0_return is {}".format(x0_return.shape))
    # print("Size of u0_return is {}".format(u0_return.shape))
    # print("Size of y0_return is {}".format(y0_return.shape))

    return t0_local, x0_return, u0_return, y0_return, xest, yest

def get_pv(time_frame):
    # TODO: define pv_power. Finish the code
    # pv_power = np.ones(24 * 3600)
    # stepVal = int(T_mpc/T_sim)
    # endVal = int((N-1) * T_mpc / T_sim) + stepVal
    # time_frame = slice(0, endVal, stepVal)
    pv = 1 * pv_power[time_frame]
    return pv


def get_temp_of_air(time_frame):
    # TODO: define pv_power. Finish the code
    # temp_air = np.ones(24 * 3600)
    # time_frame = slice(0, int((N-1) * T_mpc / T_sim), int(T_mpc/T_sim))
    # stepVal = int(T_mpc / T_sim)
    # endVal = int((N - 1) * T_mpc / T_sim) + stepVal
    # time_frame = slice(0, endVal, stepVal)
    air = 1 * temperature_outside[time_frame]
    return air

def get_soc_low_eCar(iCar,time_frame):
    pass

def get_soc_high_eCar(iCar,time_frame):
    pass


def update_constraints(mpc_iter):
    # Did not check. Check again!
    startVal = int(T_mpc*controlHorizon*mpc_iter/T_sim)
    stepVal = int(T_mpc/T_sim)
    stopVal = startVal + int((N-1)*T_mpc/T_sim) + stepVal
    timeFrame_local = slice(startVal, stopVal, stepVal)

    try:
        args['lbx'][n_states*(N+1) + 4:n_states*(N+1) + n_controls*N:n_controls] = get_temp_of_air(timeFrame_local)-0.002   # Toa
        args['ubx'][n_states*(N+1) + 4:n_states*(N+1) + n_controls*N:n_controls] = get_temp_of_air(timeFrame_local)+0.002   # Toa
    except:
        print(f"The error was at mpciter:{mpc_iter} and length get_toa:{len(get_temp_of_air(timeFrame_local))}")
    # args['lbg'][n_states*(N+1) + n_outputs*N + 2: -1: 2] = get_pv(timeFrame_local)
    # args['ubg'][n_states*(N+1) + n_outputs*N + 2: -1: 2] = get_pv(timeFrame_local)

    try:
        args['lbg'][n_states*(N+1) + n_outputs*N + 1: n_states*(N+1) + n_outputs*N + 3*N: 3] = get_pv(timeFrame_local)-0.001
        args['ubg'][n_states*(N+1) + n_outputs*N + 1: n_states*(N+1) + n_outputs*N + 3*N: 3] = get_pv(timeFrame_local)+0.001
    except:
        print(f"The error was at mpciter:{mpc_iter} and length get_pv:{len(get_pv(timeFrame_local))}")

    # args['lbx'][n_states*(N+1)+2: n_states*(N+1) + n_controls*N: n_controls] = 0
    # args['ubx'][n_states*(N+1)+2: n_states*(N+1) + n_controls*N: n_controls] = cs.inf


# Initialize state
tw = cs.SX.sym("tw")
tz = cs.SX.sym("tz")
tf = cs.SX.sym("tf")
tpip = cs.SX.sym("tpip")
t1 = cs.SX.sym("t1")
t2 = cs.SX.sym("t2")
t3 = cs.SX.sym("t3")
t4 = cs.SX.sym("t4")
cop = cs.SX.sym("cop")
time_rec = cs.SX.sym("time_rec")
SOC_bat = cs.SX.sym("SOC_bat", num_bat)
SOC_ev = cs.SX.sym("SOC_ev", num_ev)

states = cs.vertcat(tw, tz, tf, tpip, t1, t2, t3, t4, cop, time_rec, SOC_bat, SOC_ev)
n_states = states.numel()

# Initialize input
p_hp = cs.SX.sym("p_hp")
p_bought = cs.SX.sym("p_bought")
pv_used = cs.SX.sym("pv_used")
mt_dot = cs.SX.sym("mt_dot")
toa = cs.SX.sym("toa")
pv_sold = cs.SX.sym("pv_sold")
p_bat = cs.SX.sym("p_bat", num_bat)
p_ev = cs.SX.sym("p_ev", num_ev)

ctrls = cs.vertcat(p_hp, p_bought, pv_used, mt_dot, toa, pv_sold, p_bat, p_ev)
n_controls = ctrls.numel()

# print("n_states is {}".format(n_states))
# print("n_controls is {}".format(n_controls))

# OLD: This values is important
# NEW: We dont use this values anymore
# power_total_bat = cs.DM(0)
# power_total_ev = cs.DM(0)
# php = cs.SX.sym('php')  # Power input for heat pump
#
# # TODO: Implement database functionality
# for i in range(num_bat):
#     power_total_bat = power_total_bat + p_bat[i]
#
# # TODO: Implement database functionality
# for i in range(num_ev):
#     power_total_ev = power_total_ev + p_ev[i]

# OLD: Total net power
# NEW: We dont use this values anymore
# php = p_bought + pv_used - power_total_bat - power_total_ev
php = p_hp # p_hp is the total power input to the heat pump

# Model expression
mr_dot = w - mt_dot
QHP = php * cop
tF = (QHP / (mhp_dot * cwat)) + t3
Te = (mt_dot * t1 + (1 - alpha) * mr_dot * tf) / (w - alpha * mr_dot)
Tr = alpha * Te + (1 - alpha) * tf
p_bat = p_bought + pv_used - p_hp
# T_forward = QHP / (mhp_dot * cwat) + t3

# RHS
rhs = cs.vertcat((kwoa * (toa - tw) + kwz * (tz - tw)) / cw,
       (kwz * (tw - tz) + kfz * (tf - tz)) / cz,
       (kfz * (tz - tf) + kfpip * (tpip - tf)) / cf,
       (kfpip * (tf - tpip) + w * cwat * (Te - tpip)) / cpip,
       (kt * (t2 - t1) - kwt * (t1 - toa) + mt_dot * cwat * (t2 - t1)) / (m * cwat),
       (kt * (t3 - t2) - kt * (t2 - t1) - kwt * (t2 - toa) + mt_dot * cwat * (t3 - t2)
        + mhp_dot * cwat * (tF - t2)) / (m * cwat),
       (kt * (t4 - t3) - kt * (t3 - t2) - kwt * (t3 - toa) + mt_dot * cwat * (t4 - t3)
        + mhp_dot * cwat * (t2 - t3)) / (m * cwat),
       (kt * (t3 - t4) - kwt * (t4 - toa) + mt_dot * cwat * (Tr - t4)) / (m * cwat),
       (-cop + a1 + a2 * toa + a3 * t3) / taw,
       cs.SX(1))

# RHS - Battery
for i in range(num_bat):
    # TODO: Implement database functionality
    # rhs = cs.vertcat(rhs, (eta_Bat ** cs.sign(p_bat) * p_bat / T_mpc))
    rhs = cs.vertcat(rhs, (eta_Bat ** cs.sign(p_bat) * p_bat / 3600))

# RHS - Electric Car
for j in range(num_ev):
    # TODO: Implement database functionality
    # rhs = cs.vertcat(rhs, (eta_EV ** cs.sign(p_ev) * p_ev / T_mpc))
    rhs = cs.vertcat(rhs, (eta_EV * p_ev / 3600))

# RHS Output
rhsOut = cs.vertcat(tz, t1, Te, pv_sold)
n_outputs = rhsOut.numel()

# Mapping function
f_rhs = cs.Function('f_rhs', [states, ctrls], [rhs])
U = cs.SX.sym('U', n_controls, N)
P = cs.SX.sym('P', n_states + n_outputs)
X = cs.SX.sym('X', n_states, N+1)
Y = cs.SX.sym('Y', n_outputs, N)
h = cs.Function('h', [states, ctrls], [rhsOut])

# Cost function
# obj = 0
obj = cs.SX(0)
# g = []
# l1 = []
# l2 = []
# l3 = []
l1 = cs.SX.sym('l1', 0)
l2 = cs.SX.sym('l2', 0)
l3 = cs.SX.sym('l3', 0)
J_bat = cs.DM(0)
J_ev = cs.DM(0)
Q_bat = cs.DM(0.16)     # TODO: Should be configurable from GUI
Q_ev = cs.DM(0.1)      # TODO: Should be configurable from GUI
# st = X[:, 0]
g = X[:, 0] - P[:n_states]
# g.append(X[:, 0] - P[:n_states])

for k in range(N):
    st = X[:, k]
    con = U[:, k]
    y_current = Y[:, k]

    con_bat = cs.SX.zeros(num_bat, 1)
    con_ev = cs.SX.zeros(num_ev, 1)
    len_con = con.numel()
    offset_con = len_con - num_bat - num_ev
    tot_bat = cs.DM(0)
    tot_ev = cs.DM(0)
    index_con = offset_con
    i_bat = 0           # Starting index. Matlab was 1 but python start with zero. Let's see if there is a problem
    i_ev = 0            # Starting index. Matlab was 1 but python start with zero. Let's see if there is a problem

    for pp in range(offset_con, offset_con + num_bat):
        tot_bat = tot_bat + con[pp]
        con_bat[i_bat] = con[pp]
        index_con = pp + 1
        i_bat = i_bat + 1

    for qq in range(index_con, index_con + num_ev):
        tot_ev = tot_ev + con[qq]
        con_ev[i_ev] = con[qq]
        index_con = qq + 1
        i_ev = i_ev + 1

    J_bat = tot_bat
    J_ev = tot_ev

    if k != N:
        # obj = obj + 0.35 * con[0] ** 2 + 0.12 * y_current[3] ** 2 + Q_bat * J_bat ** 2 + Q_ev * J_ev ** 2
        #con_next = U[:, k + 1]
        #y_next = Y[:, k + 1]
        # obj = obj + 0.28*(con[0]-con[1]+J_bat+J_ev)** 2 + 0.22 * y_current[3] ** 2 + Q_bat * J_bat ** 2 + 5*(st[1]-cs.DM(22))**2 # + 10*((con_next[0]>600) - (con[0]>600))**2
        obj = obj + 0.28*con[1]**2 + 0.22*y_current[3]**2 + Q_bat*J_bat**2 + 0.5*(st[1] - cs.DM(22))**2
    if k == N:
        # obj = obj + 0.28*(con[0] - con[1] + J_bat + J_ev)** 2 + 0.22 * y_current[3] ** 2 + Q_bat * J_bat ** 2 + 5*(st[1]-cs.DM(22))**2 # + 10*((con_next[0]>600) - (con[0]>600))**2
        obj = obj + 0.28*con[1]**2 + 0.22*y_current[3]**2 + Q_bat*J_bat**2 + 0.5*(st[1] - cs.DM(22))**2

    st_next = X[:, k + 1]

    T_minute = int(T_mpc / T_sim)
    for i in range(T_minute):
        st = st + T_sim * f_rhs(st, con)

    l1 = cs.vertcat(l1, y_current - h(st, con))                                     # Output Constraint
    l2 = cs.vertcat(l2,
                    con[1] + con[2] + J_bat - J_ev - con[0],                        # Power balance Constraint
                    con[2] + con[5],                                                # PV power balance constraint
                    con[2] - J_bat)                                                 # Use PV first before using battery?
    st_next_RK4 = st
    g = cs.vertcat(g, st_next - st_next_RK4)

# print("Length of g before extend is {}".format(g.numel()))
# print("Length of l1 before extend is {}".format(l1.numel()))
# print("Length of l2 is {}".format(l2.numel()))

g = cs.vertcat(g, l1, l2)

# print("Length of g after extend is {}".format(g.numel()))
# Optimizer
OPT_Variables = cs.vertcat(
    X.reshape((-1, 1)),  # n_states*(N+1)
    U.reshape((-1, 1)),  # n_controls*N
    Y.reshape((-1, 1))  # n_output*N
)

# print("Number of OPT_Variables is {}".format(OPT_Variables.numel()))

nlp_prob = {
    'f': obj,
    'x': OPT_Variables,
    # 'g': cs.vertcat(*g),
    'g': g,
    'p': P
}

opts = {
    'ipopt': {
        'max_iter': 3000,
        'print_level': 1,
        'acceptable_tol': 1e-3,
        'acceptable_obj_change_tol': 1e-3
    },
    'print_time': 0
}

solver = cs.nlpsol('solver', 'ipopt', nlp_prob, opts)

# Where does this conclusion come from?
# g = {
#   g = N+1     -> 1 defined outside the loop and inside the loop N times
#   l1 = N      -> N times inside the loop
#   l2 = N*5    -> Inside the loop, in one iteration, we put 5 equality constraints equation
# }

# Length of g = (N+1) + N + N*5
# N = 96 -> g = 385.(This is not true)
# ---------------------------------------------------------------------------------------------------------
# g = {
#   g = n_states*(N+1)     -> 1 defined outside the loop and inside the loop N times
#   l1 = n_outputs*N      -> N times inside the loop
#   l2 = N*5    -> Inside the loop, in one iteration, we put 2 equality constraints equation
# }

# Length of g = n_states*(N+1) + n_outputs*N + N*2
# N = 96
# n_states = 12
# n_outputs = 4
# -> g = 1740

# Equality Constraints
# Constraint function
lbg = cs.DM.zeros((n_states*(N+1) + n_outputs*N + 3*N), 1)
ubg = cs.DM.zeros((n_states*(N+1) + n_outputs*N + 3*N), 1)

# lbg[start:stop:step]
# ubg[start:stop:step]

# Net power - This implementation is correct. This includes offset(offset is 0), length
lbg[n_states*(N+1) + n_outputs*N + 0: n_states*(N+1) + n_outputs*N + 3*N:3] = 0                  # Correct value
ubg[n_states*(N+1) + n_outputs*N + 0: n_states*(N+1) + n_outputs*N + 3*N:3] = cs.inf               # Correct value
# lbg[n_states*(N+1) + n_outputs*N + 0: n_states*(N+1) + n_outputs*N + 5*N:5] = -cs.inf              # Correct value
# ubg[n_states*(N+1) + n_outputs*N + 0: n_states*(N+1) + n_outputs*N + 5*N:5] = cs.inf               # Correct value
# lbg[n_states*(N+1) + n_outputs*N + 0: -1: 2] = 2222                    # Test: Want to see part that is not filled
# ubg[n_states*(N+1) + n_outputs*N + 0: -1: 2] = 2222                    # Test: Want to see part that is not filled

# print("length of ubg is {}".format(ubg.numel()))

# Sunlight - This implementation is correct. This includes offset(offset is 1), length
startPV = 0
stepPV = int(T_mpc/T_sim)
stopPV = int((N-1) * T_mpc / T_sim) + stepPV
timeFrame_PV = slice(startPV, stopPV, stepPV)
lbg[n_states*(N+1) + n_outputs*N + 1: n_states*(N+1) + n_outputs*N + 3*N: 3] = get_pv(timeFrame_PV) + 0.0001   # Correct value
ubg[n_states*(N+1) + n_outputs*N + 1: n_states*(N+1) + n_outputs*N + 3*N: 3] = get_pv(timeFrame_PV) + 0.0002   # Correct value
# lbg[n_states*(N+1) + n_outputs*N + 1:n_states*(N+1) + n_outputs*N + 2*N:2] = 1111    # Dummy value for testing
# ubg[n_states*(N+1) + n_outputs*N + 1:n_states*(N+1) + n_outputs*N + 2*N:2] = 1111    # Dummy value for testing
# AAA = get_pv(timeFrame_PV)
# BBB = ubg[n_states*(N+1) + n_outputs*N + 1:-1:2]
# CCC = ubg[n_states*(N+1) + n_outputs*N + 1:n_states*(N+1) + n_outputs*N + 2*N:2]
# DDD = ubg[n_states*(N+1) + n_outputs*N + 2:n_states*(N+1) + n_outputs*N + 2*N:2]
# print("Length of rhs get_pv is {}".format(len(AAA)))
# print("Length of BBB lhs get_pv is {}".format(BBB.numel()))
# print("Length of CCC lhs get_pv is {}".format(CCC.numel()))
# print("Length of DDD lhs get_pv is {}".format(DDD.numel()))

# Power from grid
lbg[n_states*(N+1) + n_outputs*N + 2: n_states*(N+1) + n_outputs*N + 3*N:3] = 0                  # p_bought*(p_bought>600)
ubg[n_states*(N+1) + n_outputs*N + 2: n_states*(N+1) + n_outputs*N + 3*N:3] = cs.inf                  # p_bought*(p_bought>600)

# # Energy balance
# lbg[n_states*(N+1) + n_outputs*N + 3: n_states*(N+1) + n_outputs*N + 5*N:5] = 0                  # Equality constraint for power from grid
# # ubg[n_states*(N+1) + n_outputs*N + 3: n_states*(N+1) + n_outputs*N + 5*N:5] = cs.inf             # Equality constraint for power from grid
# ubg[n_states*(N+1) + n_outputs*N + 3: n_states*(N+1) + n_outputs*N + 5*N:5] = 0             # Equality constraint for power from grid
#
# # Prioritize energy from PV
# lbg[n_states*(N+1) + n_outputs*N + 4: n_states*(N+1) + n_outputs*N + 5*N:5] = 0                  # Equality constraint between PV and battery
# ubg[n_states*(N+1) + n_outputs*N + 4: n_states*(N+1) + n_outputs*N + 5*N:5] = cs.inf             # Equality constraint between PV and battery

# print("length of ubg is {}".format(ubg.numel()))

with open('log_lbg_ubg.txt', 'w') as f:
    for i in range(ubg.numel()):
        print('ubg{}:{} lbg{}:{}'.format(i, ubg[i], i, lbg[i]), file=f)

lbx = cs.DM.zeros((n_states * (N + 1) + n_controls * N + n_outputs * N, 1))
ubx = cs.DM.zeros((n_states * (N + 1) + n_controls * N + n_outputs * N, 1))

# State constraint
# Tw
lbx[0:n_states * (N + 1):n_states] = -cs.inf
ubx[0:n_states * (N + 1):n_states] = cs.inf

# Tz
lbx[1:n_states * (N + 1):n_states] = 20
ubx[1:n_states * (N + 1):n_states] = 25

# Tf
lbx[2:n_states * (N + 1):n_states] = 20
ubx[2:n_states * (N + 1):n_states] = 70

# Tpip
lbx[3:n_states * (N + 1):n_states] = 20
ubx[3:n_states * (N + 1):n_states] = 70

# T1
lbx[4:n_states * (N + 1):n_states] = 21
ubx[4:n_states * (N + 1):n_states] = 71

# T2
lbx[5:n_states * (N + 1):n_states] = 22
ubx[5:n_states * (N + 1):n_states] = 72

# T3
lbx[6:n_states * (N + 1):n_states] = 23
ubx[6:n_states * (N + 1):n_states] = 73

# T4
lbx[7:n_states * (N + 1):n_states] = 24
ubx[7:n_states * (N + 1):n_states] = 74

# COP
lbx[8:n_states * (N + 1):n_states] = 0
ubx[8:n_states * (N + 1):n_states] = cs.inf

# Time
lbx[9:n_states * (N + 1):n_states] = 0
ubx[9:n_states * (N + 1):n_states] = cs.inf

# Was tested and it works!!!
index_tracking_st = 0
# index_offset_bat = n_states - num_bat - num_ev + 1
index_offset_bat_st = n_states - num_bat - num_ev
index_offset_ev = index_offset_bat_st
# index_battery_st = 11
for i in range(index_offset_bat_st, index_offset_bat_st + num_bat):
    if num_bat >= 1:
        # TODO: Implement database functionality
        # lbx[i:n_states * (N + 1):n_states, 1] = 6400
        # ubx[i:n_states * (N + 1):n_states, 1] = 32000

        lbx[i:n_states * (N+1): n_states] = 0
        ubx[i:n_states * (N+1): n_states] = 11000
        index_offset_ev = i + 1

for j in range(index_offset_ev, index_offset_ev + num_ev):
    if num_ev >= 1:
        # TODO: Implement database functionality
        # lbx[j:n_states * (N + 1):n_states, 1] = 6400
        # lbx[j:n_states * (N + 1):n_states, 1] = 32000
        startToa = 0
        stepToa = int(T_mpc / T_sim)
        stopToa = int((N - 1) * T_mpc / T_sim) + stepToa
        timeFrame_Toa = slice(startToa, stopToa, stepToa)
        lbx[j:n_states * (N+1): n_states] = soc_lower[j,timeFrame_Toa]
        ubx[j:n_states * (N+1): n_states] = soc_upper[j,timeFrame_Toa]
        index_tracking_st = j

# Control/Input constraints - Default all value to inf/-inf
lbx[n_states*(N+1) + 1: n_states*(N+1) + n_controls*N] = -cs.inf
ubx[n_states*(N+1) + 1: n_states*(N+1) + n_controls*N] = cs.inf

# p_hp
lbx[n_states*(N+1) + 0: n_states*(N+1) + n_controls*N: n_controls] = 0
ubx[n_states*(N+1) + 0: n_states*(N+1) + n_controls*N: n_controls] = cs.inf

# p_bought
lbx[n_states*(N+1) + 1: n_states*(N+1) + n_controls*N: n_controls] = 0
ubx[n_states*(N+1) + 1: n_states*(N+1) + n_controls*N: n_controls] = cs.inf

# pv_used
lbx[n_states*(N+1) + 2: n_states*(N+1) + n_controls*N: n_controls] = 0
ubx[n_states*(N+1) + 2: n_states*(N+1) + n_controls*N: n_controls] = cs.inf

# mt_dot
lbx[n_states*(N+1) + 3: n_states*(N+1) + n_controls*N: n_controls] = 0.0124
ubx[n_states*(N+1) + 3: n_states*(N+1) + n_controls*N: n_controls] = 0.124
# print("length of ubx is {}".format(ubx.numel()))

# Toa
startToa = 0
stepToa = int(T_mpc/T_sim)
stopToa = int((N-1) * T_mpc / T_sim) + stepToa
timeFrame_Toa = slice(startToa, stopToa, stepToa)
lbx[n_states*(N+1) + 4: n_states*(N+1) + n_controls*N: n_controls] = get_temp_of_air(timeFrame_Toa) + 0.0001
ubx[n_states*(N+1) + 4: n_states*(N+1) + n_controls*N: n_controls] = get_temp_of_air(timeFrame_Toa) + 0.0002

# pv_sold
lbx[n_states*(N+1) + 5: n_states*(N+1) + n_controls*N: n_controls] = 0
ubx[n_states*(N+1) + 5: n_states*(N+1) + n_controls*N: n_controls] = cs.inf

# Input battery
index_tracking_con = 0
index_offset_battery_con = n_controls - num_bat - num_ev
index_offset_ev_con = index_offset_battery_con
kk = 1
for k in range(index_offset_battery_con, index_offset_battery_con + num_bat):
    if num_bat >= kk:
        lbx[n_states * (N + 1) + k: n_states * (N + 1) + n_controls * N: n_controls] = -8000
        ubx[n_states * (N + 1) + k: n_states * (N + 1) + n_controls * N: n_controls] = 8000
        index_offset_ev_con = k + 1

ll = 1
for l in range(index_offset_ev_con, index_offset_ev_con + num_ev):
    if num_ev >= ll:
        lbx[n_states * (N + 1) + l: n_states * (N + 1) + n_controls * N: n_controls] = 0
        ubx[n_states * (N + 1) + l: n_states * (N + 1) + n_controls * N: n_controls] = 8000
        index_tracking_con = l
        ll = l + 1

# Output constraint
# lbx[n_states*(N+1) + n_controls*N + 0: n_states*(N+1) + n_controls*N + n_outputs*N: 1] = -cs.inf
# ubx[n_states*(N+1) + n_controls*N + 0: n_states*(N+1) + n_controls*N + n_outputs*N: 1] = cs.inf

# Tz
lbx[n_states*(N+1) + n_controls*N + 0: n_states*(N+1) + n_controls*N + n_outputs*N: n_outputs] = 20
ubx[n_states*(N+1) + n_controls*N + 0: n_states*(N+1) + n_controls*N + n_outputs*N: n_outputs] = 23

# T1
lbx[n_states*(N+1) + n_controls*N + 1: n_states*(N+1) + n_controls*N + n_outputs*N: n_outputs] = 20
ubx[n_states*(N+1) + n_controls*N + 1: n_states*(N+1) + n_controls*N + n_outputs*N: n_outputs] = 70

# Te
lbx[n_states*(N+1) + n_controls*N + 2: n_states*(N+1) + n_controls*N + n_outputs*N: n_outputs] = 0
ubx[n_states*(N+1) + n_controls*N + 2: n_states*(N+1) + n_controls*N + n_outputs*N: n_outputs] = 100

# PV_sold
lbx[n_states*(N+1) + n_controls*N + 3: n_states*(N+1) + n_controls*N + n_outputs*N: n_outputs] = 0
ubx[n_states*(N+1) + n_controls*N + 3: n_states*(N+1) + n_controls*N + n_outputs*N: n_outputs] = cs.inf

with open('log_lbx_ubx.txt', 'w') as f:
    for i in range(ubx.numel()):
        print('ubx{}:{} lbx{}:{}'.format(i, ubx[i], i, lbx[i]), file=f)

args = {
    'lbg': lbg,
    'ubg': ubg,
    'lbx': lbx,
    'ubx': ubx
}

# Compute
state_init = [12, 20, 15, 25, 35, 35, 35, 35, 1, 0]
# state_init = [2, 10, 12, 5, 5, 5, 5, 5, 1, 0]

# TODO: Add battery initial value from database
for i in range(num_bat):
    state_init.extend([100])

for i in range(num_ev):
    state_init.extend([2000])

x0 = cs.DM(state_init)  # Initial state value that will be passed to MPC

# TODO: Retrieve set value from database
state_target = [21, 21, 26, 50]
xs = cs.DM(state_target)

xx = np.array(state_init).reshape(1, -1)        # contains the history of states. And we want to make it row vector
t0 = 0
t = cs.DM(t0)
yy = np.array(state_target).reshape(1,-1)       # contains the history of output. And we want to make it row vector

# TODO: Can np.zeros and casadi variables working together?
# u0 = np.zeros((self.N, self.n_controls))                      # Should this be U0
# Y0 = np.zeros(int(self.N), self.n_outputs)
u0 = cs.DM.zeros(int(N), n_controls)
# X0 = cs.repmat(x0, 1, N).T  # This cs.repmat().T exist. I checked
X0 = cs.repmat(x0, 1, N+1)  # This cs.repmat().T exist. I checked
Y0 = cs.DM.zeros(int(N), n_outputs)

# Start MPC
mpciter = 0
xx1 = []
# u_cl = []  # We already have "cat_control", so no need u_cl
y0 = []

# cat_states = DM2Arr(X0.full)
# cat_controls = DM2Arr(u0[:, 0].full)
# cat_states = X0.full
# cat_controls = u0[:, 0].full
cat_states = DM2Arr(X0)
cat_controls = DM2Arr(u0[0, :]).reshape(1, -1)
# cat_outputs = DM2Arr(Y0[0,:]).reshape(1, -1)
times = np.array([0])

# time_program = []  # Is this used?
# start_time = []  # Is this used?
# tic = time.time()  # Is this used?

# TODO: What to do with this?
xest = []  # In mehrez python, there is no implementation
yest = []  # In mehrez python, there is no implementation

t_start_sim = time.time()
# while mpciter < sim_tim / T_mpc:
while mpciter < 570:                 # Max is 576
    t1 = time.time()
    # u0 = u0[:, :n_controls]  # Do we need this
    args['p'] = cs.vertcat(
        x0,  # Current state
        xs  # Target state
    )

    # Optimization variable current state
    args['x0'] = cs.vertcat(
        cs.reshape(X0, n_states * (N + 1), 1),  # Do we need to transpose this?
        cs.reshape(u0, n_controls * N, 1),  # Do we need to transpose this?
        cs.reshape(Y0, n_outputs * N, 1)  # Do we need to transpose this?
    )

    sol = solver(
        x0=args['x0'],
        lbx=args['lbx'],
        ubx=args['ubx'],
        lbg=args['lbg'],
        ubg=args['ubg'],
        p=args['p']
    )

    len_sol_x = sol['x'].numel()
    # print("Length of sol[x] is {}".format(len_sol_x))
    # Extract the answer from the sol
    X0 = cs.reshape(sol['x'][:n_states*(N+1)], n_states, N + 1)
    u = cs.reshape(sol['x'][n_states*(N+1) + 0: n_states*(N+1) + n_controls*N], n_controls, N)
    Y0 = cs.reshape(sol['x'][n_states*(N+1) + n_controls*N + 0:n_states*(N+1) + n_controls*N + n_outputs * N], n_outputs, N)

    cat_states = np.dstack((
        cat_states,
        DM2Arr(X0)
    ))

    # print("xx size before shift is {}".format(xx.shape))
    # print("x0 size before shift is {}".format(x0.shape))
    # print("u0 size before shift is {}".format(u0.shape))

    cat_controls = np.vstack((
        cat_controls,
        DM2Arr(u[:, 0].T)
    ))

    t = np.vstack((t, t0))

    t0, x0, u0, y0, xest, yest = shift_timestep(t0, x0, u, h)

    # print("xx size is {}".format(xx.shape))
    # print("x0 size after shift is {}".format(x0.shape))

    xx = np.vstack((
        xx,
        DM2Arr(x0.T)
    ))

    yy = np.vstack((
        yy,
        DM2Arr(y0.T)
        # y0.toarray()
    ))

    X0 = cs.horzcat(
        X0[:, 1:],                        # Throw away the 1st column
        cs.reshape(X0[:, -1], -1, 1)
    )

    # print("X0 size is {}".format(X0.shape))

    if mpciter > 2:
        for index_eCar in range(num_ev):
            delta_soc = time_ev[index_eCar, mpciter*controlHorizon] - time_ev[index_eCar, mpciter*controlHorizon - 1]
            if delta_soc == 1:
                pass


    t2 = time.time()
    duration = t2-t1
    times = np.vstack((times, duration))
    logging.debug('MPC iteration: {} and duration: {}'.format(mpciter, duration))

    update_constraints(mpciter)
    mpciter = mpciter + 1
    print("mpciter:{}".format(mpciter))

t_end_sim = time.time()
print("Simulation time is {}".format(t_end_sim - t_start_sim))
# print("Size of xx is {}".format(xx.shape))
# print("Size of cat_controls is {}".format(cat_controls.shape))
# print("Size of t is {}".format(t.shape))
# print("Size of times is {}".format(times.shape))

np.savetxt('log_xx_array.txt', xx, fmt='%.5f')
np.savetxt('log_yy_array.txt', yy, fmt='%.5f')
np.savetxt('log_u_array.txt', cat_controls, fmt='%.5f')
np.savetxt('log_lbg_array.txt', lbg, fmt='%.5f')
np.savetxt('log_ubg_array.txt', ubg, fmt='%.5f')
np.savetxt('log_lbx_array.txt', lbx, fmt='%.5f')
np.savetxt('log_ubx_array.txt', ubx, fmt='%.5f')

fig, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(6, sharex=True)
ax1.plot(t, cat_controls[:, 0], label="p_hp")       # P_hp
ax1.plot(t, cat_controls[:, 1], label="p_bought")   # P_bought
ax1.plot(t, cat_controls[:, 2], label="PV_used")    # PV_used
ax1.plot(t, cat_controls[:, 5], label="PV_sold")    # PV_sold
ax1.set_ylabel("Power [W]")
ax1.legend()
ax2.plot(t, cat_controls[:, 4], label="Toa")        # Toa
ax2.plot(t, xx[:, 0], label="Tw")   # Tw
ax2.plot(t, xx[:, 1], label="Tz")   # Tz
ax2.set_ylabel("Temperature [°C]")
ax2.legend()
ax4.plot(t, xx[:, 2], label="Tf")   # Tf
ax4.plot(t, xx[:, 3], label="Tpip") # Tpip
ax3.plot(t, xx[:, 4], label="T1")   # T1
ax3.plot(t, xx[:, 5], label="T2")   # T2
ax3.plot(t, xx[:, 6], label="T3")   # T3
ax3.plot(t, xx[:, 7], label="T4")   # T4
ax3.set_ylabel("Temperature [°C]")
ax4.plot(t, yy[:, 2], label="Te")   # Te
ax3.legend()
ax4.plot(t, xx[:, 8], label="COP")   # COP
ax4.legend()
ax5.plot(t, xx[:, 10], label="SOC_Bat")   # SOC_Car
ax5.plot(t, xx[:, 11], label="SOC_EV")  # SOC_EV
ax5.set_ylabel("SOC [%]")
ax5.legend()
ax6.plot(t, cat_controls[:, 6], label="P_Battery")  # Battery
ax6.plot(t, cat_controls[:, 7], label="P_EV")       # EV
ax6.set_ylabel("Power [W]")
ax6.legend()
plt.show()

# with open('log_xx.txt', 'w') as f:
#     for i in range(xx.shape[0]):
#         print('mpciter: {} xx is: {}'.format(i, xx[i, :]), file=f)



# Why after mpciter:68, the xx is nan?


