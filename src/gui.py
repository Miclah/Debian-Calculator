#!/usr/bin/python3

##
# @file: gui.py
# @brief: GUI for IVS project 2.
# @author Michal Petrán
# @Created: 22-03-2023
# @Last Modified: 25-04-2023
##


# Import necessary libraries
import sys  # Provides access to some variables and functions used or maintained by the interpreter
import re  # Provides regular expression support for pattern matching in strings
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget, QGridLayout, QLabel, QHBoxLayout, QSizePolicy, QDialog, QScrollArea  # Import necessary PyQt5 widgets for building the GUI
from PyQt5.QtGui import QFont  # Import QFont for setting font properties
from PyQt5.QtCore import Qt  # Import QtCore for access to Qt's core non-GUI functionality
from math_lib import add, sub, mul, div  # Import basic math functions from custom math_lib module
from extended_math_lib import factorial, power, sqrt, ln  # Import extended math functions from custom extended_math_lib module


##
# @brief: Checks if the parentheses in the given string are valid
# @param s: String containing the expression
# @return Boolean: value indicating whether the parentheses are valid or not
#
def is_valid_parentheses(s):
    stack = [] # Initialize an empty stack
    for c in s:
        if c == '(': # If an opening parenthesis is found, add it to the stack
            stack.append(c)
        elif c == ')': # If a closing parenthesis is found
            if not stack: # If the stack is empty, parentheses are not balanced
                return False
            stack.pop() # Remove the last opening parenthesis from the stack
    return not stack # Return True if the stack is empty, otherwise False
 

##
# @brief: Custom evaluation function for mathematical expressions
# @param expression: String containing the mathematical expression
# @return: The result of the evaluated expression
# @exception ValueError: If the input format is invalid or unsupported
#
def custom_eval(expression):
    
    ##
    # @brief: Applies an operator to the given operands
    # @param operators: List of operators
    # @param values: List of values (operands)
    # @exception ValueError: If the operation is unsupported
    #
    def apply_operator(operators, values):
        operator = operators.pop() # Remove the last operator from the list
        if operator == 'u-':
            right = values.pop() # Remove the last value from the list
            result = -right # Negate the value
            values.append(result) # Add the negated value back to the list
        else:
            right = values.pop() # Remove the last value as the right operand   
            left = values.pop() # Remove the second-last value as the left operand
            if operator == '^':
                # Handle cases with negative exponents
                if right < 0 and left > 0:
                    raise ValueError("Neg. exp. not allowed")
                if right < 0:
                    raise ValueError("Neg. exp. not allowed")
                if left < 0 and int(right) % 2 != 0:
                    result = -power(-left, right)
                else:
                    result = power(left, right)
            # Apply the operator to the operands and store the result
            else:
                result = operations[operator](left, right)
                
            # If the result is an integer, store it as an int instead of float
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            values.append(result) # Add the result back to the list

    ##
    # @brief: Compares the precedence of two operators
    # @param op1: First operator
    # @param op2: Second operator
    # @return: Boolean value indicating if op1 has greater or equal precedence than op2
    #
    def greater_precedence(op1, op2):
        precedences = {'+': 1, '-': 1, '×': 2, '÷': 2, '^': 3, 'u-': 4}
        return precedences[op1] >= precedences[op2]


    # Define the supported binary operations
    operations = {
        '+': add,
        '-': sub,
        '×': mul,
        '÷': div,
        '^': power,
    }

    # Define the supported single-operand operations
    single_operand_operations = {
        'x!': factorial,
        '√x': sqrt,
        'ln': ln
    }
    
    # Check if there are any invalid single-operand operations
    if re.search(r'\d+\s*(ln|√x|x!)', expression):
        raise ValueError("Invalid input format.")

    # Check if the input expression is valid
    if not re.match(r'^\s*[\-+\(\)]?(\d+(\.\d+)?|\.\d+|\()+\s*([\+\-\*/\^\(\)×÷]+\s*[\-+\(\)]?\s*(\d+(\.\d+)?|\.\d+|\()+\s*)*\)?$', expression) or not is_valid_parentheses(expression):
        for operator, func in single_operand_operations.items():
            if operator + '(' in expression:
                if ')' in expression and expression.index(')') > expression.index(operator + '('):
                    content = expression[expression.index(operator + '(') + len(operator + '('): expression.index(')')]
                    if re.match(r'-?\d+\.?\d*', content):
                        a = float(content)
                        return func(a)
                    else:   
                        raise ValueError("Invalid input format.")
                else:
                    raise ValueError("Invalid input format.")
        raise ValueError("Incorrect input")
    
   
    expression = expression.lstrip('+')  # Remove leading '+' sign if present
    
    expression = re.sub(r'\s+', '', expression) # Remove whitespaces from the expression

    # Tokenize the expression into operands, operators, and parentheses
    tokens = re.findall(r'\d*\.\d+|\d+|[-+×÷^()]', expression.replace(' ', ''))
    values = [] # Initialize a list to store the values (operands)
    operators = [] # Initialize a list to store the operators
    
    previous_token = None # Keep track of the previous token

    # Iterate through the tokens
    for token in tokens:
        # Handle unary minus (negative sign) and binary minus (subtraction)
        if token == '-' and (not values or (operators and operators[-1] in '+-×÷^(') or (previous_token and previous_token in '+-×÷^(')):
            token = 'u-' # Replace '-' with 'u-' for unary minus
            operators.append(token) # Add the unary minus to the operators list
            
        elif token == '-' and (values and operators and operators[-1] not in '+-×÷^('):
            operators.append(token) # Add the binary minus to the operators list
            
        # Handle numbers (operands)
        elif token.replace('.', '', 1).replace('-', '', 1).isdigit():
            value = float(token)
            if operators and operators[-1] == 'u-':
                value = -value
                operators.pop()
            values.append(value)
        
        # Handle opening parentheses
        elif token == '(':
            operators.append(token) # Add the opening parenthesis to the operators list
        
        # Handle closing parentheses
        elif token == ')':
            # Apply operators within parentheses until the opening parenthesis is reached
            while operators and operators[-1] != '(':
                apply_operator(operators, values) # Apply the operator to the operands
            operators.pop() # Remove the opening parenthesis from the operators list
            
        # Handle binary operators (+, -, ×, ÷, ^)
        else:
            # Apply operators in the operators list with greater or equal precedence than the current operator
            while (operators and operators[-1] != '(' and
                    greater_precedence(operators[-1], token) and token != 'u-'):
                apply_operator(operators, values)
            operators.append(token) # Add the current operator to the operators list
            
        previous_token = token # Update the previous token

    # Continue applying operators until the operators list is empty
    while operators:
        apply_operator(operators, values)

    result = values[0] # Get the final result
    
    # Check if the result is too large
    if abs(result) > 1e300:
        raise ValueError("Result is too large.")

    # Return the final result
    return result



##
# @brief: Provides the tutorial window for the Calculator application
# @param QDialog: Parent class
#
class TutorialWindow(QDialog):
    ##
    # @brief: Constructor of the TutorialWindow class, initializes the tutorial window
    # @param self: Instance of the TutorialWindow class
    # @param parent: Parent widget, default is None
    #
    def __init__(self, parent=None):
        # Call the QDialog constructor and pass the parent argument
        super(TutorialWindow, self).__init__(parent)
        
        # Configure the window properties
        self.setModal(True) # Make the window modal (blocks input to other windows)
        self.setWindowTitle("Tutorial") # Set the window title
        self.setMinimumSize(600, 410) # Set the minimum window size
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) # Set the size policy for the window
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog) # Set window flags to make it frameless and a dialog


        self.oldPos = None # Initialize oldPos to None; used for tracking mouse position when moving the window

        # Apply the window stylesheet for custom appearance
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

        # Create the window layout and add the title bar
        self.layout = QVBoxLayout() # Set up the main window layout as QVBoxLayout
        self.layout.setContentsMargins(20, 10, 10, 20)
        self.layout.setSpacing(0)
        self.setLayout(self.layout) # Apply the layout to the window

        self._createTitleBar() # Create and add the title bar to the layout
        
        # Create the scroll area and its contents
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)

        self.scroll_area_contents = QWidget()
        self.scroll_area.setWidget(self.scroll_area_contents)

        self.scroll_area_layout = QVBoxLayout()
        self.scroll_area_layout.setContentsMargins(30, 30, 30, 30)
        self.scroll_area_layout.setSpacing(10)  


        self.scroll_area_contents.setLayout(self.scroll_area_layout)

        # Create the scroll area and its contents
        self.tutorial_text = [
                QLabel("<p>Welcome to the Calculator Tutorial!</p>"),

                QLabel("<p><b>Using the Mouse:</b></p>"),

                QLabel("<ul>"
                    "<li><b>Input numbers:</b> Click on the number buttons (0-9) on the calculator.</li>"
                    "<li><b>Basic operations:</b> Click on the respective operation buttons:</li>"
                    "<ul>"
                    "<li>Addition (+): Click the '+' button.</li>"
                    "<li>Subtraction (-): Click the '-' button.</li>"
                    "<li>Multiplication (×): Click the '×' button.</li>"
                    "<li>Division (÷): Click the '÷' button.</li>"
                    "</ul>"
                    "<li><b>Advanced operations:</b></li>"
                    "<ul>"
                    "<li>Factorial (x!): Click the 'x!' button.</li>"
                    "<li>Power (x^y): Click the 'x^y' button.</li>"
                    "<li>Square root ( √x): Click the ' √x' button.</li>"
                    "<li>Natural logarithm (ln): Click the 'ln' button.</li>"
                    "</ul>"
                    "<li><b>Parenthesis:</b> Click the '(' and ')' buttons to input parentheses in the expression.</li>"
                    "<li><b>Clear input:</b> Click the 'C' button to clear the input field.</li>"
                    "<li><b>Delete:</b> Click the 'DEL' button to remove the last character in the input field.</li>"
                    "<li><b>Evaluate:</b> Click the '=' button to calculate the result of the expression.</li>"
                    "</ul>"),

                QLabel("<p><b>Using the Keyboard:</b></p>"),

                QLabel("<ul>"
                    "<li><b>Input numbers:</b> Press the number keys (0-9) on your keyboard.</li>"
                    "<li><b>Basic operations:</b> Press the respective operation keys:</li>"
                    "<ul>"
                    "<li>Addition (+): Press the '+' key.</li>"
                    "<li>Subtraction (-): Press the '-' key.</li>"
                    "<li>Multiplication (×): Press the '*' key (it will appear as '×' in the input window).</li>"
                    "<li>Division (÷): Press the '/' key (it will appear as '÷' in the input window).</li>"
                    "</ul>"
                    "<li><b>Advanced operations:</b></li>"
                    "<ul>"
                    "<li>Factorial (x!): Press the 'f' key.</li>"
                    "<li>Power (x^y): Press the 'p' key.</li>"
                    "<li>Square root ( √x): Press the 's' key.</li>"
                    "<li>Natural logarithm (ln): Press the 'l' key.</li>"
                    "</ul>"
                    "<li><b>Parenthesis:</b> Press the '(' and ')' keys to input parentheses in the expression.</li>"
                    "<li><b>Clear input:</b> Press the 'C' key to clear the input field.</li>"
                    "<li><b>Delete:</b> Press the 'Backspace' key to remove the last character in the input field.</li>"
                    "<li><b>Evaluate:</b> Press the 'Enter' key to calculate the result of the expression.</li>"
                    "</ul>"),
                
                QLabel("<p>You can move the calculator/calculator tutorial window and the by clicking and dragging the title bar. To close the calculator, click the 'X' button in the upper right corner. To access this tutorial at any time, click the '?' button in the title bar.</p>"),
        ]


        # Configure tutorial text labels and add them to the scroll area layout
        for label in self.tutorial_text:
            label.setWordWrap(True) # Enable word wrapping for the label
            label.setAlignment(Qt.AlignJustify) # Set label alignment to justify
            self.scroll_area_layout.addWidget(label) # Add the label to the scroll area layout
       
        self.layout.addStretch() # Add a stretch to the layout to fill any extra space

    ##
    # @brief: Creates the custom title bar for the tutorial window
    # @param self: Instance of the TutorialWindow class
    #
    def _createTitleBar(self):
        self.title_bar = QWidget(self) # Create a new QWidget instance for the title bar
        
        # Set stylesheet for the title bar
        self.title_bar.setStyleSheet("""
            background-color: none;
            border: none;
        """)
        
        self.title_bar.setFixedHeight(40)# Set a fixed height for the title bar
        
        # Create the title bar layout and configure its contents
        self.title_bar_layout = QHBoxLayout() # Set up the title bar layout as QHBoxLayout
        self.title_bar_layout.setContentsMargins(0, 0, 0, 0)
        self.title_label = QLabel("Calculator Tutorial") # Create a QLabel for the title text
        
        self.title_label.setStyleSheet("color: white; font-family: 'Segoe UI'; font-size: 16px;")
        self.title_bar_layout.addWidget(self.title_label) # Add the title label to the title bar layout
        self.title_bar_layout.addStretch(1) # Add a stretch to fill any extra space in the title bar layout
        
        # Create and configure the close button
        self.close_button = QPushButton("X") # Create and configure the close button
        
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
        
        self.close_button.setFixedSize(40, 30) # Set a fixed size for the close button
        self.close_button.clicked.connect(self.close) # Connect the button's click event to the close method
        self.title_bar_layout.addWidget(self.close_button) # Add the close button to the title bar layout
        
        # Apply the title bar layout and add it to the main layout
        self.title_bar.setLayout(self.title_bar_layout)
        self.layout.addWidget(self.title_bar)

    ##
    # @brief: Handles mouse press event for dragging the window
    # @param self: Instance of the TutorialWindow class
    # @param event: The QMouseEvent object
    #
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos() # Store the initial mouse press position

    ##
    # @brief: Handles mouse move event for dragging the window
    # @param self: Instance of the TutorialWindow class
    # @param event: The QMouseEvent object
    #
    def mouseMoveEvent(self, event):
        # If the left mouse button is pressed and the initial position is set
        if event.buttons() == Qt.LeftButton and self.oldPos is not None:
            
            delta = event.globalPos() - self.oldPos # Calculate the position difference
            self.move(self.x() + delta.x(), self.y() + delta.y()) # Move the tutorial window based on the position difference
            self.oldPos = event.globalPos() # Update the initial position

    ##
    # @brief: Handles mouse release event for dragging the window
    # @param self: Instance of the TutorialWindow class
    # @param event: The QMouseEvent object
    #
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = None # Clear the initial position when the left mouse button is released





##
# @brief: Main calculator window
# @param QMainWindow: Parent class
class Calculator(QMainWindow):
    ##
    # @brief: Initialize the Calculator instance
    # @param self: Instance of the Calculator class
    #
    def __init__(self):
        super().__init__() # Call the QMainWindow constructor
        self.setObjectName("CalculatorWidget")

        self.setFixedSize(320, 480)  # Set a fixed size for the calculator window
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)  # Set window flags for a frameless window


        self.generalLayout = QVBoxLayout()  # Set up the main window layout as QVBoxLayout
        self._centralWidget = QWidget(self)  # Create a central QWidget instance
        self.setCentralWidget(self._centralWidget)  # Set the central widget for the QMainWindow
        self._centralWidget.setLayout(self.generalLayout)  # Apply the layout to the central widget
        self._createTitleBar()  # Create and add the title bar to the layout

        self._createDisplay()  # Create the display for the calculator
        self._createButtons()  # Create the buttons for the calculator
        self.new_input = False  # Initialize a flag to track whether a new input is being entered
        self.x_y_base = None  # Initialize a variable to store the x and y base values for certain operations
        self.display.textChanged.connect(self._adjust_font_size)  # Connect the textChanged signal to adjust the font size

        self.show()  # Show the calculator window

    
    ##
    # @brief: Create the custom title bar for the calculator window
    # @param self: Instance of the Calculator class
    #
    def _createTitleBar(self):
        # Create the title bar widget and set its fixed height
        self.titleBar = QWidget()
        self.titleBar.setFixedHeight(30)

        # Create a horizontal layout for the title bar and set its margins and spacing
        titleBarLayout = QHBoxLayout()
        titleBarLayout.setContentsMargins(0, 0, 0, 0)  
        titleBarLayout.setSpacing(1)

        # Create a title label and set its style
        self.titleLabel = QLabel("Calculator")
        self.titleLabel.setStyleSheet("color: white; font-size: 14px;") 
        titleBarLayout.addWidget(self.titleLabel)

        # Add stretch to push the other buttons to the right side of the title bar
        titleBarLayout.addStretch()
        

        # Create and style the help button, and connect it to the showTutorial function
        self.helpButton = QPushButton("?")
        self.helpButton.setFixedSize(40, 30) # Set a fixed size for the help button
        self.helpButton.clicked.connect(self.showTutorial) 
        self.helpButton.setStyleSheet("background-color: transparent; border: none;") # Set the style for the help button
        titleBarLayout.addWidget(self.helpButton) # Add the help button to the title bar layout

        # Create and style the minimize button, and connect it to the showMinimized function
        self.minimizeButton = QPushButton("-")
        self.minimizeButton.setFixedSize(40, 30) # Set a fixed size for the minimize button
        self.minimizeButton.clicked.connect(self.showMinimized) 
        titleBarLayout.addWidget(self.minimizeButton) # Add the minimize button to the title bar layout
        
        # Create and style the close button, and connect it to the close function
        self.closeButton = QPushButton("X")
        self.closeButton.setFixedSize(40, 30) # Set a fixed size for the close button
        self.closeButton.clicked.connect(self.close) # Connect the button's click event to the close method
        titleBarLayout.addWidget(self.closeButton) # Add the close button to the title bar layout

        # Set the style for the help button when hovered over
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

        # Set the style for the minimize button when hovered over
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

        # Set the cursor style for the minimize button
        self.minimizeButton.setCursor(Qt.PointingHandCursor)

        # Set the style for the close button when hovered over
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

        self.closeButton.setCursor(Qt.PointingHandCursor) # Set the cursor style for the close button

        self.titleBar.setLayout(titleBarLayout) # Set the layout for the title bar widget
        
        self.generalLayout.addWidget(self.titleBar) # Add the title bar widget to the main window layout
        
    ##
    # @brief: Create the display for the calculator
    # @param self: Instance of the Calculator class
    #    
    def _createDisplay(self):
        # Create the display QLineEdit and set its fixed height
        self.display = QLineEdit()
        self.display.setFixedHeight(75) 
        
        # Configure the display properties
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.generalLayout.addWidget(self.display)
        
        
        # Set the style for the calculator
        self.setStyleSheet("""
            #CalculatorWidget {
                background-color: #202020;
                border: 1px solid #FFA07A;
                border-radius: 5px;
                padding: 1px;
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
                border: 2px solid white;
                border-radius: 0;
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
        
        
        self.display.setMaxLength(21) # Set the maximum length of the display
        self.display.setContentsMargins(0, 0, 0, 0)

    ##
    # @brief: Create the buttons for the calculator and add them to the layout
    # @param self: Instance of the Calculator class
    #
    def _createButtons(self):
        
        self.buttons = {}
        buttonsLayout = QGridLayout() # Set up a grid layout for the buttons
        buttonsLayout.setHorizontalSpacing(3) # Set horizontal spacing between buttons
        buttonsLayout.setVerticalSpacing(3) # Set vertical spacing between buttons
        
        # Dictionary containing button text and grid positions
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
        
        # Set up the tutorial button and connect it to the _buttonClicked method
        self.tutorialButton = QPushButton("?")
        self.tutorialButton.clicked.connect(self._buttonClicked)


        # Loop through the buttons dictionary and create each button with its properties
        for btnText, pos in buttons.items():
            
            button = QPushButton(btnText) # Create the button
            button.setFont(QFont("Arial", 14, QFont.Bold)) # Set the font for the button
            button.setFixedSize(72, 54) # Set the button size
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) # Set the button size policy
            
            # Set the 'operator' property for the main arithmetic operator buttons
            if btnText in {'-', '+', '÷', '×'}:
                button.setProperty('operator', True)

            # Set the 'equal_button' property and style for the equal button
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

            # Set the 'number' property for the number buttons and the tutorial button
            if btnText in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '?'}:
                button.setProperty('number', True)

            # Set the 'other_button' property for the remaining buttons
            elif btnText in {'(', ')', 'x!', 'x^y', '√x', 'C', 'DEL', '-', '+', '÷', '×', 'ln'}:
                button.setProperty('other_button', True)

            # Connect the button click to the _buttonClicked method
            button.clicked.connect(lambda ch, btn=btnText: self._buttonClicked(btn))
            
            # Add the button to the grid layout
            if len(pos) == 4:
                row, col, rowspan, colspan = pos
                buttonsLayout.addWidget(button, row, col, rowspan, colspan)
            else:
                row, col = pos
                buttonsLayout.addWidget(button, row, col)

        # Add the buttons grid layout to the general layout
        self.generalLayout.addLayout(buttonsLayout)


    ##
    # @brief: Handle the mouse press event for dragging the calculator window
    # @param self: Instance of the Calculator class
    # @param event: QMouseEvent containing information about the mouse press event
    #    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos() # Store the initial mouse press position

    ##
    # @brief: Handle the mouse move event for dragging the calculator window
    # @param self: Instance of the Calculator class
    # @param event: QMouseEvent containing information about the mouse move event
    #
    def mouseMoveEvent(self, event):
        # If the left mouse button is pressed and the initial position is set
        if event.buttons() == Qt.LeftButton and self.oldPos is not None:
            delta = event.globalPos() - self.oldPos# Calculate the position difference
            self.move(self.x() + delta.x(), self.y() + delta.y()) # Move the calculator window based on the position difference
            self.oldPos = event.globalPos() # Update the initial position
    
    ##
    # @brief: Handle the mouse release event for dragging the calculator window
    # @param event: QMouseEvent containing information about the mouse release event
    #
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = None # Clear the initial position when the left mouse button is released

    ##
    # @brief: Handles button clicks and performs the corresponding operations
    # @param self: The instance of the class
    # @param button: The button text representing the action to be performed
    # @exception ValueError: Raised when an invalid input is encountered
    # @exception Exception: Raised for other unexpected exceptions
    #
    def _buttonClicked(self, button):
        
        # If the clicked button is a number, decimal point, parentheses or an operator
        if button in {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "(", ")", "÷", "×", "-", "+"}:
            
            self.display.insert(button) # Add the button text to the display
            self._adjust_font_size() # Adjust the font size based on the display content
            current_length = len(self.display.text()) # Get the current length of the display text
            
            # If the display text length exceeds 15 characters, reduce the font size accordingly
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

        # If the clicked button is the equal sign
        elif button == "=":
            try:
                text = self.display.text() # Get the current display text
                result = custom_eval(text) # Evaluate the expression in the display
                formatted_result = self._format_number(str(result)) # Format the result
                self.display.setText(formatted_result) # Set the formatted result to the display
                self._adjust_font_size() # Adjust the font size based on the new display content

                # If the display text length exceeds 15 characters, reduce the font size accordingly
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
            # Handle value errors and display an error message
            except ValueError as e:
                self.display.setText(str(e))
            # Handle other exceptions and display an error message
            except Exception as e:
                self.display.setText(str(e))

        # If the clicked button is the clear button
        elif button == "C":
            self.display.clear() # Clear the display
            
        # If the clicked button is the delete button    
        elif button == "DEL":
            self.display.backspace() # Delete the last character in the display
            
        # If the clicked button is the factorial button
        elif button == "x!":
            try:
                text = self.display.text().replace("x!", "") # Remove the factorial symbol from the display text
                if not text:
                    return
                number = int(text) # Convert the text to an integer
                
                # If the input is too large for calculating factorial, display an error message
                if number > 170:
                    self.display.setText("Exceeds limit for x!")
                    return
                
                result = factorial(number) # Calculate the factorial of the input number
                formatted_result = self._format_number(str(result)) # Format the result
                self.display.setText(formatted_result) # Set the formatted result to the display
                self._adjust_font_size() # Adjust the font size based on the new display content
                
                # If the display text length exceeds 15 characters, reduce the font size accordingly
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
            # Handle value errors and display an error message
            except ValueError:
                self.display.setText("Invalid input for x!")
            # Handle other exceptions and display an error message
            except Exception as e:
                self.display.setText(str(e))    

        # If the clicked button is the power button button
        elif button == "x^y":
            self.display.insert("^") # Insert the caret (^) symbol for exponentiation
        
        # If the clicked button is the "?" button
        elif button == "?":
            self.showTutorial() # Show the tutorial

        # If the clicked button is the "√x" button
        elif button == "√x":
            try:
                text = self.display.text().replace("√x", "") # Remove the square root symbol from the display text
                if not text:
                    return
                number = float(text) # Convert the text to a float and calculate the square root
                result = sqrt(number)
                # Check if the result is a valid number
                if not isinstance(result, (int, float)):
                    self.display.setText("Invalid input for √x")
                    return
                formatted_result = self._format_number(str(result)) # Format the result and update the display
                self.display.setText(formatted_result)
                self._adjust_font_size()

                # If the display text length exceeds 15 characters, reduce the font size accordingly
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
            # Handle value errors and display an error message
            except ValueError as e:
                self.display.setText(str(e))
            # Handle other exceptions and display an error message
            except Exception as e:
                self.display.setText("Invalid input for √x")

        # If the clicked button is the "ln" button  
        elif button == "ln":
            text = self.display.text()
            # Check if the ln function is not already in the display text
            if 'ln(' not in text:
                self.display.insert("ln()")
                cursor_position = self.display.cursorPosition() # Set the cursor position within the parentheses
                self.display.setCursorPosition(cursor_position - 1)
                
            # If the closing parenthesis is missing, add it
            elif ')' not in text:
                self.display.insert(")")
                cursor_position = self.display.cursorPosition()
                self.display.setCursorPosition(cursor_position)
            
            # If the expression is complete, evaluate it
            else:
                try:
                    result = custom_eval(text)
                    formatted_result = self._format_number(str(result))
                    self.display.setText(formatted_result)
                    self._adjust_font_size()

                    # If the display text length exceeds 15 characters, reduce the font size accordingly
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
                # Handle value errors and display an error message
                except Exception as e:
                    self.display.setText(str(e))

    ##
    # @brief: Handles key press events for the calculator
    # @param self: The instance of the class
    # @param event: The event object containing information about the key press
    #
    def keyPressEvent(self, event):
        key = event.text() # Get the text of the pressed key

        # If the key is a digit, decimal, or arithmetic symbol, insert it into the display
        if key in '0123456789.+-()':
            self.display.insert(key)
            self._adjust_font_size()  
        
        # If the key is an asterisk, insert the multiplication symbol
        elif event.key() == Qt.Key_Asterisk:
            self.display.insert('×')
            
        # If the key is a forward slash, insert the division symbol
        elif event.key() == Qt.Key_Slash:
            self.display.insert('÷')
        
        # If the key is enter or return, trigger the equals button
        elif event.key() in {Qt.Key_Enter, Qt.Key_Return, Qt.Key_Enter - 1}:
            self._buttonClicked("=")
            
        # If the key is 'C' or 'c', trigger the clear button
        elif key.lower() == "c":
            self._buttonClicked("C")
            
        # If the key is backspace, trigger the delete button
        elif event.key() == Qt.Key_Backspace:
            self._buttonClicked("DEL")
            
        # If the key is 'S' or 's', trigger the square root button
        elif key.lower() == "s":
            self._buttonClicked("√x")
        
        # If the key is 'F' or 'f', trigger the factorial button
        elif key.lower() == "f":
            self._buttonClicked("x!")
            
        # If the key is 'L' or 'l', trigger the natural logarithm button
        elif key.lower() == "l":
            self._buttonClicked("ln")
            
        # If the key is 'P' or 'p', trigger the power button
        elif key.lower() == "p":
            self._buttonClicked("x^y")


    ##
    # @brief Show the tutorial window
    # @param self The instance of the class
    #
    def showTutorial(self):
        # Create a new instance of the tutorial window and center it on the screen
        tutorialWindow = TutorialWindow(self)
        tutorialWindow.move(self.geometry().center() - tutorialWindow.rect().center())
        tutorialWindow.exec_() # Execute the tutorial window event loop



    ##
    # @brief: Format a number string with thousands separators
    # @param self: The instance of the class
    # @param number: The number string to format
    # @return: The formatted number string
    #
    def _format_number(self, number):
        # If the number has a decimal point, format the integer and decimal parts separately
        if '.' in number:
            parts = number.split('.')
            formatted_integer = '{:,}'.format(int(parts[0]))
            return f"{formatted_integer}.{parts[1]}"
        
        # If the number is an integer, format it with thousands separators
        else:
            return '{:,}'.format(int(number))
        
    
    ##
    # @brief: Adjusts the font size of the display based on the length of the text
    # @param self: The instance of the class
    #
    def _adjust_font_size(self):
        current_length = len(self.display.text()) # Get the current length of the display text
        
        # Determine the appropriate font size based on the length of the display text
        if current_length <= 17:
            new_font_size = 30
        elif 17 < current_length < 20:
            new_font_size = 28
        elif 20 < current_length <= 23:
            new_font_size = 23
        else:
            new_font_size = 20

        # Apply the new font size and style to the display
        self.display.setStyleSheet(f"""
            QLineEdit {{
                background-color: #202020;
                color: white;
                font-size: {new_font_size}px;
                border: 2px solid white;
                padding: 0 10px;
                text-align: right;
            }}
        """)


##
# @brief: The main entry point for the calculator application
#
if __name__ == "__main__":
    app = QApplication(sys.argv) # Create a QApplication instance with command-line arguments
    app.setStyle("Fusion") # Set the application style to "Fusion"
    calc = Calculator() # Create a Calculator instance
    sys.exit(app.exec_()) # Start the application event loop and exit with the returned exit code
