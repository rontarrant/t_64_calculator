from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QSize

class ResizableLabel(QLabel):
	def __init__(self, text, properties, parent=None):
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

		if new_font_size != self._current_font_size:
			font = self.font()
			font.setPointSize(new_font_size)
			self.setFont(font)
			self._current_font_size = new_font_size
