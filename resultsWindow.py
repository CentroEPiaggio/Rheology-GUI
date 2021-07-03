from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from stringMessages import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas 
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
import numpy as np

class Results(QWidget):

    def __init__(self, res, parent=None):
        super(Results, self).__init__(parent)
        #Some useful constants:
        inputWidth = 100
        inputHeight = 20
        labelWidth = 500
        labelHeight = 25

        #Unpack results for better readability, first region:
        delP_min = res['delP_min']
        delP_target = res['delP_target']
        #Printability window:
        LH = res['LH']
        EM_min_v = res['EM_min_v']
        EM_max_v = res['EM_max_v']
        EM_max = res['EM_']
        #Printing forces:
        F = res['F']
        #Number of collapsed layers:
        collapsedLayers = res['numLayersCollapse']

        #Some results may be present or not based on user input, so find the case flag:
        case_flag = res['case_flag']

        #-----------------------------------------
        # WIDGET DEFINITION
        #-----------------------------------------
        
        #First region outputs:
        labelMinP = QLabel('Minimum pressure: '+str(round(delP_min))+' Pa')
        labelMinP.setFixedSize(labelWidth, labelHeight)

        labelDelP = QLabel('Pressure Gradient: '+str(round(delP_target))+' Pa')
        labelDelP.setFixedSize(labelWidth, labelHeight)

        labelRegion1 = QLabel(msgRegion1)
        labelRegion1.setWordWrap(True)

        #labelForces = QLabel('Tangential Printing Force: '+str(round(F[0],3))+' mN\n'\
        #    +'Normal Printing Force: '+str(round(F[1],3))+' mN'+'\n')

        #Second region outputs, the structure depends on the optimization tab. Create all the widgets
        #and enable them if necessary:
        labelRegion2 = QLabel(msgRegion2)
        labelRegion2.setWordWrap(True)

        labelSRCase0 = QLabel('')
        labelSRCase0.setFixedWidth(labelWidth)
        labelSRCase0.setWordWrap(True)

        labelSRCase1 = QLabel('')
        labelSRCase1.setFixedWidth(labelWidth)
        labelSRCase1.setWordWrap(True)

        labelSRCase2 = QLabel('')
        labelSRCase2.setFixedWidth(labelWidth)
        labelSRCase2.setWordWrap(True)

        labelSRCase3 = QLabel('')
        labelSRCase3.setFixedWidth(labelWidth)
        labelSRCase3.setWordWrap(True)

        labelSRCase4 = QLabel('')
        labelSRCase4.setFixedWidth(labelWidth)
        labelSRCase4.setWordWrap(True)

        labelSRCase5 = QLabel('')
        labelSRCase5.setFixedWidth(labelWidth)
        labelSRCase5.setWordWrap(True)

        labelSRCase6 = QLabel('')
        labelSRCase6.setFixedWidth(labelWidth)
        labelSRCase6.setWordWrap(True)

        labelSRCase7 = QLabel('')
        labelSRCase7.setFixedWidth(labelWidth)
        labelSRCase7.setWordWrap(True)

        #Third region outputs:
        labelRegion3 = QLabel(msgRegion3)
        labelRegion3.setWordWrap(True)

        labelTR = QLabel('')
        labelTR.setFixedWidth(labelWidth)
        labelTR.setWordWrap(True)

        labelLayerCollapse = QLabel('')
        labelLayerCollapse.setFixedWidth(labelWidth)
        labelLayerCollapse.setWordWrap(True)

        #Printability window:
        self.PWfig = plt.figure()
        self.PWcanvas = FigureCanvas(self.PWfig)
        
        #-----------------------------------------
        # LAYOUT DEFINITION
        #-----------------------------------------

        #FIRST REGION RESULTS
        frameFirstModel = QGroupBox()
        layoutFirstModel = QGridLayout()
        layoutFirstModel.addWidget(labelMinP,0,0)
        layoutFirstModel.addWidget(labelDelP,1,0)
        layoutFirstModel.addWidget(labelRegion1,2,0)
        frameFirstModel.setLayout(layoutFirstModel)
        frameFirstModel.setTitle('Extrusion Model Results:')

        layoutLeft = QVBoxLayout()
        layoutLeft.addWidget(frameFirstModel)

        #SECOND REGION RESULTS
        frameSecondModel = QGroupBox()
        layoutSecondModel = QVBoxLayout()
        #layoutSecondModel.addWidget(labelForces)
        layoutSecondModel.addWidget(labelRegion2)
        #Enable based on optimization inputs:
        if case_flag == 0:
            pass
        elif case_flag == 1:
            EM_opt = res['EM_opt']
            labelSRCase1.setText('Optimized range for EM: '+str(round(EM_opt[0],2))+' - '+str(round(EM_opt[1],2))+'\n\n'+msgCase1)
            layoutSecondModel.addWidget(labelSRCase1)
        elif case_flag == 2:
            LH_opt = res['LH_opt']
            labelSRCase2.setText('Optimized range for LH: '+str(round(LH_opt[0],3))+' - '+str(round(LH_opt[1],3))+\
                ' times the nozzle diameter.\n\n'+msgCase2)
            layoutSecondModel.addWidget(labelSRCase2)
        elif case_flag == 3:
            labelSRCase3.setText(msgCase3)
            layoutSecondModel.addWidget(labelSRCase3)
        elif case_flag == 4:
            LW_opt = res['LW_opt']
            labelSRCase4.setText('The LW at the specified LH-EM combination is: '+str(round(LW_opt, 2))+' mm.\n\n'+msgCase4)
            layoutSecondModel.addWidget(labelSRCase4)
        elif case_flag == 5:
            EM_opt = res['EM_opt']
            labelSRCase5.setText('The corrected EM is: '+str(round(EM_opt, 2))+'\n\n'+msgCase5)
            layoutSecondModel.addWidget(labelSRCase5)
        elif case_flag == 6:
            LH_opt = res['LH_opt']
            labelSRCase6.setText('The optimized LH is: '+str(round(LH_opt, 2))+\
                ' times the nozzle diameter.\n\n'+msgCase6)
            layoutSecondModel.addWidget(labelSRCase6)
        elif case_flag == 7:
            LW_opt = res['LW_opt']
            LW_error = res['LW_error']
            labelSRCase7.setText('The corrected LW is: '+str(round(LW_opt, 2))+' mm\n'+\
                        'The line error is: '+str(round(LW_error,2)*100)+'\n\n'+msgCase7)
            layoutSecondModel.addWidget(labelSRCase7)            

        frameSecondModel.setLayout(layoutSecondModel)
        frameSecondModel.setTitle('Line Deposition Results:')
        #Now check if the frame is empty and if true add it to the leftlayout:
        if layoutSecondModel.count() != 0:
            layoutLeft.addWidget(frameSecondModel)

        #THIRD REGION RESULTS
        frameThirdModel = QGroupBox()
        layoutThirdModel = QVBoxLayout()
        layoutThirdModel.addWidget(labelRegion3)
        #Enable based on optimization inputs:
        if case_flag != 7:
            labelTR.setText('Choose an Infill Density greater than: '+str(round(res['D_infill']*100,1))+' %')
            layoutThirdModel.addWidget(labelTR) 
        elif case_flag == 7:
            pass

        #If there is layer collapse, add a message:
        if collapsedLayers > 0:
            labelLayerCollapse.setText('Warning! A total of '+str(collapsedLayers)+' layers may collapse due to gravity!')
            layoutThirdModel.addWidget(labelLayerCollapse)

        frameThirdModel.setLayout(layoutThirdModel)
        frameThirdModel.setTitle('Post Print Results:')
        #Now check if the frame is empty and if true add it to the leftlayout:
        if layoutThirdModel.count() != 0:
            layoutLeft.addWidget(frameThirdModel)

        layoutLeft.addStretch()

        #PRINTABILITY WINDOW
        framePW = QGroupBox()
        layoutPW = QVBoxLayout()
        layoutPW.addWidget(self.PWcanvas)
        framePW.setLayout(layoutPW)
        framePW.setTitle('Printability Window:')        

        mainLayout = QHBoxLayout()
        mainLayout.addLayout(layoutLeft)
        mainLayout.addWidget(framePW)

        self.setLayout(mainLayout)

        #-----------------------------------------
        # OTHERS
        #-----------------------------------------

        #Draw the printability window:
        ax = self.PWfig.add_subplot(111)
        ax.plot(LH, EM_min_v, LH, EM_max_v)
        if case_flag == 0:
            self.cursor = Cursor(ax, useblit=True, color='red', linewidth=1)
            self.PWcanvas.mpl_connect('button_press_event', self.on_click)
        elif case_flag == 1:
            ax.vlines(x=res['LH_p'], ymin=EM_opt[0], ymax=EM_opt[1], color='red', linestyle='--')
        elif case_flag == 2:
            ax.hlines(y=res['EM_p'], xmin=LH_opt[0], xmax=LH_opt[1], color='red', linestyle='--')
        elif case_flag == 3:
            ax.plot(LH, res['EM_line'])
        elif case_flag == 4:
            ax.plot(res['LH_p'], res['EM_p'], 'ro')
        elif case_flag == 5:
            ax.plot(res['LH_p'], EM_opt, 'ro')
        elif case_flag == 6:
            ax.plot(LH_opt, res['EM_p'], 'ro')
            #ax.plot(LH, res['EM_line'])
        elif case_flag == 7:
            ax.plot(res['LH_p'], res['EM_p'], 'ro')
            ax.plot(LH, res['EM_line'])
            
        #Add an horizontal line:
        if EM_max != np.max(EM_max_v):
            ax.axhline(y=EM_max, color='red', linestyle='--')
        ax.fill_between(LH, EM_min_v, EM_max_v, color='grey', alpha=0.5)
        ax.set_xlabel('LH')
        ax.set_ylabel('EM')

        self.PWcanvas.draw()
    
    def on_click(self, event):
        print("event.xdata", event.xdata)
        print("event.ydata", event.ydata)
        print("event.inaxes", event.inaxes)

        


        

if __name__ == "__main__":
    pass