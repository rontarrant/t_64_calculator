import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QGraphicsDropShadowEffect

class MainWindow(QMainWindow):
	def __init__(self, parent=None):
		super().__init__(parent)

		self.shadow = QGraphicsDropShadowEffect()
		self.shadow.setBlurRadius(10)  # Adjust the blur radius as needed
		self.shadow.setXOffset(5)      # Adjust the X offset as needed
		self.shadow.setYOffset(5)      # Adjust the Y offset as needed

		self.button = QPushButton(self)
		self.button.setGraphicsEffect(self.shadow)

if __name__ == '__main__':
	app = QApplication()

	mainWindow = MainWindow()
	mainWindow.show()

	app.exec()
