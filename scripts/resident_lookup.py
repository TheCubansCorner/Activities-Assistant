#! python3
#! resident_lookup.py -- Main page for looking up residents in the database

from PyQt6.QtWidgets import QApplication, QWidget, QListWidget, QPushButton, QLineEdit, QLabel, QHBoxLayout, QVBoxLayout
from add_new_resident import NewResidentWindow

import os, sys


class ResidentLookup(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.initUI()
        self.applyLayouts()
        self.buttonConnections()
        self.show()

    def initUI(self) -> None:
        # Create Widgets
        self.previousPageBtn: QWidget = QPushButton('<--')
        self.refreshBtn: QWidget = QPushButton('refresh')
        self.addResidentBtn: QWidget = QPushButton('+')
        self.residentListbox: QWidget = QListWidget()
        self.previewBioLabel: QWidget = QLabel("Coming soon")
        self.previewResImage: QWidget = QLabel('Image')

    def applyLayouts(self) -> None:
        # Create the layouts
        self.layout = QVBoxLayout()
        self.navigationLayout = QHBoxLayout()
        self.listPreviewLayout = QHBoxLayout()
        self.previewLayout = QVBoxLayout()
        
        # Add WIdgets to layouts
        self.navigationLayout.addWidget(self.previousPageBtn)
        self.navigationLayout.addWidget(self.refreshBtn)
        self.navigationLayout.addWidget(self.addResidentBtn)
        self.previewLayout.addWidget(self.previewResImage)
        self.previewLayout.addWidget(self.previewBioLabel)
        self.listPreviewLayout.addWidget(self.residentListbox)
        self.listPreviewLayout.addLayout(self.previewLayout)
        self.layout.addLayout(self.navigationLayout)
        self.layout.addLayout(self.listPreviewLayout)

        # Add Set Layout
        self.setLayout(self.layout)

    def buttonConnections(self) -> None:
        self.addResidentBtn.clicked.connect(self.addResident)

    def addResident(self) -> None:
        newResidentWindow = NewResidentWindow(self)
        self.listPreviewLayout.addWidget(newResidentWindow)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    residentLookup = ResidentLookup()
    sys.exit(app.exec())
