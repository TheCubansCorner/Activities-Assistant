#! python3
#! yahtzee.py -- Application for scoreing Yahtzee

# myTableWidget->verticalHeader()->setVisible(false);

"""
TODO: Add top 3 display
TODO: Complete scoring for last 3 rounds 
"""

import sys, os


from PyQt6.QtWidgets import QWidget, QApplication, QTableWidget, QLabel
from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QHBoxLayout, QLineEdit
from PyQt6.QtWidgets import QTableWidgetItem, QCheckBox
from PyQt6.QtCore import Qt


from database_queries import DatabaseQueries
from player_selection import PlayerSelection
from top_three import TopThreeDisplay


class Yahtzee(QWidget):
    def __init__(self, mainApp: QWidget | None = None) -> None:                     # -- Initializes applicaiton 
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
        
    def initUI(self) -> None:                                                       # -- Initializes Widgets
        self.previousPageBtn: QWidget = QPushButton("<--")
        self.resetGameBtn: QWidget = QPushButton("Reset")
        self.yahtzeeLabel: QWidget = QLabel("YAHTZEE")
        self.scoreboardTable: QWidget = QTableWidget(self)
        self.playerSelection: QWidget = PlayerSelection(self)
        self.topThreeDisplay: QWidget = TopThreeDisplay(self, self.currentPlayerScore.copy())
        
        self.widgetList = [self.yahtzeeLabel, self.scoreboardTable, self.topThreeDisplay]

    def applyLayout(self) -> None:                                                  # -- Applies widgets to layout/sets primary layout
        self.layout = QVBoxLayout()
        self.navBtnLayout = QHBoxLayout()
        self.rowOneLayout = QHBoxLayout()
        self.combinedLayout = QVBoxLayout()

        self.navBtnLayout.addWidget(self.previousPageBtn)
        self.navBtnLayout.addWidget(self.resetGameBtn)

        self.rowOneLayout.addWidget(self.scoreboardTable)
        self.rowOneLayout.addWidget(self.topThreeDisplay)

        self.layout.addLayout(self.navBtnLayout)
        self.layout.addWidget(self.playerSelection, Qt.AlignmentFlag.AlignCenter)
        self.combinedLayout.addWidget(self.yahtzeeLabel)
        self.combinedLayout.addLayout(self.rowOneLayout)
        self.layout.addLayout(self.combinedLayout)

        self.setLayout(self.layout)

        for widg in self.widgetList:
            widg.hide()

    def applyStyles(self) -> None:                                                  # -- Applies the applications stylesheet
        self.yahtzeeLabel.setProperty("class", "header")

        self.yahtzeeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.scoreboardTable.setMinimumWidth(1101)
        self.scoreboardTable.setMaximumWidth(1101)

        with open(os.path.join("stylesheets", "yahtzee.css")) as file:
            self.setStyleSheet(file.read())

    def setConnections(self) -> None:                                               # -- Estabishes connecitons between widgets and functions
        self.previousPageBtn.clicked.connect(self.backToMain)
        self.resetGameBtn.clicked.connect(self.resetGame)
        self.scoreboardTable.clicked.connect(self.cellClicked)
        
    def backToMain(self) -> None:                                                   # -- Returns to the previous screen "self.mainFrame"
        if self.mainFrame:
            for widg in self.mainFrame.widgetList:
                widg.show()

            self.mainFrame.layout.removeWidget(self)
            self.destroy()
            self.close()
         
    def widgetSettings(self) -> None:                                               # -- Applies various widget settings (alignment, max size, etc)
        self.scoreboardTable.verticalHeader().setVisible(False)
        self.scoreboardTable.horizontalHeader().setVisible(False)
        self.scoreboardTable.setColumnCount(11)
        
        self.scoreboardTable.setShowGrid(True)
        self.yahtzeeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def createTable(self) -> None:                                                  # -- Creates the table for the scoreboard
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

    def resetGame(self) -> None:                                                    # -- Resets the game back to the resident seleciton area
        for widg in self.widgetList:
            widg.hide()

        self.playerSelection.show()

    def cellClicked(self) -> None:                                                  # -- Triggered when a cell is clicked to open the score menu
        column: int = self.scoreboardTable.currentColumn()
        row: int = self.scoreboardTable.currentRow()
        self.currentCell: tuple = (row, column)
        self.scoreWindow = QWidget()
        self.numberEntry: QWidget = QLineEdit()
        
        if row == 0 or column == 0:        # Returns to avoid triggering on round and name labels
            return

        if column == 1:
            header = "Round: 1"     
        elif column == 2:
            header = "Round: 2"
        elif column == 3:
            header = "Round: 3" 
        elif column == 4:
            header = "Round: 4"
        elif column == 5:
            header = "Round: 5"
        elif column == 6:
            header = "Round: 6"
        elif column == 7:
            header = "3 of a Kind"
        elif column == 8:
            header = "Strait"
        elif column == 9:
            header = "YAHTZEE?"
        else:
            return
            
        self.scoreRounds(column, header, row)

    def scoreRounds(self, column: int, header: str, row: int) -> None:              # -- Sets up window for scoring round 1 - 6
        self.scoreWindow.layout = QVBoxLayout()
        headerLabel: QWidget = QLabel(header)
        if self.scoreboardTable.item(self.scoreboardTable.currentRow(), column):
            if self.scoreboardTable.item(row, column).text():
                scoreReduction: int = int(self.scoreboardTable.item(row, column).text())
                currentTotal: int = str(int(self.scoreboardTable.item(row, 10).text()) - scoreReduction)
                self.currentPlayerScore[row] = currentTotal

                self.scoreboardTable.takeItem(row, column)
                self.scoreboardTable.setItem(row, 10, QTableWidgetItem(currentTotal))

                self.scoreRounds(column, header, row)          
        else:
            print(self.scoreboardTable.item(self.scoreboardTable.currentRow(), column))
            if column <= 6:     # Rounds 1-6
                diceNumberBtn: QWidget = QPushButton(str(column), clicked = lambda: self.updateScore(self.currentRoundScore(column)))
                
                self.scoreLayout = QHBoxLayout()

                self.scoreLayout.addWidget(self.numberEntry)
                self.scoreLayout.addWidget(diceNumberBtn)
                        
                self.scoreWindow.layout.addWidget(headerLabel)
                self.scoreWindow.layout.addLayout(self.scoreLayout)

                self.scoreWindow.setLayout(self.scoreWindow.layout)

                self.scoreWindow.show()
            elif column == 7:   # 3 of a Kind
                diceOne: QWidget = QPushButton("1")
                diceTwo: QWidget = QPushButton("2")
                diceThree: QWidget = QPushButton("3")
                diceFour: QWidget = QPushButton("4")
                diceFive: QWidget = QPushButton("5")
                diceSix: QWidget = QPushButton("6")

                self.buttonLayoutOne = QHBoxLayout()
                self.buttonLayoutTwo = QHBoxLayout()

                diceOne.clicked.connect(lambda: self.updateScore(self.currentRoundScore(column, diceOne.text())))
                diceTwo.clicked.connect(lambda: self.updateScore(self.currentRoundScore(column, diceTwo.text())))
                diceThree.clicked.connect(lambda: self.updateScore(self.currentRoundScore(column, diceThree.text())))
                diceFour.clicked.connect(lambda: self.updateScore(self.currentRoundScore(column, diceFive.text())))
                diceFive.clicked.connect(lambda: self.updateScore(self.currentRoundScore(column, diceFive.text())))
                diceSix.clicked.connect(lambda: self.updateScore(self.currentRoundScore(column, diceSix.text())))

                self.scoreWindow.layout.addWidget(headerLabel)
                self.scoreWindow.layout.addWidget(self.numberEntry)
                
                self.buttonLayoutOne.addWidget(diceOne)
                self.buttonLayoutOne.addWidget(diceTwo)
                self.buttonLayoutOne.addWidget(diceThree)
                
                self.buttonLayoutTwo.addWidget(diceFour)
                self.buttonLayoutTwo.addWidget(diceFive)
                self.buttonLayoutTwo.addWidget(diceSix)

                self.scoreWindow.layout.addLayout(self.buttonLayoutOne)
                self.scoreWindow.layout.addLayout(self.buttonLayoutTwo)

                self.scoreWindow.setLayout(self.scoreWindow.layout)

                self.scoreWindow.show()
            elif column == 8:   # Strait
                self.scoreList = []

                radioLayout = QHBoxLayout()

                diceOne: QWidget = QCheckBox("1")
                diceTwo: QWidget = QCheckBox("2")
                diceThree: QWidget = QCheckBox("3")
                diceFour: QWidget = QCheckBox("4")
                diceFive: QWidget = QCheckBox("5")
                diceSix: QWidget = QCheckBox("6")
                submitBtn: QWidget = QPushButton("Submit")

                diceOne.clicked.connect(lambda: self.straitScore(diceOne))
                diceTwo.clicked.connect(lambda: self.straitScore(diceTwo))
                diceThree.clicked.connect(lambda: self.straitScore(diceThree))
                diceFour.clicked.connect(lambda: self.straitScore(diceFour))
                diceFive.clicked.connect(lambda: self.straitScore(diceFive))
                diceSix.clicked.connect(lambda: self.straitScore(diceOne))
                submitBtn.clicked.connect(lambda: self.updateScore(self.currentRoundScore(column, self.scoreList)))

                radioLayout.addWidget(diceOne)
                radioLayout.addWidget(diceTwo)
                radioLayout.addWidget(diceThree)
                radioLayout.addWidget(diceFour)
                radioLayout.addWidget(diceFive)
                radioLayout.addWidget(diceSix)
                self.scoreWindow.layout.addLayout(radioLayout)
                self.scoreWindow.layout.addWidget(submitBtn)

                self.scoreWindow.setLayout(self.scoreWindow.layout)

                self.scoreWindow.show()
            elif column == 9:   # Yahtzee
                yesBtn: QWidget = QPushButton("Yes")
                noBtn: QWidget = QPushButton("No")

                btnLayout = QHBoxLayout()

                yesBtn.clicked.connect(lambda: self.updateScore(50))
                noBtn.clicked.connect(self.scoreWindow.close)

                btnLayout.addWidget(noBtn)
                btnLayout.addWidget(yesBtn)
                self.scoreWindow.layout.addWidget(headerLabel)
                self.scoreWindow.layout.addLayout(btnLayout)

                self.scoreWindow.setLayout(self.scoreWindow.layout)

                self.scoreWindow.show()

    def straitScore(self, dice: QWidget) -> None:                                   # -- Builds list for calculating strait score
        if dice.isChecked():
            self.scoreList.append(dice.text())    
        else:
            try:
                self.scoreList.remove(dice.text())
            except:
                pass

    def currentRoundScore(self, column: int, dice: int | list = None) -> int:       # -- Calculates the current rounds score
        alpha: str = "abcdefghijklmnopqrstuvwxyz"   # need to make this better maybe with regular expressions?
        
        if self.numberEntry.text().lower() not in alpha:
            if column <= 6:
                score = column * int(self.numberEntry.text()) if self.numberEntry.text() != "" else 0 
                return score
        elif column == 7:
            score = int(self.numberEntry.text()) * int(dice)
            return score
        elif column == 8:
            score = 0
            for i in dice:
                score += int(i) 
            return score
        else:
            print("false")
            return False

    def updateScore(self, score: int) -> None:                                      # -- Updates the residents current score as well as their total
        if score:
            score: str = str(score)
            total: str = self.totalScore(score)
            self.scoreboardTable.setItem(self.currentCell[0], self.currentCell[1], QTableWidgetItem(score))
            self.scoreboardTable.setItem(self.currentCell[0], 10, QTableWidgetItem(total))
            self.topThreeDisplay.playerDict = self.currentPlayerScore.copy()
            self.topThreeDisplay.findTopThree()
            
        self.scoreWindow.destroy()
        self.scoreWindow.close()
         
    def totalScore(self, score: str) -> str:                                        # -- Calculates the total score for the current resident
        row = self.scoreboardTable.currentRow()
        currentTotal = self.currentPlayerScore[row]
        currentTotal = int(currentTotal) + int(score)
        self.currentPlayerScore[row] = currentTotal

        return str(currentTotal)
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    yahtzee = Yahtzee()
    yahtzee.show()
    sys.exit(app.exec())