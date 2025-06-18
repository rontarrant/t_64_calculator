import sys
from functools import partial
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit

class CalculatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Calculator')
        self.setGeometry(100, 100, 300, 400)

        layout = QVBoxLayout()

        self.display = QLineEdit()
        self.display.setReadOnly(True)
        layout.addWidget(self.display)

        buttonsLayout = QGridLayout()

        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            'C', '0', '=', '+'
        ]

        row = 0
        col = 0

        for button in buttons:
            btn = QPushButton(button)
            if button == '=':
                btn.clicked.connect(self.calculate)
            elif button == 'C':
                btn.clicked.connect(self.clearDisplay)
            else:
                btn.clicked.connect(partial(self.appendToDisplay, button))

            buttonsLayout.addWidget(btn, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1

        layout.addLayout(buttonsLayout)
        self.setLayout(layout)

    def appendToDisplay(self, char):
        self.display.setText(self.display.text() + char)

    def calculate(self):
        try:
            result = eval(self.display.text())
            self.display.setText(str(result))
        except Exception as e:
            self.display.setText("Error")

    def clearDisplay(self):
        self.display.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculatorApp = CalculatorApp()
    calculatorApp.show()
    sys.exit(app.exec())

