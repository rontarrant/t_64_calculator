import sys

from PySide6.QtWidgets import (
   QApplication,
   QMainWindow,
   QPushButton,
)

class MainWindow(QMainWindow):
   def __init__(self):
      super().__init__()

      self.setWindowTitle("T-64 Calculator")

      button = QPushButton("Sample")
      button.setCheckable(True)
      button.clicked.connect(self.do_something)
      button.clicked.connect(self.toggle_something)

      self.setCentralWidget(button)

   def do_something(self):
      print("Doing Something...")

   def toggle_something(self, is_checked):
      print("Checked?", is_checked)
   
if __name__ == "__main__":
   app = QApplication(sys.argv)
   window = MainWindow()
   window.show()
   app.exec()
