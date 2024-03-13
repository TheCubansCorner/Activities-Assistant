#!  python3
#!  login.py -- App for logging into main Activities Application

import sys, os

from PyQt6.QtWidgets import QLineEdit, QPushButton, QLabel, QWidget, QApplication, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon, QCursor


from encrypt_password import EncryptPassword
from database_queries import DatabaseQueries
from main_menu import MainWindow


class Login(QWidget): 
    def __init__(self) -> None:                     # -- Initiates the Application
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_InputMethodTransparent)
        self.setFixedSize(225, 450)
        self.setWindowIcon(QIcon(os.path.join("app_icons", "fec2.png")))
        self.setWindowTitle("LOGIN")
        self.initUI()
        self.applyLayouts()
        self.setButtonConnections()
        self.applyStylesheets()

    def initUI(self) -> None:                       # -- Initiates the Widgets
        # Labels
        self.welcomeLabel: QWidget = QLabel()
        self.errorLabel: QWidget = QLabel()
        self.userLabel: QWidget = QLabel("Username:")
        self.passLabel: QWidget = QLabel("Password:")

        # LineEdits
        self.userLine: QWidget = QLineEdit()
        self.passLine: QWidget = QLineEdit()
        
        # Buttons
        self.loginBtn: QWidget = QPushButton('Login')
        self.cancelBtn: QWidget = QPushButton('Cancel')

    def applyLayouts(self) -> None:                 # -- Sets Widgets to layouts and applies layouts
        # Create layouts
        self.layout = QVBoxLayout()
        self.userLayout = QHBoxLayout()
        self.passLayout = QHBoxLayout()
        self.btnLayout = QHBoxLayout()

       # self.passLine.setEchoMode(QLineEdit.Password)

        # Add Widgets to layouts
        self.layout.addWidget(self.welcomeLabel, alignment = Qt.AlignmentFlag.AlignCenter)
        self.userLayout.addWidget(self.userLabel, alignment = Qt.AlignmentFlag.AlignLeading)
        self.userLayout.addWidget(self.userLine, alignment = Qt.AlignmentFlag.AlignCenter)
        self.layout.addLayout(self.userLayout)
        self.passLayout.addWidget(self.passLabel, alignment = Qt.AlignmentFlag.AlignCenter)
        self.passLayout.addWidget(self.passLine, alignment = Qt.AlignmentFlag.AlignCenter)
        self.layout.addLayout(self.passLayout)
        self.btnLayout.addWidget(self.cancelBtn)
        self.btnLayout.addWidget(self.loginBtn)
        self.layout.addLayout(self.btnLayout)
        self.layout.addWidget(self.errorLabel, alignment = Qt.AlignmentFlag.AlignCenter)

        # Add layouts to main layout
        self.setLayout(self.layout)
    
    def setButtonConnections(self) -> None:         # -- Establishes connections between buttons and functions
        # Button Connections
        self.cancelBtn.clicked.connect(lambda: sys.exit())
        self.loginBtn.clicked.connect(self.submitUser)

    def applyStylesheets(self) -> None:             # -- Applies Styles to Stylesheets for Widgits
        # Applies individual adjustments
        self.passLine.setEchoMode(QLineEdit.EchoMode.Password)
        self.welcomeLabel.setPixmap(QPixmap(os.path.join("app_icons", "fec.png")).scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))
        self.loginBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.cancelBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Sets classes for stylesheets
        self.welcomeLabel.setProperty("class", "welcome")
        self.errorLabel.setProperty("class", "error")
        self.loginBtn.setProperty("class", "button")
        self.cancelBtn.setProperty("class", "button")
        self.userLine.setProperty("class", "userline")
        self.passLine.setProperty("class", "passlines")
        self.userLabel.setProperty("class", "userlabel")
        self.passLabel.setProperty("class", "passlabel")
        self.userLayout.setProperty("class", "userlayout")
        self.passLayout.setProperty("class", "passLayout")

        # Applies app specific stylesheet
        with open(os.path.join("stylesheets", "login.css")) as file:
            self.setStyleSheet(file.read())
    
    def submitUser(self) -> None:                   # -- Checks the input information against the Admin database for login
        user: str = self.userLine.text()
        userPass: str = self.passLine.text()
        print(user, userPass)
        # Verify that informaiton provided is not an empty string
        if user == "" and userPass == "":
            self.errorLabel.setText("      You must input a\nUsername and Password")
            return 
        
        cryptPass: str = EncryptPassword().encrypt(userPass)
        queryData: tuple = DatabaseQueries("admin").adminLogin(user)

        # Verify Password
        if queryData:
            if cryptPass == queryData[2] and user == queryData[1]:
                print(queryData, cryptPass)
                self.app = MainWindow(queryData)
                self.close()
        else:
            self.errorLabel.setText("  Either your Username\nor Password is Incorrect")
        
          
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    with open(os.path.join("stylesheets", "main-style.css"), "r") as file:
        app.setStyleSheet(file.read())

    login = Login()
    login.show()
    sys.exit(app.exec())