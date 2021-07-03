from os import remove, listdir, path

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import saveDLG
import errorDLG

def extract_widget(obj):
    # Define a list of widgets:
    widgets = []
    # Loop over the widgets:
    for widget in obj.children():
        if isinstance(widget, QLineEdit) or isinstance(widget, QRadioButton) or isinstance(widget, QCheckBox):
            widgets.append(widget)
        elif isinstance(widget, QGroupBox):
            for widgetInGroup in widget.children():
                if isinstance(widgetInGroup, QLineEdit) or isinstance(widgetInGroup, QRadioButton) or isinstance(widgetInGroup, QCheckBox):
                    widgets.append(widgetInGroup)

    return widgets

def empty_tab(obj):
    # Get a list of all widgets in tab:
    widgets = extract_widget(obj)
    # and iterate over them to clean:
    for widget in widgets:
        if isinstance(widget, QLineEdit):
            widget.setText('')
        elif isinstance(widget, QRadioButton):
            widget.setChecked(False)

def save_dialog(obj, pathToSettings):
    # Open up the save dialog:
    saveDialog = saveDLG.SaveConfDlg()
    saveDialog.exec_()

    # Get the confName, and also check if it is valid or not:
    confName = saveDialog.inputName.text()
    if saveDialog.whichButton == 1 and confName != '':
        comboBox = obj.findChild(QComboBox)
        # Add the new conf to the combo box if new name:
        if comboBox.findText(confName) < 0:
            comboBox.blockSignals(True)
            comboBox.addItem(confName)
            comboBox.model().sort(0)
            comboBox.setCurrentIndex(comboBox.findText(confName))
            comboBox.blockSignals(False)

        # Do the actual saving:
        save_settings(obj, pathToSettings, confName)

def quick_save(obj, pathToSettings):
    #Get the current confName; if it does not exist save in default:
    comboBox = obj.findChild(QComboBox)
    if comboBox == None:
        return
    
    confName = comboBox.currentText()
    if confName == '':
        confName = 'default'
    #Do the saving and return:
    save_settings(obj, pathToSettings, confName)

def save_settings(obj, pathToSettings, confName):
    # Open up the ini file:
    settings = QSettings(pathToSettings+confName+'.ini', QSettings.IniFormat)
    # and clear it:
    settings.clear()
    # Extract the widgets:
    widgets = extract_widget(obj)
    # and save:
    for widget in widgets:
        if isinstance(widget, QLineEdit) and widget.isEnabled():
            name = widget.objectName()
            value = widget.text()
            settings.setValue(name, value)
        elif isinstance(widget, QRadioButton) and widget.isChecked():
            name = widget.objectName()
            value = widget.isChecked()
            settings.setValue(name, value)
        elif isinstance(widget, QCheckBox) and widget.isChecked():
            name = widget.objectName()
            value = widget.isChecked()
            settings.setValue(name, value)

def delete_settings(obj, pathToSettings, confName):
    # Find the combobox:
    comboBox = obj.findChild(QComboBox)
    # Delete conf only if the combo box has elements and the name is != default:
    if confName != 'default' and comboBox.count() >= 1:
        # Do the removing:
        remove(pathToSettings+confName+'.ini')        
        comboBox.removeItem(comboBox.findText(confName))

def change_settings(obj, pathToSettings, confName):
    # Open up the settings:
    settings = QSettings(pathToSettings+confName+'.ini', QSettings.IniFormat)
    # Get all properties:
    properties = settings.allKeys()
    # Extract the widget list:
    widgets = extract_widget(obj)
    # and create a supporting list with only names:
    widgetNames = [x.objectName() for x in widgets]
    # Iterate over them and set:
    for wn in widgetNames:
        # Get a pointer to the actual widget:
        widget = obj.findChild(QObject, wn)
        if wn in properties:
            # Extract the value:
            value = settings.value(wn)
            if isinstance(widget, QLineEdit):
                widget.setText(value)
            elif isinstance(widget, QRadioButton) or isinstance(widget, QCheckBox):
                widget.setChecked(True)
        else:
            if isinstance(widget, QLineEdit):
                widget.setText('')
            elif isinstance(widget, QRadioButton) or isinstance(widget, QCheckBox):
                widget.setChecked(False)

def unpack_conf(pathToSettings, confName):
    #Open up the settings:
    settings = QSettings(pathToSettings+confName+'.ini', QSettings.IniFormat)
    #Get all properties:
    properties = settings.allKeys()
    #Define a dictionary to store the settings:
    dictSettings = {k:settings.value(k) for k in properties}
    return dictSettings

def unpack_settings(obj):
    #Extract widgets from current object:
    widgets = extract_widget(obj)
    #Iterate over them, and give a list of pairs name-values:
    settings = []
    for widget in widgets:
        if isinstance(widget, QLineEdit) and widget.isEnabled():
            name = widget.objectName()
            value = widget.text()
            settings.append((name, value))
        elif isinstance(widget, QRadioButton) and widget.isChecked():
            name = widget.objectName()
            value = widget.isChecked()
            settings.append((name, value))
        elif isinstance(widget, QCheckBox) and widget.isChecked():
            name = widget.objectName()
            value = widget.isChecked()
            settings.append((name, value))
    
    return settings

def load_gui_state(obj, pathToRestore, pathToSettings, conf):
    #N.B: since the conf folder initialization and checks are done in the main window __init__
    #there will be always restoreSettings and default files
    
    #Load previous session values:
    previousSettings = QSettings(pathToRestore+'restoreSettings.ini', QSettings.IniFormat)
    #and extract the name of the last conf:
    confName = previousSettings.value(conf)
    if confName == '' or confName == None:
        confName = 'default'
        
    #Extract all names in settings folder:
    confFiles = listdir(pathToSettings)  
    confNames = [x.split('.')[0] for x in confFiles]
    #and check if the conf file exists:
    if confName not in confNames:
        raise NoConfException

    #Populate the combobox:
    obj.addItems(confNames)
    obj.setCurrentIndex(obj.findText(confName))

def tab_checks(obj):
    #Given a tab, extract all line edits and check them:
    widgetList = extract_widget(obj)
    for widget in widgetList:
        if isinstance(widget, QLineEdit) and widget.isEnabled():
            if input_checks(widget):
                return True

def input_checks(obj):
    #Function to check if string is int or float and do the conversion:
    def num(value):
        try:
            return int(value)
        except ValueError:
            return float(value)
    
    #Given an input, we want to check if the input is empty, or it is the limits. Define the limits:
    limDict = {
        'P_max': [0, 1E9],
        'Scaffold Thickness': [0, 100],
        'Scaffold Width': [0, 100],
        'Scaffold Height': [0, 100],
        'eta': [1, 1000],
        'FlowIndex': [0.01, 1],
        'K': [1, 1000],
        'tau_y': [1, 1000],
        'rho': [500, 5000],
        'E': [1, 1e9],
        'eta_0': [1, 1e9],
        'D': [0.05, 0.5],
        'LH': [0.01, 100],
        'EM': [0, 100],
        'LW': [0.01, 100],
        'Infill': [0, 1],
        'V': [0.00001, 100],
        'D': [0.01, 100]
    }
    #Get the input name:
    name = obj.objectName()
    #and its value:
    value = obj.text()
    #and do the checking:
    if name in limDict:
        if value == '' or num(value) <= limDict[name][0] or num(value) >= limDict[name][1]:
            errorDial = errorDLG.ErrorDlg(name+' is out range/empty')
            errorDial.exec_()
            return True

class NoRestoreException(Exception):
    def __init__(self):
        self.message = 'No Restore file in directory'
        super().__init__(self.message)

class NoConfException(Exception):
    def __init__(self):
        self.message = 'The Specified configuration does not exist'
        super().__init__(self.message)


if __name__ == "__main__":
    pass
