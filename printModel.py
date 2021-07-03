from operator import truediv
import sys, traceback
from math import sqrt, pi, floor, ceil, exp
import numpy as np

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from exceptions import *

class PrintModelSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(str)
    result = pyqtSignal(object)

class PrintModel(QRunnable):

    def __init__(self, materialParameters, printerParameters, optimizationParameters):
        super(PrintModel, self).__init__()

        #The model is called as a 'worker' in a thread seperate from the main GUI!
        self.signals = PrintModelSignals()

        #-----------------------------------------
        # MODEL PARAMETERS DEFINITION
        #-----------------------------------------

        #The inputs will be in a dictionary form, start by extracting the relevant information
        #based on key values. For the material properties:
        matKeys = materialParameters.keys()
        if 'Newton' in matKeys:
            self.K = self.num(materialParameters['eta'])
            self.n = 1
            self.tau_y = 0
        elif 'Power Law' in matKeys:
            self.K = self.num(materialParameters['K'])
            self.n = self.num(materialParameters['FlowIndex'])
            self.tau_y = 0
        elif 'HB' in matKeys:
            self.K = self.num(materialParameters['K'])
            self.n = self.num(materialParameters['FlowIndex'])
            self.tau_y = self.num(materialParameters['tau_y'])
        
        self.rho = self.num(materialParameters['rho'])
        self.E = self.num(materialParameters['E'])
        self.eta0 = self.num(materialParameters['eta_0'])

        #and for the printer properties:
        self.Pmax = self.num(printerParameters['P_max'])
        self.V = self.num(printerParameters['V'])*(1e-3)
        self.D = self.num(printerParameters['D'])*(1e-3)
        self.scaffH = self.num(printerParameters['Scaffold Height'])*(1e-3)
        self.scaffW = self.num(printerParameters['Scaffold Width'])*(1e-3)
        self.scaffT = self.num(printerParameters['Scaffold Thickness'])*(1e-3)

        #Moreover, set the output parameters all to None:
        self.LH = None
        self.EM = None
        self.LW = None
        self.Infill = None

        #Check if some optimization parameters are set:
        optKeys = optimizationParameters.keys()
        if 'LH' in optKeys:
            self.LH = self.num(optimizationParameters['LH'])*self.D
        if 'EM' in optKeys:
            self.EM = self.num(optimizationParameters['EM'])
        if 'LW' in optKeys:
            self.LW = self.num(optimizationParameters['LW'])*self.D
        if 'Infill' in optKeys:
            self.Infill = self.num(optimizationParameters['Infill'])

        #Then, we need to define a standard 5 ml syringe model:
        self.syringeLenghts = [12e-3, 13e-3]
        self.syringeDiameters = [30e-3, self.D]
        #Define an external needle diameter:
        self.Dext = self.D*1.7
        #Define a range for Wc:
        self.LWmin = self.D
        self.LWmax = self.Dext
        #Define a range for LH:
        self.LHmin = self.D*0.2
        self.LHmax = 0.8*self.D

        #-----------------------------------------
        # ALGORITHM PARAMETERS DEFINITION
        #-----------------------------------------

        #Define a tolerance for the bisection algorithm:
        self.tol = 1e-09
        #and a maximum number of iterations for it:
        self.N = 1000
        #and an effort for the interval optimization:
        self.effort = 0.001
        #Define a Safety Factor:
        self.SF = 1.3
        #Define a limit Reynolds number:
        self.ReLimit = 2100
        #Define a limit threshold value for the wall shear:
        self.tau_threshold = 80
        #Define the maximum deformation threshold for the post print:
        self.del_max = 0.1

    def run(self):
        try:
            #First check: material if extrudable or not based on the minimum pressure requirement:
            delP_min = (4*self.syringeLenghts[-1]*self.tau_y/self.D)*self.SF
            #and do a pressure check:
            if delP_min >= self.Pmax:
                raise PminCheckFailed

            #Second check: material if extrudable at the given flow rate/speed. Note that the speed
            #is that inside the nozzle @ EM = 1:
            delP_target = self.pressure_gradient(self.V)
            #and do a pressure check. Find a maximum EM based on the first region model:
            EM_target = 1
            step = 0.01
            cnt = 0
            while delP_target >= self.Pmax:
                EM_target -= step
                cnt += 1
                delP_target = self.pressure_gradient(self.V*EM_target)
                if EM_target < 0.4 or cnt > self.N:
                    raise HighPressureException
            
            #Pack the results from the first region:
            results = {
                'delP_min': delP_min,
                'delP_target': delP_target
            }

            #TODO: cell optimization

            #Then, output the printability window, as well as the maximum EM:
            EM_min_v, LH = self.printability_window(self.LWmin)
            EM_max_v, _ = self.printability_window(self.LWmax)
            EM_max = np.max(EM_max_v)
            EM_min = np.min(EM_min_v)
            #append to dictionary:
            results.update({'LH': LH/self.D, 'EM_min_v': EM_min_v, 'EM_max_v': EM_max_v})
            #Now verify the pressures:
            delP_max = self.pressure_gradient(EM_max*self.V)
            cnt = 0
            while delP_max >= self.Pmax:
                EM_max -= step
                cnt += 1
                delP_max = self.pressure_gradient(EM_max*self.V)
                if EM_max <= np.min(EM_min_v) or cnt >= self.N:
                    pass
            
            #Now combine the two EM together:
            if EM_target != 1:
                if EM_target <= EM_max:
                    EM_max = EM_target
            #Find the maximum printing forces:
            Ft, Fn = self.printing_forces(self.LHmax, EM_max)
            #and append to the dictionary:
            results.update({'EM_': EM_max, 'F': [Ft*(1e3), Fn*(1e3)]})

            #Check the optimization inputs:
            if self.LH is not None and (self.LH > self.LHmax or self.LH < self.LHmin):
                raise LHoutOfRangeException
            if self.LH is not None and self.EM is None and self.LW is None:
                #First case, constrain LH and output a range for EM:
                EM_opt_min = self.EM_from_LH(self.LH, self.LWmin)
                EM_opt_max = self.EM_from_LH(self.LH, self.LWmax)
                results.update({'EM_opt': [EM_opt_min, EM_opt_max], 'LH_p': self.LH/self.D, 'case_flag': 1})
                #Third region results:
                D_infill_min = self.line_deformation(self.LH, self.LWmin)
                D_infill_max = self.line_deformation(self.LH, self.LWmax)
                results.update({'D_infill': min(D_infill_max, D_infill_min)})
                LH = self.LH
            elif self.EM is not None and self.LH is None and self.LW is None:
                #Second case, constrain EM and ouput a range for LH:
                if self.EM > EM_max:
                    raise EMoutOfRangeException('Try lowering it.')
                elif self.EM < EM_min:
                    raise EMoutOfRangeException('Try increasing it.')
                elif self.EM < EM_max and self.EM > np.min(EM_max_v):
                    if self.EM > np.max(EM_min_v):
                        LH_opt_min = self.LH_from_EM(self.EM, self.LWmax)
                        LH_opt_max = self.LHmax
                    elif self.EM < np.max(EM_min_v):
                        LH_opt_min = self.LH_from_EM(self.EM, self.LWmax)
                        LH_opt_max = self.LH_from_EM(self.EM, self.LWmin)
                elif self.EM < np.min(EM_max_v):
                    if self.EM < np.max(EM_min_v):
                        LH_opt_min = self.LHmin
                        LH_opt_max = self.LH_from_EM(self.EM, self.LWmin)
                results.update({'LH_opt': [LH_opt_min/self.D, LH_opt_max/self.D], \
                                'EM_p': self.EM, 'case_flag': 2})
                #Third region results:
                D_infill_min = self.line_deformation(LH_opt_max, self.corrected_line_width(self.EM, LH_opt_max))
                D_infill_max = self.line_deformation(LH_opt_min, self.corrected_line_width(self.EM, LH_opt_min))
                results.update({'D_infill': min(D_infill_max, D_infill_min)})
                LH = (LH_opt_min+LH_opt_max)/2
            elif self.LW is not None and self.LH is None and self.EM is None:
                #Third case, constrain LW and output a line in the PW:
                EM_line, _ = self.printability_window(self.LW)
                results.update({'EM_line': EM_line, 'case_flag': 3})
                #Third region results:
                D_infill_min = self.line_deformation(self.LHmax, self.corrected_line_width(np.max(EM_line), self.LHmax))
                D_infill_max = self.line_deformation(self.LHmin, self.corrected_line_width(np.min(EM_line), self.LHmin))
                results.update({'D_infill': min(D_infill_max, D_infill_min)})
                LH = self.LH_from_EM(EM_line[floor((len(EM_line)-1)/2)], self.LW)
            elif self.EM is not None and self.LH is not None and self.LW is None:
                #Fourth case, constrain EM and LH and output the LW:
                LW_opt = self.corrected_line_width(self.EM, self.LH)
                results.update({'LW_opt': LW_opt*(1e+3), 'LH_p': self.LH/self.D, 'EM_p': self.EM, 'case_flag': 4})
                #Third region results:
                D_infill = self.line_deformation(self.LH, LW_opt)
                results.update({'D_infill': D_infill})
                LH = self.LH
            elif self.LW is not None and self.LH is not None and self.EM is None:
                #Fifth case, constrain LW and LH and output an EM:
                EM_opt = self.EM_from_LH(self.LH, self.LW)
                results.update({'EM_opt': EM_opt, 'LH_p': self.LH/self.D, 'case_flag': 5})
                #Third region results:
                D_infill = self.line_deformation(self.LH, self.LW)
                results.update({'D_infill': D_infill})
                LH = self.LH
            elif self.LW is not None and self.EM is not None and self.LH is None:
                #Sixth case, constrain LW and EM and ouput a LH:
                EM_p_max = self.EM_from_LH(self.LHmax, self.LW)
                EM_p_min = self.EM_from_LH(self.LHmin, self.LW)
                #Check the extremes to find the intersection:
                if self.EM > EM_p_max:
                    raise EMoutOfRangeException('Try lowering it.')
                elif self.EM < EM_p_min:
                    raise EMoutOfRangeException('Try increasing it.')
                LH_opt = self.LH_from_EM(self.EM, self.LW)
                EM_line, _ = self.printability_window(self.LW)
                results.update({'LH_opt': LH_opt/self.D, 'EM_p': self.EM, 'EM_line': EM_line, 'case_flag': 6})
                #Third region results:
                D_infill = self.line_deformation(LH_opt, self.LW)
                results.update({'D_infill': D_infill})
                LH = LH_opt
            elif self.LW is not None and self.EM is not None and self.LH is not None:
                #Seventh case, everything is constrained and check line error:
                W_opt = self.slicer_line_width(self.LH)
                LW_opt = W_opt+(self.EM-1)*(pi*(self.D**2))/(4*self.LH)
                EM_line, _ = self.printability_window(self.LW)
                results.update({'LW_opt': LW_opt*(1e3), 'LW_error': (LW_opt-self.LW)/self.LW, 'LH_p': self.LH/self.D, \
                    'EM_line': EM_line, 'EM_p': self.EM, 'case_flag': 7})
                LH = self.LH
            else:
                #Eight case, nothing is checked:
                results.update({'case_flag': 0})

            #Optimize the infill based on the first layer collapse:
            D_infill = results['D_infill']
            i = 1
            numLayers = floor(self.scaffT/LH)
            sigma_g = self.layer_collapse(self.scaffH, self.scaffW, self.scaffT, D_infill, LH, i)
            while True:
                if sigma_g < self.tau_y*self.del_max:
                    results.update({'numLayersCollapse': i-1})
                    break
                
                i = i+1
                sigma_g = self.layer_collapse(self.scaffH, self.scaffW, self.scaffT, D_infill, LH, i)

                if i > numLayers:
                    results.update({'numLayersCollapse': i-1})
                    break

        except Exception as err:
            self.signals.error.emit(err.message)
        else:
            self.signals.result.emit(results)
        finally:
            self.signals.finished.emit()

    def optimize_cells(self, V):
        #Find the tau_w from the speed inside the nozzle:
        tau_w = self.bisection_method(self.HB_speed, V, [1e-6, 1e6])
        #Here there are two possible cases:
        R = self.D/2
        Rp = R*self.tau_y/tau_w
        if self.tau_threshold <= self.tau_y:
            #Find the value of r at which the shear is greater than the threshold:
            r_ = self.tau_threshold*R/tau_w
        else:
            #Here all sheared region will have a tau greater than the threshold:
            r_ = Rp
        
        #Then, we can compute the mean velocity in the sheared region as follows:
        A = (1/(R-r_))*(self.n/(self.n+1))*(((R**self.n)*tau_w/self.K)**(1/self.n))
        B = ((1-R/Rp)**(1+1/self.n))*(R-r_)
        C = ((1-Rp/R)**(2+1/self.n)-((r_-Rp)/R)**(2+1/self.n))*(R*self.n/(2*self.n+1))
        v_sheared = A*(B-C)

        #The mean residence time is then:
        t_res = self.syringeLenghts[-1]/v_sheared

        #The sheared percentage is given by:
        S_sheared = 1-(r_/R)**2
        
        #The mean shear stress on the cells is:
        print(t_res)

    def printability_window(self, Wc):
        #Define the LH vector:
        LH = np.linspace(self.LHmin, self.LHmax, num=20)
        #The slicer line width is given by:
        W = self.slicer_line_width(LH)
        #The EM line is given by:
        EM = 1+(4*LH/(pi*(self.D**2)))*(Wc-W)

        return EM, LH
    
    def slicer_line_width(self, LH):
        #The slicer line width is given by:
        W = LH-pi*LH/4+pi*(self.D**2)/(4*LH)

        return W
    
    def corrected_line_width(self, EM, LH):
        W = self.slicer_line_width(LH)
        Wc = W+(EM-1)*(pi*(self.D**2))/(4*LH)

        return Wc

    def EM_from_LH(self, LH, Wc):
        #The slicer line width is given by:
        W = self.slicer_line_width(LH)
        #The EM is given by:
        EM = 1+(4*LH/(pi*(self.D**2)))*(Wc-W)

        return EM
    
    def LH_from_EM(self, EM, Wc):
        #In this case we need to find the root for a second order equation:
        a = 4-pi
        b = -4*Wc
        c = pi*(self.D**2)*EM
        #The two roots are:
        LH = (-b-sqrt((b**2)-4*a*c))/(2*a)
        
        return LH

    def gen_reynolds(self, v_mean):
        #The apparent shear rate is given by:
        sr_a = 8*v_mean/self.D
        #Find the Bingham number:
        Bi = self.tau_y/(self.K*(sr_a ** self.n))
        #The m factor for the HB model is:
        m_hb = self.n/(self.tau_y/(self.K*(sr_a ** self.n))+1)
        #Break up the Reynolds expression to make it more readable:
        A = (self.rho*(v_mean ** (2-self.n))*(self.D ** self.n))/(self.K*(8 ** (self.n-1)))
        B = ((3*m_hb+1)/(4*m_hb)) ** self.n
        Re = A/(Bi+B)

        return Re

    def HB_speed(self, tau_w):        
        #Define the phi constant:
        phi = self.tau_y/tau_w
        #Break up the equation to make it more readable:
        A = (((1-phi) ** 2)/(3*self.n+1))+2*phi*((1-phi)/(2*self.n+1))+(phi ** 2)/(self.n+1)
        #Find the mean velocity at the target wall shear stress:
        v_func = (self.D/2)*self.n*((tau_w/self.K) ** (1/self.n))*((1-phi) ** (1+1/self.n))*A
        
        return v_func

    def pressure_gradient(self, V_N):
        #N.B: V_N is the speed in the nozzle!
        #Find the major losses based on the Stokes equation:
        delP_ml = 0
        #Check if we have a yield stress:
        if self.tau_y == 0:
            minLim = 1e-6
            maxLim = 1e6
        else:
            minLim = self.tau_y*1.1
            maxLim = self.tau_y*100
        
        for index, (Ln, Dn) in enumerate(zip(self.syringeLenghts, self.syringeDiameters)):
            if Ln == 0 or Dn == 0:
                continue
            else:
                V_i = V_N*((self.D/Dn)**2)
                tauw = self.bisection_method(self.HB_speed, V_i, [minLim, maxLim])
                delP_ml += 4*Ln*tauw/Dn
        
        #Then, the total pressure gradient is given by:
        #delP = self.SF*(self.rho*9.81*sum(self.syringeLenghts)+delP_ml)
        delP = self.SF*(delP_ml)
        return delP

    def sheared_region(self, tau_w):
        #The radius of the plug region is given by:
        Rp = (self.D/2)*self.tau_y/tau_w
        #then, the percentage under shear will be given by:
        shearedPerc = 1-(Rp/(self.D/2)) ** 2

        return shearedPerc
    
    def printing_forces(self, LH, EM):
        #The shearing force is given by the product of the sheared area times
        #the wall shear stress:
        W_slicer = self.slicer_line_width(LH)
        W = W_slicer+(EM-1)*(pi*(self.D**2))/(4*LH)
        Q = (self.V*EM)*(pi*((self.D/2)**2))

        gamma_m = self.V/LH
        eta = self.tau_y/gamma_m+self.K*(gamma_m**(self.n-1))

        At = pi*(W**2)/8+(W/2)*self.Dext-pi*(self.D ** 2)/4
        tau_w = eta*abs(-6*Q/((LH ** 2)*W)+4*self.V/LH)
        Ft = tau_w*At

        #The normal force is the product of the pressure times the area:
        Pa = 0
        P = Pa+3*eta*self.V*(W-self.D)/(LH ** 2)
        Fn = P*At

        return Ft, Fn
    
    def line_deformation(self, LH, LW):
        #The maximum spacing is given by:
        SP_max = ((3*self.del_max*self.E*LH*(self.D**2))/(self.rho*9.81))**(1/4)
        #The solid spacing is:
        SP_solid = LW-(LH**2)*(1-(pi/4))
        #and the maximum infill is then:
        D_infill = SP_solid/SP_max
        
        return D_infill

    def layer_collapse(self, H, W, T, D_infill, LH, i):
        #Compute the number of layers:
        numLayers = floor(T/LH)

        #Compute the volume of all the layers minus the first one:
        V = (numLayers-i)*W*H*LH*D_infill

        #The weight force of all the layers (minus the first) is:
        totForce = V*self.rho*9.81

        #The area on which this force acts:
        totArea = H*W*(D_infill**2)
        #and the stress will be given by:
        totStress = totForce/totArea

        return totStress
            
    def bisection_method(self, func, targetValue, interval):
        #Improve the initial guesses! Define a starting point:
        a = interval[0]
        func_a = func(a)-targetValue
        cnt = 1

        while func_a > 0:
            cnt += 1
            a = interval[0]*(self.effort ** cnt)
            func_a = func(a)-targetValue
            #Break to avoid infinite loops:
            if cnt >= self.N:
                break
                
        #To define the upper extreme for the interval, take an initial guess 
        #and verify that f(b) > 0; if not, change b:
        b = interval[1]
        func_b = func(b)-targetValue
        cnt = 1
        while func_b < 0:
            cnt += 1
            b = interval[1]*((1+self.effort) ** cnt)
            func_b = func(b)-targetValue
            #Break to avoid infinite loops:
            if cnt >= self.N:
                break
        
        #Check if the bisection method can be applied:
        if func_a*func_b >= 0:
            raise BisectionMethodException
        
        #Define the two counters for the intervals:
        a_n = a
        b_n = b
        for n in range(1, self.N+1):
            #Find the intermediate point:
            c_n = (a_n+b_n)/2

            #To speed up, find all the func values:
            func_an = func(a_n)-targetValue
            func_bn = func(b_n)-targetValue
            func_cn = func(c_n)-targetValue

            if abs(func_cn) <= self.tol:
                #Solution found with tolerance
                return c_n
            elif func_an*func_cn < 0:
                #The solution is in [a,c]:
                a_n = a_n
                b_n = c_n
            elif func_bn*func_cn < 0:
                #The solution is in [c,b]:
                a_n = c_n
                b_n = b_n
            else:
                #Method does not converge:
                raise BisectionMethodException

        raise MaxIterationsException
    
    def num(self, value):
        try:
            return int(value)
        except ValueError:
            return float(value)

if __name__ == "__main__":
    materialParameters ={'model':'HB', 'K':100, 'n':0.3, 'tauy':10, 'rho':1000}
    printerParameters = {'D':0.2e-3}
    SyringeModel(materialParameters, printerParameters)