import sys
from PySide6.QtWidgets import (QApplication, QWidget, QLineEdit, QVBoxLayout,
                               QPushButton)
from PySide6.QtCore import Qt

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Calculator")

        self.input_field = QLineEdit()
        self.result_field = QLineEdit()
        self.result_field.setReadOnly(True)
        self.result_field.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.button_layout = QVBoxLayout()
        buttons = [
            '7', '8', '9', '+',
            '4', '5', '6', '-',
            '1', '2', '3', '*',
            '0', '.', '=', '/'
        ]
        row_layout = None
        for i, button_text in enumerate(buttons):
            if i % 4 == 0:
                row_layout = QVBoxLayout() # Changed to QVBoxLayout for vertical arrangement of buttons
                self.button_layout.addLayout(row_layout)
            button = QPushButton(button_text)
            button.clicked.connect(self.button_clicked)
            row_layout.addWidget(button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.input_field)
        main_layout.addWidget(self.result_field)
        main_layout.addLayout(self.button_layout)

        self.setLayout(main_layout)

    def button_clicked(self):
        sender = self.sender()
        button_text = sender.text()

        if button_text == '=':
            try:
                expression = self.input_field.text()
                result = eval(expression)
                self.result_field.setText(str(result))
            except Exception as e:
                self.result_field.setText("Error")
        else:
            current_text = self.input_field.text()
            self.input_field.setText(current_text + button_text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec())