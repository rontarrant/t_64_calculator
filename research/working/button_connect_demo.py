import sys

from PySide6.QtWidgets import (
	QApplication,
	QMainWindow,
	QPushButton,
)

class MyButton(QPushButton):
	def __init__(self, text):
		super().__init__(text)
		self.is_checked = False
		self.setChecked(self.is_checked)
		self.clicked.connect(self.do_something)
		self.pressed.connect(self.button_pressed)
		self.clicked.connect(self.toggle_something)
		self.released.connect(self.button_released) 

	def do_something(self):
		print("Doing Something...")

	def toggle_something(self, is_checked):
		if self.is_checked == True:
			self.is_checked = False
		else:
			self.is_checked = True

		print("Checked?", self.is_checked)

	def button_released(self):
		print("Button released")

	def button_pressed(self):
		print("Button pressed")


class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		self.setWindowTitle("T-64 Calculator")

		button = MyButton("Sample")

		self.setCentralWidget(button)

	
if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	app.exec()
