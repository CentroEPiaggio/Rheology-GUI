from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class ErrorDlg(QDialog):

	def __init__(self, displayText, parent=None):
		super(ErrorDlg, self).__init__(parent)

		self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)
		self.setWindowTitle('Error!')
		#self.setWindowIcon(QIcon(':/warning.png'))

		label = QLabel(displayText)
		okButton = QPushButton('Ok')

		layoutLabel = QHBoxLayout()
		layoutLabel.addStretch()
		layoutLabel.addWidget(label)
		layoutLabel.addStretch()

		layoutButton = QHBoxLayout()
		layoutButton.addStretch()
		layoutButton.addWidget(okButton)
		layoutButton.addStretch()

		mainLayout = QGridLayout()
		mainLayout.addLayout(layoutLabel,0,0)
		mainLayout.addLayout(layoutButton,1,0)

		self.setLayout(mainLayout)

		okButton.clicked.connect(lambda: self.close())


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = ErrorDlg()
    w.show()
    sys.exit(app.exec_())	