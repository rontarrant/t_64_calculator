from PySide6.QtWidgets import (
	QApplication,
	QWidget,
	QGridLayout,
	 QMainWindow,
	QVBoxLayout,
	QPushButton,
	QSizePolicy,
) 
from PySide6.QtGui import QPainter, QColor, QBrush, QPen, QFont
from PySide6.QtCore import Qt, QPoint, QRect, QSize
#from button_data import *
#from c64_palette import C64Palette

class ResizableButton(QPushButton):
	def __init__(self, text, initial_font_size = 12, parent = None):
		super().__init__(text, parent)
		self.initial_font_size = initial_font_size
		self.font_factor = 0.5  # Adjust this to control how much the font scales
		self._current_font_size = initial_font_size # Store the current font size
		self._first_resize = True  # New flag

		# Set the initial font
		font = self.font()
		font.setPointSize(self.initial_font_size)
		self.setFont(font)
		#print(f"Initial font size for '{text}': {self.initial_font_size}")

	def sizeHint(self):
		return QSize(100, 60)  # Reasonable default size

	def resizeEvent(self, event):
		super().resizeEvent(event)

		if self._first_resize:
			self._first_resize = False
		else:
			self.adjust_font_size()
		'''
		button_size = min(self.width(), self.height())
		font_size = max(button_size // 6, 8)  # Scale font, minimum size of 8
		font = self.font()
		font.setPointSize(font_size)
		self.setFont(font)
		'''

	def adjust_font_size(self):
		button_width = self.width()
		button_height = self.height()

		available_space = min(button_width, button_height)
		new_font_size = int(available_space * self.font_factor)
		
		if new_font_size < 6:
			new_font_size = 6

		if new_font_size != self._current_font_size:
			font = self.font()
			font.setPointSize(new_font_size)
			self.setFont(font)
			self._current_font_size = new_font_size

'''			
# Data to pass in:
	button_data (see example below)
	text_data (see example below)
'''
class AnalogButton(ResizableButton):
	def __init__(self, properties, parent=None):
		# Initialize with empty text - we'll handle text separately
		super().__init__("", properties.get("initial_font_size", 12), parent)
		self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

		self._is_pressed = False
		self._top_width = properties.get("width", 100) - 5
		self._top_height = properties.get("height", 50) - 5
		#self.setFixedSize(properties.get("width", 100), properties.get("height", 50))
		self._default_size = QSize(properties.get("width", 100), properties.get("height", 50))
		self._top_width = self._default_size.width() - 5
		self._top_height = self._default_size.height() - 5
		self.properties = properties
		self._is_active = properties.get("state", "active") == "active"
		self._active_palette = properties.get("palette", {})
		self._inactive_palette = properties.get("inactive_palette", self._active_palette)
		
		# Adjust font factor if needed
		self.font_factor = properties.get("font_factor", 0.5)

	def sizeHint(self):
		return self._default_size

	def resizeEvent(self, event):
		# Call ResizableButton's resizeEvent first
		super().resizeEvent(event)
		
		# Update our custom dimensions
		self._top_width = self.width() - 5
		self._top_height = self.height() - 5

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

	def set_active(self, is_active):
		if self._is_active != is_active:
			self._is_active = is_active
			self.update()

	def _get_palette(self):
		return self._inactive_palette if not self._is_active else self._active_palette

	def _get_color(self, key):
		palette = self._get_palette()
		return QColor(palette.get(key, "#000000")) # Default to black if key not found

	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)
		try:
			radius = 15
			button_rect = self.rect()
			
			# Calculate dynamic dimensions (95% of current size)
			top_width = button_rect.width() * 0.95
			top_height = button_rect.height() * 0.95
			
			# Create size and point objects correctly
			top_size = QSize(int(top_width), int(top_height))
			offset = QPoint(int(top_width), int(top_height))
			
			# Calculate rectangles
			shadow_rect = QRect(button_rect.bottomRight() - offset, top_size)
			top_rect = QRect(button_rect.topLeft() if not self._is_pressed else 
									button_rect.bottomRight() - offset, top_size)
			
			# Rest of your painting code...
			top_color = self._get_color("bg")
			outline_color = self._get_color("outline")
			shadow_color = QColor(0, 0, 0, 50)
			outline_width = self.properties.get("specs", {}).get("outline", 4)

			# Draw shadow
			painter.setPen(Qt.NoPen)
			painter.setBrush(QBrush(shadow_color))
			painter.drawRoundedRect(shadow_rect, radius, radius)

			# Draw top
			painter.setBrush(QBrush(top_color))
			painter.drawRoundedRect(top_rect, radius, radius)

			# Draw outline
			painter.setPen(QPen(outline_color, outline_width))
			painter.setBrush(Qt.NoBrush)
			area = outline_width // 2
			corner_r = radius - 2
			adjusted_outline = top_rect.adjusted(area, area, -area, -area)
			painter.drawRoundedRect(adjusted_outline, corner_r, corner_r)

			# Draw text
			if self.text():
					painter.setPen(QPen(self._get_color("text")))
					painter.drawText(button_rect, Qt.AlignCenter, self.text())
					
		finally:
			painter.end()  # Crucial - ensures painter is always properly ended

class OneLineButton(AnalogButton):
	def __init__(self, properties, parent=None):
		super().__init__(properties, parent)
		self._font_family = properties.get("specs", {}).get("font", "Arial Black")
		self._font_size = properties.get("specs", {}).get("font size", 32)
		self._text = properties.get("label", "")

	def _draw_centered_text(self, painter, rect, text, font_family, color):
		painter.setPen(color)
		font = self.font()  # Use the resizable font
		font.setFamily(font_family)
		
		# Scale font size based on button height
		font_size = max(8, int(rect.height() * 0.4))  # 40% of button height
		font.setPointSize(font_size)
		
		painter.setFont(font)
		painter.drawText(rect, Qt.AlignCenter, text)

	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)

		top_color = self._get_color("bg")
		outline_color = self._get_color("outline")
		text_color = self._get_color("font")

		radius = self.properties.get("specs", {}).get("radius", 15)
		button_area_rect = self.rect()
		top_size = QSize(self._top_width, self._top_height)
		shadow_rect = QRect(button_area_rect.bottomRight() - QPoint(self._top_width, self._top_height), top_size)
		top_rect = QRect(button_area_rect.topLeft() if not self._is_pressed else
						 button_area_rect.bottomRight() - QPoint(self._top_width, self._top_height), top_size)

		# Draw the shadow
		painter.setPen(Qt.NoPen)
		painter.setBrush(QBrush(QColor(0, 0, 0, 50)))
		painter.drawRoundedRect(shadow_rect, radius, radius)

		# Draw the top (background)
		painter.setBrush(QBrush(top_color))
		painter.drawRoundedRect(top_rect, radius, radius)

		# Draw the outline
		painter.setPen(QPen(outline_color, self.properties.get("specs", {}).get("outline_width", 4)))
		painter.setBrush(Qt.NoBrush)
		area = self.properties.get("specs", {}).get("outline_width", 4) // 2
		corner_r = radius - 2
		adjusted_outline = top_rect.adjusted(area, area, -area, -area)
		painter.drawRoundedRect(adjusted_outline, corner_r, corner_r)

		# Draw the text using the dedicated method
		self._draw_centered_text(painter, top_rect, self._text, self._font_family, self._font_size, text_color)

	def _draw_centered_text(self, painter, rect, text, font_family, font_size, color):
		painter.setPen(color)
		font = QFont(font_family, font_size)
		painter.setFont(font)
		metrics = painter.fontMetrics()
		text_rect = metrics.boundingRect(text)
		text_x = rect.center().x() - text_rect.width() / 2
		baseline_y = rect.center().y() + metrics.ascent() / 2 - 10 # Subtract 10 to move up
		painter.drawText(int(text_x), int(baseline_y), text)

class TwoLineButton(AnalogButton):
	def __init__(self, properties, parent = None):
		super().__init__(properties, parent)
		self._font_family_line1 = properties.get("specs", {}).get("font", "Arial Black") # Correct key for font family
		self._font_size_line1 = properties.get("specs", {}).get("font size", 32)   # Correct key for font size
		self._text_line1 = properties.get("label", "")
		self._color_line1 = QColor(properties.get("palette", {}).get("font", "#000000"))

		self._font_family_line2 = properties.get("specs", {}).get("font", "Arial Black")
		self._font_size_line2 = properties.get("specs", {}).get("subfont size", 14)
		self._text_line2 = properties.get("sublabel", "")

	def _draw_centered_text(self, painter, rect, text, font_family, color):
		painter.setPen(color)
		font = self.font()  # Use the resizable font
		font.setFamily(font_family)
		painter.setFont(font)
		painter.drawText(rect, Qt.AlignCenter, text)

	def paintEvent(self, event):
		super().paintEvent(event) # Draw the base button (shadow, top, outline)

		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)

		# Determine the current top_rect position
		button_area_rect = self.rect()
		top_size = QSize(self._top_width, self._top_height)
		top_rect = QRect(button_area_rect.topLeft() if not self._is_pressed else
						 button_area_rect.bottomRight() - QPoint(self._top_width, self._top_height), top_size)

		# Draw the two lines of text relative to the current top_rect
		# Font for the first line
		font_line1 = QFont(self._font_family_line1, self._font_size_line1)
		painter.setFont(font_line1)
		metrics_line1 = painter.fontMetrics()
		text_rect_line1 = metrics_line1.boundingRect(self._text_line1)
		text_x_line1 = top_rect.center().x() - text_rect_line1.width() / 2
		line1_baseline_y = top_rect.top() + (top_rect.height() / 2 + 5)
		painter.setPen(self._color_line1)
		painter.drawText(int(text_x_line1), int(line1_baseline_y), self._text_line1)

		# Font for the second line
		font_line2 = QFont(self._font_family_line2, self._font_size_line2)
		painter.setFont(font_line2)
		metrics_line2 = painter.fontMetrics()
		text_rect_line2 = metrics_line2.boundingRect(self._text_line2)
		text_x_line2 = top_rect.center().x() - text_rect_line2.width() / 2
		line2_baseline_y = top_rect.bottom() - (top_rect.height() / 4 - 5)
		painter.setPen(self._color_line1)
		painter.drawText(int(text_x_line2), int(line2_baseline_y), self._text_line2)

class AngledButton(OneLineButton):
	def __init__(self, properties, parent = None):
		super().__init__(properties, parent)
		self._angle = properties.get("specs", {}).get("angle", 0)
		self._color = QColor(properties.get("palette", {}).get("font", "#000000"))
		self._text_color = QColor(properties.get("palette", {}).get("font", "#000000"))

	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)

		top_color = QColor(self.properties.get("palette", {}).get("bg", "#FFFFFF"))
		outline_color = QColor(self.properties.get("palette", {}).get("outline", "#000000"))
		text_color = self._color # Inherited from AngledButton

		radius = 15
		button_area_rect = self.rect()
		top_size = QSize(self._top_width, self._top_height)
		shadow_rect = QRect(button_area_rect.bottomRight() - QPoint(self._top_width, self._top_height), top_size)
		top_rect = QRect(button_area_rect.topLeft() if not self._is_pressed else
						 button_area_rect.bottomRight() - QPoint(self._top_width, self._top_height), top_size)

		# Draw the shadow
		painter.setPen(Qt.NoPen)
		painter.setBrush(QBrush(QColor(0, 0, 0, 50)))
		painter.drawRoundedRect(shadow_rect, radius, radius)

		# Draw the top (background)
		painter.setBrush(QBrush(top_color))
		painter.drawRoundedRect(top_rect, radius, radius)

		# Draw the outline
		painter.setPen(QPen(outline_color, self.properties.get("specs", {}).get("outline_width", 4)))
		painter.setBrush(Qt.NoBrush)
		area = self.properties.get("specs", {}).get("outline_width", 4) // 2
		corner_r = radius - 2
		adjusted_outline = top_rect.adjusted(area, area, -area, -area)
		painter.drawRoundedRect(adjusted_outline, corner_r, corner_r)

		# Draw the angled text (logic from AngledButton's paintEvent should still apply)
		painter.setPen(text_color)
		font = QFont(self._font_family, self._font_size) # Inherited from AngledButton
		painter.setFont(font)
		metrics = painter.fontMetrics()
		text_rect = metrics.boundingRect(self._text) # Inherited from AngledButton

		angle = self.properties.get("specs", {}).get("angle", 0)
		painter.translate(top_rect.center())
		painter.rotate(angle)
		painter.translate(-top_rect.center())
		painter.drawText(top_rect.center() - text_rect.center(), self._text)
