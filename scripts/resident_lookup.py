#! python3
#! resident_lookup.py -- Main page for looking up residents in the database

import os, sys

from PyQt6.QtWidgets import QApplication, QWidget, QListWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QMainWindow
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from add_new_resident import NewResidentWindow
from database_queries import DatabaseQueries
from resident_profile import ResidentProfile


class ResidentLookup(QWidget):
    def __init__(self, main: QMainWindow = None) -> None:       # -- Initiates the Application
        super().__init__()
        self.newResidentWindow = None
        self.residentProfile = None
        self.mainApp: QApplication = main
        self.currentRes = {
            "id" : None, "firstName" : None, "middleInitial" : None,
            "lastName" : None, "age" : None, "dob" : None,
            "room" : None, "image" : None, "fall risk" : None,
            "oxygen" : None, "feeder" : None, "veteran" : None,
            "dietary" : None, "moveInDate" : None, "residentBio" : None,
        }

        self.initUI()
        self.loadResidentComboList()
        self.applyStylesheets()
        self.setButtonConnections()
        self.applyLayouts()
        self.loadResidentPreview()

    def initUI(self) -> None:                                   # -- Initiates the APP UI
        # Create Widgets
        self.previousPageBtn: QWidget = QPushButton("<--")
        self.addResidentBtn: QWidget = QPushButton("+")
        self.residentListbox: QWidget = QListWidget()
        self.previewBioLabel: QWidget = QLabel("Coming soon")
        self.previewResImage: QWidget = QLabel("Image")
        self.previewBlankLabel: QWidget = QLabel("")

        self.widgetList = [self.previousPageBtn, self.addResidentBtn, self.residentListbox, self.previewBioLabel, self.previewResImage]
        
    def applyLayouts(self) -> None:                             # -- Applies widgets to layouts, and applies main layout
        # Create the layouts
        self.layout = QVBoxLayout()
        self.navigationLayout = QHBoxLayout()
        self.listPreviewLayout = QHBoxLayout()
        self.previewLayout = QVBoxLayout()

        # Add WIdgets to layouts
        self.navigationLayout.addWidget(self.previousPageBtn)
        self.navigationLayout.addWidget(self.addResidentBtn)
        self.previewLayout.addWidget(self.previewResImage, Qt.AlignmentFlag.AlignCenter)
        self.previewLayout.addWidget(self.previewBioLabel, Qt.AlignmentFlag.AlignCenter)
        self.previewLayout.addWidget(self.previewBlankLabel, Qt.AlignmentFlag.AlignCenter)
        self.listPreviewLayout.addWidget(self.residentListbox)
        self.listPreviewLayout.addLayout(self.previewLayout)
        self.layout.addLayout(self.navigationLayout)
        self.layout.addLayout(self.listPreviewLayout)

        # Add Set Layout
        self.setLayout(self.layout)

    def setButtonConnections(self) -> None:                     # -- Establishes connection between widgets and functions
        self.addResidentBtn.clicked.connect(self.addResident)
        self.residentListbox.clicked.connect(self.loadResidentPreview)
        self.residentListbox.doubleClicked.connect(self.mainResidentView)
        self.previousPageBtn.clicked.connect(self.backToMain)
    
    def applyStylesheets(self) -> None:                         # -- Applies Stylesheets to Application
        self.previewResImage.setMaximumSize(300,300)
        self.previewResImage.setMinimumSize(300, 300)
        self.previewBioLabel.setMaximumSize(300,300)
        self.previewBioLabel.setMinimumSize(300, 300)
        self.previewBlankLabel.setMaximumSize(300,300)
        self.previewBlankLabel.setMinimumSize(300, 300)
        self.previewBlankLabel.setMaximumSize(300,300)
        self.previewBlankLabel.setMinimumSize(300, 300)

        self.previewResImage.setProperty("class", "image")
        self.previewBioLabel.setProperty("class", "bio")
        self.previewBlankLabel.setProperty("class", "blank")

        with open(os.path.join("stylesheets", "resident_lookup.css")) as file:
            self.setStyleSheet(file.read())

    def addResident(self) -> None:                              # -- Opens and adds add resident module
        if self.newResidentWindow:
            return
        else:
            self.newResidentWindow = NewResidentWindow(self)
            self.listPreviewLayout.addWidget(self.newResidentWindow)

    def loadResidentComboList(self) -> None:                    # -- Adds resident database to the QlistWidgit
        residentList: list = DatabaseQueries().getAllResidents()
        for resident in residentList:
            text: str = f"{resident[0]}) {resident[1]} {resident[2]} {resident[3]}   Room: {resident[4]}"
            self.residentListbox.addItem(text)

    def loadResidentPreview(self) -> None:                      # -- Loads current residents information for preview bio
        if self.residentListbox.currentItem() == None:
            self.previewBioLabel.setText(f"""
            Name:           --
            Age:            --
            DOB:            --
            Room:           --
            Move in Date:   --
            """)
            self.previewResImage.setPixmap(QPixmap())
        else:
            currentId: int = int(self.residentListbox.currentItem().text().split(')')[0])
            resident: tuple = DatabaseQueries(self).getCurrentResident(currentId)
            itemIndex: int = 0

            for resInfo in self.currentRes.keys():
                self.currentRes[resInfo] = resident[itemIndex]
                itemIndex += 1
            
            self.previewBioLabel.setText(f"""
            Name:               {f"{self.currentRes['firstName']} {self.currentRes['middleInitial']} {self.currentRes['lastName']}"}  
            Age:                  {self.currentRes["age"]}     
            DOB:                 {self.currentRes["dob"]}
            Room:               {self.currentRes["room"]}
            Move in Date:   {self.currentRes["moveInDate"]}
            """)        

            bioImg: str = os.path.join("images", self.currentRes['image'])
            pixmap: QWidget = QPixmap(bioImg)
            resizedImage: QPixmap = pixmap.scaled(350, 350, Qt.AspectRatioMode.KeepAspectRatio)
            self.previewResImage.setPixmap(resizedImage)

    def mainResidentView(self) -> None:                         # -- Loads the main resident profile
        residentId: int = self.currentRes["id"]
        profile = ResidentProfile(residentId, self)

        for widg in self.widgetList:
            widg.hide()

        if self.newResidentWindow:
            self.newResidentWindow.close()
            self.newResidentWindow = False

        self.layout.addWidget(profile)

    def backToMain(self) -> None:                               # -- Returns to previous application
        if self.mainApp:
            for item in self.mainApp.widgetList:
                item.show()
            self.mainApp.layout.removeWidget(self)
            self.close()

            if self.newResidentWindow:
                self.newResidentWindow.close()
                self.newResidentWindow = None
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    residentLookup: QWidget = ResidentLookup()
    residentLookup.show()
    sys.exit(app.exec())
