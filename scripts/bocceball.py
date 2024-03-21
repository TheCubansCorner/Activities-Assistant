#! python3
#! bocceball.py -- Keeps score for bocce ball rounds

import os, sys

from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QAbstractItemView
    )

from PyQt6.QtCore import Qt

from database_queries import DatabaseQueries
from team_selection import TeamSelection


class BocceBall(QWidget):
    def __init__(self, mainApp: QWidget = None) -> None:    # -- initiates the module/main variables
        super().__init__()
        self.mainFrame: QWidget = mainApp
        self.teamList: list = []

        self.initUI()
        self.initConfigWidgets()
        self.initStyleSheets()
        self.initConfigConnections()
        self.initLayouts()

    def initUI(self) -> None:                               # -- Initiates Widgets
        self.header: QWidget = QLabel("BOCCE BALL", alignment = Qt.AlignmentFlag.AlignHCenter)
        self.teamSelection: QWidget = TeamSelection(self)
        self.scoreBoard: QWidget = QTableWidget()

        self.widgetList: list = [self.teamSelection, self.scoreBoard, self.header]

    def initConfigWidgets(self) -> None:                    # -- Configures widget settings
        self.scoreBoard.verticalHeader().setVisible(False)
        self.scoreBoard.horizontalHeader().setVisible(False)
        self.scoreBoard.setRowCount(9)
        self.scoreBoard.setShowGrid(True)
        self.scoreBoard.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

    def initStyleSheets(self) -> None:                      # -- Initiates the stylesheets for the application
        with open(os.path.join("stylesheets", "bocceball.css")) as file:
            self.setStyleSheet(file.read())
    
    def initConfigConnections(self) -> None:                # -- Configures connections between widgets and functions
        self.scoreBoard.clicked.connect(self.currentCellClicked)
    
    def initLayouts(self) -> None:                          # -- Applies widgets to the layouts/applies layouts to app
        self.layout = QVBoxLayout()

        self.layout.addWidget(self.teamSelection)
        self.layout.addWidget(self.header)
        self.layout.addWidget(self.scoreBoard)

        self.setLayout(self.layout)

        self.header.hide()
        self.scoreBoard.hide()

    def backToMain(self) -> None:                           # -- Returns to main application page
        pass

    def hideAll(self) -> None:                              # -- Hides all widgets
        for widg in self.widgetList:
            widg.hide()

    def showAll(self) -> None:                              # -- Shows all widgets
        for widg in self.widgetList:
            widg.show()

    def currentCellClicked(self) -> None:                   # -- Gets location information for the current cell on the table
        row: int = self.scoreBoard.currentRow()
        column: int = self.scoreBoard.currentColumn()
        self.currentCell: tuple = (row, column)

        self.updateCell()

    def updateCell(self) -> None:                           # -- Updates the current cell to be checked as a win
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
