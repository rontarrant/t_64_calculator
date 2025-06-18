from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QGridLayout, QSizePolicy
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

class ResizableButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        # Ensure the button expands in both directions
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Dynamically adjust font size based on button size
        size = min(self.width(), self.height()) // 4
        font = self.font()
        font.setPointSize(max(size, 8))  # Minimum font size of 8
        self.setFont(font)

class GridWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Resizable Grid Layout")

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        grid_layout = QGridLayout(central_widget)
        grid_layout.setContentsMargins(10, 10, 10, 10)
        grid_layout.setSpacing(5)

        # Add buttons to the grid
        for row in range(5):
            for col in range(4):
                button = ResizableButton(f"Button {row+1},{col+1}")
                grid_layout.addWidget(button, row, col)

        # Ensure equal stretch for both rows and columns
        for row in range(5):
            grid_layout.setRowStretch(row, 1)
        for col in range(4):
            grid_layout.setColumnStretch(col, 1)

if __name__ == "__main__":
    app = QApplication([])

    window = GridWindow()
    window.resize(800, 600)
    window.show()

    app.exec()
