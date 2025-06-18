from PySide6.QtWidgets import QApplication, QMainWindow
import sys
from labels import *
from c64_palette import *
from button_specs import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #label = ResizableLabel("Resizable Text", properties, self)
        label = LineEditColourLabel(lineedit_properties, "Resizable Text", self)
        label.setGeometry(50, 50, 100, 50)  # Initial size
        self.setCentralWidget(label)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(200, 100)
    window.show()
    sys.exit(app.exec())
