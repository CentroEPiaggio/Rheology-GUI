from os import listdir, remove

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import guiSettings

class SecondTab(QWidget):

    def __init__(self, parent, pathToMaterial):
        super(SecondTab, self).__init__(parent)

        #Define the path to the material settings folder:
        self.pathToMaterial = pathToMaterial

        #Some useful constants:
        inputWidth = 100
        inputHeight = 20
        labelWidth = 200
        labelHeight = 25

        #Define a validator to block inputs on line edits:
        digitValidator = QRegExpValidator(QRegExp(r'[0-9]{1,4}\.[0-9]{1,4}'))
        integerValidator = QRegExpValidator(QRegExp(r'[1-9][0-9]{,4}'))

        #-----------------------------------------
        # WIDGET DEFINITION
        #-----------------------------------------

        #CONFIG
        self.materialSettings = QComboBox()
        self.materialSettings.setFixedWidth(100)

        self.buttonSaveMaterial = QPushButton('&Save...')
        self.buttonDeleteMaterial = QPushButton('&Delete...')

        #MATERIAL MODEL
        self.radioNewtonian = QRadioButton('Newtonian')
        self.radioNewtonian.setObjectName('Newton')
        self.radioNewtonian.setChecked(True)
        
        self.radioPowerLaw = QRadioButton('Power Law')
        self.radioPowerLaw.setObjectName('PowerLaw')
        self.radioPowerLaw.setChecked(False)

        self.radioHB = QRadioButton('Herschel-Bulkley')
        self.radioHB.setObjectName('HB')
        self.radioHB.setChecked(False)

        #Create a button group with index:
        self.radioGroup = QButtonGroup()
        self.radioGroup.addButton(self.radioNewtonian, 0)
        self.radioGroup.addButton(self.radioPowerLaw, 1)
        self.radioGroup.addButton(self.radioHB, 2)

        #VISCOSITY
        labelViscosity = QLabel('Material Viscosity [Pa*s]:')
        labelViscosity.setFixedSize(labelWidth, labelHeight)
        self.inputViscosity = QLineEdit()
        self.inputViscosity.setObjectName('eta')
        self.inputViscosity.setFixedSize(inputWidth, inputHeight)
        self.inputViscosity.setValidator(integerValidator)
        self.inputViscosity.setEnabled(True)
        labelViscosity.setBuddy(self.inputViscosity)

        #FLOW INDEX n
        labeln = QLabel('Flow Index:')
        labeln.setFixedSize(labelWidth, labelHeight)
        self.inputn = QLineEdit()
        self.inputn.setObjectName('FlowIndex')
        self.inputn.setFixedSize(inputWidth, inputHeight)
        self.inputn.setValidator(digitValidator)
        self.inputn.setEnabled(False)
        labeln.setBuddy(self.inputn)

        #CONSISTENCY INDEX K
        labelK = QLabel('Consistency Index [Pa*s^n]:')
        labelK.setFixedSize(labelWidth, labelHeight)
        self.inputK = QLineEdit()
        self.inputK.setObjectName('K')
        self.inputK.setFixedSize(inputWidth, inputHeight)
        self.inputK.setValidator(digitValidator)
        self.inputK.setEnabled(False)
        labelK.setBuddy(self.inputK)

        #YIELD STRESS
        labelYield = QLabel('Yield Stress [Pa]:')
        labelYield.setFixedSize(labelWidth, labelHeight)
        self.inputYield = QLineEdit()
        self.inputYield.setObjectName('tau_y')
        self.inputYield.setFixedSize(inputWidth, inputHeight)
        self.inputYield.setValidator(digitValidator)
        self.inputYield.setEnabled(False)
        labelYield.setBuddy(self.inputYield)

        #RHO
        labelDensity = QLabel('Density [kg/m^3]:')
        labelDensity.setFixedSize(labelWidth, labelHeight)
        self.inputDensity = QLineEdit()
        self.inputDensity.setObjectName('rho')
        self.inputDensity.setFixedSize(inputWidth, inputHeight)
        self.inputDensity.setValidator(digitValidator)
        labelDensity.setBuddy(self.inputDensity)

        #ELASTIC MODULUS
        labelE = QLabel("Elastic modulus [Pa]:")
        labelE.setFixedSize(labelWidth, labelHeight)
        self.inputE = QLineEdit()
        self.inputE.setObjectName('E')
        self.inputE.setValidator(integerValidator)
        self.inputE.setFixedSize(inputWidth, inputHeight)
        labelE.setBuddy(self.inputE)

        #ETA 0
        labelEta0 = QLabel("Zero-shear viscosity [Pa*s]:")
        labelEta0.setFixedSize(labelWidth, labelHeight)
        self.inputEta0 = QLineEdit()
        self.inputEta0.setObjectName('eta_0')
        self.inputEta0.setValidator(integerValidator)
        self.inputEta0.setFixedSize(inputWidth, inputHeight)
        labelEta0.setBuddy(self.inputEta0)

        #MOVE BUTTONS
        self.buttonNextTo3 = QPushButton('&Next...')
        self.buttonBackTo1 = QPushButton('&Back...')

        #-----------------------------------------
        # LAYOUT DEFINITION
        #-----------------------------------------

        #SAVE SETTINGS
        upperLayout = QHBoxLayout()
        upperLayout.addWidget(self.materialSettings)
        upperLayout.addWidget(self.buttonSaveMaterial)
        upperLayout.addWidget(self.buttonDeleteMaterial)
        upperLayout.addStretch()
        upperLayout.setSpacing(10)

        #RADIO LAYOUT
        layoutRadioMaterial = QGridLayout()
        layoutRadioMaterial.addWidget(self.radioNewtonian,0,0)
        layoutRadioMaterial.addWidget(self.radioPowerLaw,0,1)
        layoutRadioMaterial.addWidget(self.radioHB,0,2)

        #VISCOSITY LAYOUT
        layoutViscosity = QHBoxLayout()
        layoutViscosity.addWidget(labelViscosity)
        layoutViscosity.addStretch()
        layoutViscosity.addWidget(self.inputViscosity)

        #n LAYOUT
        layoutn = QHBoxLayout()
        layoutn.addWidget(labeln)
        layoutn.addStretch()
        layoutn.addWidget(self.inputn)

        #K LAYOUT
        layoutK = QHBoxLayout()
        layoutK.addWidget(labelK)
        layoutK.addStretch()
        layoutK.addWidget(self.inputK)

        #YIELD LAYOUT
        layoutYield = QHBoxLayout()
        layoutYield.addWidget(labelYield)
        layoutYield.addStretch()
        layoutYield.addWidget(self.inputYield)

        #RHO LAYOUT
        layoutDensity = QHBoxLayout()
        layoutDensity.addWidget(labelDensity)
        layoutDensity.addStretch()
        layoutDensity.addWidget(self.inputDensity)

        #E LAYOUT
        LayoutE = QHBoxLayout()
        LayoutE.addWidget(labelE)
        LayoutE.addStretch()
        LayoutE.addWidget(self.inputE)

        #ETA 0 LAYOUT
        layoutEta0 = QHBoxLayout()
        layoutEta0.addWidget(labelEta0)
        layoutEta0.addStretch()
        layoutEta0.addWidget(self.inputEta0)

        #RHEOLOGICAL PROPERTIES
        frameRheo = QGroupBox()
        layoutRheo = QGridLayout()
        layoutRheo.addLayout(layoutRadioMaterial,0,0)
        layoutRheo.addLayout(layoutViscosity,1,0)
        layoutRheo.addLayout(layoutn,2,0)
        layoutRheo.addLayout(layoutK,3,0)
        layoutRheo.addLayout(layoutYield,4,0)
        frameRheo.setLayout(layoutRheo)
        frameRheo.setTitle('Rheological Model:')

        #MECHANICAL PROPERTIES
        frameMech = QGroupBox()
        layoutMech = QGridLayout()
        layoutMech.addLayout(layoutDensity,0,0)
        layoutMech.addLayout(LayoutE,1,0)
        layoutMech.addLayout(layoutEta0,2,0)
        frameMech.setLayout(layoutMech)
        frameMech.setTitle('Mechanical Properties:')

        #BUTTON LAYOUT
        layoutButton = QHBoxLayout()
        layoutButton.addWidget(self.buttonBackTo1)
        layoutButton.addStretch()
        layoutButton.addWidget(self.buttonNextTo3)		
        
        #MAIN LAYOUT
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(upperLayout)
        mainLayout.addWidget(frameRheo)
        mainLayout.addWidget(frameMech)
        mainLayout.addStretch()
        mainLayout.addLayout(layoutButton)

        self.setLayout(mainLayout)

        #-----------------------------------------
        # CONNECTIONS
        #-----------------------------------------

        self.radioNewtonian.toggled.connect(self.radioToggled)
        self.radioPowerLaw.toggled.connect(self.radioToggled)
        self.radioHB.toggled.connect(self.radioToggled)

        self.buttonSaveMaterial.clicked.connect(lambda: guiSettings.save_dialog(self, self.pathToMaterial))
        self.buttonDeleteMaterial.clicked.connect(lambda: guiSettings.delete_settings(self, self.pathToMaterial, self.materialSettings.currentText()))
        self.materialSettings.currentIndexChanged.connect(lambda: guiSettings.change_settings(self, self.pathToMaterial, self.materialSettings.currentText()))

    def radioToggled(self):
        #Get material model:
        matModel = self.radioGroup.checkedButton().text()
        if matModel == 'Newtonian':
            self.inputViscosity.setEnabled(True)
            self.inputn.setEnabled(False)
            self.inputK.setEnabled(False)
            self.inputYield.setEnabled(False)
        elif matModel == 'Power Law':
            self.inputViscosity.setEnabled(False)
            self.inputn.setEnabled(True)
            self.inputK.setEnabled(True)
            self.inputYield.setEnabled(False)
        elif matModel == 'Herschel-Bulkley':
            self.inputViscosity.setEnabled(False)
            self.inputn.setEnabled(True)
            self.inputK.setEnabled(True)
            self.inputYield.setEnabled(True)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = FirstTab()
    w.show()
    sys.exit(app.exec_())