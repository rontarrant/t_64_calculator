from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QGridLayout, 
                              QPushButton, QSizePolicy)
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt

class ChequeredGridLayout(QGridLayout):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSpacing(0)
        self.color1 = QColor("#e0f2f7")
        self.color2 = QColor("#b2ebf2")
    
    def addWidget(self, widget, row, col, rowspan = 1, colspan = 1):
        # Create container widget with checkerboard background
        container = QWidget()
        container.setAutoFillBackground(True)
        
        # Set the appropriate color
        palette = container.palette()
        palette.setColor(container.backgroundRole(), 
                        self.color1 if (row + col) % 2 == 0 else self.color2)
        container.setPalette(palette)
        
        # Create layout for container
        container_layout = QGridLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.addWidget(widget)
        
        # Add to main layout
        super().addWidget(container, row, col, rowspan, colspan)
    
    def setCellColors(self, color1, color2):
        self.color1 = QColor(color1)
        self.color2 = QColor(color2)
        for i in range(self.count()):
            widget = self.itemAt(i).widget()
            if widget:
                row, col, _, _ = self.getItemPosition(i)
                palette = widget.palette()
                palette.setColor(widget.backgroundRole(), 
                               self.color1 if (row + col) % 2 == 0 else self.color2)
                widget.setPalette(palette)
if __name__ == "__main__":
	class MainWindow(QMainWindow):
		def __init__(self):
			super().__init__()
			
			# Create central widget
			central_widget = QWidget()
			self.setCentralWidget(central_widget)
			
			# Use our ChequeredGridLayout instead of regular QGridLayout
			self.button_layout = ChequeredGridLayout(central_widget)
			central_widget.setLayout(self.button_layout)
			
			# Add buttons directly to button_layout (no need for special methods)
			self.add_button("Button 1", 0, 0)
			self.add_button("Button 2", 0, 1)
			self.add_button("Button 3", 1, 0)
			self.add_button("Button 4", 1, 1)
			
			# Set colors
			self.button_layout.setCellColors("#e0f2f7", "#b2ebf2")
			
			self.setWindowTitle("Checkerboard Grid Layout")
			self.resize(400, 300)
		
		def add_button(self, text, row, col):
			button = QPushButton(text)
			button.setStyleSheet("""
					QPushButton {
						background: rgba(255, 255, 255, 150);
						border: 1px solid #888;
						padding: 10px;
					}
					QPushButton:hover {
						background: rgba(255, 255, 255, 200);
					}
			""")
			self.button_layout.addWidget(button, row, col)
			return button

	app = QApplication([])
	window = MainWindow()
	window.show()
	app.exec()