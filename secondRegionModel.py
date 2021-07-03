
class LineDepositionModel():

    def __init__(self, materialProperties, printerProperties, v_max):

        #-----------------------------------------
		# PARAMETERS DEFINITION
		#-----------------------------------------

        #The inputs will be in a dictionary form, start by extracting the relevant information
        #based on key values. For the material properties:
        if materialParameters['model'] == 'newtonian':
            self.K = materialParameters['viscosity']
            self.n = 1
            self.tau_y = 0
        elif materialParameters['model'] == 'powerlaw':
            self.K = materialParameters['K']
            self.n = materialParameters['n']
            self.tau_y = 0
        elif materialParameters['model'] == 'HB':
            self.K = materialParameters['K']
            self.n = materialParameters['n']
            self.tau_y = materialParameters['tauy']
        
        self.rho = materialParameters['rho']

        #and for the printer properties:
        self.D = printerParameters['D']
        self.LH = printerProperties['LH']

        #Define an external needle diameter:
        self.Dext = self.D*1.5        
        #TODO: verify the general relationship, you can also multiply it by a SF

        #Define a minimum LH, to avoid collision with printing plate:
        self.LHmin = self.D*0.2
        #TODO: find a general relationship!

        #Define a maximum LH, to keep the material under pressure:
        self.LHmax = 0.8*self.D

        #From the region 1 model, we know the maximum mean velocity:
        self.v_max = v_max
        
        #-----------------------------------------
		# LINE DEPOSITION MODEL
		#-----------------------------------------

        #The output will be a printability window!

        #From the region 1 model we know the maximum piston speed.

    
    def printing_forces(self, W, LH, Q, U, Dn, Dext, eta):
        #The shearing force is given by the product of the sheared area times
        #the wall shear stress:
        At = 3.14*((W/2) ** 2)/2+(W/2)*Dext-3.14*(Dn ** 2)/4
        tau_w = eta*abs(-6*Q/((LH ** 2)*W)+4*U/LH)
        Ft = tau_w*At

        #The normal force is the product of the pressure times the area:
        Pa = 1
        P = Pa+3*eta*U*(W-Dn)/(LH ** 2)
        Fn = P*At

        return Fn, Ft

    def line_width(self, LH, Dn, EM):
        #The Slic3r line width is given by:
        W = LH-3.14*LH/4+3.14*(Dn ** 2)/(4*LH)

        #The corrected line width is given by:
        Wc = W+(3.14*(Dn ** 2)/(4*LH))*(EM-1)

        return Wc

