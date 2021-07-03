from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import guiSettings


class ThirdTab(QWidget):
    """
    A class that defines the third tab of the main tab widget

    """
    def __init__(self, parent, pathToOpt):
        super(ThirdTab, self).__init__(parent)

        #Define the path to the optimization settings folder:
        self.pathToOpt = pathToOpt

        #Some useful constants:
        inputWidth = 100
        inputHeight = 20
        labelWidth = 150
        labelHeight = 25

        #Define a validator to block inputs on line edits:
        digitValidator = QRegExpValidator(QRegExp(r'[0-9]{1,4}\.[0-9]{1,4}'))
        integerValidator = QRegExpValidator(QRegExp(r'[1-9][0-9]{,4}'))
        scientificValidator = QRegExpValidator(QRegExp(r'[1-9](\.[0-9]{1})?[e,E][0-9]'))

        #-----------------------------------------
        # WIDGET DEFINITION
        #-----------------------------------------

        #CONFIG
        self.optSettings = QComboBox()
        self.optSettings.setFixedWidth(100)

        self.buttonSaveOptSet = QPushButton('&Save...')
        self.buttonDelOptSet = QPushButton('&Delete...')

        #INPUT OPTIMIZATION CHECK BOXES
        self.checkLH = QCheckBox('Layer Height')
        self.checkLH.setObjectName('LH_check')
        self.checkEM = QCheckBox('Extrusion Multiplier')
        self.checkEM.setObjectName('EM_check')
        self.checkLW = QCheckBox('Line Width')
        self.checkLW.setObjectName('LW_check')
        self.checkInfill = QCheckBox('Infill Density')
        self.checkInfill.setObjectName('Infill_check')

        #LAYER HEIGHT:
        labelLH = QLabel('Constrain LH to (relative to the nozzle diameter):')
        #labelLH.setFixedSize(labelWidth, labelHeight)
        labelLH.adjustSize()
        self.inputLH = QLineEdit()
        self.inputLH.setEnabled(False)
        self.inputLH.setObjectName('LH')
        self.inputLH.setFixedSize(inputWidth, inputHeight)
        self.inputLH.setValidator(digitValidator)
        labelLH.setBuddy(self.inputLH)

        #EXTRUSION MULTIPLIER:
        labelEM = QLabel('Constrain EM to:')
        #labelEM.setFixedSize(labelWidth, labelHeight)
        labelEM.adjustSize()
        self.inputEM = QLineEdit()
        self.inputEM.setEnabled(False)
        self.inputEM.setObjectName('EM')
        self.inputEM.setFixedSize(inputWidth, inputHeight)
        self.inputEM.setValidator(digitValidator)
        labelEM.setBuddy(self.inputEM)

        #LINE WIDTH:
        labelLW = QLabel('Constrain LW to (relative to the nozzle diameter):')
        labelLW.adjustSize()
        #labelLW.setFixedSize(labelWidth, labelHeight)
        self.inputLW = QLineEdit()
        self.inputLW.setEnabled(False)
        self.inputLW.setObjectName('LW')
        self.inputLW.setFixedSize(inputWidth, inputHeight)
        self.inputLW.setValidator(digitValidator)
        labelLW.setBuddy(self.inputLW)

        #MOVE BUTTONS
        self.buttonNextTo4 = QPushButton('&Optimize...')
        self.buttonBackTo2 = QPushButton('&Back...')

        #-----------------------------------------
        # LAYOUT DEFINITION
        #-----------------------------------------

        #SAVE SETTINGS
        upperLayout = QHBoxLayout()
        upperLayout.addWidget(self.optSettings)
        upperLayout.addWidget(self.buttonSaveOptSet)
        upperLayout.addWidget(self.buttonDelOptSet)
        upperLayout.addStretch()
        upperLayout.setSpacing(10)

        #LAYER HEIGHT
        layoutLH = QHBoxLayout()
        layoutLH.addWidget(self.checkLH)
        layoutLH.addStretch()
        layoutLH.addWidget(labelLH)
        layoutLH.addWidget(self.inputLH)

        #EXTRUSION MULTIPLIER
        layoutEM = QHBoxLayout()
        layoutEM.addWidget(self.checkEM)
        layoutEM.addStretch()
        layoutEM.addWidget(labelEM)
        layoutEM.addWidget(self.inputEM)

        #LAYER WIDTH
        layoutLW = QHBoxLayout()
        layoutLW.addWidget(self.checkLW)
        layoutLW.addStretch()
        layoutLW.addWidget(labelLW)
        layoutLW.addWidget(self.inputLW)

        #CHECK BOXES LAYOUT
        frameOptimization = QGroupBox()
        layoutOptimization = QGridLayout()
        layoutOptimization.addLayout(layoutLH,0,0)
        layoutOptimization.addLayout(layoutEM,1,0)
        layoutOptimization.addLayout(layoutLW,2,0)
        frameOptimization.setLayout(layoutOptimization)
        frameOptimization.setTitle('Optimization Inputs:')
        
        #BUTTON LAYOUT
        layoutButton = QHBoxLayout()
        layoutButton.addWidget(self.buttonBackTo2)
        layoutButton.addStretch()
        layoutButton.addWidget(self.buttonNextTo4)		
        
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(upperLayout)
        mainLayout.addWidget(frameOptimization)
        mainLayout.addStretch()
        mainLayout.addLayout(layoutButton)

        self.setLayout(mainLayout)

        #-----------------------------------------
        # CONNECTIONS
        #-----------------------------------------

        self.checkLH.toggled.connect(self.inputLH.setEnabled)
        self.checkEM.toggled.connect(self.inputEM.setEnabled)
        self.checkLW.toggled.connect(self.inputLW.setEnabled)

        self.buttonSaveOptSet.clicked.connect(lambda: guiSettings.save_dialog(self, self.pathToOpt))
        self.buttonDelOptSet.clicked.connect(lambda: guiSettings.delete_settings(self, self.pathToOpt, self.optSettings.currentText()))
        self.optSettings.currentIndexChanged.connect(lambda: guiSettings.change_settings(self, self.pathToOpt, self.optSettings.currentText()))


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = FirstTab()
    w.show()
    sys.exit(app.exec_())