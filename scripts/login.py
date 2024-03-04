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
    def __init__(self) -> QWidget:                                      # -- Initiates the login widget
        super().__init__()
        self.initUI()

    def initUI(self) -> None:                                           # -- Initiates the Widgets
        self.layout = QVBoxLayout()
        self.userLayout = QHBoxLayout()
        self.passLayout = QHBoxLayout()
        self.btnLayout = QHBoxLayout()

        # Labels
        self.welcomeLabel = QLabel("WELCOME!")
        self.errorLabel = QLabel()
        self.userLabel = QLabel("Username: ")
        self.passLabel = QLabel("Password: ")

        # LineEdits
        self.userLine = QLineEdit()
        self.passLine = QLineEdit()

        # Buttons
        self.loginBtn = QPushButton('Login')
        self.cancelBtn = QPushButton('Cancel')

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
        
        # Button Connections
        self.cancelBtn.clicked.connect(lambda: sys.exit())
        self.loginBtn.clicked.connect(self.submitUser)

    def styleWidgets(self) -> None:                                     # -- Applies Styles to Stylesheets for Widgits
        pass
    
    def submitUser(self) -> None:                                       # -- Function that checks the input information against the Admin database for login
        queryData = DatabaseQueries().getMasterAdmin()
        user = self.userLine.text()
        userPass = self.passLine.text()
        cryptPass = EncryptPassword().encrypt(userPass)

        # Check username
        if user == queryData[1]:
            pass
        else:
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