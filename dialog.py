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
		buttons = QDialogButtonBox.Ok
		self.buttonBox = QDialogButtonBox(buttons)
		self.buttonBox.accepted.connect(self.accept)
		self.buttonBox.rejected.connect(self.reject)
		self.layout = QVBoxLayout()
		message = "<html><h2>T-64 Calculator</h2> \
This calculator is a companion utility for the VICE and X16 emulators.\
<h3>Special Features</h3>\
<h4>Shifting Left or Right</h4> \
After entering the first number&mdash;the number to shift&mdash;and \
clicking on a shift button, you can then enter the number of bit \
positions to shift by. Entering '1' or '2' would be sane, but \
anything higher than '7' will simply result in '0'. \
<h4>Base Conversions</h4>\
If you change the number base by clicking one of the base buttons\
&mdash;HEX, DEC, or BIN&mdash;any numbers already visible in the \
number fields will be converted to the new base.</html>"

		message_label = QLabel(message)
		self.resize(395, 400)
		message_label.setWordWrap(True)
		self.layout.addWidget(message_label)
		self.layout.addWidget(self.buttonBox)
		self.setLayout(self.layout)
