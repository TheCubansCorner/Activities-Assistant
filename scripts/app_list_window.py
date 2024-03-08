#! python3
#! app_list_window.py -- Main Menu for accessing applications

import sys, os

from PyQt6.QtWidgets import QLabel, QPushButton, QWidget, QApplication, QVBoxLayout, QHBoxLayout, QMainWindow
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize

from resident_lookup import ResidentLookup

class AppListWindow(QWidget):
    def __init__(self, mainApp: QMainWindow = None) -> None:
        super().__init__()
        self.mainApp = mainApp
        self.appDict: dict = {
            "residentLookup" : ResidentLookup(self),
            "residentHistory" : None,
            "yahtzee" : None,
            "beanBagToss" : None,
            "bingo" : None,
            "bocceBall" : None,
            "uno" : None
        }

        self.initUI()
        self.applyLayouts()
        self.setConnections()
        self.applyStylsheets()
        self.applyBtnImg()
    
    def initUI(self) -> None:
        self.residentLookupLabel: QWidget = QLabel("Resident Lookup")                                       # -- QLabels
        self.residentHistoryLabel: QWidget = QLabel("Historic Data")
        self.yahtzeeLabel: QWidget = QLabel("Yahtzee")
        self.beanBagTossLabel: QWidget = QLabel("Bean Bag Toss")
        self.bingoLabel: QWidget = QLabel("Bingo")
        self.bocceBallLabel: QWidget = QLabel("Bocce Ball")
        self.unoLabel: QWidget = QLabel("Uno Tracker")

        self.residentLookupBtn: QWidget = QPushButton()                                              # -- QPushButtons
        self.residentHistoryBtn: QWidget = QPushButton()
        self.yahtzeeBtn: QWidget = QPushButton()
        self.beanBagTossBtn: QWidget = QPushButton()
        self.bingoBtn: QWidget = QPushButton()
        self.bocceBallBtn: QWidget = QPushButton()
        self.unoBtn: QWidget = QPushButton()

        self.labelList: list = [                                                                            # -- Widget Lists
            self.residentLookupLabel, self.residentHistoryLabel, self.yahtzeeLabel,
            self.beanBagTossLabel, self.bingoLabel, self.bocceBallLabel,
            self.unoLabel
            ]
        self.buttonList: list = [
            self.residentLookupBtn, self.residentHistoryBtn, self.yahtzeeBtn,
            self.beanBagTossBtn, self.bingoBtn, self.bocceBallBtn,
            self.unoBtn
            ]

    def applyLayouts(self) -> None:
        self.layout = QVBoxLayout()
        self.appButtonLayout = QHBoxLayout()

        for inx, item in enumerate(self.labelList):
            layout = QVBoxLayout()
            layout.addWidget(item)
            layout.addWidget(self.buttonList[inx])
            self.appButtonLayout.addLayout(layout)

        self.layout.addLayout(self.appButtonLayout)

        self.setLayout(self.layout)

    def setConnections(self) -> None:
        self.residentLookupBtn.clicked.connect(lambda: self.openApp(self.appDict["residentLookup"]))
        self.residentHistoryBtn.clicked.connect(lambda: self.openApp(self.appDict["residentHistory"]))
        self.yahtzeeBtn.clicked.connect(lambda: self.openApp(self.appDict["yahtzee"]))
        self.beanBagTossBtn.clicked.connect(lambda: self.openApp(self.appDict["beanBagToss"]))
        self.bingoBtn.clicked.connect(lambda: self.openApp(self.appDict["bingo"]))
        self.bocceBallBtn.clicked.connect(lambda: self.openApp(self.appDict["bocceBall"]))
        self.unoBtn.clicked.connect(lambda: self.openApp(self.appDict["uno"]))

    def applyStylsheets(self) -> None:
        pass

    def applyBtnImg(self) -> None:
        for _, _, file in os.walk("app_icons"):
            images: list = file

        for inx, item in enumerate(self.buttonList):
            item.setIcon(QIcon(os.path.join("app_icons", images[inx])))
            item.setIconSize(QSize(100, 100))

    def openApp(self, currentApp) -> None:
        for inx, item in enumerate(self.buttonList):
            item.hide()
            self.labelList[inx].hide()
            self.layout.addWidget(currentApp)
            currentApp.show()


if __name__ == "__main__":
    app: QWidget = QApplication(sys.argv)
    appListWindow = AppListWindow()
    appListWindow.show()
    sys.exit(app.exec())