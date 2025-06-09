# from casadi import *
# This version will be replace with the one without a class called mpc_controller_script.py
import casadi as cs
import numpy as np
import time

class MPC_Model:

    def __init__(self, num_bat, num_ev):

        self.num_bat = num_bat
        self.num_ev = num_ev

        # MPC settings
        self.T_sim = 60
        self.T_mpc = 900
        self.sim_day = 3
        self.sim_tim = self.sim_day*86400
        self.N = 24*3600 / self.T_mpc
        self.controlHorizon = 1

        # States
        self.tw = None
        self.tz = None
        self.tf = None
        self.tpip = None
        self.t1 = None
        self.t2 = None
        self.t3 = None
        self.t4 = None
        self.cop = None
        self.time = None
        self.SOC_bat = None
        self.SOC_ev = None
        self.states = None
        self.n_states = None

        # Inputs
        self.p_bought = None
        self.pv_used = None
        self.mt_dot = None
        self.toa = None
        self.pv_sold = None
        self.p_bat = None
        self.p_ev = None
        self.ctrls = None
        self.n_controls = None
        self.power_total_bat = 0
        self.power_total_ev = 0
        self.php = 0

        # Expressions
        self.mr_dot = None
        self.QHP = None
        self.tF = None
        self.Te = None
        self.Tr = None
        self.T_forward = None

        # Outputs
        self.rhs = None
        self.rhsOut = None
        self.n_outputs = None

        # Mapping Function
        self.f = None
        self.U = None
        self.P = None
        self.X = None
        self.Y = None
        self.h = None

        # Cost Function
        self.obj = 0
        self.g = []
        self.l1 = []
        self.l2 = []
        self.l3 = []
        self.J_bat = 0
        self.J_ev = 0
        self.Q_bat = 0.5
        self.Q_ev = 0.5

        # Constraint Function
        self.lbg = None
        self.ubg = None
        self.lbx = None
        self.ubx = None

        # Building
        self.cw = 42e5
        self.cz = 6e6
        self.cf = 18e5
        self.cpip = 1.7e6
        self.kwoa = 86
        self.kwz = 86
        self.kfz = 594
        self.kfpip = 506
        self.w = 0.124
        self.cwat = 4180
        self.kp = 383
        self.capacity = 200e-3
        self.alpha = 0.06
        self.kt = 18.8
        self.mhp_dot = 0.2
        self.kwt = 0.99
        self.m = 4.18e1
        self.taw = 60
        self.m_dot = 0.2
        self.ts = 30

        self.a1 = 6.1189
        self.a2 = 0.0676
        self.a3 = -0.0632

        # Battery - TODO:Implement using database
        self.eta_Bat = 0.96
        self.n_Bat_mod = 8
        self.E_Bat_nom = 4000 * self.n_Bat_mod
        self.E_Bat_min = 0
        self.E_Bat_max = self.E_Bat_nom

        # Electric Car - TODO:Implement using database
        self.eta_EV = 0.88
        self.n_EV_mod = 6
        self.E_EV_nom = 3800 * self.n_Bat_mod
        self.E_EV_min = 0
        self.E_EV_max = self.E_Bat_nom

        # Input definition - TODO:Implement using database
        self.p_max = 4800
        self.p_min = 4800*0.25
        self.mt_dot_max = 0.124
        self.mt_dot_min = 0.124*0.25

    def initState(self):
        self.tw = cs.SX.sym("tw")
        self.tz = cs.SX.sym("tz")
        self.tf = cs.SX.sym("tf")
        self.tpip = cs.SX.sym("tpip")
        self.t1 = cs.SX.sym("t1")
        self.t2 = cs.SX.sym("t1")
        self.t3 = cs.SX.sym("t1")
        self.t4 = cs.SX.sym("t1")
        self.cop = cs.SX.sym("cop")
        self.time = cs.SX.sym("time")
        self.SOC_bat = cs.SX.sym("SOC_bat", self.num_bat)
        self.SOC_ev = cs.SX.sym("SOC_ev", self.num_ev)

        self.states = [self.tw, self.tz, self.tf, self.tpip, self.t1, self.t2, self.t3, self.t4, self.cop, self.time,
                       self.SOC_bat, self.SOC_ev]
        self.n_states = len(self.states)

    def initInput(self):
        self.p_bought = cs.SX.sym("p_bought")
        self.pv_used = cs.SX.sym("pv_used")
        self.mt_dot = cs.SX.sym("mt_dot")
        self.toa = cs.SX.sym("toa")
        self.pv_sold = cs.SX.sym("pv_sold")
        self.p_bat = cs.SX.sym("p_bat", self.num_bat)
        self.p_ev = cs.SX.sym("p_ev", self.num_ev)

        self.ctrls = [self.p_bought, self.pv_used, self.mt_dot, self.toa, self.pv_sold, self.p_bat, self.p_ev]
        self.n_controls = len(self.ctrls)

        # TODO: Implement database functionality
        for i in range(self.num_bat):
            self.power_total_bat = self.power_total_bat + self.p_bat[i]

        # TODO: Implement database functionality
        for i in range(self.num_ev):
            self.power_total_ev = self.power_total_ev + self.p_ev[i]

        # Total net power
        self.php = self.p_bought + self.pv_used - self.power_total_bat - self.power_total_ev

    def modelExpression(self):
        self.mr_dot = self.w - self.mt_dot
        self.QHP = self.php * self.cop
        self.tF = self.QHP / (self.mhp_dot * self.cwat) + self.t3
        self.Te = (self.mt_dot * self.t1 + (1 - self.alpha) * self.mr_dot * self.tf) / (
                    self.w - self.alpha * self.mr_dot)
        self.Tr = self.alpha * self.Te + (1 - self.alpha) * self.tf
        self.T_forward = self.QHP / (self.mhp_dot * self.cwat) + self.t3

    def rhsEq(self):
        self.rhs = [(self.kwoa * (self.toa - self.tw) + self.kwz * (self.tz - self.tw)) / self.cw,
                  (self.kwz * (self.tw - self.tz) + self.kfz * (self.tf - self.tz)) / self.cz,
                  (self.kfz * (self.tz - self.tf) + self.kfpip * (self.tpip - self.tf)) / self.cf,
                  (self.kfpip * (self.tf - self.tpip) + self.w * self.cwat * (self.Te - self.tpip)) / self.cpip,
                  (self.kt * (self.t2 - self.t1) - self.kwt * (self.t1 - self.toa) + self.mt_dot * self.cwat * (self.t2 - self.t1)) / (self.m * self.cwat),
                  (self.kt * (self.t3 - self.t2) - self.kt * (self.t2 - self.t1) - self.kwt * (self.t2 - self.toa) + self.mt_dot * self.cwat * (self.t3 - self.t2)
                        + self.mhp_dot * self.cwat * (self.tF - self.t2)) / (self.m * self.cwat),
                  (self.kt * (self.t4 - self.t3) - self.kt * (self.t3 - self.t2) - self.kwt * (self.t3 - self.toa) + self.mt_dot * self.cwat * (self.t4 - self.t3)
                        + self.mhp_dot * self.cwat * (self.t2 - self.t3)) / (self.m * self.cwat),
                  (self.kt * (self.t3 - self.t4) - self.kwt * (self.t4 - self.toa) + self.mt_dot * self.cwat * (self.Tr - self.t4)) / (self.m * self.cwat),
                  (self.cop + self.a1 + self.a2 * self.toa + self.a3 * self.t3) / self.taw,
                  1]
        # Battery
        for i in range(self.num_bat):
            # TODO: Implement database functionality
            self.rhs.extend([self.eta_Bat**np.sign(self.p_bat)*self.p_bat/self.T_mpc])

        # Electric Car
        for j in range(self.num_ev):
            # TODO: Implement database functionality
            self.rhs.extend([self.eta_EV**np.sign(self.p_ev) * self.p_ev / self.T_mpc])
        return self.rhs

    def rhsOutput(self):
        self.rhsOut = [self.tz, self.t1, self.Te, self.pv_sold]
        self.n_outputs = len(self.rhsOut)

    def mappingFunction(self):
        self.f = cs.Function('f', [self.states, self.ctrls], [self.rhs])
        self.U = cs.SX.sym('U', self.n_controls, self.N)
        self.P = cs.SX.sym('P', self.n_states + self.n_outputs)
        self.X = cs.SX.sym('X', self.n_states, self.N)
        self.Y = cs.SX.sym('Y', self.n_outputs, self.N)
        self.h = cs.Function('h', [self.states, self.ctrls], [self.rhsOut])

    def costFunction(self):
        self.st = self.X[:, 1]
        self.g.extend([self.st-self.P[:self.n_states]])

        for k in range(self.N):
            self.st = self.X[:, k]
            self.con = self.U[:, k]
            self.y_current = self.Y[:, k]

            con_bat = cs.SX.zeros(self.num_bat, 1)
            con_ev = cs.SX.zeros(self.num_ev, 1)
            len_con = len(self.con)
            offset_con = len_con - self.num_bat - self.num_ev
            tot_bat = 0
            tot_ev = 0
            index_con = offset_con
            i_bat = 1
            i_ev = 1

            for pp in range(offset_con+1, offset_con+self.num_bat):
                tot_bat = tot_bat + self.con[pp]
                con_bat[i_bat] = self.con[pp]
                index_con = pp
                i_bat = i_bat + 1

            for qq in range(index_con+1, index_con+self.num_ev):
                tot_ev = tot_ev + self.con[qq]
                con_ev[i_ev] = self.con[qq]
                index_con = qq
                i_ev = i_ev + 1

            self.J_bat = tot_bat
            self.J_ev = tot_ev

            if k != self.N:
                self.obj = self.obj + 0.35 * self.con[1] ** 2 + 0.12 * self.y_current[4] ** 2 + self.Q_bat * self.J_bat ** 2 + self.Q_ev * self.J_ev ** 2
            if k == self.N:
                self.obj = self.obj + 0.35 * self.con[1] ** 2 + 0.12 * self.y_current[4] ** 2 + self.Q_bat * self.J_bat ** 2 + self.Q_ev * self.J_ev ** 2

            st_next = self.X[:, k+1]

            T_minute = int(self.T_mpc/self.T_sim)
            for i in range(T_minute):
                self.st = self.st + self.T_sim * self.f(self.st, self.con)

            self.l1.extend([self.y_current - self.h(self.st, self.con)])                                                        # Output Constraint
            self.l2.extend([self.con[1] + self.con[2] - self.J_bat - self.J_ev, self.con[2] + self.y_current[4]])               # Input Constraint
            st_next_RK4 = self.st
            self.g.extend([st_next - st_next_RK4])
            self.g.extend([self.l1, self.l2])

    def optimizer(self):
        # TODO: Should I include a function inside a function like this?
        self.mappingFunction()
        self. OPT_Variables = cs.vertcat(
            self.X.reshape((-1, 1)),             # n_states*(N+1)
            self.U.reshape((-1, 1)),             # n_controls*N
            self.Y.reshape((-1, 1))              # n_output*N
        )

        self.nlp_prob = {
            'f': self.obj,
            'x': self.OPT_Variables,
            'g': self.g,
            'p': self.P
        }

        self.opts = {
            'ipopt': {
                'max_iter':3000,
                'print_level':1,
                'acceptable_tol': 1e-3,
                'acceptable_obj_change_tol':1e-3
            },
            'print_time':0
        }

        self.solver = cs.nlpsol('solver', 'ipopt', self.nlp_prob, self.opts)

    def constraintFunction(self):
        # TODO: Check all the offsets
        n_states = self.n_states
        n_controls = self.n_controls
        n_outputs = self.n_outputs
        N = self.N

        self.lbg = cs.DM.zeros((n_states * (N + 1) + n_outputs * N + 2 * N, 1))
        self.ubg = cs.DM.zeros((n_states * (N + 1) + n_outputs * N + 2 * N, 1))

        # Net power?
        self.lbg[n_states * (N + 1) + n_outputs * N + 1:2:-1] = 0
        self.ubg[n_states * (N + 1) + n_outputs * N + 1:2:-1] = 4800

        # Sunlight
        self.lbg[n_states * (N + 1) + n_outputs * N + 2:2:-1] = self.get_pv()
        self.ubg[n_states * (N + 1) + n_outputs * N + 2:2:-1] = self.get_pv()

        self.lbx = cs.DM.zeros((n_states * (N + 1) + n_controls * N + n_outputs * N, 1))
        self.ubx = cs.DM.zeros((n_states * (N + 1) + n_controls * N + n_outputs * N, 1))

        # State constraint
        self.lbx[0:n_states:n_states * (N + 1), 1] = -cs.inf
        self.ubx[0:n_states:n_states * (N + 1), 1] = cs.inf

        # Tz
        self.lbx[1:n_states:n_states * (N + 1), 1] = 20
        self.ubx[1:n_states:n_states * (N + 1), 1] = 23

        # T1
        self.lbx[4:n_states:n_states * (N + 1), 1] = 20
        self.lbx[4:n_states:n_states * (N + 1), 1] = 70

        # T2
        self.lbx[5:n_states:n_states * (N + 1), 1] = 20
        self.lbx[5:n_states:n_states * (N + 1), 1] = 70

        # T3
        self.lbx[6:n_states:n_states * (N + 1), 1] = 20
        self.lbx[6:n_states:n_states * (N + 1), 1] = 70

        # T4
        self.lbx[7:n_states:n_states * (N + 1), 1] = 20
        self.lbx[7:n_states:n_states * (N + 1), 1] = 70

        index_tracking_st = 0
        index_battery_st = 11
        for i in range(index_battery_st, index_battery_st + self.num_bat):
            if self.num_bat >= 1:
                # TODO: Implement database functionality
                self.lbx[i:n_states:n_states * (N + 1), 1] = 6400
                self.lbx[i:n_states:n_states * (N + 1), 1] = 32000
                index_tracking_st = i

        for j in range(index_tracking_st+1, index_tracking_st+self.num_ev):
            if self.num_ev >= 1:
                # TODO: Implement database functionality
                self.lbx[j:n_states:n_states * (N + 1), 1] = 6400
                self.lbx[j:n_states:n_states * (N + 1), 1] = 32000
                index_tracking_st = j

        # Control/Input constraints
        self.lbx[n_states*(N+1)+1: n_states*(N+1) + n_controls*N, 1] = -cs.inf
        self.ubx[n_states*(N+1)+1: n_states*(N+1) + n_controls*N, 1] = cs.inf

        # p_bought
        self.lbx[n_states*(N+1)+1: n_controls: n_states*(N+1) + n_controls*N, 1] = 0
        self.ubx[n_states*(N+1)+1: n_controls: n_states*(N+1) + n_controls*N, 1] = cs.inf

        # p_bought
        self.lbx[n_states*(N+1)+2: n_controls: n_states*(N+1) + n_controls*N, 1] = 0
        self.ubx[n_states*(N+1)+2: n_controls: n_states*(N+1) + n_controls*N, 1] = cs.inf

        # mt_dot
        self.lbx[n_states * (N + 1) + 3: n_controls: n_states * (N + 1) + n_controls * N, 1] = 0.0124
        self.ubx[n_states * (N + 1) + 3: n_controls: n_states * (N + 1) + n_controls * N, 1] = 0.124

        # toa
        self.lbx[n_states * (N + 1) + 4: n_controls: n_states * (N + 1) + n_controls * N, 1] = self.get_temp_of_air()
        self.ubx[n_states * (N + 1) + 4: n_controls: n_states * (N + 1) + n_controls * N, 1] = self.get_temp_of_air()

        # Input battery
        index_tracking_con = 0
        index_battery_con = 6
        kk = 1
        for k in range(index_battery_con, index_battery_con+self.num_bat):
            if self.num_bat >= kk:
                self.lbx[n_states * (N + 1) + k: n_controls: n_states * (N + 1) + n_controls * N, 1] = -8000
                self.ubx[n_states * (N + 1) + k: n_controls: n_states * (N + 1) + n_controls * N, 1] = 8000
                index_tracking_con = k
                kk = kk+1

        ll = 1
        for l in range(index_tracking_con, index_tracking_con + self.num_ev):
            if self.num_bat >= ll:
                self.lbx[n_states * (N + 1) + l: n_controls: n_states * (N + 1) + n_controls * N, 1] = -8000
                self.ubx[n_states * (N + 1) + l: n_controls: n_states * (N + 1) + n_controls * N, 1] = 8000
                index_tracking_con = l
                ll = l + 1

        # Output constraint
        self.lbx[n_states*(N+1) + n_controls*N + 0: 1: n_states*(N+1) + n_controls*N + n_outputs*N] = -cs.inf
        self.ubx[n_states * (N + 1) + n_controls * N + 0: 1: n_states * (N + 1) + n_controls * N + n_outputs * N] = cs.inf

        self.lbx[n_states * (N + 1) + n_controls * N + 1: n_outputs: n_states * (N + 1) + n_controls * N + n_outputs * N] = 20
        self.ubx[n_states * (N + 1) + n_controls * N + 1: n_outputs: n_states * (N + 1) + n_controls * N + n_outputs * N] = 70

        self.lbx[n_states * (N + 1) + n_controls * N + 3: n_outputs: n_states * (N + 1) + n_controls * N + n_outputs * N] = 0
        self.ubx[n_states * (N + 1) + n_controls * N + 3: n_outputs: n_states * (N + 1) + n_controls * N + n_outputs * N] = cs.inf

        # TODO: I am not sure if this belongs here
        self.args = {
            'lbg': self.lbg,
            'ubg': self.ubg,
            'lbx': self.lbx,
            'ubx': self.ubx
        }

    def compute(self):
        # TODO: The variables in which an empty list is created and later appended, need/should be converted into an array/numpy array for faster execution?
        t0 = 0
        x0_st = [12, 21, 25, 25, 25, 25, 25, 25, 1, 0]

        # TODO: Add battery initial value from database
        for i in range(self.num_bat):
            x0_st.extend([100])

        for i in range(self.num_ev):
            x0_st.extend([200])

        x0 = cs.DM(x0_st)
        # TODO: Retrieve set value from database
        xs = cs.DM([21, 21, 40, 50])

        xx = x0         # contains the history of states
        t = 0
        yy = []         # contains the history of output. TODO: What should the datatypes be? list or casadi type variable

        # TODO: Can np.zeros and casadi variables working together?
        # u0 = np.zeros((self.N, self.n_controls))            # Should this be U0
        # Y0 = np.zeros(int(self.N), self.n_outputs)
        u0 = cs.DM.zeros(int(self.N), self.n_controls)
        X0 = cs.repmat(x0, 1, self.N).T  # This cs.repmat().T exist. I checked
        Y0 = cs.DM.zeros(int(self.N), self.n_outputs)

        # Start MPC
        mpciter = 0
        xx1 = []
        u_cl = []                       # We already have "cat_control", so no need u_cl
        y0 = []

        #cat_states = np.array(X0.full)
        #cat_controls = np.array(u0[:,0].full)

        cat_states = self.DM2Arr(X0.full)
        cat_controls = self.DM2Arr(u0[:,0].full)

        time_program = []
        start_time = []
        tic = time.time()

        xest = []
        yest = []

        while mpciter < self.sim_tim/self.T_mpc:
            u0 = u0[:, :self.n_controls]
            self.args['p'] = cs.vertcat(
                x0,                                         # current state
                xs                                          # target state
            )
            # args.x0  = [reshape(X0',n_states*(N+1),1);reshape(u0',n_controls*N,1);reshape(Y0',n_outputs*N,1)]
            self.args['x0'] = cs.vertcat(
                cs.reshape(X0.T, self.n_states*(self.N+1), 1),
                cs.reshape(u0.T, self.n_controls*self.N, 1),
                cs.reshape(Y0.T, self.n_outputs*self.N, 1)
            )

            sol = self.solver(
                x0=self.args['x0'],
                lbx=self.args['lbx'],
                ubx=self.args['ubx'],
                lbg=self.args['lbg'],
                ubg=self.args['ubg'],
                p=self.args['p']
            )

            # In the original matlab code, they transpose this line 2 times. Why?
            u = cs.reshape(sol['x'][self.n_states*(self.N+1)+1:self.n_controls*self.N],self.n_controls, self.N)
            X0 = cs.reshape(sol['x'][:self.n_states*(self.N+1)],self.n_states, self.N + 1)

            cat_states = np.dstack((
                cat_states,
                self.DM2Arr(X0)
            ))

            cat_controls = np.vstack((
                cat_controls,
                self.DM2Arr(u[:,0])
            ))

            t = np.vstack((t,t0))

            t0, x0, u0, y0, xest, yest = self.shift_timestep(self.T_sim, self.T_mpc, t0, x0, u, f)

            # We throw away the 1st column(which is the old state) and have the same column for -1 and -2
            X0 = cs.horzcat(
                X0[:, 1:],
                cs.reshape(X0[:, -1], -1,1)
            )

    def shift_timestep(self):
        pass

    def DM2Arr(self,dm):
        return np.array(dm.full)

    def get_pv(self):
        # TODO: define pv_power. Finish the code
        pv_power = np.ones(24*3600)
        time_frame = np.arange(0, (self.N * self.T_mpc), self.T_mpc)
        pv = 1*pv_power[time_frame/self.T_sim + 1]
        return pv

    def get_temp_of_air(self):
        # TODO: define pv_power. Finish the code
        temp_air = np.ones(24 * 3600)
        time_frame = np.arange(0, (self.N * self.T_mpc), self.T_mpc)
        air = 1 * temp_air[time_frame / self.T_sim + 1]
        return air