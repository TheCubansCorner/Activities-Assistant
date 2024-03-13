#! python3
#! resident_lookup.py -- Main page for looking up residents in the database

"""
TODO: Need to update module to incorporate the entire resident profile
"""

import os, sys

from PyQt6.QtWidgets import QApplication, QWidget, QListWidget, QPushButton
from PyQt6.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QMainWindow
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
        firstId = DatabaseQueries().getAllResidents()[0][0]
        # Create Widgets
        self.previousPageBtn: QWidget = QPushButton("<--")
        self.addResidentBtn: QWidget = QPushButton("+")
        self.residentListbox: QWidget = QListWidget()
        self.residentProfile = ResidentProfile(firstId, self)

        self.widgetList = [self.previousPageBtn, self.addResidentBtn, self.residentListbox, self.residentProfile]
        
    def applyLayouts(self) -> None:                             # -- Applies widgets to layouts, and applies main layout
        # Create the layouts
        self.layout = QVBoxLayout()
        self.navigationLayout = QHBoxLayout()
        self.listPreviewLayout = QHBoxLayout()
        self.previewLayout = QVBoxLayout()

        # Add WIdgets to layouts
        self.navigationLayout.addWidget(self.previousPageBtn)
        self.navigationLayout.addWidget(self.addResidentBtn)
        self.previewLayout.addWidget(self.residentProfile, Qt.AlignmentFlag.AlignCenter)
        self.listPreviewLayout.addWidget(self.residentListbox)
        self.listPreviewLayout.addLayout(self.previewLayout)
        self.layout.addLayout(self.navigationLayout)
        self.layout.addLayout(self.listPreviewLayout)

        # Add Set Layout
        self.setLayout(self.layout)

    def setButtonConnections(self) -> None:                     # -- Establishes connection between widgets and functions
        self.addResidentBtn.clicked.connect(self.addResident)
        self.residentListbox.clicked.connect(self.loadResidentPreview)
        self.previousPageBtn.clicked.connect(self.backToMain)
    
    def applyStylesheets(self) -> None:                         # -- Applies Stylesheets to Application
        self.residentListbox.setMaximumWidth(300)
        self.residentListbox.setMinimumWidth(300)

        with open(os.path.join("stylesheets", "resident_lookup.css")) as file:
            self.setStyleSheet(file.read())

    def addResident(self) -> None:                              # -- Opens and adds add resident module
        if self.newResidentWindow:
            return
        else:
            for widge in self.residentProfile.widgetList:
                widge.hide()
                
            self.newResidentWindow = NewResidentWindow(self)
            self.listPreviewLayout.addWidget(self.newResidentWindow)

    def loadResidentComboList(self) -> None:                    # -- Adds resident database to the QlistWidgit
        residentList: list = DatabaseQueries().getAllResidents()
        for resident in residentList:
            text: str = f"{resident[0]}) {resident[1]} {resident[2]} {resident[3]}   Room: {resident[4]}"
            self.residentListbox.addItem(text)

    def loadResidentPreview(self) -> None:                      # -- Loads current residents information for preview bio
        if self.residentListbox.currentItem() == None:
            # Set Current resident to first in list
            pass
        else:
            currentId: int = int(self.residentListbox.currentItem().text().split(')')[0])
            resident: tuple = DatabaseQueries(self).getCurrentResident(currentId)
            itemIndex: int = 0

            for resInfo in self.currentRes.keys():
                self.currentRes[resInfo] = resident[itemIndex]
                itemIndex += 1
            
            self.residentProfile.loadResidentInformation(self.currentRes['id'])

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
