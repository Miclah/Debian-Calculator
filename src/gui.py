##
# @file: gui.py
# @brief: GUI for IVS project 2.
# @author Michal Petrán (xpetra32)
# @Created: 22-03-2023
# @Last Modified: 09-04-2023
##

#TODO: 
# make a white outline around the calculator and tutorial window. 
# add the white line around the input/output window
# sqrt x crashes the calculator,
# tutorial window still has some things left to tweak
# () sometimes cause a problem with calculations
# make an error handling for pressing function twice/without input(for example x! displays: invalid literal for i instead of no input or something) the same goes for other functions
# no idea how to handle log, has to figure something out
# Make light mode and dark mode

import sys
import re
import locale
from PyQt5.QtWidgets import QDialog, QTextEdit, QVBoxLayout, QScrollArea, QGraphicsDropShadowEffect, QGraphicsOpacityEffect
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget, QGridLayout, QLabel, QHBoxLayout, QSizePolicy
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt, QSize
from math_lib import add, sub, mul, div
from extended_math_lib import factorial, power, sqrt, ln

def custom_eval(expression):
    operations = {
        '+': add,
        '-': sub,
        '×': mul,
        '÷': div,
        '^': power,
    }

    single_operand_operations = {
        'x!': factorial,
        '√x': sqrt,
        'ln(': ln
    }

    for operator, func in single_operand_operations.items():
        if operator in expression:
            a = float(re.sub(r'[^\d.-]', '', expression))
            return func(a)

    for operator, func in operations.items():
        if operator in expression:
            a, b = map(float, re.split(r'(?<!e)' + re.escape(operator), expression))
            try:
                result = func(a, b)
                if operator == '^' and not -1e6 < result < 1e6:
                    raise ValueError("Result is too large")
                return result
            except ValueError as e:
                return str(e)

    return 0


class TutorialWindow(QDialog):
    def __init__(self, parent=None):
        super(TutorialWindow, self).__init__(parent)
        self.setModal(True)
        self.setWindowTitle("Tutorial")
        self.setMinimumSize(600, 410)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog) 

        self.oldPos = None

            
        self.setStyleSheet('''
            QDialog {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                stop: 0 #303030, stop: 1 #505050);
                border: 1px solid rgba(255, 255, 255, 50);
                border-radius: 10px;
            }
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollArea QWidget {
                background-color: transparent;
            }
            QLabel {
                color: white;
                font-family: "Segoe UI";
                font-size: 16px;
                font-weight: normal;
                background-color: transparent;
            }

            QLabel[heading="true"] {
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton {
                background-color: #505050;
                color: white;
                font-family: "Segoe UI";
                font-size: 14px;
                border: 1px solid #707070;
                padding: 4px 10px;
            }
            QPushButton:hover {
                background-color: #707070;
            }
        ''')
        
        
        
        heading_label = QLabel("Using the Mouse:")
        heading_label.setProperty("heading", True)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 10, 10, 20)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        self._createTitleBar()

        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)

        self.scroll_area_contents = QWidget()
        self.scroll_area.setWidget(self.scroll_area_contents)

        self.scroll_area_layout = QVBoxLayout()
        self.scroll_area_layout.setContentsMargins(30, 30, 30, 30)
        self.scroll_area_layout.setSpacing(10)  


        self.scroll_area_contents.setLayout(self.scroll_area_layout)

        self.tutorial_text = [
            QLabel("<p>Welcome to the Calculator Tutorial! This calculator is designed to be user-friendly and easy to use.</p>"),
            QLabel("<p>You can perform calculations using either your mouse or your keyboard. Let's go through each option.</p>"),
            QLabel("<p><b>Using the Mouse:</b></p>"),
            QLabel("<ul>"
                "<li>To input numbers, click on the number buttons (0-9) on the calculator.</li>"
                "<li>To perform basic operations, click on the respective operation buttons:</li>"
                "<ul>"
                "<li>Addition (+): Click the '+' button.</li>"
                "<li>Subtraction (-): Click the '-' button.</li>"
                "<li>Multiplication (×): Click the '×' button.</li>"
                "<li>Division (÷): Click the '÷' button.</li>"
                "<li>Power (^): Click the '^' button.</li>"
                "<li>Logarithm (log): Click the 'log' button.</li>"
                "</ul>"
                "<li>To clear the input field, click the 'C' button.</li>"
                "<li>To evaluate the expression, click the '=' button.</li>"
                "</ul>"),
            QLabel("<p><b>Using the Keyboard:</b></p>"),
            QLabel("<ul>"
                "<li>To input numbers, press the number keys (0-9) on your keyboard.</li>"
                "<li>To perform basic operations, press the respective operation keys:</li>"
                "<ul>"
                "<li>Addition (+): Press the '+' key.</li>"
                "<li>Subtraction (-): Press the '-' key.</li>"
                "<li>Multiplication (×): Press the '*' key.</li>"
                "<li>Division (÷): Press the '/' key.</li>"
                "<li>Power (^): Press the '^' key.</li>"
                "<li>Logarithm (log): Type 'log' followed by the base, a comma, and the number, e.g., 'log10,100'.</li>"
                "</ul>"
                "<li>To clear the input field, press the 'C' key.</li>"
                "<li>To evaluate the expression, press the 'Enter' key.</li>"
                "</ul>"),
            QLabel("<p>You can move the calculator window by clicking and dragging the title bar. To close the tutorial window, click the 'X' button in the upper right corner or press the 'Esc' key on your keyboard.</p>"),
        ]

        
        for label in self.tutorial_text:
            label.setWordWrap(True)
            label.setAlignment(Qt.AlignJustify)
            self.scroll_area_layout.addWidget(label)
       
        self.layout.addStretch()

    def _createTitleBar(self):
        self.title_bar = QWidget(self)
        self.title_bar.setStyleSheet("""
            background-color: none;
            border: none;
        """)
        self.title_bar.setFixedHeight(40)
        self.title_bar_layout = QHBoxLayout()
        self.title_bar_layout.setContentsMargins(0, 0, 0, 0)
        self.title_label = QLabel("Calculator Tutorial")
        self.title_label.setStyleSheet("color: white; font-family: 'Segoe UI'; font-size: 16px;")
        self.title_bar_layout.addWidget(self.title_label)
        self.title_bar_layout.addStretch(1)
        self.close_button = QPushButton("X")
        self.close_button.setStyleSheet("""
            QPushButton {
            color: white;
            background-color: transparent;
            border: none;
            font-family: 'Segoe UI';
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
        self.display.textChanged.connect(self._adjust_font_size)

        self.show()

    

    def _createTitleBar(self):
        self.titleBar = QWidget()
        self.titleBar.setFixedHeight(30)

        titleBarLayout = QHBoxLayout()
        titleBarLayout.setContentsMargins(0, 0, 0, 0)  
        titleBarLayout.setSpacing(1)

        self.titleLabel = QLabel("Calculator")
        self.titleLabel.setStyleSheet("color: white; font-size: 14px;")
        titleBarLayout.addWidget(self.titleLabel)

        titleBarLayout.addStretch()
        

        
        self.helpButton = QPushButton("?")
        self.helpButton.setFixedSize(40, 30)
        self.helpButton.clicked.connect(self.showTutorial) 
        self.helpButton.setStyleSheet("background-color: transparent; border: none;")  
        titleBarLayout.addWidget(self.helpButton)

        self.minimizeButton = QPushButton("-")
        self.minimizeButton.setFixedSize(40, 30)
        self.minimizeButton.clicked.connect(self.showMinimized)
        titleBarLayout.addWidget(self.minimizeButton)
        

        self.closeButton = QPushButton("X")
        self.closeButton.setFixedSize(40, 30)
        self.closeButton.clicked.connect(self.close)
        titleBarLayout.addWidget(self.closeButton)

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
        self.display.setMaxLength(21)  
        self.display.setContentsMargins(0, 0, 0, 0)

    def _createButtons(self):
        self.buttons = {}
        buttonsLayout = QGridLayout()
        buttonsLayout.setHorizontalSpacing(1)  
        buttonsLayout.setVerticalSpacing(3)  
        
        
        
        buttons = {
            "(": (0, 0),
            ")": (0, 1),
            "C": (0, 2),
            "DEL": (0, 3),
            "x!": (1, 0),
            "x^y": (1, 1),
            "√x": (1, 2),
            "ln": (1, 3), 
            "7": (2, 0),
            "8": (2, 1),
            "9": (2, 2),
            "÷": (2, 3),  
            "4": (3, 0),
            "5": (3, 1),
            "6": (3, 2),
            "×": (3, 3),
            "1": (4, 0),
            "2": (4, 1),
            "3": (4, 2),
            "-": (4, 3),  
            ".": (5, 0),  
            "0": (5, 1),
            "=": (5, 2),  
            "+": (5, 3),  
        }
        
        self.tutorialButton = QPushButton("?")
        self.tutorialButton.clicked.connect(self._buttonClicked)



        for btnText, pos in buttons.items():
            button = QPushButton(btnText)
            button.setFont(QFont("Arial", 14, QFont.Bold))
            button.setFixedSize(72, 54) 
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
                """)  

            if btnText in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '?'}:
                button.setProperty('number', True)

            elif btnText in {'(', ')', 'x!', 'x^y', '√x', 'C', 'DEL', '-', '+', '÷', '×', 'ln'}:
                button.setProperty('other_button', True)

            button.clicked.connect(lambda ch, btn=btnText: self._buttonClicked(btn))
            if len(pos) == 4:
                row, col, rowspan, colspan = pos
                buttonsLayout.addWidget(button, row, col, rowspan, colspan)
            else:
                row, col = pos
                buttonsLayout.addWidget(button, row, col)

        self.generalLayout.addLayout(buttonsLayout)

        
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

    def _buttonClicked(self, button):
        
        print(f"Button clicked: {button}") 
        
        if button in {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "(", ")", "÷", "×", "-", "+"}:
            self.display.insert(button)
            self._adjust_font_size()
            current_length = len(self.display.text())
            if current_length > 15:
                new_font_size = 30 - (current_length - 15) * 2
                new_font_size = max(new_font_size, 10)  
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
                    new_font_size = max(new_font_size, 10) 
                    self.display.setStyleSheet(f"""
                        QLineEdit {{
                            background-color: #202020;
                            color: white;
                            font-size: {new_font_size}px;
                            border: none;
                            padding: 0 10px
                        }}
                    """)


            except Exception as e:
                self.display.setText(str(e))

                
        elif button == "C":
            self.display.clear()
            
        
            
        elif button == "DEL":
            self.display.backspace()
            
        elif button == "x!":
            try:
                text = self.display.text().replace("x!", "")
                if not text:
                    return
                number = int(text)
                if number > 170:
                    self.display.setText("Exceeds limit for x!")
                    return
                result = factorial(number)
                formatted_result = self._format_number(str(result))
                self.display.setText(formatted_result)
                self._adjust_font_size()    
                
                

                current_length = len(self.display.text())
                if current_length > 15:
                    new_font_size = 30 - (current_length - 15) * 2
                    new_font_size = max(new_font_size, 10)  
                    self.display.setStyleSheet(f"""
                        QLineEdit {{
                            background-color: #202020;
                            color: white;
                            font-size: {new_font_size}px;
                            border: none;
                            padding: 0 10px;
                        }}
                    """)
            except ValueError:
                self.display.setText("Invalid input for x!")
            except Exception as e:
                self.display.setText(str(e))    



                
        elif button == "x^y":
            self.display.insert("^")
            

            
        elif button == "?":
            print("Tutorial button clicked")
            self.showTutorial()


        elif button == "√x":
            try:
                text = self.display.text().replace("√x", "")
                if not text:
                    return
                number = float(text)
                result = sqrt(number)
                formatted_result = self._format_number(str(result))
                self.display.setText(formatted_result)
                self._adjust_font_size()

                current_length = len(self.display.text())
                if current_length > 15:
                    new_font_size = 30 - (current_length - 15) * 2
                    new_font_size = max(new_font_size, 10)
                    self.display.setStyleSheet(f"""
                        QLineEdit {{
                            background-color: #202020;
                            color: white;
                            font-size: {new_font_size}px;
                            border: none;
                            padding: 0 10px;
                        }}
                    """)
            except ValueError as e:
                self.display.setText(str(e))
            except Exception as e:
                self.display.setText("Invalid input for √x")

                
        elif button == "ln":
            text = self.display.text()
            if 'ln(' not in text:
                self.display.insert("ln()")
                cursor_position = self.display.cursorPosition()
                self.display.setCursorPosition(cursor_position - 1)
            elif ')' not in text:
                self.display.insert(")")
                cursor_position = self.display.cursorPosition()
                self.display.setCursorPosition(cursor_position)
            else:
                try:
                    result = custom_eval(text)
                    formatted_result = self._format_number(str(result))
                    self.display.setText(formatted_result)
                    self._adjust_font_size()

                    current_length = len(self.display.text())
                    if current_length > 15:
                        new_font_size = 30 - (current_length - 15) * 2
                        new_font_size = max(new_font_size, 10)
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
            self._adjust_font_size()  
        elif event.key() in {Qt.Key_Enter, Qt.Key_Return, Qt.Key_Enter - 1}:
            self._buttonClicked("=")
        elif key.lower() == "c":
            self._buttonClicked("C")
        elif event.key() == Qt.Key_Backspace:
            self._buttonClicked("DEL")
        elif event.key() == Qt.Key_Asterisk:
            self._buttonClicked("×")
        elif key.lower() == "s":
            self._buttonClicked("√x")
        elif key.lower() == "f":
            self._buttonClicked("x!")
        elif key.lower() == "l":
            self._buttonClicked("ln")
        elif key.lower() == "p":
            self._buttonClicked("x^y")

  
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
            new_font_size = 20

        
        self.display.setStyleSheet(f"""
            QLineEdit {{
                background-color: #202020;
                color: white;
                font-size: {new_font_size}px;
                border: 2px solid white;
                padding: 0 10px;
            }}
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    calc = Calculator()
    sys.exit(app.exec_())
