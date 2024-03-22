#! python3
#! uno.py -- Application for tracking winners in uno. 

"""
TODO: Need to extend functionality to save the winner information to a second database with the resident id as foreign key
"""

import os, sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QApplication, QHBoxLayout, QVBoxLayout,
    QListWidget, QPushButton, QLabel, QAbstractItemView,
    QTableWidget, QTableWidgetItem
    )

from database_queries import DatabaseQueries

class Uno(QWidget):
    def __init__(self, mainApp: QWidget = None):    # -- initiates the module/main variables
        super().__init__()
        self.mainFrame = mainApp
        self.currentCell = None
        self.residentList = DatabaseQueries().getAllResidents()

        self.initUI()
        self.initConfigWidgets()
        self.initStyleSheets()
        self.initConfigConnections()
        self.initLayouts()

    def initUI(self) -> None:                       # -- Initiates Widgets
        self.backToMainBtn: QWidget = QPushButton("<--")                        # - QPushButtons
        self.scoreboardTable: QWidget = QTableWidget()
        self.submitPlayersBtn: QWidget = QPushButton('Submit')

        self.header: QWidget = QLabel("UNO")                                    # - QLabels
        self.playerSelectionLabel: QWidget = QLabel("Player Selection")
        self.residentsLabel: QWidget = QLabel("Residents")
        self.playersLabel: QWidget = QLabel("Players")

        self.residentListbox: QWidget = QListWidget()                           # - QListWidgets
        self.playerListBox: QWidget = QListWidget()

        self.widgetList: list = [self.backToMainBtn, self.header, self.residentsLabel,
                                self.playersLabel, self.residentListbox, self.playerListBox,
                                self.playerSelectionLabel
                                ]
        
        self.selectionWidgetList: list = [self.residentsLabel, self.playersLabel, self.residentListbox,
                                        self.playerListBox, self.playerSelectionLabel, self.submitPlayersBtn
                                        ]

        self.mainAppWidgetList = [self.header, self.scoreboardTable]

        self.loadResidentListbox()

    def initConfigWidgets(self) -> None:            # -- Configures widget settings
        self.playerListBox.setAcceptDrops(True)
        self.residentListbox.setAcceptDrops(True)

        self.playerListBox.setDragEnabled(True)
        self.residentListbox.setDragEnabled(True)

        self.playerListBox.setDragDropMode(QAbstractItemView.DragDropMode.DragDrop)
        self.residentListbox.setDragDropMode(QAbstractItemView.DragDropMode.DragDrop)

        self.playerListBox.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.residentListbox.setDefaultDropAction(Qt.DropAction.MoveAction)

        self.scoreboardTable.verticalHeader().setVisible(False)
        self.scoreboardTable.horizontalHeader().setVisible(False)
        self.scoreboardTable.setShowGrid(True)
        self.scoreboardTable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.scoreboardTable.setColumnCount(2)

    def initStyleSheets(self) -> None:              # -- Initiates the stylesheets for the application
        with open(os.path.join("stylesheets", "uno.css")) as file:
            self.setStyleSheet(file.read())

    def initConfigConnections(self) -> None:        # -- Configures connections between widgets and functions
        self.submitPlayersBtn.clicked.connect(self.submitPlayers)
        self.scoreboardTable.clicked.connect(self.currentCellClicked)

    def initLayouts(self) -> None:                  # -- Applies widgets to the layouts/applies layouts to app
        self.layout = QVBoxLayout()
        self.navButtonLayout = QHBoxLayout()
        self.playerSelectionLayout = QHBoxLayout()

        self.navButtonLayout.addWidget(self.backToMainBtn)

        self.playerSelectionLayout.addWidget(self.residentListbox)
        self.playerSelectionLayout.addWidget(self.playerListBox)

        self.layout.addLayout(self.navButtonLayout)
        self.layout.addWidget(self.header)
        self.layout.addWidget(self.scoreboardTable)
        self.layout.addWidget(self.playerSelectionLabel)
        self.layout.addLayout(self.playerSelectionLayout)
        self.layout.addWidget(self.submitPlayersBtn)

        self.setLayout(self.layout)

        for widg in self.mainAppWidgetList:
            widg.hide()

    def backToMain(self) -> None:                   # -- Returns to main application page
        pass

    def showAll(self) -> None:                      # -- Shows all widgets
        for widg in self.widgetList:
            widg.show()

    def hideAll(self) -> None:          
        for widg in self.widgetList:                # -- Hides all widgets
            widg.hide()

    def loadResidentListbox(self) -> None:          # -- Inserts resident informaiton into listbox
        for resident in self.residentList:
            self.residentListbox.addItem(f"{resident[1]} {resident[3][0]}.")

    def submitPlayers(self):
        self.playerList: list = []
        for item in range(self.playerListBox.count()):
            self.playerList.append(self.playerListBox.item(item).text())

        for widg in self.selectionWidgetList:
            widg.hide()
        
        for widg in self.mainAppWidgetList:
            widg.show()

        self.scoreboardTable.setRowCount(len(self.playerList) + 1)

        self.buildTable()

    def buildTable(self) -> None:                   # -- Inserts resident informaiton into the table
        headers: str = ["Names", "Wins"]
        for inx, head in enumerate(headers):
            self.scoreboardTable.setItem(0, inx, QTableWidgetItem(head))

        for inx, res in enumerate(self.playerList):
            inx += 1
            self.scoreboardTable.setItem(inx, 0, QTableWidgetItem(res)) 
            self.scoreboardTable.setItem(inx, 1, QTableWidgetItem("0"))

    def currentCellClicked(self) -> None:           # -- Determines the row/column the current cell is located in
        self.currentCell: tuple = (self.scoreboardTable.currentRow(), self.scoreboardTable.currentColumn())
        self.cellAction()

    def cellAction(self) -> None:                   # -- Generates Window for counting a win
        self.row = self.currentCell[0]
        self.column = self.currentCell[1]

        if self.row == 0 or self.column == 0:
            return
        
        self.winnerWindow: QWidget = QWidget()
        self.winnerWindow.layout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout()

        self.questionLabel: QWidget = QLabel("Winner?")
        self.noBtn: QWidget = QPushButton("No")
        self.yesBtn: QWidget = QPushButton("Yes")

        self.noBtn.clicked.connect(self.winnerWindow.close)
        self.yesBtn.clicked.connect(self.winnerWinner)

        self.buttonLayout.addWidget(self.noBtn)
        self.buttonLayout.addWidget(self.yesBtn)

        self.winnerWindow.layout.addWidget(self.questionLabel)
        self.winnerWindow.layout.addLayout(self.buttonLayout)

        self.winnerWindow.setLayout(self.winnerWindow.layout)

        self.winnerWindow.show()

    def winnerWinner(self) -> None:                 # -- Increases residents number of wins
        currentTotal: int = int(self.scoreboardTable.item(self.row, self.column).text())
        currentTotal += 1
        self.scoreboardTable.setItem(self.row, self.column, QTableWidgetItem(str(currentTotal)))
        self.winnerWindow.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    uno = Uno()
    uno.show()
    sys.exit(app.exec())