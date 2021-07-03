from os.path import dirname, realpath, expanduser, exists
from os import listdir, remove, makedirs
from math import floor

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import centralWidgetTab1
import centralWidgetTab2
import centralWidgetTab3
import resultsWindow
from errorDLG import ErrorDlg

from printModel import PrintModel
from resultsWindow import Results
import guiSettings


class TabWidget(QWidget):

    def __init__(self, parent, pathToDir, pathToPrint, pathToMaterial, pathToOpt):

        super(TabWidget, self).__init__(parent)
        self.parent = parent

        self.pathToDir = pathToDir
        self.pathToPrint = pathToPrint
        self.pathToMaterial = pathToMaterial
        self.pathToOpt = pathToOpt

        #-----------------------------------------
        # WIDGET DEFINITION
        #-----------------------------------------

        self.firstTab = centralWidgetTab1.FirstTab(self, self.pathToPrint)
        self.secondTab = centralWidgetTab2.SecondTab(self, self.pathToMaterial)
        self.thirdTab = centralWidgetTab3.ThirdTab(self, self.pathToOpt)
        
        #-----------------------------------------
        # LAYOUT DEFINITION
        #-----------------------------------------

        self.tabWidget = QTabWidget()
        self.tabWidget.addTab(self.firstTab, 'Printer and Geometry Settings')
        self.tabWidget.addTab(self.secondTab, 'Material Settings')
        self.tabWidget.addTab(self.thirdTab, 'Optimization Settings')

        #Only first tab enabled at start-up:
        self.tabWidget.setTabEnabled(1, False)
        self.tabWidget.setTabEnabled(2, False)

        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.tabWidget)
        self.setLayout(mainLayout)

        #-----------------------------------------
        # CONNECTIONS
        #-----------------------------------------

        self.firstTab.buttonNextTo2.clicked.connect(lambda: self.changeTabs(1, self.pathToPrint))
        self.secondTab.buttonBackTo1.clicked.connect(lambda: self.changeTabs(0, self.pathToMaterial))
        self.secondTab.buttonNextTo3.clicked.connect(lambda: self.changeTabs(2, self.pathToMaterial))
        self.thirdTab.buttonBackTo2.clicked.connect(lambda: self.changeTabs(1))
        self.thirdTab.buttonNextTo4.clicked.connect(lambda: self.do_optimization())
        
        #-----------------------------------------
        # OTHERS
        #-----------------------------------------

        #Set-up multi-threading:
        self.threadpool = QThreadPool()

    def changeTabs(self, targetTab, pathToSettings=None):
        #Check that all inputs in current tab are ok:
        currentTab = self.tabWidget.currentWidget()
        currentTabID = self.tabWidget.currentIndex()
        if currentTabID < targetTab:
            if guiSettings.tab_checks(currentTab):
                return
            #If everything is ok, do a save in the current tab:
            guiSettings.quick_save(currentTab, pathToSettings)
        
        #Next, if there were no error in inputs, which to the target tab
        for i in range(self.tabWidget.count()):
            if i == targetTab:
                self.tabWidget.setTabEnabled(i, True)
            else:
                self.tabWidget.setTabEnabled(i, False)
        
        #Move to target tab:
        self.tabWidget.setCurrentIndex(targetTab)
    
    def do_optimization(self):
        #First check for empty inputs:
        if guiSettings.tab_checks(self.thirdTab):
            return
        #and if everything is ok do a quick save:
        guiSettings.quick_save(self.thirdTab, self.pathToOpt)
        #TODO: add a pop-up window to ask continue-back
        
        #Unpack the current settings:
        printConfName = self.firstTab.printSettings.currentText()
        printProp = guiSettings.unpack_conf(self.pathToPrint, printConfName)

        matConfName = self.secondTab.materialSettings.currentText()
        materialProp = guiSettings.unpack_conf(self.pathToMaterial, matConfName)

        optConfName = self.thirdTab.optSettings.currentText()
        optProp = guiSettings.unpack_conf(self.pathToOpt, optConfName)

        #Now, initialize the extrusion model:
        model = PrintModel(materialProp, printProp, optProp)
        model.signals.finished.connect(self.print_finish)
        model.signals.result.connect(self.show_res)
        model.signals.error.connect(self.error_handling)
        self.threadpool.start(model)
    
    def error_handling(self, errorString):
        print(errorString)
        self.errDLG = ErrorDlg(errorString)
        self.errDLG.show()

    def print_finish(self):
        print('Finished')

    def show_res(self, res):
        #Show the results window:
        self.resWindow = Results(res)
        self.resWindow.show()


#Move the model to a separate thread:
class PrintModelWorker(QRunnable):
    def __init__(self):
        super(PrintModelWorker, self).__init__()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = TabWidget()
    w.show()
    sys.exit(app.exec_())	