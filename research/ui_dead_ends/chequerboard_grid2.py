from PySide6.QtWidgets import (QApplication, QWidget, QGridLayout, QPushButton,
                              QSizePolicy, QLabel)
from PySide6.QtGui import QPainter, QBrush, QColor
from PySide6.QtCore import Qt, QRect

class CheckeredGridLayoutWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(0)  # No spacing between cells
        self.color1 = QColor("#e0f2f7")
        self.color2 = QColor("#b2ebf2")
        self.setLayout(self.grid_layout)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def addWidgetToGrid(self, widget, row, col, rowspan=1, colspan=1):
        # Create a container widget with the background color
        container = QWidget()
        container.setAutoFillBackground(True)
        
        # Set the appropriate color based on position
        palette = container.palette()
        palette.setColor(container.backgroundRole(), 
                        self.color1 if (row + col) % 2 == 0 else self.color2)
        container.setPalette(palette)
        
        # Create a layout for the container
        container_layout = QGridLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.addWidget(widget)
        
        self.grid_layout.addWidget(container, row, col, rowspan, colspan)

    def setCellColors(self, color1, color2):
        self.color1 = QColor(color1)
        self.color2 = QColor(color2)
        # Update existing widgets
        for i in range(self.grid_layout.count()):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                row, col, _, _ = self.grid_layout.getItemPosition(i)
                palette = widget.palette()
                palette.setColor(widget.backgroundRole(), 
                               self.color1 if (row + col) % 2 == 0 else self.color2)
                widget.setPalette(palette)

class MyMainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Checkerboard Grid Example")
        self.setGeometry(100, 100, 400, 400)
        
        main_layout = QGridLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.central_widget = CheckeredGridLayoutWidget()
        main_layout.addWidget(self.central_widget, 0, 0)
        
        # Create buttons with some styling
        button_style = """
        QPushButton {
            background: rgba(255, 255, 255, 150);
            border: 1px solid #888;
            padding: 5px;
        }
        QPushButton:hover {
            background: rgba(255, 255, 255, 200);
        }
        """
        
        self.button1 = QPushButton("Button 1")
        self.button1.setStyleSheet(button_style)
        self.button2 = QPushButton("Button 2")
        self.button2.setStyleSheet(button_style)
        self.button3 = QPushButton("Button 3")
        self.button3.setStyleSheet(button_style)
        self.button4 = QPushButton("Button 4")
        self.button4.setStyleSheet(button_style)

        self.central_widget.addWidgetToGrid(self.button1, 0, 0)
        self.central_widget.addWidgetToGrid(self.button2, 0, 1)
        self.central_widget.addWidgetToGrid(self.button3, 1, 0)
        self.central_widget.addWidgetToGrid(self.button4, 1, 1)

app = QApplication([])
window = MyMainWindow()
window.show()
app.exec()