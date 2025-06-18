from PySide6.QtWidgets import (
	QApplication,
	QWidget,
	 QGridLayout,
	  QMainWindow,
		QVBoxLayout,
		QPushButton,
)

from PySide6.QtGui import QPainter, QBrush, QColor, QPen, QFont, QTransform # Import QTransform
from PySide6.QtCore import Qt, QPoint, QRect, QSize

class AnalogButton(QPushButton):
	def __init__(self, properties, parent = None):
		super().__init__("", parent)
		self._is_pressed = False
		self._top_width = properties.get("width", 100)
		self._top_height = properties.get("height", 50)
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
		top_width = self._top_width
		top_height = self._top_height
		shadow_rect = QRect(button_area_rect.bottomRight() - QPoint(top_width, top_height), QSize(top_width, top_height))

		font = QFont(self._font_family, self._font_size)
		painter.setFont(font)
		metrics = painter.fontMetrics()
		text_rect = metrics.boundingRect(self._text)
		text_x = button_area_rect.center().x() - text_rect.width() / 2
		baseline_y = button_area_rect.center().y() + metrics.ascent() / 2 - 10 # Scale the offset
		painter.drawText(int(text_x), int(baseline_y), self._text)

		top_rect = QRect(button_area_rect.topLeft() if not self._is_pressed else button_area_rect.bottomRight() - QPoint(top_width, top_height), QSize(top_width, top_height))

		# Draw the shadow
		painter.setPen(Qt.NoPen)
		painter.setBrush(QBrush(QColor(0, 0, 0, 50)))
		painter.drawRoundedRect(shadow_rect, radius, radius)

		# Draw the top (background)
		painter.setBrush(QBrush(top_color))
		painter.drawRoundedRect(top_rect, radius, radius)

		# Draw the outline
		outline_width = self.properties.get("specs", {}).get("outline_width", 4)
		painter.setPen(QPen(outline_color, outline_width))
		painter.setBrush(Qt.NoBrush)
		area = outline_width // 2
		corner_r = radius - 2
		adjusted_outline = top_rect.adjusted(area, area, -area, -area)
		painter.drawRoundedRect(adjusted_outline, corner_r, corner_r)

		# Draw the text using the dedicated method (adjust font size here too)
		self._draw_centered_text(painter, top_rect, self._text, self._font_family, self._font_size, text_color)

	def _draw_centered_text(self, painter, rect, text, font_family, font_size, color):
		painter.setPen(color)
		font = QFont(font_family, font_size)
		painter.setFont(font)
		metrics = painter.fontMetrics()
		text_rect = metrics.boundingRect(text)
		text_x = rect.center().x() - text_rect.width() / 2
		baseline_y = rect.center().y() + metrics.ascent() / 2 - 10 # Scale the offset
		painter.drawText(int(text_x), int(baseline_y), text)

class TwoLineButton(AnalogButton):
	def __init__(self, properties, parent=None):
		super().__init__(properties, parent)
		self._font_family = properties.get("specs", {}).get("font", "Arial Black")
		self._font_size = properties.get("specs", {}).get("font size", 32)
		self._subfont_size = properties.get("specs", {}).get("subfont size", 14)
		self._text = properties.get("label", "")
		self._subtext = properties.get("sublabel", "")

	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)

		top_color = self._get_color("bg")
		outline_color = self._get_color("outline")
		text_color = self._get_color("font")

		radius = 15
		button_area_rect = self.rect()
		top_width = self._top_width
		top_height = self._top_height
		shadow_rect = QRect(button_area_rect.bottomRight() - QPoint(top_width, top_height), QSize(top_width, top_height))

		top_rect = QRect(button_area_rect.topLeft() if not self._is_pressed else button_area_rect.bottomRight() - QPoint(top_width, top_height), QSize(top_width, top_height))

		# Draw the shadow
		painter.setPen(Qt.NoPen)
		painter.setBrush(QBrush(QColor(0, 0, 0, 50)))
		painter.drawRoundedRect(shadow_rect, radius, radius)

		# Draw the top (background)
		painter.setBrush(QBrush(top_color))
		painter.drawRoundedRect(top_rect, radius, radius)

		# Draw the outline
		outline_width = self.properties.get("specs", {}).get("outline_width", 4)
		painter.setPen(QPen(outline_color, outline_width))
		painter.setBrush(Qt.NoBrush)
		area = outline_width // 2
		corner_r = radius - 2
		adjusted_outline = top_rect.adjusted(area, area, -area, -area)
		painter.drawRoundedRect(adjusted_outline, corner_r, corner_r)

		# Draw the main text (relative to top)
		main_font = QFont(self._font_family, self._font_size)
		painter.setFont(main_font)
		main_metrics = painter.fontMetrics()
		main_text_rect = main_metrics.boundingRect(self._text)
		main_text_x = top_rect.center().x() - main_text_rect.width() / 2
		main_baseline_y = top_rect.top() + (top_rect.height() * 0.3) + main_metrics.ascent() / 2 # Position 30% down from top
		painter.drawText(int(main_text_x), int(main_baseline_y), self._text)

		# Draw the subtext (relative to top)
		sub_font = QFont(self._font_family, self._subfont_size)
		painter.setFont(sub_font)
		sub_metrics = painter.fontMetrics()
		sub_text_rect = sub_metrics.boundingRect(self._subtext)
		sub_text_x = top_rect.center().x() - sub_text_rect.width() / 2
		sub_baseline_y = top_rect.top() + (top_rect.height() * 0.7) + sub_metrics.ascent() / 2 # Position 70% down from top
		painter.drawText(int(sub_text_x), int(sub_baseline_y), self._subtext)

class AngledButton(AnalogButton):
	def __init__(self, properties, parent=None):
		super().__init__(properties, parent)
		self._font_family = properties.get("specs", {}).get("font", "Arial Black")
		self._font_size = properties.get("specs", {}).get("font size", 26)
		self._angle = properties.get("specs", {}).get("angle", -30)
		self._text = properties.get("label", "")

	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)

		top_color = self._get_color("bg")
		outline_color = self._get_color("outline")
		text_color = self._get_color("font")

		radius = 15
		button_area_rect = self.rect()
		top_width = self._top_width
		top_height = self._top_height
		shadow_rect = QRect(button_area_rect.bottomRight() - QPoint(top_width, top_height), QSize(top_width, top_height))

		top_rect = QRect(button_area_rect.topLeft() if not self._is_pressed else button_area_rect.bottomRight() - QPoint(top_width, top_height), QSize(top_width, top_height))

		# Draw the shadow
		painter.setPen(Qt.NoPen)
		painter.setBrush(QBrush(QColor(0, 0, 0, 50)))
		painter.drawRoundedRect(shadow_rect, radius, radius)

		# Draw the top (background)
		painter.setBrush(QBrush(top_color))
		painter.drawRoundedRect(top_rect, radius, radius)

		# Draw the outline
		outline_width = self.properties.get("specs", {}).get("outline_width", 4)
		painter.setPen(QPen(outline_color, outline_width))
		painter.setBrush(Qt.NoBrush)
		area = outline_width // 2
		corner_r = radius - 2
		adjusted_outline = top_rect.adjusted(area, area, -area, -area)
		painter.drawRoundedRect(adjusted_outline, corner_r, corner_r)

		painter.save()
		transform = QTransform().translate(top_rect.center().x(), top_rect.center().y()).rotate(self._angle).translate(-top_rect.center().x(), -top_rect.center().y())
		painter.setTransform(transform)

		font = QFont(self._font_family, self._font_size)
		painter.setFont(font)
		metrics = painter.fontMetrics()
		text_rect = metrics.boundingRect(self._text)
		text_x = top_rect.center().x() - text_rect.width() / 2
		vertical_offset = 5  # This is the line you should have
		baseline_y = top_rect.center().y() + metrics.ascent() / 2 - vertical_offset
		painter.drawText(int(text_x), int(baseline_y), self._text)

		painter.restore()
