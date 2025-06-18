# line_edit_colour_label.py
import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QLabel, QSizePolicy
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QPainterPath, QKeyEvent
from PySide6.QtCore import Qt, QRect, QRectF, QPointF, Signal

class LineEditColourLabel(QLabel):
	clicked = Signal()

	def __init__(self, text="", width = 200, height = 40, corner_radius = 4,
				 outline_color="#880000", text_color="#FF7777",
				 background_color="#AAFFEE", outline_width = 4, font_size = 12):
		super().__init__(text)
		# Initialize custom drawing properties
		self.outline_color = QColor(outline_color)
		self.text_color = QColor(text_color)
		self.background_color = QColor(background_color)
		self.outline_width = outline_width
		self.font_size = font_size
		self.corner_radius = corner_radius
		self.label_width = width
		self.label_height = height
		self.setContentsMargins(8, 0, 16, 0)

		# Initialize line edit specific properties
		self.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
		self.setSizePolicy(self.sizePolicy().horizontalPolicy(), QSizePolicy.Fixed)
		self.setFixedHeight(height)
		self.setCursor(Qt.CursorShape.IBeamCursor)
		self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
		self.setFocus()
		self._update_stylesheet()

	def _update_stylesheet(self):
		self.setStyleSheet(f"""
			background-color: transparent; /* Let paintEvent handle background */
			border: none; /* Let paintEvent handle border */
			padding: 2px;
		""")

	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)

		# Calculate inset for outline
		inset = self.outline_width / 2
		rect = QRectF(inset, inset, 
					self.width() - self.outline_width,
					self.height() - self.outline_width)

		# Create rounded rectangle path
		path = QPainterPath()
		path.addRoundedRect(rect, self.corner_radius, self.corner_radius)

		# Draw background
		painter.fillPath(path, self.background_color)

		# Draw outline
		pen = QPen(self.outline_color, self.outline_width)
		pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
		painter.setPen(pen)
		painter.drawPath(path)

		# Draw right-aligned text with padding
		text_rect = QRectF(rect)
		font = QFont()
		font.setPointSize(self.font_size)
		painter.setFont(font)
		painter.setPen(self.text_color)
		
		# Right-align with 8px padding from edge
		text_flags = Qt.AlignRight | Qt.AlignVCenter
		painter.drawText(text_rect.adjusted(0, 0, -8, 0),  # Right padding
						text_flags, 
						self.text())

	def keyPressEvent(self, event: QKeyEvent):
		if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
			self.clearFocus()
		elif event.key() == Qt.Key.Key_Backspace:
			self.setText(self.text()[:-1])
		else:
			self.setText(self.text() + event.text())

	def mousePressEvent(self, event):
		self.setFocus()

	# Setter methods
	def set_outline_color(self, color):
		if isinstance(color, QColor):
			self.outline_color = color
			self.update()

	def set_text_color(self, color):
		if isinstance(color, QColor):
			self.text_color = color
			self.update()

	def set_background_color(self, color):
		if isinstance(color, QColor):
			self.background_color = color
			self.update()

	def set_outline_width(self, width):
		if width >= 0:
			self.outline_width = width
			self.update()

	def set_font_size(self, size):
		if size > 0:
			self.font_size = size
			self.update()

	def set_corner_radius(self, radius):
		if radius >= 0:
			self.corner_radius = radius
			self.update()

	def setFixedSize(self, width, height):
		super().setFixedSize(width, height)
		self.label_width = width
		self.label_height = height
		self.update()

	def setFixedWidth(self, width):
		super().setFixedWidth(width)
		self.label_width = width
		self.update()

	def setFixedHeight(self, height):
		super().setFixedHeight(height)
		self.label_height = height
		self.update()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = QMainWindow()
	window.setWindowTitle("LineEditColourLabel Demo (Single Class)")
	central_widget = QWidget()
	window.setCentralWidget(central_widget)
	layout = QGridLayout(central_widget)

	label1 = LineEditColourLabel("", 200, 40, 10)
	layout.addWidget(label1, 0, 0)

	label2 = LineEditColourLabel("", 250, 50, 15,
								 background_color = "#f0fff0",
								 outline_color = "#008000",
								 text_color = "#228b22",
								 outline_width = 2,
								 font_size = 16)
	layout.addWidget(label2, 1, 0)

	window.show()
	sys.exit(app.exec())