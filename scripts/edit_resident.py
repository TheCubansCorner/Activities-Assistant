#! python3
#! edit_resident.py -- Edits current resident informaiton

import os, sys

from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit
from PyQt6.QtWidgets import QDateEdit, QPushButton, QComboBox, QTextEdit
from PyQt6.QtCore import QDate

from add_new_resident import NewResidentWindow
from database_queries import DatabaseQueries


class EditResident(NewResidentWindow):
    def __init__(self, id: int = None, mainApp: QWidget = None) -> None:
        super().__init__()
        self.mainApp: QWidget = mainApp
        self.currentResident: str = DatabaseQueries().getCurrentResident(id)
        self.residentToedit: dict = {
            "id" : self.currentResident[0], "firstName" : self.currentResident[1], "middleInitial" : self.currentResident[2],
            "lastName" : self.currentResident[3], "age" : self.currentResident[4], "dob" : self.currentResident[5],
            "room" : self.currentResident[6], "image" : self.currentResident[7], "fallRisk" : self.currentResident[8],
            "oxygen" : self.currentResident[9], "feeder" : self.currentResident[10], "veteran" : self.currentResident[11],
            "dietary" : self.currentResident[12], "moveInDate" : self.currentResident[13], "residentBio" : self.currentResident[14]
        }

        self.fillInformation()
    
    def setConnections(self) -> None:
        self.cancelBtn.clicked.connect(self.cancelSubmission)

    def fillInformation(self) -> None:
        comboChoices: dict = {"--" : 0, "Yes" : 1, "No" : 2}
        
        self.firstNameEntry.setText(self.residentToedit["firstName"])
        self.middleNameEntry.setText(self.residentToedit["middleInitial"])
        self.lastNameEntry.setText(self.residentToedit["lastName"])
        self.dobEntry.setDate(self.addDate(self.residentToedit["dob"]))
        self.roomNumEntry.setText(self.residentToedit["room"])
        self.resImageLabel.setText(self.residentToedit["image"])
        self.moveInDateEntry.setDate(self.addDate(self.residentToedit["moveInDate"]))
        self.fallRiskCombo.setCurrentIndex(comboChoices[self.residentToedit["fallRisk"]])
        self.oxygenCombo.setCurrentIndex(comboChoices[self.residentToedit["oxygen"]])
        self.feederCombo.setCurrentIndex(comboChoices[self.residentToedit["feeder"]])
        self.veteranCombo.setCurrentIndex(comboChoices[self.residentToedit["veteran"]])
        self.dietRestrictEntry.setText(self.residentToedit["dietary"])
        self.residentBioEntry.setText(self.residentToedit["residentBio"])

    def cancelSubmission(self) -> None:
        if self.mainApp:
            for widg in self.mainApp.widgetList:
                widg.show()
            
            self.mainApp.layout.removeWidget(self)
            self.hide()

    def addDate(self, date) -> None:
        dateToAdd = date.split('/')
        birthDay = int(dateToAdd[1])
        birthMonth = int(dateToAdd[0])
        birthYear = int(dateToAdd[2])
        return QDate(birthYear, birthMonth, birthDay)
    
    def submitResident(self) -> None:
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    editResident = EditResident(1)
    editResident.show()
    sys.exit(app.exec())