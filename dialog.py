from PySide6.QtWidgets import \
	(
		QDialog,
		QPushButton,
		QVBoxLayout,
		QLabel,
		QDialogButtonBox,
	)

class T64Dialog(QDialog):
	def __init__(self, parent):
		super().__init__(parent)
		
		self.setWindowTitle("About the T-64 Calculator")
		buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
		self.buttonBox = QDialogButtonBox(buttons)
		self.buttonBox.accepted.connect(self.accept)
		self.buttonBox.rejected.connect(self.reject)
		self.layout = QVBoxLayout()

		message = "Something happened, is that OK?"

		message_label = QLabel(message)
		self.layout.addWidget(message_label)
		self.layout.addWidget(self.buttonBox)
		self.setLayout(self.layout)
