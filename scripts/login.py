#!  python3
#!  login.py -- App for logging into main Activities Application

import sys

from PyQt6.QtWidgets import QLineEdit, QPushButton, QLabel, QWidget, QApplication, QVBoxLayout, QHBoxLayout

if __name__ != "__main__":
    from scripts.encrypt_password import EncryptPassword 
    from scripts.database_queries import DatabaseQueries
else:
    from encrypt_password import EncryptPassword
    from database_queries import DatabaseQueries


class Login(QWidget): 
    def __init__(self) -> None:                     # -- Initiates the Application
        super().__init__()
        self.initUI()
        self.applyLayouts()
        self.setButtonConnections()
        self.applyStylesheets()

    def initUI(self) -> None:                       # -- Initiates the Widgets
        # Labels
        self.welcomeLabel: QWidget = QLabel("WELCOME!")
        self.errorLabel: QWidget = QLabel()
        self.userLabel: QWidget = QLabel("Username: ")
        self.passLabel: QWidget = QLabel("Password: ")

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

        # Add Widgets to layouts
        self.layout.addWidget(self.welcomeLabel)
        self.userLayout.addWidget(self.userLabel)
        self.userLayout.addWidget(self.userLine)
        self.layout.addLayout(self.userLayout)
        self.passLayout.addWidget(self.passLabel)
        self.passLayout.addWidget(self.passLine)
        self.layout.addLayout(self.passLayout)
        self.btnLayout.addWidget(self.cancelBtn)
        self.btnLayout.addWidget(self.loginBtn)
        self.layout.addLayout(self.btnLayout)
        self.layout.addWidget(self.errorLabel)

        # Add layouts to main layout
        self.setLayout(self.layout)
    
    def setButtonConnections(self) -> None:         # -- Establishes connections between buttons and functions
        # Button Connections
        self.cancelBtn.clicked.connect(lambda: sys.exit())
        self.loginBtn.clicked.connect(self.submitUser)

    def applyStylesheets(self) -> None:             # -- Applies Styles to Stylesheets for Widgits
        pass
    
    def submitUser(self) -> None:                   # -- Checks the input information against the Admin database for login
        queryData: tuple = DatabaseQueries("Admin").getMasterAdmin()
        user: str = self.userLine.text()
        userPass: str = self.passLine.text()
        cryptPass: str = EncryptPassword().encrypt(userPass)

        # Check username
        if user != queryData[1]:
            self.errorLabel.setText("Username is incorrect!")
            return 
        
        # Check Password
        if cryptPass == queryData[2]:
            self.errorLabel.setText("Login Successful")
        else:
            self.errorLabel.setText("Your password is incorrect")
        
          
if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = Login()
    sys.exit(app.exec())