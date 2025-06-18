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
	def __init__(self, text, toggle_buttons):
		super().__init__(text)
		self.clicked.connect(self.toggle_something)

		self.toggle_buttons = []

		for toggle_button in toggle_buttons:
			self.toggle_buttons.append(toggle_button)

	def toggle_something(self):
		if self.toggle_buttons[0].isEnabled() == True:
			for button in self.toggle_buttons:
				button.setEnabled(False)
			print(button, " disabled")
		else:
			for button in self.toggle_buttons:
				button.setEnabled(True)
				print(button, " enabled")


class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		self.setWindowTitle("T-64 Calculator")

		toggle_button1 = ToggleButton("Toggle On/Off")
		toggle_button2 = ToggleButton("Toggle On/Off")
		
		toggler = PushButton("Toggler", [toggle_button1, toggle_button2])
			
		layout = QHBoxLayout()
		layout_widget = QWidget()
		layout_widget.setLayout(layout)
		layout.addWidget(toggler)
		layout.addWidget(toggle_button1)
		layout.addWidget(toggle_button2)
		
		self.setCentralWidget(layout_widget)

	
if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	app.exec()
