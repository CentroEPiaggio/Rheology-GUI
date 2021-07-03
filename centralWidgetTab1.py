from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import guiSettings

class FirstTab(QWidget):
    """
    A class that defines the first tab of the main tab widget

    """
    def __init__(self, parent, pathToPrint):
        super(FirstTab, self).__init__(parent)

        self.pathToPrint = pathToPrint

        #Some useful constants:
        inputWidth = 100
        inputHeight = 20
        labelWidth = 200
        labelHeight = 25

        #Define a validator to block inputs on line edits:
        digitValidator = QRegExpValidator(QRegExp(r'[0-9]{1,4}\.[0-9]{1,4}'))
        integerValidator = QRegExpValidator(QRegExp(r'[1-9][0-9]{,4}'))
        scientificValidator = QRegExpValidator(QRegExp(r'[1-9](\.[0-9]{1})?[e,E][0-9]'))

        #-----------------------------------------
        # WIDGET DEFINITION
        #-----------------------------------------

        #CONFIG
        self.printSettings = QComboBox()
        self.printSettings.setFixedWidth(100)

        self.buttonSavePrintSet = QPushButton('&Save...')
        self.buttonDelPrintSet = QPushButton('&Delete...')

        #PRINTER MAX PRESSURE
        labelPrintMaxP = QLabel('Printer Max Pressure [Pa]:')
        labelPrintMaxP.setFixedSize(labelWidth, labelHeight)
        self.inputPrintMaxP = QLineEdit()
        self.inputPrintMaxP.setObjectName('P_max')
        self.inputPrintMaxP.setFixedSize(inputWidth, inputHeight)
        self.inputPrintMaxP.setValidator(scientificValidator)
        labelPrintMaxP.setBuddy(self.inputPrintMaxP)

        #PRINT SPEED:
        labelV = QLabel('Print Speed [mm/s]:')
        labelV.setFixedSize(labelWidth, labelHeight)
        self.inputV = QLineEdit()
        self.inputV.setObjectName('V')
        self.inputV.setFixedSize(inputWidth, inputHeight)
        self.inputV.setValidator(digitValidator)
        labelV.setBuddy(self.inputV)

        #NOZZLE DIAMETER:
        labelD = QLabel('Nozzle Diameter [mm]:')
        labelD.setFixedSize(labelWidth, labelHeight)
        self.inputD = QLineEdit()
        self.inputD.setObjectName('D')
        self.inputD.setFixedSize(inputWidth, inputHeight)
        self.inputD.setValidator(digitValidator)
        labelD.setBuddy(self.inputD)

        #SCAFFOLD HEIGHT
        labelScaffoldH = QLabel('Scaffold Height [mm]:')
        labelScaffoldH.setFixedSize(labelWidth, labelHeight)
        self.inputScaffoldH = QLineEdit()
        self.inputScaffoldH.setObjectName('Scaffold Height')
        self.inputScaffoldH.setFixedSize(inputWidth, inputHeight)
        self.inputScaffoldH.setValidator(digitValidator)
        labelScaffoldH.setBuddy(self.inputScaffoldH)

        #SCAFFOLD WIDTH
        labelScaffoldW = QLabel('Scaffold Width [mm]:')
        labelScaffoldW.setFixedSize(labelWidth, labelHeight)
        self.inputScaffoldW = QLineEdit()
        self.inputScaffoldW.setObjectName('Scaffold Width')
        self.inputScaffoldW.setFixedSize(inputWidth, inputHeight)
        self.inputScaffoldW.setValidator(digitValidator)
        labelScaffoldW.setBuddy(self.inputScaffoldW)

        #SCAFFOLD THICKNESS
        labelScaffoldT = QLabel('Scaffold Thickness [mm]:')
        labelScaffoldT.setFixedSize(labelWidth, labelHeight)
        self.inputScaffoldT = QLineEdit()
        self.inputScaffoldT.setObjectName('Scaffold Thickness')
        self.inputScaffoldT.setFixedSize(inputWidth, inputHeight)
        self.inputScaffoldT.setValidator(digitValidator)
        labelScaffoldT.setBuddy(self.inputScaffoldT)

        #NEXT BUTTON
        self.buttonNextTo2 = QPushButton('&Next...')

        #-----------------------------------------
        # LAYOUT DEFINITION
        #-----------------------------------------

        #SAVE SETTINGS
        upperLayout = QHBoxLayout()
        upperLayout.addWidget(self.printSettings)
        upperLayout.addWidget(self.buttonSavePrintSet)
        upperLayout.addWidget(self.buttonDelPrintSet)
        upperLayout.addStretch()
        upperLayout.setSpacing(10)

        #MAX PRESSURE
        layoutPrintMaxP = QHBoxLayout()
        layoutPrintMaxP.addWidget(labelPrintMaxP)
        layoutPrintMaxP.addStretch()
        layoutPrintMaxP.addWidget(self.inputPrintMaxP)

        #PRINT SPEED
        layoutV = QHBoxLayout()
        layoutV.addWidget(labelV)
        layoutV.addStretch()
        layoutV.addWidget(self.inputV)

        #NOZZLE DIAMETER
        layoutD = QHBoxLayout()
        layoutD.addWidget(labelD)
        layoutD.addStretch()
        layoutD.addWidget(self.inputD)

        #PRINTER SETTINGS
        framePrinter = QGroupBox()
        layoutPrinter = QGridLayout()
        layoutPrinter.addLayout(layoutPrintMaxP,0,0)
        layoutPrinter.addLayout(layoutV,1,0)
        layoutPrinter.addLayout(layoutD,2,0)
        framePrinter.setLayout(layoutPrinter)
        framePrinter.setTitle('Printer Settings:')

        #SCAFFOLD HEIGHT
        layoutScaffoldH = QHBoxLayout()
        layoutScaffoldH.addWidget(labelScaffoldH)
        layoutScaffoldH.addStretch()
        layoutScaffoldH.addWidget(self.inputScaffoldH)

        #SCAFFOLD WIDTH
        layoutScaffoldW = QHBoxLayout()
        layoutScaffoldW.addWidget(labelScaffoldW)
        layoutScaffoldW.addStretch()
        layoutScaffoldW.addWidget(self.inputScaffoldW)

        #SCAFFOLD THICKNESS
        layoutScaffoldT = QHBoxLayout()
        layoutScaffoldT.addWidget(labelScaffoldT)
        layoutScaffoldT.addStretch()
        layoutScaffoldT.addWidget(self.inputScaffoldT)

        #SCAFFOLD SETTINGS
        frameScaffold = QGroupBox()
        layoutScaffold = QGridLayout()
        layoutScaffold.addLayout(layoutScaffoldH,0,0)
        layoutScaffold.addLayout(layoutScaffoldW,1,0)
        layoutScaffold.addLayout(layoutScaffoldT,2,0)
        frameScaffold.setLayout(layoutScaffold)
        frameScaffold.setTitle('Scaffold Dimensions:')

        #BUTTON LAYOUT
        layoutButton = QHBoxLayout()
        layoutButton.addStretch()
        layoutButton.addWidget(self.buttonNextTo2)		
        
        settingsLayout = QVBoxLayout()
        settingsLayout.addWidget(framePrinter)
        settingsLayout.addWidget(frameScaffold)
        settingsLayout.setSpacing(10)
        
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(upperLayout)
        mainLayout.addLayout(settingsLayout)
        mainLayout.addStretch()
        mainLayout.addLayout(layoutButton)

        self.setLayout(mainLayout)

        #-----------------------------------------
        # CONNECTIONS
        #-----------------------------------------

        self.buttonSavePrintSet.clicked.connect(lambda: guiSettings.save_dialog(self, self.pathToPrint))
        self.buttonDelPrintSet.clicked.connect(lambda: guiSettings.delete_settings(self, self.pathToPrint, self.printSettings.currentText()))
        self.printSettings.currentIndexChanged.connect(lambda: guiSettings.change_settings(self, self.pathToPrint, self.printSettings.currentText()))


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = FirstTab()
    w.show()
    sys.exit(app.exec_())