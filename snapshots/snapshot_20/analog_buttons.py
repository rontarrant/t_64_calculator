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
QFontMetrics # Import QFontMetrics
)

from PySide6.QtCore import (
Qt,
QPoint,
QRect,
QSize,
QEvent # Import QEvent
)

# Assuming c64_palette, callbacks, and button_specs are available
from c64_palette import C64Palette
# from callbacks import * # Make sure individual callback functions are imported or accessible
# from button_specs import * # Make sure button_specs are imported or accessible


class ResizableLineEdit(QLineEdit):
	def __init__(self, text, properties, parent = None):
		super().__init__(text, parent)
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


	def resizeEvent(self, event: QEvent):
		super().resizeEvent(event)
		self.adjust_font_size()
		# Inform the layout that our size hints might have changed
		self.updateGeometry()


	def adjust_font_size(self):
		lineedit_width = self.width()
		lineedit_height = self.height()

		# Use the smaller dimension to determine font size
		available_space = min(lineedit_width, lineedit_height)
		# Calculate new font size, ensuring it's at least 1 to avoid issues
		new_font_size = max(1, int(available_space * self.font_factor))

		# Enforce a minimum readable font size, e.g., 6 points
		min_readable_font_size = 6
		new_font_size = max(new_font_size, min_readable_font_size)

		# Set the font size if it's different to avoid unnecessary updates
		font = self.font()
		if font.pointSize() != new_font_size:
			font.setPointSize(new_font_size)
			self.setFont(font)


	def sizeHint(self):
		# Provide a size hint based on the current font size and text
		# This helps the layout understand the preferred size
		font_metrics = QFontMetrics(self.font())
		text_size = font_metrics.size(0, self.text() if self.text() else " ") # Use " " for size of empty text

		# Increased padding for better initial fit
		# QLineEdit has internal margins, this padding is in addition to those.
		horizontal_padding = self.textMargins().left() + self.textMargins().right() + 20 # Increased example padding
		vertical_padding = self.textMargins().top() + self.textMargins().bottom() + 20 # Increased example padding

		width = text_size.width() + horizontal_padding
		height = text_size.height() + vertical_padding

		# Ensure a minimum hint size that's visually acceptable even with padding
		# You might need to adjust these values
		min_visual_width = 50
		min_visual_height = 30

		return QSize(max(width, min_visual_width), max(height, min_visual_height))


	def minimumSizeHint(self):
		# Provide a minimum size hint based on the minimum readable font size (6pt) and text
		# Use the enforced minimum font size (6) to calculate the minimum hint
		temp_font = QFont(self.font())
		min_readable_font_size = 6
		temp_font.setPointSize(min_readable_font_size)

		font_metrics = QFontMetrics(temp_font)
		text_size = font_metrics.size(0, self.text() if self.text() else " ") # Use " " for size of empty text

		# Increased padding (consistent with sizeHint)
		horizontal_padding = self.textMargins().left() + self.textMargins().right() + 20 # Increased example padding
		vertical_padding = self.textMargins().top() + self.textMargins().bottom() + 20 # Increased example padding

		min_width = text_size.width() + horizontal_padding
		min_height = text_size.height() + vertical_padding

		# Ensure a minimum hint size that's visually acceptable
		min_visual_width = 50
		min_visual_height = 30

		return QSize(max(min_width, min_visual_width), max(min_height, min_visual_height))

class AnalogLineEdit(ResizableLineEdit): # Inherits from ResizableLineEdit
	def __init__(self, properties, parent = None):
		# Pass text and properties up to ResizableLineEdit
		text = properties.get("text", "")
		super().__init__(text, properties, parent)

		# AnalogLineEdit specific properties
		self._is_active = properties.get("state", "active") == "active"
		self._active_palette = properties.get("palette", {})
		self._inactive_palette = properties.get("inactive_palette", self._active_palette)
		self.properties = properties # Store properties again for paintEvent access

		# The size policy is already set in ResizableLineEdit

		# AnalogLineEdit custom drawing requires text alignment to be handled in paintEvent
		self.setAlignment(Qt.AlignRight | Qt.AlignVCenter) # Set default alignment, can be overridden in paintEvent


	# sizeHint and minimumSizeHint are inherited from ResizableLineEdit and should work
	# if you override them here, make sure they also provide size hints based on font metrics.
	# def sizeHint(self):
	#    return super().sizeHint() # Inherit from parent


	# def minimumSizeHint(self):
	#    return super().minimumSizeHint() # Inherit from parent


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

		try:
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
				text_draw_rect = top_rect.adjusted(outline_width + 5, outline_width + 5,
																-(outline_width + 5), -(outline_width + 5)) # Example padding

				# Draw text aligned within the adjusted rectangle
				painter.drawText(text_draw_rect, self.alignment(), text)


		finally:
			painter.end() # Ensure painter is always properly ended

# Remove or comment out _draw_left_justifed_text as painting is handled in paintEvent
# def _draw_left_justifed_text(self, painter, rect, text, font_family, font_size, color):
#    pass # This method is likely no longer needed with the new paintEvent logic


class ResizableButton(QPushButton): # This is the base for AnalogButton family
	def __init__(self, text, properties, parent = None):
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


	def resizeEvent(self, event: QEvent):
		super().resizeEvent(event)
		self.adjust_font_size()
		# Inform the layout that our size hints might have changed
		self.updateGeometry()


	def adjust_font_size(self):
		button_width = self.width()
		button_height = self.height()

		# Use the smaller dimension to determine font size
		available_space = min(button_width, button_height)
		# Calculate new font size, ensuring it's at least 1 to avoid issues
		new_font_size = max(1, int(available_space * self.font_factor))

		# Enforce a minimum readable font size, e.g., 6 points
		min_readable_font_size = 6
		new_font_size = max(new_font_size, min_readable_font_size)

		# Set the font size if it's different to avoid unnecessary updates
		font = self.font()
		if font.pointSize() != new_font_size:
			font.setPointSize(new_font_size)
			self.setFont(font)


	def sizeHint(self):
		# Provide a size hint based on the current font size and text
		# This is used by the layout to determine the preferred size
		font_metrics = QFontMetrics(self.font())
		# Measure text size, adding padding for button appearance (borders, margins)
		# Consider if button text wraps or not - QPushButton handles this by default,
		# but custom painting might need more careful measurement.
		# For simplicity here, assume single line text for measurement.
		text = self.text() if self.text() else " "
		text_size = font_metrics.size(0, text)

		# Add padding for the button's appearance (adjust as needed)
		# This padding should be enough to contain the text at the given font size
		padding = 20 # Example padding

		width = text_size.width() + padding
		height = text_size.height() + padding # Assuming roughly square buttons or similar padding

		return QSize(width, height)


	def minimumSizeHint(self):
		# Provide a minimum size hint based on the minimum readable font size (6pt) and text
		# This is the smallest the layout can make the button
		# Temporarily create a font with the minimum size to measure
		temp_font = QFont(self.font())
		min_readable_font_size = 6
		temp_font.setPointSize(min_readable_font_size)

		font_metrics = QFontMetrics(temp_font)
		text = self.text() if self.text() else " "
		text_size = font_metrics.size(0, text)

		# Add padding (should be consistent with sizeHint's padding logic)
		padding = 20 # Example padding

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
		# Pass text and properties up to ResizableButton.
		# The actual drawing of the text is done in paintEvent of derivatives.
		# We pass the main label as text so the base class size hints can use it.
		super().__init__(properties.get("label", ""), properties, parent)

		# AnalogButton specific properties
		self._is_pressed = False
		self.properties = properties # Store properties for paintEvent access
		self._is_active = properties.get("state", "active") == "active"
		self._active_palette = properties.get("palette", {})
		self._inactive_palette = properties.get("inactive_palette", self._active_palette)

		# The size policy and font factor are handled in ResizableButton

		# Remove or comment out fixed size properties, as size is managed by layout and hints
		# self._top_width = properties["width"] - 5
		# self._top_height = properties["height"] - 5
		# self._default_size = QSize(properties["width"], properties["height"])
		# self._top_width = self._default_size.width() - 5
		# self._top_height = self._default_size.height() - 5

	# sizeHint and minimumSizeHint are inherited from ResizableButton and should work.
	# Override if you need specific behavior, but ensure they support shrinking.
	# def sizeHint(self):
	#    return super().sizeHint() # Inherit from parent

	# def minimumSizeHint(self):
	#    return super().minimumSizeHint() # Inherit from parent

	def resizeEvent(self, event):
		# Call ResizableButton's resizeEvent first to handle font adjustment and updateGeometry
		super().resizeEvent(event)

		# Update custom dimensions based on the *current* size after layout has resized
		# These will be used in paintEvent
		self._top_width = self.width() * 0.95 # Example factor
		self._top_height = self.height() * 0.95 # Example factor


	def mousePressEvent(self, event):
		if event.button() == Qt.LeftButton:
			self._is_pressed = True
			self.update() # Request a repaint
		super().mousePressEvent(event)

	def mouseReleaseEvent(self, event):
		if event.button() == Qt.LeftButton:
			self._is_pressed = False
			self.update() # Request a repaint
		super().mouseReleaseEvent(event)

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
		try:
			radius = self.properties.get("radius", 15) # Default radius

			# Use the dynamically updated _top_width and _top_height calculated in resizeEvent
			top_size = QSize(int(self._top_width), int(self._top_height))

			button_rect = self.rect() # The full rectangle of the widget

			# Calculate rectangles based on the current widget size and calculated top_size
			# Adjust positions based on pressed state
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


			# Get colors from palette
			top_color = self._get_color("bg")
			outline_color = self._get_color("outline")
			shadow_color = QColor(0, 0, 0, 50) # Example shadow color
			outline_width = self.properties.get("specs", {}).get("outline", 4) # Default outline width


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
			# Adjust outline rectangle to be inside the top_rect
			outline_rect = top_rect.adjusted(outline_width // 2, outline_width // 2,
														-(outline_width // 2), -(outline_width // 2))
			painter.drawRoundedRect(outline_rect, max(0, radius - outline_width), max(0, radius - outline_width)) # Adjust corner radius

			# Note: Text drawing is handled in the derived classes' paintEvent

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
		super().paintEvent(event) # Draw the base button (shadow, top, outline)

		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)

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
		super().paintEvent(event) # Draw the base button (shadow, top, outline)

		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)

		# Determine the current top_rect position based on pressed state
		button_area_rect = self.rect()
		top_size = QSize(int(self._top_width), int(self._top_height)) # Use dynamic dimensions

		if not self._is_pressed:
			start_point = button_area_rect.topLeft()
		else:
			offset = QPoint(int(self._top_width), int(self._top_height)) # Use dynamic dimensions
			start_point = button_area_rect.bottomRight() - offset

		top_rect = QRect(start_point, top_size)


		# Draw the two lines of text using the dynamically adjusted font
		font = self.font() # Use the font set by ResizableButton's logic
		font.setFamily(self._font_family) # Apply font family

		# --- Draw Line 1 ---
		painter.setFont(font)
		metrics_line1 = painter.fontMetrics()
		text_rect_line1 = metrics_line1.boundingRect(self._text_line1)

		# Calculate position for Line 1 (top part of the button)
		# Adjust vertical position to place it in the upper half
		line1_x = top_rect.center().x() - text_rect_line1.width() / 2
		line1_y = top_rect.center().y() - text_rect_line1.height() / 2 - text_rect_line1.height() / 4 # Adjust vertical position

		# Add small vertical offset if needed
		vertical_offset_line1 = -3 # Adjust this value
		line1_y += vertical_offset_line1


		painter.setPen(self._color_line1)
		painter.drawText(int(line1_x), int(line1_y + metrics_line1.ascent()), self._text_line1) # Adjust baseline


		# --- Draw Line 2 ---
		# If there's sublabel text
		if self._text_line2:
			# Optionally adjust font size for the second line, relative to the main size
			# For now, let's use a slightly smaller version of the main font size
			subfont_size = max(1, int(font.pointSize() * 0.7)) # Example: 70% of main font size
			subfont = QFont(font)
			subfont.setPointSize(subfont_size)
			painter.setFont(subfont)

			metrics_line2 = painter.fontMetrics()
			text_rect_line2 = metrics_line2.boundingRect(self._text_line2)

			# Calculate position for Line 2 (bottom part of the button)
			# Adjust vertical position to place it in the lower half
			line2_x = top_rect.center().x() - text_rect_line2.width() / 2
			line2_y = top_rect.center().y() - text_rect_line2.height() / 2 + text_rect_line1.height() / 4 # Adjust vertical position relative to line 1

			# Add small vertical offset if needed
			vertical_offset_line2 = 5 # Adjust this value
			line2_y += vertical_offset_line2


			painter.setPen(self._color_line1) # Assuming same color for both lines
			painter.drawText(int(line2_x), int(line2_y + metrics_line2.ascent()), self._text_line2) # Adjust baseline


class AngledButton(OneLineButton): # Inherits from OneLineButton
	def __init__(self, properties, parent = None):
		super().__init__(properties, parent)
		self._angle = properties.get("specs", {}).get("angle", 0) # Default angle
		# Text color is already inherited from OneLineButton

	# sizeHint and minimumSizeHint are inherited

	# paintEvent overrides OneLineButton's paintEvent to add angled text drawing
	def paintEvent(self, event):
		# Draw the base button (shadow, top, outline) - this will be done by
		# calling the parent's paintEvent, which in turn calls AnalogButton's paintEvent.
		# We don't call super().paintEvent(event) here directly because
		# AngledButton's _draw_centered_text is specifically for *angled* text,
		# not the standard centered text drawn in OneLineButton's paintEvent.
		# We need to replicate the drawing of the button shape here, then draw text angled.

		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)
		try:
			radius = self.properties.get("radius", 15) # Default radius

			# Use the dynamically updated _top_width and _top_height calculated in resizeEvent
			top_size = QSize(int(self._top_width), int(self._top_height))

			button_rect = self.rect() # The full rectangle of the widget

			# Calculate rectangles based on the current widget size and calculated top_size
			# Adjust positions based on pressed state
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

			# Get colors from palette
			top_color = self._get_color("bg")
			outline_color = self._get_color("outline")
			shadow_color = QColor(0, 0, 0, 50) # Example shadow color
			outline_width = self.properties.get("specs", {}).get("outline", 4) # Default outline width

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


			# Draw the angled text using the dynamically adjusted font
			painter.setPen(self._text_color)
			# Use the font currently set on the widget by ResizableButton's logic
			font = self.font()
			font.setFamily(self._font_family) # Apply font family
			painter.setFont(font)

			metrics = painter.fontMetrics()
			text = self._text if self._text else " " # Handle empty text
			text_rect = metrics.boundingRect(text)

			# Translate and rotate for angled text
			painter.translate(top_rect.center()) # Translate origin to the center of the top_rect
			painter.rotate(self._angle) # Rotate by the specified angle
			# After rotation, the origin is still at the center of the original top_rect.
			# We need to draw the text rectangle centered around this new origin.
			# The top-left corner of the text rectangle, relative to the new origin,
			# is (-text_rect.width() / 2, -text_rect.height() / 2).
			painter.drawText(QPoint(-text_rect.width() // 2, text_rect.height() // 2 - metrics.descent()), text) # Adjust for baseline


		finally:
			painter.end() # Ensure painter is always properly ended

		# Remove or comment out the unnecessary _draw_centered_text method from OneLineButton
		# def _draw_centered_text(self, painter, rect):
		#    pass # Not used in AngledButton's paintEvent