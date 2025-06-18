from PySide6.QtWidgets import (
	QPushButton,
	QSizePolicy,
	QLineEdit,
)

from PySide6.QtGui import (
	QPainter,
	QColor,
	QBrush,
	QPen,
	QFont
)

from PySide6.QtCore import (
	Qt,
	QPoint,
	QRect,
	QSize
)

class ResizableLineEdit(QLineEdit):
	def __init__(self, text, properties, parent = None):
		super().__init__(text, parent)
		self.font_size = properties["font_size"]
		self.font_factor = properties["font_factor"]  # Adjust this to control how much the font scales
		self._current_font_size = self.font_size  # Store the current font_size
		self._first_resize = True  # New flag

		# Set the initial font
		font = self.font()
		font.setPointSize(self.font_size)
		self.setFont(font)

	def sizeHint(self):
		return QSize(100, 40)  # Reasonable default size

	def resizeEvent(self, event):
		super().resizeEvent(event)
		#print("ResizableLineEdit::resizeEvent()")

		if self._first_resize:
			self._first_resize = False
		else:
			self.adjust_font_size()

	def adjust_font_size(self):
		#print("ResizableLineEdit::adjust_font_size()")
		lineedit_width = self.width()
		lineedit_height = self.height()

		available_space = min(lineedit_width, lineedit_height)
		new_font_size = int(available_space * self.font_factor)
		if new_font_size < 6:
			new_font_size = 6

		if new_font_size != self._current_font_size:
			font = self.font()
			font.setPointSize(new_font_size)
			self.setFont(font)
			self._current_font_size = new_font_size

class AnalogLineEdit(ResizableLineEdit):
	def __init__(self, properties, parent = None):
		text = properties.get("text", "")
		font_size = properties.get("font_size")
		super().__init__(text, properties, parent)
		self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		
		self._is_active = properties.get("state", "active") == "active"
		self._active_palette = properties.get("palette", {})
		self._inactive_palette = properties.get("inactive_palette", self._active_palette)
		self.font_factor = properties["font_factor"]
		
		self.properties = properties
		width = properties.get("width")
		height = properties.get("height")
		self._default_size = QSize(width, height)
		
	def sizeHint(self):
		return self._default_size

	def set_active(self, is_active):
		if self._is_active != is_active:
			self._is_active = is_active
			self.update()

	def _get_palette(self):
		return self._inactive_palette if not self._is_active else self._active_palette

	def _get_color(self, key):
		palette = self._get_palette()
		return QColor(palette.get(key, "#000000"))  # Default to black if key not found

	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)
		
		try:
			radius = self.properties["radius"]
			lineedit_rect = self.rect()
			
			# Calculate dynamic dimensions (95% of current size)
			top_width = lineedit_rect.width() * 0.95
			top_height = lineedit_rect.height() * 0.95
			
			# Create size and point objects correctly
			top_size = QSize(int(top_width), int(top_height))
			offset = QPoint(int(top_width), int(top_height))
			
			# Calculate rectangles
			shadow_rect = QRect(lineedit_rect.bottomRight() - offset, top_size)
			top_rect = QRect(lineedit_rect.topLeft(), top_size)
			
			# Get colors from palette
			bg_color = self._get_color("bg")
			outline_color = self._get_color("outline")
			text_color = self._get_color("text")
			outline_width = self.properties.get("specs", {}).get("outline")

			# Draw shadow
			painter.setPen(Qt.NoPen)
			painter.drawRoundedRect(shadow_rect, radius, radius)

			# Draw background
			painter.setBrush(QBrush(bg_color))
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
				painter.drawText(top_rect, Qt.AlignRight, self.text())

		finally:
			painter.end()

	def _draw_left_justifed_text(self, painter, rect, text, font_family, font_size, color):
		painter.setPen(color)
		font = QFont(font_family, font_size)
		painter.setFont(font)
		metrics = painter.fontMetrics()
		text_rect = metrics.boundingRect(text)
		text_x = rect.right().x() - text_rect.width() / 2
		baseline_y = rect.right().y() + metrics.ascent() / 2 - 10 # Subtract 10 to move up
		painter.drawText(int(text_x), int(baseline_y), text)


class ResizableButton(QPushButton):
	def __init__(self, text, properties, parent = None):
		super().__init__(text, parent)
		self.properties = properties
		self.font_size = properties["font_size"]
		self.font_factor = 0.5  # Adjust this to control how much the font scales
		self._current_font_size = self.font_size # Store the current font_size
		self._first_resize = True  # New flag

		# Set the initial font
		font = self.font()
		font.setPointSize(self.font_size)
		self.setFont(font)
		#print(f"Initial font_size for '{text}': {self.font_size}")

	def sizeHint(self):
		return QSize(100, 60)  # Reasonable default size

	def resizeEvent(self, event):
		super().resizeEvent(event)

		if self._first_resize:
			self._first_resize = False
		else:
			self.adjust_font_size()

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
	def __init__(self, properties, parent = None):
		# Initialize with empty text - we'll handle text separately
		super().__init__("", properties, parent)
		self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

		self._is_pressed = False
		self._top_width = properties["width"] - 5
		self._top_height = properties["height"] - 5
		self._default_size = QSize(properties["width"], properties["height"])
		self._top_width = self._default_size.width() - 5
		self._top_height = self._default_size.height() - 5
		self.properties = properties
		self._is_active = properties.get("state", "active") == "active"
		self._active_palette = properties["palette"]
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
		self._font_family = properties["specs"]["font"]
		self._font_size = properties["font_size"]
		self._text = properties["label"]

	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)

		top_color = self._get_color("bg")
		outline_color = self._get_color("outline")
		text_color = self._get_color("font")

		radius = self.properties["specs"]["radius"]
		button_area_rect = self.rect()
		top_size = QSize(self._top_width, self._top_height)

		# shadow size calculation
		bottom_right = button_area_rect.bottomRight()
		offset = QPoint(self._top_width, self._top_height)
		adjusted_point = bottom_right - offset
		shadow_rect = QRect(adjusted_point, top_size)

		if not self._is_pressed:
			top_rect = QRect(button_area_rect.topLeft(), top_size)
		else:
			bottom_right = button_area_rect.bottomRight()
			offset = QPoint(self._top_width, self._top_height)
			adjusted_point = bottom_right - offset
			top_rect = QRect(adjusted_point, top_size)

		# Draw the shadow
		painter.setPen(Qt.NoPen)
		painter.setBrush(QBrush(self.properties["shadow_colour"]))
		painter.drawRoundedRect(shadow_rect, radius, radius)

		# Draw the top (background)
		painter.setBrush(QBrush(top_color))
		painter.drawRoundedRect(top_rect, radius, radius)

		# Draw the outline
		painter.setPen(QPen(outline_color, self.properties["specs"]["outline"]))
		painter.setBrush(Qt.NoBrush)
		area = self.properties["specs"]["outline"] // 2
		corner_r = radius - 2
		adjusted_outline = top_rect.adjusted(area, area, -area, -area)
		painter.drawRoundedRect(adjusted_outline, corner_r, corner_r)

		# Draw the text using the dedicated method
		self._draw_centered_text(painter, top_rect)

	def _draw_centered_text(self, painter, rect):
		colour = self._get_color("font")
		painter.setPen(colour)
		font = QFont(self._font_family, self._font_size)
		painter.setFont(font)
		metrics = painter.fontMetrics()
		text_rect = metrics.boundingRect(self._text)
		text_x = rect.center().x() - text_rect.width() / 2
		baseline_y = rect.center().y() + metrics.ascent() / 2 - 10 # Subtract 10 to move up
		painter.drawText(int(text_x), int(baseline_y), self._text)

class TwoLineButton(AnalogButton):
	def __init__(self, properties, parent = None):
		super().__init__(properties, parent)
		self._font_family1 = properties["specs"]["font"] # Correct key for font family
		self._font_size1 = properties["specs"]["font_size"]   # Correct key for font_size
		self._text_line1 = properties["label"]
		self._color_line1 = properties["palette"]["font"]
		#print("properties: ", properties)
		self._font_family2 = properties["specs"]["font"]
		self._font_size2 = properties["specs"]["subfont_size"]
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

		# top rectangle shape
		if not self._is_pressed:
			start_point = button_area_rect.topLeft()
		else:
			offset = QPoint(self._top_width, self._top_height)
			start_point = button_area_rect.bottomRight() - offset

		top_rect = QRect(start_point, top_size)

		# Draw the two lines of text relative to the current top_rect
		# Font for the first line
		_font1 = QFont(self._font_family1, self._font_size1)
		painter.setFont(_font1)
		metrics_line1 = painter.fontMetrics()
		text_rect_line1 = metrics_line1.boundingRect(self._text_line1)
		text_x_line1 = top_rect.center().x() - text_rect_line1.width() / 2
		line1_baseline_y = top_rect.top() + (top_rect.height() / 2 + 5)
		painter.setPen(self._color_line1)
		painter.drawText(int(text_x_line1), int(line1_baseline_y), self._text_line1)

		# Font for the second line
		_font2 = QFont(self._font_family2, self._font_size2)
		painter.setFont(_font2)
		metrics_line2 = painter.fontMetrics()
		text_rect_line2 = metrics_line2.boundingRect(self._text_line2)
		text_x_line2 = top_rect.center().x() - text_rect_line2.width() / 2
		line2_baseline_y = top_rect.bottom() - (top_rect.height() / 4 - 5)
		painter.setPen(self._color_line1)
		painter.drawText(int(text_x_line2), int(line2_baseline_y), self._text_line2)

class AngledButton(OneLineButton):
	def __init__(self, properties, parent = None):
		super().__init__(properties, parent)
		self._angle = properties["specs"]["angle"]
		self._color = properties["palette"]["font"]
		self._text_color = properties["palette"]["font"]

	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)

		top_color = self.properties["palette"]["bg"]
		outline_color = self.properties["palette"]["outline"]
		text_color = self._color # Inherited from AngledButton

		radius = self.properties["radius"]
		button_area_rect = self.rect()
		top_size = QSize(self._top_width, self._top_height)

		# Break down shadow_rect
		bottom_right = button_area_rect.bottomRight()
		shadow_offset = QPoint(self._top_width, self._top_height)
		shadow_start_point = bottom_right - shadow_offset
		shadow_rect = QRect(shadow_start_point, top_size)

		# Break down top_rect
		if not self._is_pressed:
			top_start_point = button_area_rect.topLeft()
		else:
			top_offset = QPoint(self._top_width, self._top_height)
			top_start_point = button_area_rect.bottomRight() - top_offset

		top_rect = QRect(top_start_point, top_size)

		# Draw the shadow
		painter.setPen(Qt.NoPen)
		painter.setBrush(QBrush(QColor(0, 0, 0, 50)))
		painter.drawRoundedRect(shadow_rect, radius, radius)

		# Draw the top (background)
		painter.setBrush(QBrush(top_color))
		painter.drawRoundedRect(top_rect, radius, radius)

		# Draw the button top outline
		specs = self.properties.get("specs", {})
		outline_width = specs["outline"]
		pen = QPen(outline_color, outline_width)
		painter.setPen(pen)

		painter.setBrush(Qt.NoBrush)
		area = self.properties["specs"]["outline"] // 2
		corner_r = radius - 2
		adjusted_outline = top_rect.adjusted(area, area, -area, -area)
		painter.drawRoundedRect(adjusted_outline, corner_r, corner_r)

		# Draw the angled text (logic from AngledButton's paintEvent should still apply)
		painter.setPen(text_color)
		font = QFont(self._font_family, self._font_size) # Inherited from AngledButton
		painter.setFont(font)
		metrics = painter.fontMetrics()
		text_rect = metrics.boundingRect(self._text) # Inherited from AngledButton

		angle = self.properties["specs"]["angle"]
		painter.translate(top_rect.center())
		painter.rotate(angle)
		painter.translate(-top_rect.center())
		painter.drawText(top_rect.center() - text_rect.center(), self._text)
