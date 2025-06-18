import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

class ButtonGenerator(QWidget):
	def __init__(self, data):
		super().__init__()
		self.data = data
		self.buttons = {}
		self.init_ui()

	def init_ui(self):
		layout = QVBoxLayout()

		for key, value in self.data.items():
			button = QPushButton(key)
			button.clicked.connect(lambda v = value: self.button_click(v)) #using lambda to avoid late binding issues.
			layout.addWidget(button)
			self.buttons[key] = button #Store the button object.

		self.setLayout(layout)

	def button_click(self, value):
		print(f"Button clicked, value: {value}")

if __name__ == "__main__":
	app = QApplication(sys.argv)
	button_data = {"Red": "Color 1", "Blue": "Color 2", "Green": "Color 3"}
	generator = ButtonGenerator(button_data)
	generator.show()
	app.exec()

'''
Explanation:

	Imports:
		We import QApplication, QWidget, QPushButton, and QVBoxLayout from PySide6.QtWidgets.
	QWidget Inheritance:
		The ButtonGenerator class now inherits from QWidget, which is the base class for all widgets in PySide6.
	init_ui Method:
		Instead of directly creating buttons in the __init__ method, we create a separate init_ui method to handle
		UI initialization. This is a common practice in PySide6.
		We create a QVBoxLayout to arrange the buttons vertically.
		button.clicked.connect(): this is how we connect a signal (the button click) to a slot (our button_click method).
		layout.addWidget(button): This adds the button to the layout.
		self.setLayout(layout): This sets the layout for the ButtonGenerator widget.
	Application Execution:
		app = QApplication(sys.argv): Creates a PySide6 application object.
		generator.show(): Displays the ButtonGenerator widget.
		sys.exit(app.exec()): Starts the PySide6 event loop, which handles user interactions.
	Lambda for clicked.connect:
		Just like in Tkinter, we use a lambda function to pass the button's value to the button_click method while avoiding late binding issues.
	Storing Buttons:
		The self.buttons dictionary stores the button objects. This allows them to be accessed later.
'''