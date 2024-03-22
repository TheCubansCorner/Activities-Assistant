#! python3
#! bowling.py -- Module for tracking bowling scores for residents

"""
TODO: 
"""

import os, sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QApplication, QHBoxLayout, QVBoxLayout,
    QPushButton, QTableWidget, QLabel, QAbstractItemView,
    QTableWidgetItem, QLineEdit, QFormLayout
    )

from database_queries import DatabaseQueries
from player_selection import PlayerSelection


class Bowling(QWidget):
    def __init__(self, mainApp: QWidget = None):            # -- initiates the module/main variables
        super().__init__()
        self.appTitle = "bowling"
        self.mainFrame: QWidget = mainApp
        self.playerList: list = []
        self.rounds: list = ["Names", "Frame 1", "Frame 2", "Frame 3", "Frame 4", "Frame 5", "Strikes", "Spares"]
        self.currentCell = None

        self.initUI()
        self.initConfigWidgets()
        self.initStyleSheets()
        self.initConfigConnections()
        self.initLayouts()

    def initUI(self) -> None:                               # -- Initiates Widgets
        self.backToMainBtn: QWidget = QPushButton("<--")
        self.refreshBtn: QWidget = QPushButton("Refresh")
        self.playerSelect: QWidget = PlayerSelection(self)
        self.headerLabel: QWidget = QLabel("BOWLING")
        self.scoreboardTable: QWidget = QTableWidget()

        self.widgetList = [self.headerLabel, self.scoreboardTable]

    def initConfigWidgets(self) -> None:                    # -- Configures widget settings
        self.scoreboardTable.verticalHeader().setVisible(False)
        self.scoreboardTable.horizontalHeader().setVisible(False)
        self.scoreboardTable.setShowGrid(True)
        self.scoreboardTable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.scoreboardTable.setColumnCount(8)

    def initStyleSheets(self) -> None:                      # -- Initiates the stylesheets for the application
        with open(os.path.join("stylesheets", "bowling.css")) as file:
            self.setStyleSheet(file.read())

    def initConfigConnections(self) -> None:                # -- Configures connections between widgets and functions
        self.scoreboardTable.clicked.connect(self.currentCellClicked)

    def initLayouts(self) -> None:                          # -- Applies widgets to the layouts/applies layouts to app
        self.layout = QVBoxLayout()
        self.navLayout = QHBoxLayout()

        self.navLayout.addWidget(self.backToMainBtn)
        self.navLayout.addWidget(self.refreshBtn)

        self.layout.addLayout(self.navLayout)
        self.layout.addWidget(self.playerSelect)
        self.layout.addWidget(self.headerLabel)
        self.layout.addWidget(self.scoreboardTable)

        self.setLayout(self.layout)

        self.hideAll()

    def backToMain(self) -> None:                           # -- Returns to main application page
        pass

    def showAll(self) -> None:                              # -- Shows all widgets
        for widg in self.widgetList:
            widg.show()

    def hideAll(self) -> None:                              # -- Hides all Widgets
        for widg in self.widgetList:          
            widg.hide()

    def buildTable(self) -> None:                           # -- Inserts information into the Scorboard for names and rounds
        for inx, label in enumerate(self.rounds):
            self.scoreboardTable.setItem(0, inx, QTableWidgetItem(label))

        for inx, resident in enumerate(self.playerList):
            self.scoreboardTable.setItem(inx + 1, 0, QTableWidgetItem(resident))

            self.scoreboardTable.setItem((inx + 1), 6, QTableWidgetItem("0"))
            self.scoreboardTable.setItem((inx + 1), 7, QTableWidgetItem("0"))

    def currentCellClicked(self) -> None:                   # -- Finds the current active cell
        self.currentCell: tuple = (self.scoreboardTable.currentRow(), self.scoreboardTable.currentColumn())
        self.openScoringWindow()

    def openScoringWindow(self) -> None:                    # -- Opens window for selecting spare or strike
        self.scoreingWindow: QWidget = QWidget()

        self.scoreingWindow.layout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout()

        self.questionLabel: QWidget = QLabel("Strike or Spare?")
        self.strikeBtn: QWidget = QPushButton("X")
        self.spareBtn: QWidget = QPushButton("/")

        self.strikeBtn.clicked.connect(lambda: self.updateCell("X"))
        self.spareBtn.clicked.connect(lambda: self.updateCell("/"))

        self.buttonLayout.addWidget(self.spareBtn)
        self.buttonLayout.addWidget(self.strikeBtn)

        self.scoreingWindow.layout.addWidget(self.questionLabel)
        self.scoreingWindow.layout.addLayout(self.buttonLayout)

        self.scoreingWindow.setLayout(self.scoreingWindow.layout)

        self.scoreingWindow.show()

    def updateCell(self, score: str):                       # -- Updates the informaiton in the current cell
        self.scoreboardTable.setItem(self.currentCell[0], self.currentCell[1], QTableWidgetItem(score))

        if score == "/":
            currentSpares: int = int(self.scoreboardTable.item(self.currentCell[0], 7).text())
            currentSpares += 1
            self.scoreboardTable.setItem(self.currentCell[0], 7, QTableWidgetItem(str(currentSpares)))
        else:
            currentStrikes: int = int(self.scoreboardTable.item(self.currentCell[0], 6).text())
            currentStrikes += 1
            self.scoreboardTable.setItem(self.currentCell[0], 6, QTableWidgetItem(str(currentStrikes)))

        self.scoreingWindow.close()
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    bowling = Bowling()
    bowling.show()
    sys.exit(app.exec())