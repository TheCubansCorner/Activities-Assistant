#! python3
#! yahtzee.py -- Application for scoreing Yahtzee

# myTableWidget->verticalHeader()->setVisible(false);

import sys, os


from PyQt6.QtWidgets import QWidget, QApplication, QTableWidget, QLabel
from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QHBoxLayout, QLineEdit
from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6.QtCore import Qt


from database_queries import DatabaseQueries
from player_selection import PlayerSelection

class Yahtzee(QWidget):
    def __init__(self, mainApp: QWidget | None = None) -> None:
        super().__init__()
        self.playerList = None
        self.gameReset: bool = True
        self.mainFrame: QWidget = mainApp
        self.residentList: list = DatabaseQueries().getAllResidents()
        self.currentPlayerScore: dict = {}
        self.rounds: list = ["NAMES", "ROUND 1", "ROUND 2",
                             "ROUND 3", "ROUND 4", "ROUND 5",
                             "ROUND 6", "3K", "STRAIT",
                             "YAHTZEE", "TOTAL"
                             ]

        self.initUI()
        self.applyStyles()
        self.widgetSettings()
        self.setConnections()
        self.applyLayout()  
        
    def initUI(self) -> None:
        self.previousPageBtn: QWidget = QPushButton("<--")
        self.resetGameBtn: QWidget = QPushButton("Reset")
        self.yahtzeeLabel: QWidget = QLabel("YAHTZEE")
        self.scoreboardTable: QWidget = QTableWidget(self)
        self.playerSelection: QWidget = PlayerSelection(self)
        
        self.widgetList = [self.yahtzeeLabel, self.scoreboardTable]

    def applyLayout(self) -> None:
        self.layout = QVBoxLayout()
        self.navBtnLayout = QHBoxLayout()

        self.navBtnLayout.addWidget(self.previousPageBtn)
        self.navBtnLayout.addWidget(self.resetGameBtn)

        self.layout.addLayout(self.navBtnLayout)
        self.layout.addWidget(self.playerSelection, Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.yahtzeeLabel)
        self.layout.addWidget(self.scoreboardTable)

        self.setLayout(self.layout)

        for widg in self.widgetList:
            widg.hide()

    def applyStyles(self) -> None:
        with open(os.path.join("stylesheets", "yahtzee.css")) as file:
            self.setStyleSheet(file.read())

    def setConnections(self) -> None:
        self.previousPageBtn.clicked.connect(self.backToMain)
        self.resetGameBtn.clicked.connect(self.resetGame)
        self.scoreboardTable.clicked.connect(self.cellClicked)
        
    def backToMain(self) -> None:
        if self.mainFrame:
            for widg in self.mainFrame.widgetList:
                widg.show()

            self.mainFrame.layout.removeWidget(self)
            self.destroy()
            self.close()
         
    def widgetSettings(self) -> None:
        self.scoreboardTable.verticalHeader().setVisible(False)
        self.scoreboardTable.horizontalHeader().setVisible(False)
        self.scoreboardTable.setColumnCount(11)
        
        self.scoreboardTable.setShowGrid(True)
        self.yahtzeeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def createTable(self) -> None:  
        # Create horizontal layout
        for inx, title in enumerate(self.rounds):
            label: QWidget = QLabel(title)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.scoreboardTable.setCellWidget(0, inx, label)

        # Create Vertical Layout
        for inx, title in enumerate(self.playerList):
            label: QWidget = QLabel(title)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.scoreboardTable.setCellWidget(inx + 1, 0, label)

    def resetGame(self) -> None:
        for widg in self.widgetList:
            widg.hide()

        self.playerSelection.show()

    def cellClicked(self) -> None:
        column: int = self.scoreboardTable.currentColumn()
        self.currentCell: tuple = (self.scoreboardTable.currentRow(), column)
        self.scoreWindow = QWidget()
        self.numberEntry: QWidget = QLineEdit()
        
        if column == 1:
            header = "1"     
        elif column == 2:
            header = "2"
        elif column == 3:
            header = "3" 
        elif column == 4:
            header = "4"
        elif column == 5:
            header = "5"
        elif column == 6:
            header = "6"
        else:
            if column == 7:    
                return
            
        headerLabel: QWidget = QLabel(f"Round {header}")
        diceNumberBtn: QWidget = QPushButton(header, clicked = lambda: self.updateScore(self.currentRoundScore(column)))
        self.scoreWindow.layout = QVBoxLayout()
        self.scoreLayout = QHBoxLayout()

        self.scoreLayout.addWidget(self.numberEntry)
        self.scoreLayout.addWidget(diceNumberBtn)
                
        self.scoreWindow.layout.addWidget(headerLabel)
        self.scoreWindow.layout.addLayout(self.scoreLayout)

        self.scoreWindow.setLayout(self.scoreWindow.layout)

        self.scoreWindow.show()
    
    def currentRoundScore(self, column: int) -> int:
        if self.numberEntry.text().lower() not in "abcdefghijklmnopqrstuvwxyz":
            score = column * int(self.numberEntry.text()) if self.numberEntry.text() != "" else 0 
            return score
        else:
            return False

    def updateScore(self, score: int) -> None:
        if score:
            score: str = str(score)
            total: str = self.totalScore(score)
            self.scoreboardTable.setItem(self.currentCell[0], self.currentCell[1], QTableWidgetItem(score))
            self.scoreboardTable.setItem(self.currentCell[0], 10, QTableWidgetItem(total))
        
        self.scoreWindow.destroy()
        self.scoreWindow.close()
    
    def totalScore(self, score: str) -> str:
        row = self.scoreboardTable.currentRow()
        currentTotal = self.currentPlayerScore[row]
        currentTotal += int(score)
        self.currentPlayerScore[row] = currentTotal

        return str(currentTotal)
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    yahtzee = Yahtzee()
    yahtzee.show()
    sys.exit(app.exec())