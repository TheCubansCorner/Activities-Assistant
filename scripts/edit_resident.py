#! python3
#! edit_resident.py -- Edits current resident informaiton

"""
TODO: Make app reload last page with new informaiton on it.
"""

import os, sys

from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import QDate

from add_new_resident import NewResidentWindow
from database_queries import DatabaseQueries


class EditResident(NewResidentWindow):      # -- Child of add_new_resident.py
    def __init__(self, residentId: int = None, mainApp: QWidget = None) -> None:        # -- Initiates the module and its Parent Class
        super().__init__()
        self.mainFrame: QWidget = mainApp
        self.currentResident: str = DatabaseQueries().getCurrentResident(residentId)
        self.residentToedit: dict = {
            "id" : self.currentResident[0], "firstName" : self.currentResident[1], "middleInitial" : self.currentResident[2],
            "lastName" : self.currentResident[3], "age" : self.currentResident[4], "dob" : self.currentResident[5],
            "room" : self.currentResident[6], "image" : self.currentResident[7], "fallRisk" : self.currentResident[8],
            "oxygen" : self.currentResident[9], "feeder" : self.currentResident[10], "veteran" : self.currentResident[11],
            "dietary" : self.currentResident[12], "moveInDate" : self.currentResident[13], "residentBio" : self.currentResident[14]
        }

        self.fillInformation()
    
    def setConnections(self) -> None:                                           # -- Resets connections of Parent Class
        self.cancelBtn.clicked.connect(self.cancelSubmission)

    def fillInformation(self) -> None:                                          # -- Auto Fills selections with current resident information
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

    def cancelSubmission(self) -> None:                                         # -- Cancels the current submission
        if self.mainFrame:
            for widg in self.mainFrame.widgetList:
                widg.show()
            
            self.mainFrame.layout.removeWidget(self)
            self.hide()

    def addDate(self, date: str) -> QDate:                                      # -- Creates a QDate for DateWidgets
        dateToAdd = date.split('/')
        birthDay = int(dateToAdd[1])
        birthMonth = int(dateToAdd[0])
        birthYear = int(dateToAdd[2])
        return QDate(birthYear, birthMonth, birthDay)
    
    def submitResident(self) -> None:                                           # -- Submits resident to the database
        resID: int = int(self.residentToedit["id"])
        residentToEdit: list = [
            self.firstNameEntry.text(), self.middleNameEntry.text(),
            self.lastNameEntry.text(), self.calculateAge(),
            self.dobEntry.text(), self.roomNumEntry.text(),
            self.resImageLabel.text(), self.fallRiskCombo.currentText(),
            self.oxygenCombo.currentText(), self.feederCombo.currentText(),
            self.veteranCombo.currentText(), self.dietRestrictEntry.toPlainText(),
            self.moveInDateEntry.text(), self.residentBioEntry.toPlainText()
        ]


        # Check for missing informaiton
        for item in residentToEdit:
            if item == '' or item == '--' or item == 'None Selected':
                return print('Missing information')
            
        # Update the residents informaiton in the database
        DatabaseQueries().updateResident(resID, residentToEdit)

        for widg in self.mainFrame.widgetList:
            widg.show()

        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    editResident = EditResident(1)
    editResident.show()
    sys.exit(app.exec())