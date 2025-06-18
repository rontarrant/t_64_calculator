# line_edit_colour_label.py
import sys

from PySide6.QtWidgets import (
	QApplication,
	QMainWindow,
	QWidget,
	QGridLayout,
	QLabel,
	QSizePolicy,
	QLabel,
) 
from PySide6.QtGui import (
	QPainter,
	QColor,
	QPen,
	QFont,
	QPainterPath,
	QKeyEvent,
)
from PySide6.QtCore import (
	Qt,
	QRect,
	QRectF,
	QPointF,
	Signal,
	QSize)

from button_specs import lineedit_properties

class ResizableLabel(QLabel):
	def __init__(self, properties, text, parent = None):
		super().__init__(text, parent)
		self.properties = properties
		self._default_size = QSize(self.properties["width"], self.properties["height"])
		self.font_size = self.properties["font_size"]
		self.font_factor = self.properties["font_factor"]  # Adjust this to control how much the font scales
		self._current_font_size = self.font_size  # Store the current font size
		self._first_resize = True  # New flag

		# Set the initial font
		font = self.font()
		font.setPointSize(self.font_size)
		self.setFont(font)

	def sizeHint(self):
		return self._default_size  # Reasonable default size

	def resizeEvent(self, event):
		super().resizeEvent(event)
		print(f"ResizableLabel: resizeEvent - New size: {self.width()}x{self.height()}")

		if self._first_resize:
			self._first_resize = False
		else:
			self.adjust_font_size()

	def adjust_font_size(self):
		label_width = self.width()
		label_height = self.height()

		available_space = min(label_width, label_height)
		new_font_size = int(available_space * self.font_factor)

		if new_font_size < 6:
			new_font_size = 6

		print(f"ResizableLabel: adjust_font_size - Available space: {available_space}, New font size: {new_font_size}, Current font size: {self._current_font_size}")

		if new_font_size != self._current_font_size:
			font = self.font()
			font.setPointSize(new_font_size)
			self.setFont(font)
			self._current_font_size = new_font_size

class LineEditColourLabel(ResizableLabel):
	clicked = Signal()

	def __init__(self, properties, text="", parent=None):
		super().__init__(properties, text, parent)

		# Initialize custom drawing properties
		self.outline_color = properties["palette"]["outline"]
		self.text_color = properties["palette"]["text"]
		self.background_color = properties["palette"]["bg"]
		self.outline_width = properties["specs"]["outline"]
		self.corner_radius = properties["radius"]
		self.label_width = properties["width"]
		self.label_height = properties["height"]
		self.setContentsMargins(8, 0, 16, 0)

		# Initialize line edit specific properties
		self.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
		self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) # Allow vertical expansion
		# self.setFixedHeight(self.label_height) # Remove the fixed height
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
		#self.adjust_font_size()

		# 1. Get parent background (with fallback)
		parent_bg = self.parent().palette().window().color() if self.parent() else Qt.gray

		# 2. Paint full widget with parent background
		painter.fillRect(self.rect(), parent_bg)

		# 3. Create main content area (accounting for outline)
		content_rect = QRectF(
			self.outline_width/2,
			self.outline_width/2,
			self.width() - self.outline_width,
			self.height() - self.outline_width
		)

		# 4. Draw rounded background
		bg_path = QPainterPath()
		bg_path.addRoundedRect(content_rect, self.corner_radius, self.corner_radius)
		painter.fillPath(bg_path, self.background_color)

		# 5. Draw perfect outline
		outline_path = QPainterPath()
		outline_path.addRoundedRect(content_rect, self.corner_radius, self.corner_radius)

		pen = QPen(self.outline_color, self.outline_width)
		pen.setJoinStyle(Qt.RoundJoin)
		painter.setPen(pen)
		painter.drawPath(outline_path)

		'''
		# 6. Draw text with proper alignment
		text_rect = QRectF(
			self.contentsMargins().left(),
			0,
			self.width() - self.contentsMargins().right() - 8,  # Right padding
			self.height()
		)
		'''
		text_rect = QRectF(
			self.contentsMargins().left(),
			0,
			self.width() - self.contentsMargins().left() - self.contentsMargins().right(),
			self.height()
		)
		
		painter.setPen(self.text_color)
		current_font = self.font()
		print(f"LineEditColourLabel: paintEvent - Drawing with font size: {current_font.pointSize()}")
		painter.setFont(current_font)
		painter.drawText(text_rect, Qt.AlignRight | Qt.AlignVCenter, self.text())

		painter.end()

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
			self.adjust_font_size() # Adjust font based on new size
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

	label1 = LineEditColourLabel(lineedit_properties, "")
	layout.addWidget(label1, 0, 0)

	label2 = LineEditColourLabel(lineedit_properties, "")
	layout.addWidget(label2, 1, 0)

	window.show()
	sys.exit(app.exec())