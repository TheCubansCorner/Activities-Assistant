#! pthon3
#! add_new_resident.py -- Window for adding residents to the database

import sys, os, shutil
from datetime import datetime

from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QComboBox, QPushButton, QFileDialog
from PyQt6.QtWidgets import QLabel, QDateEdit, QVBoxLayout, QHBoxLayout, QTextEdit

from database_queries import DatabaseQueries


class NewResidentWindow(QWidget):
    def __init__(self, main = None) -> None:        # -- Initiates the Application
        super().__init__()
        self.mainFrame: object = main
        self.initUI()
        self.applyLayouts()
        self.setButtonConnections()
        self.loadComboOptions()
        self.applyStylesheets()

    def initUI(self) -> None:                       # -- Initiates Apps Widgets
        # Create Widgets
        self.firstNameLabel: QWidget = QLabel("First Name:")                            # -- QLabels
        self.middleNameLabel: QWidget = QLabel("Middle:")
        self.lastNameLabel: QWidget = QLabel("Last Name:")
        self.dobLabel: QWidget = QLabel("D.O.B.:")
        self.roomNumLabel: QWidget = QLabel("Room#:")
        self.resImageLabel: QWidget = QLabel("None Selected")
        self.fallRiskLabel: QWidget = QLabel("Fall Risk:")
        self.oxygenLabel: QWidget = QLabel("Oxygen:")
        self.feederLabel: QWidget = QLabel("Feeder:")
        self.veteranLabel: QWidget = QLabel("Veteran:") 
        self.moveInDateLabel: QWidget = QLabel("Move in Date:")
        self.dietRestrictLabel: QWidget = QLabel("Dietary Restrictions:")
        self.residentBioLabel: QWidget = QLabel("Bio:")

        self.firstNameEntry: QWidget = QLineEdit()                                      # -- QLineEdits
        self.middleNameEntry: QWidget = QLineEdit()
        self.lastNameEntry: QWidget = QLineEdit()
        self.roomNumEntry: QWidget = QLineEdit()

        self.dobEntry: QWidget = QDateEdit()                                            # -- QDateEdits
        self.moveInDateEntry: QWidget = QDateEdit()

        self.uploadBtn: QWidget = QPushButton("upload")                                 # -- QPushButtons
        self.submitBtn: QWidget = QPushButton("Submit")
        self.cancelBtn: QWidget = QPushButton("Cancel")                                

        self.fallRiskCombo: QWidget = QComboBox()                                       # -- QComboboxs
        self.oxygenCombo: QWidget = QComboBox()
        self.feederCombo: QWidget = QComboBox()
        self.veteranCombo: QWidget = QComboBox()

        self.dietRestrictEntry: QWidget = QTextEdit()                                   # -- QTextEdits
        self.residentBioEntry: QWidget = QTextEdit()

    def applyLayouts(self) -> None:                 # -- Applies widgets to layout, and sets the main layout
        # Create layouts 
        self.layout = QVBoxLayout()
        self.rowOneLayout = QHBoxLayout()
        self.rowTwoLayout = QHBoxLayout()
        self.buttonLayout = QHBoxLayout()

        # Apply Widgets to Layouts
        self.rowOneLayout.addWidget(self.firstNameLabel)
        self.rowOneLayout.addWidget(self.firstNameEntry)
        self.rowOneLayout.addWidget(self.middleNameLabel)
        self.rowOneLayout.addWidget(self.middleNameEntry)
        self.rowOneLayout.addWidget(self.lastNameLabel)
        self.rowOneLayout.addWidget(self.lastNameEntry)
        self.rowOneLayout.addWidget(self.dobLabel)
        self.rowOneLayout.addWidget(self.dobEntry)
        self.layout.addLayout(self.rowOneLayout)
        self.rowTwoLayout.addWidget(self.roomNumLabel)
        self.rowTwoLayout.addWidget(self.roomNumEntry)
        self.rowTwoLayout.addWidget(self.resImageLabel)
        self.rowTwoLayout.addWidget(self.uploadBtn)
        self.rowTwoLayout.addWidget(self.moveInDateLabel)
        self.rowTwoLayout.addWidget(self.moveInDateEntry)
        self.rowTwoLayout.addWidget(self.fallRiskLabel)
        self.rowTwoLayout.addWidget(self.fallRiskCombo)
        self.rowTwoLayout.addWidget(self.oxygenLabel)
        self.rowTwoLayout.addWidget(self.oxygenCombo)
        self.rowTwoLayout.addWidget(self.feederLabel)
        self.rowTwoLayout.addWidget(self.feederCombo)
        self.rowTwoLayout.addWidget(self.veteranLabel)
        self.rowTwoLayout.addWidget(self.veteranCombo)
        self.layout.addLayout(self.rowTwoLayout)
        self.layout.addWidget(self.dietRestrictLabel)
        self.layout.addWidget(self.dietRestrictEntry)
        self.layout.addWidget(self.residentBioLabel)
        self.layout.addWidget(self.residentBioEntry)
        self.buttonLayout.addWidget(self.cancelBtn)
        self.buttonLayout.addWidget(self.submitBtn)
        self.layout.addLayout(self.buttonLayout)

        # Apply layout to main Widgit
        self.setLayout(self.layout)
    
    def setButtonConnections(self) -> None:         # -- Establish connection between widgets and functions
        self.submitBtn.clicked.connect(self.submitResident)
        self.cancelBtn.clicked.connect(self.cancelSubmission)
        self.uploadBtn.clicked.connect(self.uploadPhoto)
        
    def applyStylesheets(self) -> None:             # -- Applies Stylesheets to Application
        self.dietRestrictLabel.setProperty("class", "textbox")
        self.residentBioLabel.setProperty("class", "textbox")
        
        with open(os.path.join("stylesheets", "add_new_resident.css")) as file:
            self.setStyleSheet(file.read())

    def loadComboOptions(self) -> None:             # -- Inserts options to comboboxs
        options: list = ["--", "Yes", "No"]
        self.fallRiskCombo.insertItems(0, options)
        self.oxygenCombo.insertItems(0, options)
        self.feederCombo.insertItems(0, options)
        self.veteranCombo.insertItems(0, options)

    def calculateAge(self) -> str:                  # -- Uses current date and residents DOB to determine age
        # Calculate resident DOB
        dateOfBirth: list = self.dobEntry.text().split('/')
        age: str = datetime.today().year - int(dateOfBirth[2])

        if int(dateOfBirth[0]) > datetime.today().month:
            return str(age - 1)
        else:
            return str(age)

    def submitResident(self) -> None:               # -- Checks entry windows and submits resident to database
        residentToAdd: tuple = (
            self.firstNameEntry.text(), self.middleNameEntry.text(),
            self.lastNameEntry.text(), self.calculateAge(),
            self.dobEntry.text(), self.roomNumEntry.text(),
            self.resImageLabel.text(), self.fallRiskCombo.currentText(),
            self.oxygenCombo.currentText(), self.feederCombo.currentText(),
            self.veteranCombo.currentText(), self.dietRestrictEntry.toPlainText(),
            self.moveInDateEntry.text(), self.residentBioEntry.toPlainText()
        )

        # Check for missing informaiton
        for item in residentToAdd:
            if item == '' or item == '--' or item == 'None Selected':
                return print('Missing information')
            
        # submit the resident to the database
        DatabaseQueries("resident").addNewResident(residentToAdd)

        # Copies image from its origional path to the images folder
        shutil.copy(self.absolute_path, os.path.join('images', self.resImageLabel.text())) 

        # CLose the window pane 
        if self.mainFrame != None:
            self.mainFrame.layout.removeWidget(self)
            self.mainFrame.mainFrame.residentListbox.clear()
            self.mainFrame.mainFrame.loadResidentComboList()
            self.mainFrame.mainFrame.loadResidentPreview()
            self.mainFrame.newResidentWindow = None
            self.cancelSubmission()
        else:
            sys.exit()

    def cancelSubmission(self) -> None:             # -- Cancel and close add resident window pane
        if self.mainFrame != None:
            self.mainFrame.layout.removeWidget(self)
            self.mainFrame.newResidentWindow = False
            self.close()
            id = DatabaseQueries().getAllResidents()[0][0]
            self.mainFrame.mainFrame.residentProfile.loadResidentInformation(id)
            for widg in self.mainFrame.mainFrame.residentProfile.widgetList:
                widg.show()
        else:
            sys.exit()

    def uploadPhoto(self) -> str:                   # -- Uploads photo to resident form
        img_to_save = QFileDialog.getOpenFileName(filter = '(*.jpg)')
        path: str = os.path.split(img_to_save[0])
        self.resImageLabel.setText(path[1])
        self.absolute_path: str = os.path.join(path[0], path[1])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    addResidentScreen: QWidget = NewResidentWindow()
    addResidentScreen.show()
    sys.exit(app.exec())
    