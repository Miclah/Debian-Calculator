##
# @file: gui.py
# @brief: GUI for IVS project 2.
# @author Michal Petrán (xpetra32)
# @Created: 22-03-2023
# @Last Modified: 09-04-2023
##

#TODO: 
# sqrt x crashes the calculator,
# tutorial window still has some things left to tweak
# () sometimes cause a problem with calculations
# make an error handling for pressing function twice/without input(for example x! displays: invalid literal for i instead of no input or something) the same goes for other functions
# no idea how to handle log, has to figure something out
# Make light mode and dark mode

import sys
import locale
from PyQt5.QtWidgets import QDialog, QTextEdit, QVBoxLayout
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget, QGridLayout, QLabel, QHBoxLayout, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QSize
from math_lib import add, sub, mul, div
from extended_math_lib import factorial, power, sqrt, logarithm

def custom_eval(expression):
    operations = {
        '+': add,
        '-': sub,
        '×': mul,
        '÷': div,   
        '^': power,
        'log': logarithm
    }

    for operator, func in operations.items():
        if operator in expression:
            a, b = map(float, expression.split(operator))
            return func(a, b)

    return 0


class TutorialWindow(QDialog):
    def __init__(self, parent=None):
        super(TutorialWindow, self).__init__(parent)
        self.setModal(True)
        self.setWindowTitle("Tutorial")
        self.setFixedSize(400, 300)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)  # Add Qt.Dialog flag

        self.oldPos = None

        self.setStyleSheet("""
            QDialog {
                background-color: #202020;
            }
            QLabel {
                color: white;
                font-size: 14px;
            }
            QPushButton {
                background-color: #505050;
                color: white;
                font-size: 14px;
                border: 1px solid #707070;
                padding: 4px 10px;
            }
            QPushButton:hover {
                background-color: #707070;
            }
        """)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 10, 10, 20)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        self._createTitleBar()

        self.label = QLabel("Welcome to the Calculator Tutorial")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        self.tutorial_text = QLabel("This calculator is designed to be user-friendly and easy to use. "
                                    "To perform calculations, you can either use your mouse to click on the buttons "
                                    "or use your keyboard to input numbers and operators.\n\n"
                                    "Basic Operations:\n"
                                    "1. Addition (+): Click the '+' button or press the '+' key on your keyboard.\n"
                                    "2. Subtraction (-): Click the '-' button or press the '-' key on your keyboard.\n"
                                    "3. Multiplication (×): Click the '×' button or press the '*' key on your keyboard.\n"
                                    "4. Division (÷): Click the '÷' button or press the '/' key on your keyboard.\n\n"
                                    "Advanced Operations:\n"
                                    "1. Factorial (x!): Click the 'x!' button or press the '!' key on your keyboard.\n"
                                    "2. Square Root (√x): Click the '√x' button or press the 'r' key on your keyboard.\n"
                                    "3. Exponentiation (x^y): Click the 'x^y' button or press the '^' key on your keyboard.\n"
                                    "4. Logarithms (log): Click the 'log' button or press the 'l' key on your keyboard.\n\n"
                                    "Clearing the Display:\n"
                                    "1. To clear the entire display, click the 'C' button or press the 'C' key on your keyboard.\n"
                                    "2. To delete the last character, click the 'DEL' button or press the 'Backspace' key on your keyboard.")
        self.tutorial_text.setWordWrap(True)
        
        self.tutorial_text.setAlignment(Qt.AlignJustify)
        self.layout.addWidget(self.tutorial_text)

        self.layout.addStretch()

    def _createTitleBar(self):
        self.title_bar = QWidget(self)
        self.title_bar.setStyleSheet("background-color: #202020;")
        self.title_bar.setFixedHeight(40)
        self.title_bar_layout = QHBoxLayout()
        self.title_label = QLabel("Calculator Tutorial")
        self.title_label.setStyleSheet("color: white; font-size: 16px;")
        self.title_bar_layout.addWidget(self.title_label)
        self.close_button = QPushButton("X")
        self.close_button.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #202020;
                border: none;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: rgb(200, 50, 50);
            }
        """)
        self.close_button.setFixedSize(40, 30)
        self.close_button.clicked.connect(self.close)
        self.title_bar_layout.addWidget(self.close_button)
        self.title_bar.setLayout(self.title_bar_layout)
        self.layout.addWidget(self.title_bar)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.oldPos is not None:
            delta = event.globalPos() - self.oldPos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = None

                
        

class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setFixedSize(320, 480)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)

        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        self._createTitleBar()

        self._createDisplay()
        self._createButtons()
        self.new_input = False
        self.x_y_base = None
        self.display.textChanged.connect(self._adjust_font_size)  # Add this line

        self.show()

    def _createTitleBar(self):
        self.titleBar = QWidget()
        self.titleBar.setFixedHeight(30)

        titleBarLayout = QHBoxLayout()
        titleBarLayout.setContentsMargins(0, 0, 0, 0)  # Add -1 to the bottom margin
        titleBarLayout.setSpacing(1)

        self.titleLabel = QLabel("Calculator")
        self.titleLabel.setStyleSheet("color: white; font-size: 14px;")
        titleBarLayout.addWidget(self.titleLabel)

        titleBarLayout.addStretch()
        
        self.helpButton = QPushButton("?")
        self.helpButton.setFixedSize(40, 30)
        self.helpButton.clicked.connect(self.showTutorial) # Use the showTutorial method you already have
        self.helpButton.setStyleSheet("background-color: transparent; border: none;")  # Set the button to be transparent and blend in with the title bar
        titleBarLayout.addWidget(self.helpButton)

        self.minimizeButton = QPushButton("-")
        self.minimizeButton.setFixedSize(40, 30)
        self.minimizeButton.clicked.connect(self.showMinimized)
        titleBarLayout.addWidget(self.minimizeButton)
        

        self.closeButton = QPushButton("X")
        self.closeButton.setFixedSize(40, 30)
        self.closeButton.clicked.connect(self.close)
        titleBarLayout.addWidget(self.closeButton)

        # Adjusting the vertical position of the minimize button and the X button
        titleBarLayout.addSpacing(10)

        self.helpButton.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                font-size: 22px;
                border: none;
            }
            QPushButton:hover {
                background-color: #323232;
            }
        """)

        self.minimizeButton.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                font-size: 40px;
                border: none;
            }
            QPushButton:hover {
                background-color: #323232;
            }
        """)

        self.minimizeButton.setCursor(Qt.PointingHandCursor)

        self.closeButton.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                font-size: 18px;
                border: none;
            }
            QPushButton:hover {
                background-color: rgb(200, 50, 50);
            }
        """)

        self.closeButton.setCursor(Qt.PointingHandCursor)

        self.titleBar.setLayout(titleBarLayout)
        self.generalLayout.addWidget(self.titleBar)
        
        
    def _createDisplay(self):
        self.display = QLineEdit()
        self.display.setFixedHeight(75)
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.generalLayout.addWidget(self.display)
        self.setStyleSheet("""
           QWidget {
                background-color: #202020;
            }

            QPushButton {
                background-color: #ededed;
                color: #333;
                border: 1px solid #bbb;
                font-size: 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #d9d9d9;
            }
            QPushButton:pressed {
                background-color: #c6c6c6;
            }
            QPushButton[equal_button="true"] {
                background-color: #78B8E8;
                color: white;
                border: 1px solid #78B8E8;
            }

            QPushButton[equal_button="true"]:hover {
                background-color: #67A8D8;
            }

            QPushButton[equal_button="true"]:pressed {
                background-color: #5698C8;
            }


            QLineEdit {
                background-color: #202020;
                color: white;
                font-size: 34px;
                border: none;
                padding: 0 10px;
            }

            QPushButton[number="true"] {
                background-color: #3B3B3B;
                color: white;
                border: 1px solid #3B3B3B;
            }

            QPushButton[number="true"]:hover {
                background-color: #323232;
            }
            
            QPushButton[other_button="true"] {
                background-color: #323232;
                color: white;
                border: 1px solid #323232;
            }

            QPushButton[other_button="true"]:hover {
                background-color: #3B3B3B;
            }


            
        """)
        self.display.setMaxLength(21)  # Limit to 21 characters, considering commas
        self.display.setContentsMargins(0, 0, 0, 0)

    def _createButtons(self):
        self.buttons = {}
        buttonsLayout = QGridLayout()
        buttonsLayout.setHorizontalSpacing(1)  # Add horizontal spacing between buttons
        buttonsLayout.setVerticalSpacing(3)  # Add vertical spacing between buttons
        
        
        buttons = {
            "(": (0, 0),
            ")": (0, 1),
            "C": (0, 2),
            "DEL": (0, 3),
            "x!": (1, 0),
            "x^y": (1, 1),
            "√x": (1, 2),
            "log": (1, 3),  # Add the log button
            "7": (2, 0),
            "8": (2, 1),
            "9": (2, 2),
            "÷": (2, 3),  # Move the ÷ button one row down
            "4": (3, 0),
            "5": (3, 1),
            "6": (3, 2),
            "x": (3, 3),  # Move the x button one row down
            "1": (4, 0),
            "2": (4, 1),
            "3": (4, 2),
            "-": (4, 3),  # Move the - button one row down
            ".": (5, 0),  # Move the . button to the position of the ? button
            "0": (5, 1),
            "=": (5, 2),  # Move the = button one column to the right
            "+": (5, 3),  # Move the + button one row down
        }
        
        self.tutorialButton = QPushButton("?")
        self.tutorialButton.clicked.connect(self._buttonClicked)



        for btnText, pos in buttons.items():
            button = QPushButton(btnText)
            button.setFont(QFont("Arial", 14, QFont.Bold))
            button.setFixedSize(72, 54)  # Set a fixed size for the buttons (5% smaller)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            if btnText in {'-', '+', '÷', '×'}:
                button.setProperty('operator', True)

            if btnText == '=':
                button.setProperty('equal_button', True)
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #78B8E8;
                        color: #202020;
                        font-size: 20px;
                        border: 1px solid #78B8E8;
                        border-radius: 5px;
                    }
                    QPushButton:hover {
                        background-color: #67A8D8;
                    }
                    QPushButton:pressed {
                        background-color: #5698C8;
                    }
                """)  # Set the "=" button style

            if btnText in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '?'}:
                button.setProperty('number', True)

            elif btnText in {'(', ')', 'x!', 'x^y', '√x', 'C', 'DEL', '-', '+', '÷', 'x', 'log'}:
                button.setProperty('other_button', True)

            button.clicked.connect(lambda ch, btn=btnText: self._buttonClicked(btn))
            if len(pos) == 4:
                row, col, rowspan, colspan = pos
                buttonsLayout.addWidget(button, row, col, rowspan, colspan)
            else:
                row, col = pos
                buttonsLayout.addWidget(button, row, col)

        self.generalLayout.addLayout(buttonsLayout)

        


    def _buttonClicked(self, button):
        
        button = self.sender().text()
        print(f"Button clicked: {button}") 
        
        if button in {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "(", ")", "÷", "×", "-", "+"}:
            self.display.insert(button)
            self._adjust_font_size()
            current_length = len(self.display.text())
            if current_length > 15:
                new_font_size = 30 - (current_length - 15) * 2
                new_font_size = max(new_font_size, 10)  # Minimum font size
                self.display.setStyleSheet(f"""
                    QLineEdit {{
                        background-color: #202020;
                        color: white;
                        font-size: {new_font_size}px;
                        border: none;
                        padding: 0 10px;
                    }}
                """)

        elif button == "=":
            try:
                text = self.display.text()
                result = custom_eval(text)
                formatted_result = self._format_number(str(result))
                self.display.setText(formatted_result)
                self._adjust_font_size()

                current_length = len(self.display.text())
                if current_length > 15:
                    new_font_size = 30 - (current_length - 15) * 2
                    new_font_size = max(new_font_size, 10)  # Minimum font size
                    self.display.setStyleSheet(f"""
                        QLineEdit {{
                            background-color: #202020;
                            color: white;
                            font-size: {new_font_size}px;
                            border: none;
                            padding: 0 10px;
                        }}
                    """)


            except Exception as e:
                self.display.setText(str(e))

                
        elif button == "C":
            self.display.clear()
            
        elif button == "⌫":
            self.display.backspace()
            
        elif button == "DEL":
            self.display.backspace()
            
        elif button == "x!":
            try:
                text = self.display.text()
                number = int(text)
                if number > 170:
                    raise ValueError("Exceeds limit for x!")
                result = factorial(number)
                formatted_result = self._format_number(str(result))
                self.display.setText(formatted_result)
                self._adjust_font_size()

                current_length = len(self.display.text())
                if current_length > 15:
                    new_font_size = 30 - (current_length - 15) * 2
                    new_font_size = max(new_font_size, 10)  # Minimum font size
                    self.display.setStyleSheet(f"""
                        QLineEdit {{
                            background-color: #202020;
                            color: white;
                            font-size: {new_font_size}px;
                            border: none;
                            padding: 0 10px;
                        }}
                    """)
            except Exception as e:
                self.display.setText(str(e))



                
        elif button == "x^y":
            self.display.insert("^")
            

            
        elif button == "?":
            print("Tutorial button clicked")
            self.showTutorial()


        elif button == "√x":
            try:
                text = self.display.text()
                if float(text) < 0:
                    raise ValueError("Cannot compute square root of a negative number")
                result = sqrt(float(text))
                formatted_result = self._format_number(str(result))
                self.display.setText(formatted_result)
                self._adjust_font_size()

                current_length = len(self.display.text())
                if current_length > 15:
                    new_font_size = 30 - (current_length - 15) * 2
                    new_font_size = max(new_font_size, 10)  # Minimum font size
                    self.display.setStyleSheet(f"""
                        QLineEdit {{
                            background-color: #202020;
                            color: white;
                            font-size: {new_font_size}px;
                            border: none;
                            padding: 0 10px;
                        }}
                    """)
            except Exception as e:
                self.display.setText(str(e))

                
        elif button == "log":
            try:
                text = self.display.text()
                if ',' not in text:
                    self.display.setText("Error: Please enter both base and number separated by a comma")
                else:
                    self.display.insert("log")
                base, number = text.split(',')
                result = logarithm(float(base), float(number))
                formatted_result = self._format_number(str(result))
                self.display.setText(formatted_result)
                self._adjust_font_size()

                current_length = len(self.display.text())
                if current_length > 15:
                    new_font_size = 30 - (current_length - 15) * 2
                    new_font_size = max(new_font_size, 10)  # Minimum font size
                    self.display.setStyleSheet(f"""
                        QLineEdit {{
                            background-color: #202020;
                            color: white;
                            font-size: {new_font_size}px;
                            border: none;
                            padding: 0 10px;
                        }}
                    """)

            except Exception as e:
                self.display.setText(str(e))

                
        


    def keyPressEvent(self, event):
        key = event.text()

        if key in '0123456789.+-/*()':
            self.display.insert(key)
            self._adjust_font_size()  # Add this line
        elif event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self._buttonClicked("=")
        elif key.lower() == "c":
            self._buttonClicked("C")
        elif event.key() == Qt.Key_Backspace:
            self._buttonClicked("⌫")
        elif event.key() == Qt.Key_Delete:
            self._buttonClicked("CE")

            
    def showTutorial(self):
        print("Showing tutorial window")
        tutorialWindow = TutorialWindow(self)
        tutorialWindow.move(self.geometry().center() - tutorialWindow.rect().center())
        tutorialWindow.exec_()



        
    def _format_number(self, number):
        if '.' in number:
            parts = number.split('.')
            formatted_integer = '{:,}'.format(int(parts[0]))
            return f"{formatted_integer}.{parts[1]}"
        else:
            return '{:,}'.format(int(number))
        
        
    def _adjust_font_size(self):
        current_length = len(self.display.text())
        
        if current_length <= 17:
            new_font_size = 30
        elif 17 < current_length < 20:
            new_font_size = 28
        elif 20 < current_length <= 23:
            new_font_size = 23
        
        else:
            new_font_size = 30
        
        self.display.setStyleSheet(f"""
            QLineEdit {{
                background-color: #202020;
                color: white;
                font-size: {new_font_size}px;
                border: none;
                padding: 0 10px;
            }}
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    calc = Calculator()
    sys.exit(app.exec_())

