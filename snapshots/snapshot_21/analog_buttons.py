# analog_buttons.py

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
	QFont,
	QFontMetrics
)

from PySide6.QtCore import (
	Qt,
	QPoint,
	QRect,
	QSize,
	QEvent
)

# Assuming c64_palette is available
# from c64_palette import C64Palette # Make sure this import is resolvable


class ResizableLineEdit(QLineEdit):
	def __init__(self, properties, parent = None):
		# Pass text and properties up to QLineEdit.
		# The actual drawing of the text is done in paintEvent.
		super().__init__(properties.get("text", ""), parent)

		self.properties = properties
		# Initial font size from properties, fallback to a default
		self.initial_font_size = properties.get("font_size", 12)
		self.font_factor = properties.get("font_factor", 0.5) # Factor from properties, fallback to 0.5

		# Set the initial font - will be adjusted on first resize
		font = self.font()
		font.setPointSize(self.initial_font_size)
		self.setFont(font)

		# Set the size policy to expanding
		self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

		# Set text alignment (you can still set this here)
		self.setAlignment(Qt.AlignRight | Qt.AlignVCenter)


	def resizeEvent(self, event: QEvent):
		super().resizeEvent(event)
		self.adjust_font_size()
		# No need to call updateGeometry() here, resizeEvent handles it


	def adjust_font_size(self):
		# Get the available space for text drawing, accounting for padding/margins
		# Adjust these values based on your widget's paintEvent drawing logic
		# Example padding, should ideally be derived from outline width + text padding
		outline_padding = self.properties.get("specs", {}).get("outline", 4) + 5
		available_width = self.width() - (self.textMargins().left() + self.textMargins().right() + outline_padding * 2)
		available_height = self.height() - (self.textMargins().top() + self.textMargins().bottom() + outline_padding * 2)


		if available_width <= 0 or available_height <= 0:
			return # Avoid issues with zero or negative size

		# Calculate a candidate font size based on the smaller dimension of the available space
		# You might need to tune the font_factor here
		new_font_size = max(1, int(min(available_width, available_height) * self.font_factor))

		# Enforce a minimum readable font size
		min_readable_font_size = 6
		new_font_size = max(new_font_size, min_readable_font_size)

		# Check if the text fits horizontally and vertically at this new font size
		font = self.font()
		font.setPointSize(new_font_size)
		metrics = QFontMetrics(font)
		text = self.text() if self.text() else " "
		text_rect = metrics.boundingRect(text)

		# If the text is wider or taller than the available area, reduce the font size iteratively
		# This is a simple approach; a binary search could be more efficient for large font ranges.
		while (text_rect.width() > available_width or text_rect.height() > available_height) and new_font_size > min_readable_font_size:
			new_font_size -= 1
			font.setPointSize(new_font_size)
			metrics = QFontMetrics(font)
			text_rect = metrics.boundingRect(text)


		  # Set the font size if it's different to avoid unnecessary updates
		if self.font().pointSize() != new_font_size:
			self.setFont(font)


	def sizeHint(self):
		# *** MODIFIED: Prioritize dimensions from properties if available ***
		if "width" in self.properties and "height" in self.properties:
			# Return the size from properties as the preferred size
			return QSize(self.properties["width"], self.properties["height"])
		else:
			# Fallback to a font-based hint if no explicit size is in properties
			font_metrics = QFontMetrics(self.font())
			text_size = font_metrics.size(0, self.text() if self.text() else " ")
			# Use consistent padding values as in adjust_font_size or paintEvent
			outline_padding = self.properties.get("specs", {}).get("outline", 4) + 5
			horizontal_padding = self.textMargins().left() + self.textMargins().right() + outline_padding * 2
			vertical_padding = self.textMargins().top() + self.textMargins().bottom() + outline_padding * 2
			width = text_size.width() + horizontal_padding
			height = text_size.height() + vertical_padding
			min_visual_width = 50 # Ensure a minimum hint size
			min_visual_height = 30
			return QSize(max(width, min_visual_width), max(height, min_visual_height))


	def minimumSizeHint(self):
		# *** MODIFIED: Base minimum size on properties if available, otherwise a default ***
		if "width" in self.properties and "height" in self.properties:
			# Return a minimum size that is a fraction of the preferred size,
			# but ensure it's large enough for a minimum readable font.
			min_factor = 0.3 # Allow shrinking to 30% of preferred size (adjustable)
			min_readable_font_size = 6

			# Calculate a minimum size based on minimum readable font + padding
			temp_font = QFont(self.font())
			temp_font.setPointSize(min_readable_font_size)
			font_metrics = QFontMetrics(temp_font)
			text_size = font_metrics.size(0, self.text() if self.text() else " ")
			# Use consistent padding values
			outline_padding = self.properties.get("specs", {}).get("outline", 4) + 5
			horizontal_padding = self.textMargins().left() + self.textMargins().right() + outline_padding * 2
			vertical_padding = self.textMargins().top() + self.textMargins().bottom() + outline_padding * 2
			min_based_on_font = QSize(text_size.width() + horizontal_padding, text_size.height() + vertical_padding)

			# Calculate a minimum size based on a factor of the preferred size
			min_based_on_factor = QSize(int(self.properties["width"] * min_factor), int(self.properties["height"] * min_factor))

			# Return the maximum of the two minimums to ensure readability and shrinkability
			return QSize(max(min_based_on_font.width(), min_based_on_factor.width()),
								  max(min_based_on_font.height(), min_based_on_factor.height()))
		else:
			# Fallback to a default font-based minimum hint if no explicit size is in properties
			temp_font = QFont(self.font())
			min_readable_font_size = 6
			temp_font.setPointSize(min_readable_font_size)
			font_metrics = QFontMetrics(temp_font)
			text_size = font_metrics.size(0, self.text() if self.text() else " ")
			outline_padding = self.properties.get("specs", {}).get("outline", 4) + 5
			horizontal_padding = self.textMargins().left() + self.textMargins().right() + outline_padding * 2
			vertical_padding = self.textMargins().top() + self.textMargins().bottom() + outline_padding * 2
			min_width = text_size.width() + horizontal_padding
			min_height = text_size.height() + vertical_padding
			min_visual_width = 50
			min_visual_height = 30
			return QSize(max(min_width, min_visual_width), max(min_height, min_visual_height))


class AnalogLineEdit(ResizableLineEdit): # Inherits from ResizableLineEdit
	def __init__(self, properties, parent = None):
		# Pass text and properties up to ResizableLineEdit
		super().__init__(properties, parent)

		# AnalogLineEdit specific properties (keep these)
		self._is_active = properties.get("state", "active") == "active"
		self._active_palette = properties.get("palette", {})
		self._inactive_palette = properties.get("inactive_palette", self._active_palette)
		# self.properties is already stored in the base class

		# The size policy and font factor are handled in ResizableLineEdit

		# Text alignment is now set in ResizableLineEdit __init__


	# sizeHint and minimumSizeHint are inherited from ResizableLineEdit and should work


	def set_active(self, is_active):
		if self._is_active != is_active:
			self._is_active = is_active
			self.update() # Request a repaint

	def _get_palette(self):
		return self._inactive_palette if not self._is_active else self._active_palette

	def _get_color(self, key):
		palette = self._get_palette()
		# Default to black if key not found, handle QColor creation from string
		color_value = palette.get(key, "#000000")
		if isinstance(color_value, tuple): # Handle tuple colors if necessary
			return QColor(*color_value)
		return QColor(color_value)


	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)

		try: # Correctly place the try block to cover painting
			radius = self.properties.get("radius", 10) # Default radius
			lineedit_rect = self.rect() # The full rectangle of the widget

			# Calculate dynamic dimensions based on current widget size
			# Use a slightly smaller percentage to account for the shadow/border effect
			content_width_factor = 0.95 # Adjust this factor as needed
			content_height_factor = 0.95 # Adjust this factor as needed

			content_width = lineedit_rect.width() * content_width_factor
			content_height = lineedit_rect.height() * content_height_factor

			# Create size and point objects
			content_size = QSize(int(content_width), int(content_height))

			# Calculate rectangle for the "top" part (where text and outline are drawn)
			# This rectangle is offset from the bottom-right for the shadow effect
			offset_x = lineedit_rect.width() - content_size.width()
			offset_y = lineedit_rect.height() - content_size.height()

			# Adjust the top_rect calculation to ensure it's within the widget bounds
			top_rect = QRect(lineedit_rect.topLeft().x() + offset_x, lineedit_rect.topLeft().y() + offset_y,
									content_size.width(), content_size.height())

			# Calculate the shadow rectangle offset from the bottom-right
			shadow_rect = QRect(lineedit_rect.bottomRight().x() - content_size.width(),
										lineedit_rect.bottomRight().y() - content_size.height(),
										content_size.width(), content_size.height())

			# Get colors from palette
			bg_color = self._get_color("bg")
			outline_color = self._get_color("outline")
			text_color = self._get_color("text") # Use "text" key for text color
			shadow_color = QColor(0, 0, 0, 50) # Example shadow color

			# Draw shadow - drawn slightly offset
			painter.setPen(Qt.NoPen)
			painter.setBrush(QBrush(shadow_color))
			painter.drawRoundedRect(shadow_rect, radius, radius)

			# Draw background (top part) - drawn at the adjusted top_rect
			painter.setBrush(QBrush(bg_color))
			painter.drawRoundedRect(top_rect, radius, radius)

			# Draw outline
			outline_width = self.properties.get("specs", {}).get("outline", 4) # Default outline width
			painter.setPen(QPen(outline_color, outline_width))
			painter.setBrush(Qt.NoBrush)
			# Adjust outline rectangle to be inside the top_rect
			outline_rect = top_rect.adjusted(outline_width // 2, outline_width // 2,
														-(outline_width // 2), -(outline_width // 2))
			painter.drawRoundedRect(outline_rect, max(0, radius - outline_width), max(0, radius - outline_width)) # Adjust corner radius

			# Draw text using the current font set by ResizableLineEdit's resize logic
			text = self.text()
			if text:
				painter.setPen(QPen(text_color))
				# Use the font currently set on the widget
				painter.setFont(self.font())

				# Adjust the text drawing rectangle to be inside the top_rect and add some padding
				# Ensure this padding is consistent with what's subtracted in adjust_font_size
				text_draw_rect = top_rect.adjusted(outline_width + 5, outline_width + 5,
																-(outline_width + 5), -(outline_width + 5)) # Example padding

				# Draw text aligned within the adjusted rectangle
				painter.drawText(text_draw_rect, self.alignment(), text)


		finally:
			painter.end() # Ensure painter is always properly ended


class ResizableButton(QPushButton): # This is the base for AnalogButton family
	def __init__(self, text, properties, parent = None):
		# Pass text and properties up to QPushButton.
		# The actual drawing of the text is done in paintEvent of derivatives.
		# We pass the main label as text so the base class size hints can use it
		# if properties don't specify width/height.
		super().__init__(text, parent)
		self.properties = properties
		# Initial font size from properties, fallback to a default
		self.initial_font_size = properties.get("font_size", 12)
		self.font_factor = properties.get("font_factor", 0.5)  # Factor from properties, fallback to 0.5

		# Set the initial font - will be adjusted on first resize
		font = self.font()
		font.setPointSize(self.initial_font_size)
		self.setFont(font)

		# Set the size policy to expanding
		self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

		# Initialize dynamic dimensions for drawing (will be set in resizeEvent)
		self._top_width = 0
		self._top_height = 0


	def resizeEvent(self, event: QEvent):
		super().resizeEvent(event)

		# Update custom dimensions based on the *current* size after layout has resized
		# These will be used in paintEvent. Use factors consistent with paintEvent.
		self._top_width = self.width() * 0.95 # Example factor
		self._top_height = self.height() * 0.95 # Example factor

		self.adjust_font_size() # Adjust font based on the new size


	def adjust_font_size(self):
		# Get the available space for text drawing, accounting for padding/margins
		# These values should correspond to the area where text is drawn in paintEvent
		# For a general button, let's use the calculated top_width and top_height minus padding
		# Example padding, should ideally be derived from outline width + text padding in derived classes
		outline_padding = self.properties.get("specs", {}).get("outline", 4) + 5
		available_width = self._top_width - outline_padding * 2
		available_height = self._top_height - outline_padding * 2

		if available_width <= 0 or available_height <= 0:
			return # Avoid issues with zero or negative size

		# Calculate a candidate font size based on the smaller dimension of the available space
		new_font_size = max(1, int(min(available_width, available_height) * self.font_factor))

		# Enforce a minimum readable font size
		min_readable_font_size = 6
		new_font_size = max(new_font_size, min_readable_font_size)

		# Check if the *main label* text fits horizontally and vertically at this new font size
		# Derived classes (TwoLineButton, AngledButton) will need to handle their specific
		# text fitting within their paintEvent or by overriding this method with more complex logic.
		font = self.font()
		font.setPointSize(new_font_size)
		metrics = QFontMetrics(font)
		text = self.properties.get("label", "") # Measure the main label
		text_width = metrics.size(0, text).width()
		text_height = metrics.size(0, text).height() # Needed for general height check

		# If the text is wider or taller than the available area, reduce the font size
		while (text_width > available_width or text_height > available_height) and new_font_size > min_readable_font_size:
			new_font_size -= 1
			font.setPointSize(new_font_size)
			metrics = QFontMetrics(font)
			text_width = metrics.size(0, text).width()
			text_height = metrics.size(0, text).height()

		# Set the font size if it's different
		if self.font().pointSize() != new_font_size:
			self.setFont(font)


	def sizeHint(self):
		# *** MODIFIED: Prioritize dimensions from properties if available ***
		if "width" in self.properties and "height" in self.properties:
			# Return the size from properties as the preferred size
			return QSize(self.properties["width"], self.properties["height"])
		else:
			# Fallback to a font-based hint if no explicit size is in properties
			# This part remains similar to your original font-based hint logic
			font_metrics = QFontMetrics(self.font())
			text = self.text() if self.text() else " "
			text_size = font_metrics.size(0, text)
			padding = 20 # Example padding
			width = text_size.width() + padding
			height = text_size.height() + padding
			return QSize(width, height)


	def minimumSizeHint(self):
		# *** MODIFIED: Base minimum size on properties if available, otherwise a default ***
		if "width" in self.properties and "height" in self.properties:
			min_factor = 0.3 # Allow shrinking to 30% of preferred size (adjustable)
			min_readable_font_size = 6

			# Calculate a minimum size based on minimum readable font + padding
			temp_font = QFont(self.font())
			temp_font.setPointSize(min_readable_font_size)
			font_metrics = QFontMetrics(temp_font)
			text = self.text() if self.text() else " "
			text_size = font_metrics.size(0, text)
			padding = 20 # Consistent with sizeHint

			min_based_on_font = QSize(text_size.width() + padding, text_size.height() + padding)

			# Calculate a minimum size based on a factor of the preferred size
			min_based_on_factor = QSize(int(self.properties["width"] * min_factor), int(self.properties["height"] * min_factor))

			# Return the maximum of the two minimums
			return QSize(max(min_based_on_font.width(), min_based_on_factor.width()),
								max(min_based_on_font.height(), min_based_on_factor.height()))
		else:
			# Fallback to a default font-based minimum hint if no explicit size is in properties
			temp_font = QFont(self.font())
			min_readable_font_size = 6
			temp_font.setPointSize(min_readable_font_size)
			font_metrics = QFontMetrics(temp_font)
			text = self.text() if self.text() else " "
			text_size = font_metrics.size(0, text)
			padding = 20
			min_width = text_size.width() + padding
			min_height = text_size.height() + padding
			return QSize(min_width, min_height)


'''
# Data to pass in:
button_data (see example below)
text_data (see example below)
'''
class AnalogButton(ResizableButton): # Inherits from ResizableButton
	def __init__(self, properties, parent = None):
		# Pass text (main label) and properties up to ResizableButton.
		super().__init__(properties.get("label", ""), properties, parent)

		# AnalogButton specific properties (keep these)
		self._is_pressed = False
		# self.properties is already stored in the base class
		self._is_active = properties.get("state", "active") == "active"
		self._active_palette = properties.get("palette", {})
		self._inactive_palette = properties.get("inactive_palette", self._active_palette)

		# Size policy and font factor are handled in ResizableButton


	# sizeHint and minimumSizeHint are inherited from ResizableButton

	# resizeEvent is inherited from ResizableButton and updates _top_width/_top_height and adjusts font


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
		# Default to black if key not found, handle QColor creation from string
		color_value = palette.get(key, "#000000")
		if isinstance(color_value, tuple): # Handle tuple colors if necessary
			return QColor(*color_value)
		return QColor(color_value)

	def paintEvent(self, event):
		# Base AnalogButton paintEvent - draws shadow, top, outline
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)
		try: # Correctly place the try block to cover painting
			radius = self.properties.get("radius", 15)

			# Use the dynamically updated _top_width and _top_height calculated in resizeEvent
			top_size = QSize(int(self._top_width), int(self._top_height))

			button_rect = self.rect()

			if not self._is_pressed:
					top_start_point = button_rect.topLeft()
					shadow_rect = QRect(button_rect.bottomRight().x() - top_size.width(),
											button_rect.bottomRight().y() - top_size.height(),
											top_size.width(), top_size.height())
					top_rect = QRect(top_start_point, top_size)
			else:
					shadow_start_point = button_rect.topLeft()
					top_rect = QRect(button_rect.bottomRight().x() - top_size.width(),
										button_rect.bottomRight().y() - top_size.height(),
										top_size.width(), top_size.height())
					shadow_rect = QRect(shadow_start_point, top_size)

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
			outline_rect = top_rect.adjusted(outline_width // 2, outline_width // 2,
														-(outline_width // 2), -(outline_width // 2))
			painter.drawRoundedRect(outline_rect, max(0, radius - outline_width), max(0, radius - outline_width))

			# Text drawing is handled in derived classes

		finally:
			painter.end()  # Crucial - ensures painter is always properly ended


class OneLineButton(AnalogButton): # Inherits from AnalogButton
	def __init__(self, properties, parent=None):
		super().__init__(properties, parent)
		self._font_family = properties["specs"]["font"]
		# We no longer store fixed font sizes, we'll use the font from self.font()
		self._text = properties["label"]
		self._text_color = self._get_color("font") # Get color using the inherited method

	# sizeHint and minimumSizeHint are inherited from AnalogButton (and ultimately ResizableButton)

	# paintEvent overrides AnalogButton's paintEvent to add text drawing
	def paintEvent(self, event):
		super().paintEvent(event) # Draw the base button (shadow, top, outline) using its painter

		# Create a new painter for drawing the text on top
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)
		try: # Correctly place try block for this painter
			# Determine the current top_rect position based on pressed state
			button_area_rect = self.rect()
			top_size = QSize(int(self._top_width), int(self._top_height)) # Use dynamic dimensions

			if not self._is_pressed:
				start_point = button_area_rect.topLeft()
			else:
				offset = QPoint(int(self._top_width), int(self._top_height)) # Use dynamic dimensions
				start_point = button_area_rect.bottomRight() - offset

			top_rect = QRect(start_point, top_size)

			# Draw the text using the dynamically adjusted font
			self._draw_centered_text(painter, top_rect)

		finally:
			painter.end() # Ensure this painter is properly ended


	def _draw_centered_text(self, painter, rect):
		painter.setPen(self._text_color)
		# Use the font currently set on the widget by ResizableButton's logic
		font = self.font()
		# You can still set the family if needed, but pointSize is set by resizing
		font.setFamily(self._font_family)
		painter.setFont(font)

		# Calculate text position for centering within the rect
		metrics = painter.fontMetrics()
		text_rect = metrics.boundingRect(self._text)

		# Center the text rectangle within the provided rect
		text_x = rect.center().x() - text_rect.width() / 2
		text_y = rect.center().y() - text_rect.height() / 2 + metrics.ascent() # Adjust for baseline

		# Add a small vertical offset if needed for visual centering within the button
		vertical_offset = -2 # Adjust this value
		text_y += vertical_offset

		painter.drawText(int(text_x), int(text_y), self._text)


class TwoLineButton(AnalogButton): # Inherits from AnalogButton
	def __init__(self, properties, parent = None):
		super().__init__(properties, parent)
		self._font_family = properties["specs"]["font"] # Common font family
		# No fixed font sizes here, use the resizable font's size
		self._text_line1 = properties["label"]
		self._color_line1 = self._get_color("font") # Get color using inherited method
		self._text_line2 = properties.get("sublabel", "")
		# Assuming line2 uses the same color, or get a different color if specified

	# sizeHint and minimumSizeHint are inherited from AnalogButton (and ultimately ResizableButton)

	# paintEvent overrides AnalogButton's paintEvent to add text drawing
	def paintEvent(self, event):
		super().paintEvent(event) # Draw the base button (shadow, top, outline) using its painter

		# Create a new painter for drawing the text on top
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)
		try: # Correctly place try block for this painter
			# Determine the current top_rect position based on pressed state
			button_area_rect = self.rect()
			top_size = QSize(int(self._top_width), int(self._top_height)) # Use dynamic dimensions

			if not self._is_pressed:
				start_point = button_area_rect.topLeft()
			else:
				offset = QPoint(int(self._top_width), int(self._top_height)) # Use dynamic dimensions
				start_point = button_area_rect.bottomRight() - offset

			top_rect = QRect(start_point, top_size)

			# --- Text Drawing for Two Lines ---
			painter.setPen(self._color_line1)
			font = self.font() # Use the font set by ResizableButton
			font.setFamily(self._font_family)
			painter.setFont(font)

			metrics = painter.fontMetrics()
			text1_rect = metrics.boundingRect(self._text_line1)
			text2_rect = metrics.boundingRect(self._text_line2)

			# Calculate total text height including spacing
			line_spacing = metrics.leading() # Get recommended spacing
			total_text_height = text1_rect.height() + text2_rect.height() + line_spacing

			# Determine the vertical center of the available drawing area (top_rect)
			outline_width = self.properties.get("specs", {}).get("outline", 4)
			# Adjust available text area based on outline and desired padding
			available_text_area = top_rect.adjusted(outline_width + 5, outline_width + 5,
																 -(outline_width + 5), -(outline_width + 5))

			# Check if available area is valid
			if available_text_area.width() <= 0 or available_text_area.height() <= 0:
				return # Nothing to draw if area is invalid

			center_y = available_text_area.center().y()

			# Calculate the starting Y for the top line to center the block of text
			start_y_block = center_y - total_text_height / 2

			# Calculate baseline for each line
			# Adjust baseline calculation relative to the start of the block and text height
			baseline1_y = start_y_block + text1_rect.height() - metrics.descent()
			baseline2_y = baseline1_y + text2_rect.height() + line_spacing


			# Draw the lines centered horizontally within the available text area
			text1_x = available_text_area.center().x() - text1_rect.width() / 2
			painter.drawText(int(text1_x), int(baseline1_y), self._text_line1)

			text2_x = available_text_area.center().x() - text2_rect.width() / 2
			painter.drawText(int(text2_x), int(baseline2_y), self._text_line2)

		finally:
			painter.end() # Ensure this painter is properly ended

# Add the AngledButton class definition
class AngledButton(AnalogButton): # Inherits from AnalogButton
	def __init__(self, properties, parent = None):
		super().__init__(properties, parent)
		self._font_family = properties["specs"]["font"]
		self._text = properties["label"]
		self._text_color = self._get_color("font")
		self._angle = properties.get("specs", {}).get("angle", 0) # Get angle with default


	# sizeHint and minimumSizeHint inherited

	def paintEvent(self, event):
		super().paintEvent(event) # Draw the base button using its painter

		# Create a new painter for drawing the text on top
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)
		try: # Correctly place try block for this painter
			# Determine the current top_rect position based on pressed state
			button_area_rect = self.rect()
			top_size = QSize(int(self._top_width), int(self._top_height))

			if not self._is_pressed:
				start_point = button_area_rect.topLeft()
			else:
				offset = QPoint(int(self._top_width), int(self._top_height))
				start_point = button_area_rect.bottomRight() - offset

			top_rect = QRect(start_point, top_size)

			# --- Angled Text Drawing ---
			painter.setPen(self._text_color)
			font = self.font() # Use the font set by ResizableButton
			font.setFamily(self._font_family)
			painter.setFont(font)

			outline_width = self.properties.get("specs", {}).get("outline", 4)
			text_draw_area = top_rect.adjusted(outline_width + 5, outline_width + 5,
															-(outline_width + 5), -(outline_width + 5)) # Example padding

			if text_draw_area.width() <= 0 or text_draw_area.height() <= 0:
				return

			painter.save() # Save painter state before transformation

			painter.translate(text_draw_area.center()) # Translate to the center of the text drawing area
			painter.rotate(self._angle) # Rotate

			metrics = painter.fontMetrics()
			text_rect = metrics.boundingRect(self._text)

			# Drawing at (-text_rect.width()/2, text_rect.height()/2 - metrics.descent()) centers the text
			# horizontally and positions the baseline vertically at the center relative to the origin.
			text_x = -text_rect.width() / 2
			text_y = text_rect.height() / 2 - metrics.descent()

			vertical_offset_after_rotation = -2 # Adjust this value
			text_y += vertical_offset_after_rotation

			painter.drawText(int(text_x), int(text_y), self._text)

			painter.restore() # Restore painter state

		finally:
			painter.end() # Ensure this painter is properly ended