from PySide6.QtWidgets import QApplication, QPushButton, QMainWindow, QWidget, QVBoxLayout
from PySide6.QtCore import Qt, QPoint, QRect, QSize
from PySide6.QtGui import QPainter, QColor, QBrush, QPen, QFont

class AnalogLookButton(QPushButton):
	def __init__(self, button_data, parent = None):
		super().__init__(button_data["text"], parent)
		self._is_pressed = False
		self._top_width = button_data["width"] - 5
		self._top_height = button_data["height"] - 5
		self.setFixedSize(button_data["width"], button_data["height"])
		self._font_family = button_data["font"]
		self._font_size = button_data["font_size"]
		self.button_data = button_data

	def mousePressEvent(self, event):
		if event.button() == Qt.LeftButton:
			self._is_pressed = True
			self.update()
		super().mousePressEvent(event)

	def mouseReleaseEvent(self, event):
		if event.button() == Qt.LeftButton:
			self._is_pressed = False
			self.update()
		super().mouseReleaseEvent(event)

	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)
		radius = 15

		top_color = self.button_data["top_color"] # light blue
		shadow_color = self.button_data["shadow_color"] # 80% black
		outline_color = self.button_data["outline_color"] # dark blue
		outline_width = 4 # width of the button top outline
		text_color = QColor("#0055D4") # text color same as outline

		font = QFont(self._font_family, self._font_size)
		font.setBold(True)
		painter.setFont(font)

		# Define rectangles based on the button area
		button_area_rect = self.rect()
		top_size = QSize(self._top_width, self._top_height)

		# Shadow should be in the initial 'covered' position
		shadow_rect = QRect(button_area_rect.bottomRight()
							- QPoint(self._top_width, self._top_height), top_size)

		# Button top's position depends on the pressed state
		if not self._is_pressed:
			top_rect = QRect(button_area_rect.topLeft(), top_size)
		else:
			top_rect = QRect(button_area_rect.bottomRight()
							 - QPoint(self._top_width, self._top_height), top_size)

		# Draw the drop shadow
		painter.setPen(Qt.NoPen)
		painter.setBrush(QBrush(shadow_color))
		painter.drawRoundedRect(shadow_rect, radius, radius)

		# Don't draw the button area. (Code deleted)

		# Draw the button top (fill first)
		painter.setPen(Qt.NoPen) # QPen draws the outline
		painter.setBrush(QBrush(top_color)) # QBrush draws the fill
		painter.drawRoundedRect(top_rect, radius, radius)

		# Draw the brown outline INSIDE the button top
		painter.setPen(QPen(outline_color, outline_width))
		painter.setBrush(Qt.NoBrush) # Important: Don't fill the outline
		area = outline_width // 2 # shrink the area of the outline
		corner_r = radius - 2 # radius of the rectangle corners
		adjusted_outline = top_rect.adjusted(area, area, -area, -area)
		painter.drawRoundedRect(adjusted_outline, corner_r, corner_r)

		# Because we're drawing a custom button top, we also have to 
		# draw the text ourselves with the font defined above.
		painter.setPen(text_color)
		painter.drawText(top_rect, Qt.AlignCenter, self.text())

if __name__ == '__main__':
	class MainWindow(QMainWindow):
		def __init__(self):
			super().__init__()
			self.setWindowTitle("Shifting Top Button Example")
			central_widget = QWidget()
			layout = QVBoxLayout(central_widget)

			# All data having to do with the button size, font, text,
			# etc. is defined here and passed in, making AnalogLookButton
			# as flexible as possible.
			button_data = {
				"text": "Click me!",
				"font": "Arial",
				"font_size": 20,
				"width": 160,
				"height": 100,
				"top_color": QColor("#AAEEFF"), # button top: light blue
				"shadow_color": QColor(0, 0, 0, 80), # black, 80% transparency
				"outline_color": QColor("#0055D4"), # button top outline: dark blue
				"outline_width": 4, # width of the button top outline
				"text_color": QColor("#0055D4") # text color same as outline
			}

			analog_look_button = AnalogLookButton(button_data)
			layout.addWidget(analog_look_button)
			layout.setAlignment(Qt.AlignCenter)

			central_widget.setLayout(layout)
			self.setCentralWidget(central_widget)
			self.resize(300, 200)
			self.show()

	app = QApplication([])
	window = MainWindow()
	app.exec()
