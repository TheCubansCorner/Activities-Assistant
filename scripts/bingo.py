#! python3
#! bingo.py -- Application for running bingo and tracking winners

import sys, os, random

from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QListWidget
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QComboBox
from PyQt6.QtCore import Qt

from database_queries import DatabaseQueries

class Bingo(QWidget):
    def __init__(self, mainApp: QWidget = None) -> None:
        super().__init__()
        self.mainFrame: QWidget = mainApp
        self.letterList: list = []
        self.usedLetters: list = []
        self.residentList: list = DatabaseQueries().getAllResidents()

        self.initUI()
        self.applyStyleSheets()
        self.applyLayout()
        self.setConnections()
        
    def initUI(self) -> None:
        self.previousPageBtn: QWidget = QPushButton("<--")
        self.resetGameBtn: QWidget = QPushButton("Refresh")
        self.currentRoundDisplay: QWidget = QPushButton('START')
        self.winnerBtn: QWidget = QPushButton("WINNER")
        self.bingoLabel: QWidget = QLabel("BINGO")
        self.usedLetterLabel: QWidget = QLabel("Used Letters")
        self.usedListbox: QWidget = QListWidget()

        self.widgetList: list = [self.currentRoundDisplay, self.winnerBtn, self.bingoLabel, self.previousPageBtn, self.resetGameBtn]

    def applyLayout(self) -> None:
        self.layout = QVBoxLayout()
        self.navigationLayout = QHBoxLayout()
        self.usedLettersLayout = QVBoxLayout()
        self.mainGameLayout = QVBoxLayout()
        self.combinedLayout = QHBoxLayout()

        self.navigationLayout.addWidget(self.previousPageBtn)
        self.navigationLayout.addWidget(self.resetGameBtn)

        self.mainGameLayout.addLayout(self.navigationLayout)
        self.mainGameLayout.addWidget(self.bingoLabel)
        self.mainGameLayout.addWidget(self.currentRoundDisplay)
        self.mainGameLayout.addWidget(self.winnerBtn)

        self.usedLettersLayout.addWidget(self.usedLetterLabel)
        self.usedLettersLayout.addWidget(self.usedListbox)

        self.combinedLayout.addLayout(self.mainGameLayout)
        self.combinedLayout.addLayout(self.usedLettersLayout)

        self.layout.addLayout(self.combinedLayout)

        self.setLayout(self.layout)

    def setConnections(self) -> None:
        self.previousPageBtn.clicked.connect(self.backToMain)
        self.currentRoundDisplay.clicked.connect(self.generateLetter)
        self.resetGameBtn.clicked.connect(self.resetGame)
        self.winnerBtn.clicked.connect(self.selectWinner)

    def applyStyleSheets(self) -> None:
        self.bingoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.currentRoundDisplay.setFixedSize(1630, 850)
        self.usedListbox.setMaximumWidth(200)

        self.currentRoundDisplay.setProperty("class", "currentletter")
        self.bingoLabel.setProperty("class", "header")
        self.usedLetterLabel.setProperty("class", "usedlabel")
        self.usedListbox.setProperty("class", "usedlist")
        
        with open(os.path.join("stylesheets", "bingo.css")) as file:
            self.setStyleSheet(file.read())

    def backToMain(self) -> None:
        if self.mainFrame:
            for widg in self.mainFrame.widgetList:
                widg.show()

            self.resetGame()
            self.destroy()
            self.close()
            self.mainFrame.layout.removeWidget(self)

    def generateLetter(self):
        if not self.letterList:
            self.letterList = [
                "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "B10", "B11", "B12", "B13", "B14", "B15",
                "I16", "I17", "I18", "I19", "I20", "I21", "I22", "I23", "I24", "I25", "I26", "I27", "I28", "I29", "I30",
                "N31", "N32", "N33", "N34", "N35", "N36", "N37", "N38", "N39", "N40", "N41", "N42", "N43", "N44", "N45",
                "G46", "G47", "G48", "G49", "G50", "G51", "G52", "G53", "G54", "G55", "G56", "G57", "G58", "G59", "G60",
                "O61", "O62", "O63", "O64", "O65", "O66", "O67", "O68", "O69", "O70", "O71", "O72", "O73", "O74", "O75"
            ]

        random.shuffle(self.letterList)     
        letterToDisplay: str = random.choice(self.letterList)

        self.letterList.remove(letterToDisplay)
        self.usedLetters.append(letterToDisplay)

        self.usedListbox.clear()
        self.usedLetters.sort()
        for letter in self.usedLetters:
            self.usedListbox.addItem(letter)

        self.currentRoundDisplay.setText(letterToDisplay)
    
    def resetGame(self) -> None:
        self.letterList: list = []
        self.usedLetters: list = []
        self.currentRoundDisplay.setText("Press to Start")
        self.usedListbox.clear()

    def selectWinner(self) -> None:
        self.app = QWidget()

        self.residentCombo: QWidget = QComboBox()
        self.submitWinnerBtn: QWidget = QPushButton("Submit")
        self.cancelBtn: QWidget = QPushButton("Cancel")

        self.buttonLayout = QHBoxLayout()
        self.vLayout = QVBoxLayout()

        self.buttonLayout.addWidget(self.cancelBtn)
        self.buttonLayout.addWidget(self.submitWinnerBtn)
        self.vLayout.addWidget(self.residentCombo)
        self.vLayout.addLayout(self.buttonLayout)

        self.cancelBtn.clicked.connect(self.app.close)
        self.submitWinnerBtn.clicked.connect(self.submitWinner)
        
        self.residentCombo.addItem("------------")
        for resident in self.residentList:
            self.residentCombo.addItem(f"{resident[1]} {resident[2]} {resident[3]}")

        self.app.setLayout(self.vLayout)

        self.app.show()
    
    def submitWinner(self) -> None:
        winner = self.residentCombo.currentText()
        
        if winner == "------------":
            return
        
        print(winner)
        
        # SUbmit to winner database for wins


if __name__ == "__main__":
    app = QApplication(sys.argv)
    bingo = Bingo()
    bingo.show()
    sys.exit(app.exec())
