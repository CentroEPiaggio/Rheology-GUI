class MaxIterationsException(Exception):
    def __init__(self):
        self.message = 'Maximum Number of Iterations reached'
        super().__init__(self.message)

class BisectionMethodException(Exception):
    def __init__(self):
        self.message = 'Bisection Method not converged'
        super().__init__(self.message)

class PminCheckFailed(Exception):
    def __init__(self):
        self.message = 'The material is not extrudable for the given printer. You can try to:\n'
        self.message += '* increase the nozzle diameter'

class HighPressureException(Exception):
    def __init__(self):
        self.message = 'The printer cannot extrude the material at the given flow rate. You can try to:\n'
        self.message += '* increase the nozzle diameter\n'
        self.message += '* decrease the printing speed'

class EMoutOfRangeException(Exception):
    def __init__(self, msgStr):
        self.message = 'The constrained EM is out of range.\n'
        self.message += msgStr

class LHoutOfRangeException(Exception):
    def __init__(self):
        self.message = 'The constrained LH is out of range.'

class LWoutOfRangeException(Exception):
    def __init__(self):
        self.message = 'The constrained LW is out of range.'
