import sys

from PySide6.QtWidgets import (
	QApplication,
	QMainWindow,
	QWidget,
	QPushButton,
	QHBoxLayout
)

class ToggleButton(QPushButton):
	def __init__(self, text):
		super().__init__(text)
		self.is_checked = False
		self.setChecked(self.is_checked)
		self.clicked.connect(self.do_something)

	def do_something(self):
		print("Doing Something...")


class PushButton(QPushButton):
	def __init__(self, text, toggle_button):
		super().__init__(text)
		self.clicked.connect(self.toggle_something)
		self.toggle_button = toggle_button
		

	def toggle_something(self):
		if self.toggle_button.isEnabled() == True:
			self.toggle_button.setEnabled(False)
			print("Button Disabled")
		else:
			self.toggle_button.setEnabled(True)
			print("Button Enabled")


class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		self.setWindowTitle("T-64 Calculator")

		toggle_button = ToggleButton("Toggle On/Off")

		toggler = PushButton("Toggler", toggle_button)
			
		layout = QHBoxLayout()
		layout_widget = QWidget()
		layout_widget.setLayout(layout)
		layout.addWidget(toggler)
		layout.addWidget(toggle_button)
		self.setCentralWidget(layout_widget)

	
if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	app.exec()
