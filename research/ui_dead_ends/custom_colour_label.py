from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QPainterPath
from PySide6.QtCore import Qt, QRect

class CustomColourLabel(QLabel):
	def __init__(self, text, width, height, corner_radius, parent=None):
		super().__init__(text, parent)
		self.outline_color = QColor("#880000")
		self.text_color = QColor("#FF7777")
		self.background_color = QColor("#AAFFEE")
		self.outline_width = 4
		self.font_size = 30  # Default font size
		self.label_width = width
		self.label_height = height
		self.corner_radius = corner_radius

		self.setFixedSize(self.label_width, self.label_height)

	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)

		# 1. Create a rounded rectangle path
		path = QPainterPath()
		rect = QRect(0, 0, self.width(), self.height())
		path.addRoundedRect(rect, self.corner_radius, self.corner_radius)

		# 2. Draw the background with rounded corners
		painter.fillPath(path, self.background_color)

		# 3. Draw the outline with rounded corners
		pen = QPen(self.outline_color, self.outline_width)
		painter.setPen(pen)
		painter.drawPath(path)

		# 4. Draw the text, ensuring it's within the rounded rectangle
		font = QFont()
		font.setPointSize(self.font_size)
		painter.setFont(font)
		painter.setPen(self.text_color)
		painter.drawText(rect, Qt.AlignCenter, self.text())

		painter.end()

	def set_font_size(self, size):
		if size > 0:
			self.font_size = size
			self.update()

	def set_label_size(self, width, height):
		if width > 0 and height > 0:
			self.label_width = width
			self.label_height = height
			self.setFixedSize(self.label_width, self.label_height)
			self.update()

	def set_corner_radius(self, radius):
		if radius >= 0:
			self.corner_radius = radius
			self.update()

if __name__ == '__main__':
	app = QApplication([])
	label = CustomColourLabel("Rounded Label", 300, 80, 15)
	label.show()
	'''
	# Example of changing properties after creation
	label.set_font_size(20)
	label.set_label_size(250, 80)
	label.set_corner_radius(25)
	'''
	app.exec()
