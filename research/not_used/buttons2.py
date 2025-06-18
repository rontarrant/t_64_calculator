# PySide6 libraries
from PySide6.QtWidgets import (
	QApplication,
	QMainWindow,
	QPushButton,
	QWidget,
	QVBoxLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap, QColor, QPalette

# Python libraries
import sys

class ImageButton(QPushButton):
	def __init__(self, id, up_image, down_image, parent = None):
		super().__init__(parent)
		self.up_icon = QIcon(up_image)
		self.down_icon = QIcon(down_image)
		self.setIcon(self.up_icon)
		self.setIconSize(QPixmap(up_image).size())
		self.setFixedSize(64, 64)
		self.setStyleSheet("QPushButton { border: none; }")


	def mousePressEvent(self, event):
		if event.button() == Qt.LeftButton:
			self.setIcon(self.down_icon)

		super().mousePressEvent(event)


	def mouseReleaseEvent(self, event):
		if event.button() == Qt.LeftButton:
			self.setIcon(self.up_icon)

		super().mouseReleaseEvent(event)


class CalcButton(QPushButton):
	def __init__(self, properties):
		super().__init__()
		# common to all CalcButtons
		id = properties.id
		self.up_image = properties.up_image
		self.down_image = properties.down_image
	
	def callback(self):
		pass
		# use the id to do what needs doing

button_image_path = "./images"

buttons: dict[str, str, str] = {
	"0": ["button_0_up.png", "button_0_down.png"],
	"1": ["button_1_up.png", "button_1_down.png"],
	"2": ["button_2_up.png", "button_2_down.png"],
	"3": ["button_3_up.png", "button_3_down.png"],
	"4": ["button_4_up.png", "button_4_down.png"],
	"5": ["button_5_up.png", "button_5_down.png"],
	"6": ["button_6_up.png", "button_6_down.png"],
	"7": ["button_7_up.png", "button_7_down.png"],
	"8": ["button_8_up.png", "button_8_down.png"],
	"9": ["button_9_up.png", "button_9_down.png"],
	"a": ["button_a_up.png", "button_a_down.png"],
	"b": ["button_b_up.png", "button_b_down.png"],
	"c": ["button_c_up.png", "button_c_down.png"],
	"d": ["button_d_up.png", "button_d_down.png"],
	"e": ["button_e_up.png", "button_e_down.png"],
	"f": ["button_f_up.png", "button_f_down.png"],
	"add": ["button_add_up.png", "button_add_down.png"],
	"sub": ["button_sub_up.png", "button_sub_down.png"],
	"mult": ["button_mult_up.png", "button_mult_down.png"],
	"div": ["button_div_up.png", "button_div_down.png"],
	"equals": ["equals", "button_equals_up.png", "button_equals_down.png"],
	"8bit": ["button_8bit_up.png", "button_8bit_down.png"],
	"16bit": ["button_16bit_up.png", "button_16bit_down.png"],
	"32bit": ["button_32bit_up.png", "button_32bit_down.png"],
	"64bit": ["button_64bit_up.png", "button_64bit_down.png"],
	"back": ["button_back_up.png", "button_back_down.png"],
	"clear": ["button_clear_up.png", "button_clear_down.png"],
	"dot": ["button_dot_up.png", "button_dot_down.png"],
	"signed": ["button_signed_on.png", "button_signed_off.png"]
}

###
# Testing
###
if __name__ == "__main__":
	app = QApplication(sys.argv)

	child_widget = QWidget()
	child_widget.setAutoFillBackground(True)
	palette = child_widget.palette()
	palette.setColor(QPalette.Window, QColor("red"))
	child_widget.setPalette(palette)

	layout = QVBoxLayout()
	layout.addWidget(child_widget)

	container_widget = QWidget()
	container_widget.setLayout(layout)

	window = QMainWindow()
	window.setWindowTitle("Buttons Test")
	window.setCentralWidget(container_widget)
	window.show()

	sys.exit(app.exec())
	
