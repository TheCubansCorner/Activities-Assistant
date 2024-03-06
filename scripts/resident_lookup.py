#! python3
#! resident_lookup.py -- Main page for looking up residents in the database

from PyQt6.QtWidgets import QApplication, QWidget, QListWidget, QPushButton, QLineEdit, QLabel, QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from add_new_resident import NewResidentWindow
from database_queries import DatabaseQueries

import os, sys


class ResidentLookup(QWidget):
    def __init__(self) -> None:                     # -- Initiates the Application
        super().__init__()
        self.newResidentWindow = None
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

    def initUI(self) -> None:                       # -- Initiates the APP UI
        # Create Widgets
        self.previousPageBtn: QWidget = QPushButton("<--")
        self.addResidentBtn: QWidget = QPushButton("+")
        self.residentListbox: QWidget = QListWidget()
        self.previewBioLabel: QWidget = QLabel("Coming soon")
        self.previewResImage: QWidget = QLabel("Image")
        
    def applyLayouts(self) -> None:                 # -- Applies widgets to layouts, and applies main layout
        # Create the layouts
        self.layout = QVBoxLayout()
        self.navigationLayout = QHBoxLayout()
        self.listPreviewLayout = QHBoxLayout()
        self.previewLayout = QVBoxLayout()

        # Add WIdgets to layouts
        self.navigationLayout.addWidget(self.previousPageBtn)
        self.navigationLayout.addWidget(self.addResidentBtn)
        self.previewLayout.addWidget(self.previewResImage)
        self.previewLayout.addWidget(self.previewBioLabel)
        self.listPreviewLayout.addWidget(self.residentListbox)
        self.listPreviewLayout.addLayout(self.previewLayout)
        self.layout.addLayout(self.navigationLayout)
        self.layout.addLayout(self.listPreviewLayout)

        # Add Set Layout
        self.setLayout(self.layout)

    def setButtonConnections(self) -> None:         # -- Establishes connection between widgets and functions
        self.addResidentBtn.clicked.connect(self.addResident)
        self.residentListbox.clicked.connect(self.loadResidentPreview)
    
    def applyStylesheets(self) -> None:             # -- Applies Stylesheets to Application
        pass

    def addResident(self) -> None:                  # -- Opens and adds add resident module
        if self.newResidentWindow:
            return
        else:
            self.newResidentWindow = NewResidentWindow(self)
            self.listPreviewLayout.addWidget(self.newResidentWindow)

    def loadResidentComboList(self) -> None:              # -- Adds resident database to the QlistWidgit
        residentList: list = DatabaseQueries().getAllResidents()
        for resident in residentList:
            text: str = f"{resident[0]}) {resident[1]} {resident[2]} {resident[3]}   Room: {resident[4]}"
            self.residentListbox.addItem(text)

    def loadResidentPreview(self) -> None:          # -- Loads current residents information for preview bio
        if self.residentListbox.currentItem() == None:
            self.previewBioLabel.setText(f"""
            Name:           --
            Age:            --
            DOB:            --
            Room:           --
            Move in Date:   --
            """)
        else:
            currentId: int = int(self.residentListbox.currentItem().text().split(')')[0])
            resident: tuple = DatabaseQueries(self).getCurrentResident(currentId)
            itemIndex: int = 0

            for resInfo in self.currentRes.keys():
                self.currentRes[resInfo] = resident[itemIndex]
                itemIndex += 1

            name: str = f"{self.currentRes['firstName']} {self.currentRes['middleInitial']} {self.currentRes['lastName']}"
            age: str = self.currentRes["age"]
            dob: str = self.currentRes["dob"]
            room: str = self.currentRes["room"]
            moveInDate: str = self.currentRes["moveInDate"]
            
            self.previewBioLabel.setText(f"""
            Name:               {name}  
            Age:                  {age}     
            DOB:                 {dob}
            Room:               {room}
            Move in Date:   {moveInDate}
            """)        

            bioImg: str = os.path.join("images", self.currentRes['image'])
            pixmap: QWidget = QPixmap(bioImg)
            resized_image = pixmap.scaled(350, 350, Qt.AspectRatioMode.KeepAspectRatio)
            self.previewResImage.setPixmap(resized_image)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    residentLookup: QWidget = ResidentLookup()
    residentLookup.show()
    sys.exit(app.exec())
