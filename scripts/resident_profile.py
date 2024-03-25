#! python3
#! resident_profile.py -- Displays resident BIO information

import sys, os

from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QPushButton
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from database_queries import DatabaseQueries
from edit_resident import EditResident
from delete_resident import DeleteResident
from add_new_resident import NewResidentWindow


class ResidentProfile(QWidget):
    def __init__(self, residentId: int = 1, mainApp: QWidget = None) -> None:           # -- Initiates the application
        super().__init__()
        self.resident: tuple = DatabaseQueries().getCurrentResident(residentId)
        self.mainFrame: QWidget = mainApp
        self.newResidentWindow: bool = False

        self.initUI()
        self.initConfigWidgets()
        self.initLayouts()
        self.initConfigConnections()
        self.initStyleSheets()
        self.loadResidentInformation(residentId)
        
    def initUI(self) -> None:                                                           # -- Creates Widgets
        # Create Widgets
        self.basicBioLabel: QWidget = QLabel("Basic Bio Info")                          # -- QLabels
        self.imageLabel: QWidget = QLabel("Image")
        self.dietaryLabel: QWidget = QLabel("Dietary Restrictions Label")
        self.mainBioLabel: QWidget = QLabel("Main Bio info")

        self.addBtn: QWidget = QPushButton("Add")
        self.editBtn: QWidget = QPushButton("Edit")                                     # -- QPushButton
        self.removeResidentBtn: QWidget = QPushButton("Delete")
        
        self.widgetList = [
            self.basicBioLabel, self.imageLabel, self.dietaryLabel,
            self.mainBioLabel, self.editBtn, self.addBtn,
            self.removeResidentBtn
        ]
    
    def initConfigWidgets(self) -> None:                                                # -- Initializes widget congfigs such as height, width, etc
        self.dietaryLabel.setWordWrap(True)
        self.mainBioLabel.setWordWrap(True)

    def initConfigConnections(self) -> None:                                            # -- Establishes button Connections
        self.addBtn.clicked.connect(self.addResident)
        self.editBtn.clicked.connect(self.editResidentInfo)
        self.removeResidentBtn.clicked.connect(self.deleteResidentInfo)

    def initStyleSheets(self) -> None:                                                  # -- Applies stylesheets to the application
        self.basicBioLabel.setProperty("class", "minibio")
        self.imageLabel.setProperty("class", "image")
        self.dietaryLabel.setProperty("class", "bio")
        self.mainBioLabel.setProperty("class", "bio")

        with open(os.path.join("stylesheets", "resident_profile.css")) as file:
            self.setStyleSheet(file.read())

    def initLayouts(self) -> None:                                                      # -- Applies Layouts to the application
        # Create Layouts
        self.layout = QVBoxLayout()
        self.navigationLayout = QHBoxLayout()
        self.basicBioImageLayout = QHBoxLayout()

        # Apply Widgets to layouts
        self.navigationLayout.addWidget(self.addBtn)
        self.navigationLayout.addWidget(self.editBtn)
        self.navigationLayout.addWidget(self.removeResidentBtn)

        self.basicBioImageLayout.addWidget(self.basicBioLabel)                          # -- Basic Bio/Image Layout
        self.basicBioImageLayout.addWidget(self.imageLabel)

        self.layout.addLayout(self.navigationLayout)                                    # -- Main Layout
        self.layout.addLayout(self.basicBioImageLayout)
        self.layout.addWidget(self.dietaryLabel)
        self.layout.addWidget(self.mainBioLabel)

        # Apply main layout to APP
        self.setLayout(self.layout)

    def hideAll(self) -> None:                                                          # -- Hides all widgets on this application
        for widg in self.widgetList:
            widg.hide()
        
    def showAll(self) -> None:                                                          # -- Shows all widgets on this application
        for widg in self.widgetList:
            widg.show()

    def loadResidentInformation(self, residentId: int):                                                  # -- Loads the current residents information based on ID
        self.resident: tuple = DatabaseQueries().getCurrentResident(residentId)
        self.basicBioLabel.setText(
            f"""
            Name:\t\t{self.resident[1]} {self.resident[2]} {self.resident[3]}
            Age:\t\t{self.resident[4]}
            DOB:\t\t{self.resident[5]}
            Room:\t\t{self.resident[6]}
            Move In Date:\t{self.resident[13]}
            Fall Risk:\t\t{self.resident[8]}
            Oxygen:\t\t{self.resident[9]}
            Feeder:\t\t{self.resident[10]}
            Veteran:\t\t{self.resident[11]}
        """)

        dietaryInformation = ""
        if len(self.resident[12]) > 89:         # - if text is greater than 86 it adds a new line every 86 characters
            for inx, character in enumerate(self.resident[12]):
                if (inx + 1) % 86 == 0:
                    dietaryInformation += f"\n{character}"
                else:
                    dietaryInformation += character
        else:
            dietaryInformation = self.resident[12]


        self.dietaryLabel.setText(f"Dietary Restrictions:\n\t{self.resident[12]}")
        self.mainBioLabel.setText(f"Resident Bio:\n\t{self.resident[14]}")

        path: str = os.path.join('images', self.resident[7])
        pixmap: QWidget = QPixmap(path)
        resizeImage: QPixmap = pixmap.scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio)
        self.imageLabel.setPixmap(resizeImage)

    def editResidentInfo(self) -> None:                                                 # -- Opens WIndow Pane to Edit resident informaiton
        edit = EditResident(self.resident[0], self)
        for widg in self.widgetList:
            widg.hide()

        self.layout.addWidget(edit)

    def deleteResidentInfo(self) -> None:                                               # -- Deletes resident information
        self.deleteResident: QWidget = DeleteResident(self.resident[0], self)
        self.deleteResident.show()

    def previousPage(self) -> None:                                                     # -- Closes application and returns to previous page
        if self.mainFrame:
            for widg in self.mainFrame.widgetList:
                widg.show()   

            self.mainFrame.layout.removeWidget(self)
            self.mainFrame.residentListbox.clear()
            self.mainFrame.loadResidentComboList()
            self.close()

    def addResident(self) -> None:                              # -- Opens and adds add resident module
        if self.newResidentWindow:
            return
        else:
            for widge in self.widgetList:
                widge.hide()
                
            self.newResidentWindow = NewResidentWindow(self)
            self.mainFrame.listPreviewLayout.addWidget(self.newResidentWindow)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    residentProfile = ResidentProfile()
    residentProfile.show()
    app.exec()
