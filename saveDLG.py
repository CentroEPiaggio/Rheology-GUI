from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class SaveConfDlg(QDialog):
	"""docstring for SaveConfDlg"""
	def __init__(self, currentText='', parent=None):
		super(SaveConfDlg, self).__init__(parent)

		self.currentText = currentText
		self.whichButton = 0

		self.setWindowTitle('Save to .INI')
		self.setFixedSize(200,80)

		self.okButton = QPushButton('Ok')
		self.cancelButton = QPushButton('Cancel')
		self.inputName = QLineEdit()
		self.inputName.setText(self.currentText)

		mainLayout = QGridLayout()
		mainLayout.addWidget(self.inputName,0,0,1,2)
		mainLayout.addWidget(self.okButton,1,0)
		mainLayout.addWidget(self.cancelButton,1,1)

		self.setLayout(mainLayout)

		self.okButton.clicked.connect(self.ok_clicked)
		self.cancelButton.clicked.connect(self.cancel_clicked)

	def ok_clicked(self):
		self.whichButton = 1
		self.close()

	def cancel_clicked(self):
		self.whichButton = 0
		self.close()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = SaveConfDlg()
    w.show()
    sys.exit(app.exec_())	