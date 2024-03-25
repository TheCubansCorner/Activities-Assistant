#! python3
#! bocceball.py -- Keeps score for bocce ball rounds]

"""
TODO: BACK TO MAIN BUTTON 
"""

import os, sys

from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout, 
    QPushButton, QTableWidget, QTableWidgetItem, QAbstractItemView,
    QGridLayout
    )

from PyQt6.QtCore import Qt

from database_queries import DatabaseQueries
from team_selection import TeamSelection


class BocceBall(QWidget):
    def __init__(self, mainApp: QWidget = None) -> None:        # -- initiates the module/main variables
        super().__init__()
        self.appTitle: str = "bocce"
        self.mainFrame: QWidget = mainApp
        self.teamList: list = []
        self.screenWidth: int = self.width()
        self.screenHeight: int = self.height()

        self.initUI()
        self.initConfigWidgets()
        self.initStyleSheets()
        self.initConfigConnections()
        self.initLayouts()

    def initUI(self) -> None:                                   # -- Initiates Widgets
        self.header: QWidget = QLabel("BOCCE BALL", alignment = Qt.AlignmentFlag.AlignCenter)
        self.teamSelection: QWidget = TeamSelection(self)
        self.scoreBoard: QWidget = QTableWidget()

        self.widgetList: list = [self.teamSelection, self.scoreBoard, self.header]

    def initConfigWidgets(self) -> None:                        # -- Configures widget settings
        self.scoreBoard.minimumWidth
        self.scoreBoard.verticalHeader().setVisible(False)
        self.scoreBoard.horizontalHeader().setVisible(False)
        self.scoreBoard.setRowCount(9)
        self.scoreBoard.setShowGrid(True)
        self.scoreBoard.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        #self.header.setMaximumHeight(30)
        #self.header.setMinimumHeight(30)

    def initStyleSheets(self) -> None:                          # -- Initiates the stylesheets for the application
        with open(os.path.join("stylesheets", "bocceball.css")) as file:
            self.setStyleSheet(file.read())
    
    def initConfigConnections(self) -> None:                    # -- Configures connections between widgets and functions
        self.scoreBoard.clicked.connect(self.currentCellClicked)
    
    def initLayouts(self) -> None:                              # -- Applies widgets to the layouts/applies layouts to app
        self.layout = QGridLayout()
        self.appLayout = QVBoxLayout()
        self.appLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.placeholder = QLabel()

        self.layout.addWidget(self.teamSelection, 0, 2)
        self.appLayout.addWidget(self.header, alignment = Qt.AlignmentFlag.AlignBottom)
        self.appLayout.addWidget(self.scoreBoard, alignment = Qt.AlignmentFlag.AlignTop)
        self.appLayout.addWidget(self.placeholder)
        self.layout.addLayout(self.appLayout, 0, 1)

        self.setLayout(self.layout)
        
        self.header.hide()
        self.scoreBoard.hide()

    def backToMain(self) -> None:                               # -- Returns to main application page
        pass

    def hideAll(self) -> None:                                  # -- Hides all widgets
        for widg in self.widgetList:
            widg.hide()

    def showAll(self) -> None:                                  # -- Shows all widgets
        for widg in self.widgetList:
            widg.show()

    def currentCellClicked(self) -> None:                       # -- Gets location information for the current cell on the table
        row: int = self.scoreBoard.currentRow()
        column: int = self.scoreBoard.currentColumn()
        self.currentCell: tuple = (row, column)

        self.updateCell()

    def updateCell(self) -> None:                               # -- Updates the current cell to be checked as a win
        currentTotal: QWidget = self.scoreBoard.item(8, self.currentCell[1])

        if not self.scoreBoard.item(self.currentCell[0], self.currentCell[1]):
            self.scoreBoard.setItem(self.currentCell[0], self.currentCell[1], QTableWidgetItem("WIN"))
       
            if currentTotal != None:
                currentTotal = int(currentTotal.text()) + 1
                self.scoreBoard.setItem(8, self.currentCell[1], QTableWidgetItem(str(currentTotal)))

        else:
            self.scoreBoard.takeItem(self.currentCell[0], self.currentCell[1])

            if currentTotal != None:
                currentTotal = int(currentTotal.text()) - 1
                self.scoreBoard.setItem(8, self.currentCell[1], QTableWidgetItem(str(currentTotal)))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    bocceBall: QWidget = BocceBall()
    bocceBall.show()
    sys.exit(app.exec())
