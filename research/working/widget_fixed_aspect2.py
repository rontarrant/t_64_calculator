import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QSizePolicy
from PySide6.QtCore import QSize

class AspectWidget(QWidget):
    '''
    A widget that maintains its aspect ratio.
    '''
from PySide6.QtWidgets import QWidget, QSizePolicy
from PySide6.QtCore import Qt

class AspectWidget(QWidget):
	'''
	A widget that maintains its aspect ratio.
	'''
	def __init__(self, *args, ratio=7/5, **kwargs):
		super().__init__(*args, **kwargs)
		self.ratio = ratio
		self.adjusted_to_size = (-1, -1)
		self.setSizePolicy(QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored))

	def resizeEvent(self, event):
		size = event.size()
		if size == self.adjusted_to_size:
			return
		self.adjusted_to_size = size

		full_width = size.width()
		full_height = size.height()
		width = min(full_width, full_height * self.ratio)
		height = min(full_height, full_width / self.ratio)

		h_margin = round((full_width - width) / 2)
		v_margin = round((full_height - height) / 2)

		self.setContentsMargins(h_margin, v_margin, h_margin, v_margin)

class AspectRatioButton(QWidget):
    def __init__(self, text, aspect_ratio=7/5, parent=None):
        super().__init__(parent)
        self.aspect_widget = AspectWidget(ratio=aspect_ratio)
        self.button = QPushButton(text)
        self.button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout = QVBoxLayout(self.aspect_widget)
        layout.addWidget(self.button)
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins within AspectWidget

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.aspect_widget)
        self.setLayout(main_layout)

    def clicked(self):
        return self.button.clicked

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aspect Ratio Buttons in QMainWindow")

        # Create the aspect ratio buttons
        square_button = AspectRatioButton("Square")
        wide_button = AspectRatioButton("Wide")
        tall_button = AspectRatioButton("Tall")

        # Create a central widget to hold the buttons
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(square_button)
        layout.addWidget(wide_button)
        layout.addWidget(tall_button)
        central_widget.setLayout(layout)

        # Set the central widget of the QMainWindow
        self.setCentralWidget(central_widget)

        # Set an initial size for the main window
        self.resize(400, 600)  # Adjust these values as needed
        self.setMinimumWidth(330)
        self.setMinimumHeight(500)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())