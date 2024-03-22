#! python3
#! bean_bag_toss.py -- Application for tracking scores for bean bag toss. 


import os, sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QApplication, QHBoxLayout, QVBoxLayout,
    QPushButton, QTableWidget, QLabel, QAbstractItemView,
    QTableWidgetItem, QLineEdit, QFormLayout
    )

from database_queries import DatabaseQueries
from player_selection import PlayerSelection

class BeanBagToss(QWidget):
    def __init__(self, mainApp: QWidget = None):        # -- initiates the module/main variables
        super().__init__()
        self.mainFrame = mainApp
        self.currentCell = None
        self.playerList = []
        self.residentList: list = DatabaseQueries().getAllResidents()
        self.currentPlayerScore: dict = {}
        self.rounds: list = [
            "NAMES", "ROUND 1", "ROUND 2",
            "ROUND 3", "ROUND 4", "ROUND 5",
            "ROUND 6", "ROUND 7", "TOTAL"]

        self.initUI()
        self.initConfigWidgets()
        self.initStyleSheets()
        self.initConfigConnections()
        self.initLayouts()

    def initUI(self) -> None:                           # -- Initiates Widgets
        self.backToMainBtn: QWidget = QPushButton("<--")
        self.refreshBtn: QWidget = QPushButton("Refresh")

        self.playerSelection: QWidget = PlayerSelection(self)
        self.header: QWidget = QLabel("Bean Bag Toss")
        self.scoreboardTable: QWidget = QTableWidget()
        self.scoreboardTable.item

        self.widgetList = [self.scoreboardTable, self.header]

    def initConfigWidgets(self) -> None:                # -- Configures widget settings
        self.scoreboardTable.verticalHeader().setVisible(False)
        self.scoreboardTable.horizontalHeader().setVisible(False)
        self.scoreboardTable.setShowGrid(True)
        self.scoreboardTable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.scoreboardTable.setColumnCount(9)

    def initStyleSheets(self) -> None:                  # -- Initiates the stylesheets for the application
        with open(os.path.join("stylesheets", "bean_bag_toss.css")) as file:
            self.setStyleSheet(file.read())

    def initConfigConnections(self) -> None:            # -- Configures connections between widgets and functions
        self.scoreboardTable.clicked.connect(self.currentCellClicked)

    def initLayouts(self) -> None:                      # -- Applies widgets to the layouts/applies layouts to app
        self.layout = QVBoxLayout()
        self.navLayout = QHBoxLayout()

        self.navLayout.addWidget(self.backToMainBtn)
        self.navLayout.addWidget(self.refreshBtn)

        self.layout.addLayout(self.navLayout)
        self.layout.addWidget(self.playerSelection)
        self.layout.addWidget(self.header)
        self.layout.addWidget(self.scoreboardTable)
        
        self.setLayout(self.layout)

        self.hideAll()

    def backToMain(self) -> None:                       # -- Returns to main application page
        pass

    def showAll(self) -> None:                          # -- Shows all widgets
        for widg in self.widgetList:
            widg.show()

    def hideAll(self) -> None:                          # -- Hide all widgets
        for widg in self.widgetList:
            widg.hide()

    def createTable(self) -> None:                      # -- Inserts the players and round informaiton
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
            self.scoreboardTable.setItem(inx + 1, 8, QTableWidgetItem("0"))
        
    def currentCellClicked(self) -> None:               # -- Finds the current active cell
        self.currentCell: tuple = (self.scoreboardTable.currentRow(), self.scoreboardTable.currentColumn())
        
        if self.currentCell[0] == 0 or self.currentCell[1] == 0 or self.currentCell[1] == 8:
            return
        
        self.openScoreWindow()

    def openScoreWindow(self) -> None:                  # -- Creates popup window for inputing scores
        self.scoreWindow: QWidget = QWidget()                       # QLabels
        self.beanBagLabel: QWidget = QLabel("Bean Bags:")
        self.tennisBallLabel: QWidget = QLabel("Tennis Ball:")
        self.diceLabel: QWidget = QLabel("Dice:")
        self.specialLabel: QWidget = QLabel("Special:")

        self.beanBagLine: QWidget = QLineEdit()                     # -- QlineEdits
        self.tennisBallLine: QWidget = QLineEdit()
        self.diceLine: QWidget = QLineEdit()
        self.specialLine: QWidget = QLineEdit()

        self.cancelBtn: QWidget = QPushButton("Cancel")             # -- QPushButtons
        self.submitBtn: QWidget = QPushButton("Submit")

        self.scoreWindowLineWidgets: list = [self.beanBagLine, self.tennisBallLine, self.diceLine, self.specialLine]

        self.cancelBtn.clicked.connect(self.scoreWindow.close)      # -- Connections
        self.submitBtn.clicked.connect(self.submitScore)

        self.scoreWindow.layout = QVBoxLayout()                     # -- QLayouts
        self.pointForm = QFormLayout()
        self.buttonLayout = QHBoxLayout()

        self.pointForm.addRow(self.beanBagLabel, self.beanBagLine)
        self.pointForm.addRow(self.tennisBallLabel, self.tennisBallLine)
        self.pointForm.addRow(self.diceLabel, self.diceLine)
        self.pointForm.addRow(self.specialLabel, self.specialLine)

        self.buttonLayout.addWidget(self.cancelBtn)
        self.buttonLayout.addWidget(self.submitBtn)

        self.scoreWindow.layout.addLayout(self.pointForm)
        self.scoreWindow.layout.addLayout(self.buttonLayout)

        self.scoreWindow.setLayout(self.scoreWindow.layout)

        self.scoreWindow.show()

    def submitScore(self) -> None:                      # -- Submits the score to the QTableWidget
        pointInfo: list = [x.text() for x in self.scoreWindowLineWidgets]
        blankLines: int = 0

        try:
            item = self.scoreboardTable.item(self.currentCell[0], self.currentCell[1]).text()
        except:
            item = None

        if item != None:
            currentTotal: int = int(self.scoreboardTable.item(self.currentCell[0], 8).text())
            currentCellAmount: int = int(self.scoreboardTable.item(self.currentCell[0], self.currentCell[1]).text())
            currentTotal -= currentCellAmount

            self.scoreboardTable.takeItem(self.currentCell[0], self.currentCell[1])
            self.scoreboardTable.setItem(self.currentCell[0], 8, QTableWidgetItem(str(currentTotal)))
        
        for inx, line in enumerate(pointInfo):
            if line == "":
                if blankLines > 3:
                    return self.clearLines()
                
                blankLines += 1
            
            try:
                pointInfo[inx] = int(line)
            except:
                return self.clearLines()
                
        row: int = self.currentCell[0]
        column: int = self.currentCell[1]

        currentTotal: int = sum([(pointInfo[0] * 3), (pointInfo[1] * 5), (pointInfo[2] * 10), (pointInfo[3] * 20)])
        total: int = int(self.scoreboardTable.item(row, 8).text())
        newTotal: str = str(total + currentTotal)

        self.scoreboardTable.setItem(row, column, QTableWidgetItem(str(currentTotal)))
        self.scoreboardTable.setItem(row, 8, QTableWidgetItem(newTotal))

        self.scoreWindow.close()

    def clearLines(self) -> None:                       # -- Clears QLineEdits for score window
        for line in self.scoreWindowLineWidgets:
            line.setText("")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    beanBagToss = BeanBagToss()
    beanBagToss.show()
    sys.exit(app.exec())
