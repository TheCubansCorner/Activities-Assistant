#! python3
#! resident_profile.py -- Displays resident BIO information

import sys, os

from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QPushButton
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from database_queries import DatabaseQueries


class ResidentProfile(QWidget):
    def __init__(self, residentId: int = 1, mainApp: QWidget = None) -> None:        # -- Initiates the application
        super().__init__()
        self.resident: tuple = DatabaseQueries().getCurrentResident(residentId)
        self.mainApp = mainApp

        self.initUI()
        self.applyLayouts()
        self.setButtonConnections()
        self.applyStyleSheets()
        self.loadResidentInformation()
        
    def initUI(self) -> None:                               # -- Creates Widgets
        # Create Widgets
        self.basicBioLabel: QWidget = QLabel("Basic Bio Info")                          # -- QLabels
        self.imageLabel: QWidget = QLabel("Image")
        self.dietaryLabel: QWidget = QLabel("Dietary Restrictions Label")
        self.mainBioLabel: QWidget = QLabel("Main Bio info")

        self.backBtn: QWidget = QPushButton("<--")                                      # -- QPushButton
        self.editBtn: QWidget = QPushButton("Edit")
        self.removeResidentBtn: QWidget = QPushButton("Delete")

        self.widgetList = [
            self.basicBioLabel, self.imageLabel, self.dietaryLabel,
            self.mainBioLabel, self.backBtn, self.editBtn,
            self.removeResidentBtn
        ]

    def applyLayouts(self) -> None:                         # -- Applies Layouts to the application
        # Create Layouts
        self.layout = QVBoxLayout()
        self.navigationLayout = QHBoxLayout()
        self.basicBioImageLayout = QHBoxLayout()

        # Apply Widgets to layouts
        self.navigationLayout.addWidget(self.backBtn)                                   # -- Navigation Layout
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

    def setButtonConnections(self) -> None:                 # -- Establishes button Connections
        self.backBtn.clicked.connect(self.previousPage)
        self.editBtn.clicked.connect(self.editResidentInfo)
        self.removeResidentBtn.clicked.connect(self.deleteResidentInfo)

    def applyStyleSheets(self) -> None:                     # -- Applies stylesheets to the application
        pass

    def loadResidentInformation(self):
        self.basicBioLabel.setText(
            f"""
            Name: {self.resident[1]} {self.resident[2]} {self.resident[3]}
            Age: {self.resident[4]}
            DOB: {self.resident[5]}
            Room: {self.resident[6]}
            Move In Date: {self.resident[13]}
            Fall Risk: {self.resident[8]}
            Oxygen: {self.resident[9]}
            Feeder: {self.resident[10]}
            Veteran: {self.resident[11]}
        """)
        self.dietaryLabel.setText(f"Dietary Restrictions:\n\t{self.resident[12]}")
        self.mainBioLabel.setText(f"Resident Bio:\n\t{self.resident[14]}")

        path: str = os.path.join('images', self.resident[7])
        pixmap: QWidget = QPixmap(path)
        resizeImage: QPixmap = pixmap.scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio)
        self.imageLabel.setPixmap(resizeImage)

    def editResidentInfo(self) -> None:                     # -- Opens WIndow Pane to Edit resident informaiton
        pass

    def deleteResidentInfo(self) -> None:                   # -- Deletes resident information
        pass

    def previousPage(self) -> None:                         # -- Closes application and returns to previous page
        if self.mainApp:
            for widg in self.mainApp.widgetList:
                widg.show()   

            self.mainApp.layout.removeWidget(self)
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    residentProfile = ResidentProfile()
    residentProfile.show()
    app.exec()
