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
	"0": ["button_0.png", "inactive_0.png"],
	"1": ["button_1.png", "inactive_1.png"],
	"2": ["button_2.png", "inactive_2.png"],
	"3": ["button_3.png", "inactive_3.png"],
	"4": ["button_4.png", "inactive_4.png"],
	"5": ["button_5.png", "inactive_5.png"],
	"6": ["button_6.png", "inactive_6.png"],
	"7": ["button_7.png", "inactive_7.png"],
	"8": ["button_8.png", "inactive_8.png"],
	"9": ["button_9.png", "inactive_9.png"],
	"a": ["button_a.png", "inactive_a.png"],
	"b": ["button_b.png", "inactive_b.png"],
	"c": ["button_c.png", "inactive_c.png"],
	"d": ["button_d.png", "inactive_d.png"],
	"e": ["button_e.png", "inactive_e.png"],
	"f": ["button_f.png", "inactive_f.png"],
	"add":    ["button_add.png",    "inactive_add.png"   ],
	"sub":    ["button_sub.png",    "inactive_sub.png"   ],
	"mult":   ["button_mult.png",   "inactive_mult.png"  ],
	"div":    ["button_div.png",    "inactive_div.png"   ],
	"equals": ["button_equals.png", "inactive_equals.png"],
	"8bit":   ["button_8bit.png",   "inactive_8bit.png"  ],
	"16bit":  ["button_16bit.png",  "inactive_16bit.png" ],
	"32bit":  ["button_32bit.png",  "inactive_32bit.png" ],
	"64bit":  ["button_64bit.png",  "inactive_64bit.png" ],
	"back":   ["button_back.png",   "inactive_back.png"  ],
	"clear":  ["button_clear.png",  "inactive_clear.png" ],
	"dot":    ["button_dot.png",    "inactive_dot.png"   ],
	"signed": ["button_signed.png", "button_unsigned.png"]
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
	
