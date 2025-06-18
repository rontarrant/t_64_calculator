from PySide6.QtWidgets import (
	QApplication,
	QMainWindow,
	QLabel,
	QLineEdit,
	QVBoxLayout,
	QWidget,
)

import sys

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		self.setWindowTitle("My App")

		# The QLabel.setText() Slot accepts a string argument.
		self.label = QLabel()

		self.input = QLineEdit()

		# The QLineEdit.textChanged Signal emits a string.
		# Note that we leave out the brackets for setText so
		# we don't call the method as we're hooking it up.
		self.input.textChanged.connect(self.label.setText)

		layout = QVBoxLayout()
		layout.addWidget(self.input)
		layout.addWidget(self.label)

		container = QWidget()
		container.setLayout(layout)

		# Set the central widget of the Window.
		self.setCentralWidget(container)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
