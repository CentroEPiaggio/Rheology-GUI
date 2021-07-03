import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from centralTab import TabWidget
import guiSettings

__version__ = '0.0.1'


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.pathToDir = os.getcwd()
        self.pathToRestore = self.pathToDir+'\\config\\'
        self.pathToPrint = self.pathToRestore+'print\\'
        self.pathToMaterial = self.pathToRestore+'material\\'
        self.pathToOpt = self.pathToRestore+'optimization\\'

        #Check if the folder structure is ok, if not create it:
        if not os.path.exists(self.pathToRestore):
            os.makedirs(self.pathToRestore)
        if not os.path.exists(self.pathToPrint):
            os.makedirs(self.pathToPrint)
        if not os.path.exists(self.pathToMaterial):
            os.makedirs(self.pathToMaterial)
        if not os.path.exists(self.pathToOpt):
            os.makedirs(self.pathToOpt)
        
        #Check if the resotre file is present, if not create it:
        if not os.path.exists(self.pathToRestore+'restoreSettings.ini'):
            restoreSettings = QSettings(self.pathToRestore+'restoreSettings.ini', QSettings.IniFormat)
            restoreSettings.setValue('printID', 'default')
            restoreSettings.setValue('materialID', 'default')
            restoreSettings.setValue('optID', 'default')
        #and also check the default files:
        if not os.path.exists(self.pathToPrint+'default.ini'):
            open(self.pathToPrint+'default.ini', 'a')
        if not os.path.exists(self.pathToMaterial+'default.ini'):
            open(self.pathToMaterial+'default.ini', 'a')
        if not os.path.exists(self.pathToOpt+'default.ini'):
            open(self.pathToOpt+'default.ini', 'a')

        #-----------------------------------------
        # WIDGET DEFINITION
        #-----------------------------------------

        #STATUS BAR
        self.labelStatus = QLabel()
        self.labelStatus.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.addPermanentWidget(self.labelStatus)
        #status.showMessage('Version: '+__version__)

        #MENU BAR
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        windowMenu = menuBar.addMenu('&Window')

        #CENTRAL TAB
        self.centralTab = TabWidget(self, self.pathToDir, self.pathToPrint, self.pathToMaterial, self.pathToOpt)
        self.setCentralWidget(self.centralTab)

        #-----------------------------------------
        # OTHERS
        #-----------------------------------------

        self.setGeometry(0,0,700,400)
        self.setWindowTitle('Rheology GUI')
        self.load_all()

    def load_all(self):
        #Load print settings:
        printObj = self.centralTab.firstTab.printSettings
        guiSettings.load_gui_state(printObj, self.pathToRestore, self.pathToPrint, 'printID')
        #Load material settings:
        matObj = self.centralTab.secondTab.materialSettings
        guiSettings.load_gui_state(matObj, self.pathToRestore, self.pathToMaterial, 'materialID')
        #Load optimization settings:
        optObj = self.centralTab.thirdTab.optSettings
        guiSettings.load_gui_state(optObj, self.pathToRestore, self.pathToOpt, 'optID')

    def closeEvent(self, event):
        #Save current index in combobox:
        mainSettings = QSettings(self.pathToRestore+'restoreSettings.ini', QSettings.IniFormat)
        mainSettings.setValue('printID', self.centralTab.firstTab.printSettings.currentText())
        mainSettings.setValue('materialID', self.centralTab.secondTab.materialSettings.currentText())
        mainSettings.setValue('optID', self.centralTab.thirdTab.optSettings.currentText())


if __name__ == "__main__":
	app = QApplication(sys.argv)
	mainWindow = MainWindow()
	mainWindow.show()
	app.exec_()
