from PySide6.QtWidgets import (
	QApplication,
	QWidget,
	 QGridLayout,
	  QMainWindow,
		QVBoxLayout,
		QPushButton,
) 
from PySide6.QtGui import QPainter, QColor, QBrush, QPen, QFont
from PySide6.QtCore import Qt, QPoint, QRect, QSize
#from button_data import *
from c64_palette import C64Palette

class AnalogButton(QPushButton):
	def __init__(self, properties, parent = None):
		super().__init__("", parent)
		self._is_pressed = False
		self._top_width = properties.get("width", 100) - 5
		self._top_height = properties.get("height", 50) - 5
		self.setFixedSize(properties.get("width", 100), properties.get("height", 50))
		self.properties = properties  # Store the entire properties dictionary
		self._is_active = properties.get("state", "active") == "active"
		self._active_palette = properties.get("palette", {})
		self._inactive_palette = properties.get("inactive_palette", self._active_palette)

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
		radius = 15

		top_color = self._get_color("bg")
		outline_color = self._get_color("outline")
		shadow_color = QColor(0, 0, 0, 50)
		outline_width = self.properties.get("specs", {}).get("outline", 4)

		# Define rectangles
		button_area_rect = self.rect()
		top_size = QSize(self._top_width, self._top_height)
		shadow_rect = QRect(button_area_rect.bottomRight() - QPoint(self._top_width, self._top_height), top_size)
		top_rect = QRect(button_area_rect.topLeft() if not self._is_pressed else
					 button_area_rect.bottomRight() - QPoint(self._top_width, self._top_height), top_size)

		# Draw shadow, top, and outline
		painter.setPen(Qt.NoPen)
		painter.setBrush(QBrush(shadow_color))
		painter.drawRoundedRect(shadow_rect, radius, radius)

		painter.setBrush(QBrush(top_color))
		painter.drawRoundedRect(top_rect, radius, radius)

		painter.setPen(QPen(outline_color, outline_width))
		painter.setBrush(Qt.NoBrush)
		area = outline_width // 2
		corner_r = radius - 2
		adjusted_outline = top_rect.adjusted(area, area, -area, -area)
		painter.drawRoundedRect(adjusted_outline, corner_r, corner_r)

		# Derived classes will draw text here after calling super().paintEvent()

class OneLineButton(AnalogButton):
	def __init__(self, properties, parent=None):
		super().__init__(properties, parent)
		self._font_family = properties.get("specs", {}).get("font", "Arial Black")
		self._font_size = properties.get("specs", {}).get("font size", 32)
		self._text = properties.get("label", "")

	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)

		top_color = self._get_color("bg")
		outline_color = self._get_color("outline")
		text_color = self._get_color("font")

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
	'''
	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)
		# ... (draw background and outline as in OneLineButton) ...
		top_rect = QRect(self.rect().topLeft(), QSize(self._top_width, self._top_height))
		self._draw_centered_text(painter, top_rect, self._text, self._font_family, self._font_size, self._text_color)
	'''
class NumberSystemButton(OneLineButton):
	def __init__(self, properties, parent = None):
		super().__init__(properties, parent)
		self._text_color = QColor(properties.get("palette", {}).get("font", "#000000"))
		# Potentially override attributes if needed

	'''
	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)

		top_color = QColor(self.properties.get("palette", {}).get("bg", "#FFFFFF"))
		outline_color = QColor(self.properties.get("palette", {}).get("outline", "#000000"))

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

		# Draw the text using the inherited method
		self._draw_centered_text(painter, top_rect, self._text, self._font_family, self._font_size, self._text_color)
	'''
class BitWidthButton(TwoLineButton): # Still inherit from TwoLineButton for _text_line1, _text_line2, etc.
	def __init__(self, properties, parent = None):
		super().__init__(properties, parent)
		self.id = properties.get("label")
		self.group = properties.get("group")
		self._is_active = properties.get("state") == "active"
		self._inactive_alpha = 127
	'''
	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)

		top_color = QColor(self.properties.get("palette", {}).get("bg", "#FFFFFF"))
		outline_color = QColor(self.properties.get("palette", {}).get("outline", "#000000"))
		color_line1 = QColor(self._color_line1)
		color_line2 = QColor(self._color_line1)

		if not self._is_active:
			top_color.setAlpha(self._inactive_alpha)
			outline_color.setAlpha(self._inactive_alpha)
			color_line1.setAlpha(self._inactive_alpha)
			color_line2.setAlpha(self._inactive_alpha)

		# Draw the base button
		radius = 15
		button_area_rect = self.rect()
		top_size = QSize(self._top_width, self._top_height)
		shadow_rect = QRect(button_area_rect.bottomRight() - QPoint(self._top_width, self._top_height), top_size)
		top_rect = QRect(button_area_rect.topLeft() if not self._is_pressed else
						 button_area_rect.bottomRight() - QPoint(self._top_width, self._top_height), top_size)

		painter.setPen(Qt.NoPen)
		painter.setBrush(QBrush(QColor(0, 0, 0, 50)))
		painter.drawRoundedRect(shadow_rect, radius, radius)

		painter.setBrush(QBrush(top_color))
		painter.drawRoundedRect(top_rect, radius, radius)

		painter.setPen(QPen(outline_color, self.properties.get("specs", {}).get("outline_width", 4)))
		painter.setBrush(Qt.NoBrush)
		area = self.properties.get("specs", {}).get("outline_width", 4) // 2
		corner_r = radius - 2
		adjusted_outline = top_rect.adjusted(area, area, -area, -area)
		painter.drawRoundedRect(adjusted_outline, corner_r, corner_r)

		# Draw the first line of text
		font_line1 = QFont(self._font_family_line1, self._font_size_line1)
		painter.setFont(font_line1)
		metrics_line1 = painter.fontMetrics()
		text_rect_line1 = metrics_line1.boundingRect(self._text_line1)
		text_x_line1 = top_rect.center().x() - text_rect_line1.width() / 2
		line1_baseline_y = top_rect.top() + (top_rect.height() / 2 + 5)
		painter.setPen(color_line1)
		painter.drawText(int(text_x_line1), int(line1_baseline_y), self._text_line1)

		# Draw the second line of text
		font_line2 = QFont(self._font_family_line2, self._font_size_line2)
		painter.setFont(font_line2)
		metrics_line2 = painter.fontMetrics()
		text_rect_line2 = metrics_line2.boundingRect(self._text_line2)
		text_x_line2 = top_rect.center().x() - text_rect_line2.width() / 2
		line2_baseline_y = top_rect.bottom() - (top_rect.height() / 4 - 5)
		painter.setPen(color_line2)
		painter.drawText(int(text_x_line2), int(line2_baseline_y), self._text_line2)
	'''
class PermanentButton(OneLineButton):
	def __init__(self, properties, parent = None):
		super().__init__(properties, parent)
		self._text_color = QColor(properties.get("palette", {}).get("font", "#000000"))
		# Potentially override attributes if needed
	'''
	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)

		top_color = QColor(self.properties.get("palette", {}).get("bg", "#FFFFFF"))
		outline_color = QColor(self.properties.get("palette", {}).get("outline", "#000000"))

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

		# Draw the text using the inherited method
		self._draw_centered_text(painter, top_rect, self._text, self._font_family, self._font_size, self._text_color)
	'''
class HexadecimalButton(OneLineButton):
	def __init__(self, properties, parent = None):
		super().__init__(properties, parent)
		self._text_color = QColor(properties.get("palette", {}).get("font", "#000000"))
		# Potentially override attributes if needed

	def paintEvent(self, event):
		# We don't need to override the paintEvent anymore.
		# The active/inactive state is now controlled by set_active()
		super().paintEvent(event)

class DecimalButton(OneLineButton):
	def __init__(self, properties, parent = None):
		super().__init__(properties, parent)
		self._text_color = QColor(properties.get("palette", {}).get("font", "#000000"))
		# Potentially override attributes if needed
	'''
	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)

		top_color = QColor(self.properties.get("palette", {}).get("bg", "#FFFFFF"))
		outline_color = QColor(self.properties.get("palette", {}).get("outline", "#000000"))

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

		# Draw the text using the inherited method
		self._draw_centered_text(painter, top_rect, self._text, self._font_family, self._font_size, self._text_color)
	'''
class AboutButton(AngledButton):
	def __init__(self, properties, parent = None):
		super().__init__(properties, parent)
		self.id = properties.get("label")
		self.group = properties.get("group")
		# About button is always active
	'''
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
	'''