import sys
import os

from PySide6.QtWidgets import (
	QApplication,
	QMainWindow,
	QWidget,
	QPushButton,
	QHBoxLayout,
)

from PySide6.QtGui import QPainter, QPixmap, QColor
from PySide6.QtCore import QPoint, Qt, Signal


class PermanentButton(QPushButton):
	"""
	A customized QPushButton that simulates an analog button with a drop shadow effect
	and a visual "press" effect.

	This class extends QRTRadioButton to provide a more visually appealing button
	that mimics the behavior of physical buttons. It uses custom painting to
	draw a drop shadow and to shift the button's image when it's pressed,
	creating a sense of depth and interactivity.

	Attributes:
		image (QPixmap): The main image displayed on the button.
		pressed_offset (QPoint): The offset applied to the image when the button is pressed.
		current_offset (QPoint): The current offset of the image, used for animation.
		is_pressed (bool): Indicates whether the button is currently pressed.
		original_image_path (str): The file path to the original image.
	"""
	def __init__(self, image_path, parent = None):
		"""
		Initializes the PermanentButton.

		Args:
			image_path (str): The file path to the image to be used for the button.
			parent (QWidget, optional): The parent widget. Defaults to None.
		"""
		super().__init__(parent)
		self.original_image_path = image_path + ".png"
		self.image = QPixmap(image_path + ".png")
		self.pressed_offset = QPoint(5, 5)
		self.current_offset = QPoint(0, 0)
		self.is_pressed = False
		#self.original_image_path = image_path
		print("original_image_path: ", self.original_image_path)

		size = self.image.size()
		size.setWidth(size.width() + self.pressed_offset.x() + 2)
		size.setHeight(size.height() + self.pressed_offset.y() + 2)
		self.setFixedSize(size)

	def mousePressEvent(self, event):
		"""
		Handles the mouse press event.

		When the button is pressed, this method:
		1. Sets the `is_pressed` flag to True.
		2. Updates the `current_offset` to the `pressed_offset`.
		3. Triggers a repaint of the button.

		Args:
			event (QMouseEvent): The mouse press event.
		"""
		super().mousePressEvent(event)
		self.is_pressed = True
		self.current_offset = self.pressed_offset
		self.update()

	def mouseReleaseEvent(self, event):
		"""
		Handles the mouse release event.

		When the button is released, this method:
		1. Sets the `is_pressed` flag to False.
		2. Resets the `current_offset` to (0, 0).
		3. Triggers a repaint of the button.

		Args:
			event (QMouseEvent): The mouse release event.
		"""
		super().mouseReleaseEvent(event)
		self.is_pressed = False
		self.current_offset = QPoint(0, 0)
		self.update()

	def paintEvent(self, event):
		"""
		Paints the button.

		This method is responsible for drawing the button's appearance,
		including the drop shadow and the image.

		1. Creates a QPainter object.
		2. Enables antialiasing for smoother rendering.
		3. If the button is not pressed:
			a. Creates a shadow image by making the original image darker.
			b. Draws the shadow image with an offset and reduced opacity.
		4. Draws the main image with the current offset.

		Args:
			event (QPaintEvent): The paint event.
		"""
		painter = QPainter(self)
		painter.setRenderHint(QPainter.RenderHint.Antialiasing)

		if not self.is_pressed:
			shadow_image = self.image.toImage()

			for x in range(shadow_image.width()):
				for y in range(shadow_image.height()):
					color = shadow_image.pixelColor(x, y)

					if color.alpha() > 0:
						alpha = round(color.alpha() * 0.75)
						shadow_image.setPixelColor(x, y, QColor(0, 0, 0, alpha))

			painter.setOpacity(0.5)
			painter.drawImage(self.pressed_offset, shadow_image)
			painter.setOpacity(1.0)

		painter.drawPixmap(self.current_offset, self.image)
		painter.end()

	def change_image(self, new_image_path):
		"""
		Changes the image displayed on the button.

		This method updates the button's image and resizes the button to fit the new image.

		Args:
			new_image_path (str): The file path to the new image.
		"""
		self.image = QPixmap(new_image_path)
		size = self.image.size()
		size.setWidth(size.width() + self.pressed_offset.x() + 2)
		size.setHeight(size.height() + self.pressed_offset.y() + 2)
		self.setFixedSize(size)
		self.update()

class GhostableButton(PermanentButton):
	"""
	A custom button that toggles between an active and inactive state,
	visually represented by different images.

	This class extends PermanentButton to create a button that can be
	switched on or off. It uses two different images to represent
	the active and inactive states and emits a signal when its
	enabled state changes.

	Signals:
		enabled_changed (bool): Emitted when the button's enabled state changes.
								The boolean argument indicates whether the
								button is now enabled (True) or disabled (False).

	Attributes:
		active_image_path (str): The file path to the image used when the button is active.
		inactive_image_path (str): The file path to the image used when the button is inactive.
		is_checked (bool): Indicates whether the button is currently in the "checked" state.
	"""
	# Custom signal to indicate enabled/disabled state change
	enabled_changed = Signal(bool)

	def __init__(self, image_file_name):
		"""
		Initializes the GhostableButton.

		Args:
			active_image_file_name (str): The file name of the image to use when the button is active.
			inactive_image_file_name (str): The file name of the image to use when the button is inactive.
		"""
		super().__init__(image_file_name)
		self.active_image_path = image_file_name
		self.inactive_image_path = image_file_name + "inactive"
		self.is_checked = False
		self.setEnabled(True)  # Ensure buttons start enabled
		self.clicked.connect(self.do_something)
		self.enabled_changed.connect(self.on_enabled_changed)

	def do_something(self):
		"""
		Placeholder method for actions to be performed when the button is clicked.

		This method is currently a placeholder and can be overridden in subclasses
		to implement specific behavior when the button is clicked.
		"""
		print("Doing Something...")

	def setEnabled(self, enabled):
		"""
		Sets the enabled state of the button and emits the `enabled_changed` signal.

		This method overrides the base class's `setEnabled` to emit the
		`enabled_changed` signal whenever the button's enabled state is modified.

		Args:
			enabled (bool): True to enable the button, False to disable it.
		"""
		super().setEnabled(enabled)
		self.enabled_changed.emit(enabled)

	def on_enabled_changed(self, enabled):
		"""
		Changes the button's image based on its enabled state.

		This slot is connected to the `enabled_changed` signal and updates the
		button's image to the active or inactive image, depending on the
		`enabled` state.

		Args:
			enabled (bool): True if the button is enabled, False if it's disabled.
		"""
		if enabled:
			self.change_image(self.active_image_path)
		else:
			self.change_image(self.inactive_image_path)


class RTRadioButton(PermanentButton):
	"""
	A custom button that controls the enabled state of other buttons.

	This class extends PermanentButton to create a button that, when clicked,
	toggles the enabled state of a list of other buttons (GhostableButton instances).

	Attributes:
		switch_buttons (list[GhostableButton]): A list of GhostableButton instances that this
											button controls.
	"""
	def __init__(self, image_file_name):
		"""
		Initializes the RTRadioButton.

		Args:
			image_file_name (str): The file name of the image to use for this button.
			switch_buttons (list[GhostableButton]): A list of GhostableButton instances that this
												button will control.
		"""
		super().__init__(image_file_name)
		self.clicked.connect(self.toggle_something)
		#self.switch_buttons = switch_buttons

	def toggle_something(self):
		"""
		Toggles the enabled state of the associated GhostableButtons.

		This method is called when the button is clicked. It checks if the first
		GhostableButton in the `switch_buttons` list is enabled. If it is, it
		disables all GhostableButtons in the list. Otherwise, it enables them all.
		"""
		if self.switch_buttons[0].isEnabled():
			for button in self.switch_buttons:
				button.setEnabled(False)
				print(button, " disabled")
		else:
			for button in self.switch_buttons:
				button.setEnabled(True)
				print(button, " enabled")


'''
if __name__ == "__main__":
	class MainWindow(QMainWindow):
		def __init__(self):
			super().__init__()

			self.setWindowTitle("T-64 Calculator")

			switch1_on_image = button_data['button_e']['name']
			switch1_off_image = switch1_on_image + "_inactive"
			switch_button1 = GhostableButton(switch1_on_image, switch1_off_image)

			switch2_on_image = button_data['button_f']['name']
			switch2_off_image = switch2_on_image + "_inactive"
			switch_button2 = GhostableButton(switch2_on_image, switch2_off_image)

			selector_file_name = button_data['button_hex']['name']
			selector_button = RTRadioButton(selector_file_name, [switch_button1, switch_button2])

			layout = QHBoxLayout()
			layout_widget = QWidget()
			layout_widget.setLayout(layout)
			layout.addWidget(selector_button)
			layout.addWidget(switch_button1)
			layout.addWidget(switch_button2)

			self.setCentralWidget(layout_widget)

	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	app.exec()
'''