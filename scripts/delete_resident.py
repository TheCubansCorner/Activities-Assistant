#! python3
#! delete_resident.py -- Gives resident the option to delete a resident and add them to the historic data

"""
TODO: Complete remove resident function
"""

import sys, os

from PyQt6.QtWidgets import QPushButton, QApplication, QWidget, QComboBox, QLabel, QHBoxLayout, QVBoxLayout

from database_queries import DatabaseQueries

class DeleteResident(QWidget):
    def __init__(self, id = 1) -> None:         # -- Initiates the Module
        super().__init__()
        self.initUI()
        self.applyLayout()
        self.setConnections()
        self.applyStylesheets()
        self.loadComboOptions()

    def initUI(self) -> None:                   # -- Initiates the Modules Widgets
        self.messageLabel: QWidget = QLabel("Select a Reason")

        self.deadAliveCombo: QWidget = QComboBox()

        self.cancelBtn: QWidget = QPushButton("Cancel")
        self.submitBtn: QWidget = QPushButton("Yes")

    def applyLayout(self) -> None:              # -- Applies widgets to layouts/Sets main layout
        self.layout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout()

        self.buttonLayout.addWidget(self.cancelBtn)
        self.buttonLayout.addWidget(self.submitBtn)

        self.layout.addWidget(self.messageLabel)
        self.layout.addWidget(self.deadAliveCombo)
        self.layout.addLayout(self.buttonLayout)
        
        self.setLayout(self.layout)

    def setConnections(self) -> None:           # -- Sets connecitons between widgets and functions
        self.cancelBtn.clicked.connect(self.close)
        self.submitBtn.clicked.connect(self.submitRemoval)

    def applyStylesheets(self) -> None:         # -- Applies stylesheets to the widgets
        pass

    def loadComboOptions(self) -> None:         # -- Loads informaiton into combobox
        options: list = ["None Selected", "Deceased", "Moved Out"]
        self.deadAliveCombo.insertItems(0, options)

    def submitRemoval(self) -> None:            # -- Submit resident for removal
        pass


if __name__ == "__main__":
    app: QWidget = QApplication(sys.argv)
    deleteResident = DeleteResident()
    deleteResident.show()
    sys.exit(app.exec())