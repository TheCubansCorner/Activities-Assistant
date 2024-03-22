#! python3
#! app_list_window.py -- Main Menu for accessing applications

import sys, os

from PyQt6.QtWidgets import QLabel, QPushButton, QWidget, QApplication
from PyQt6.QtWidgets import QMainWindow, QGridLayout
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import QSize, Qt

from resident_lookup import ResidentLookup
from bingo import Bingo
from yahtzee import Yahtzee
from bocceball import BocceBall
from bean_bag_toss import BeanBagToss
from uno import Uno

class AppListWindow(QWidget):
    def __init__(self, mainApp: QMainWindow = None, user: tuple = None) -> None:        # -- Initiates the module
        super().__init__()
        self.mainApp = mainApp
        self.appDict: dict = {
            "residentLookup" : ResidentLookup(self),
            "residentHistory" : None,
            "yahtzee" : Yahtzee(self),
            "beanBagToss" : BeanBagToss(self),
            "bingo" : Bingo(self),
            "bocceBall" : BocceBall(self),
            "uno" : Uno(self),
            "bowling" : None
        }

        self.initUI()
        self.applyLayouts()
        self.setConnections()
        self.applyStylsheets()
        self.applyBtnImg()
    
    def initUI(self) -> None:                                       # -- Creates WIdgets
        self.header: QWidget = QLabel()
        self.residentLookupBtn: QWidget = QPushButton()                                              # -- QPushButtons
        self.residentHistoryBtn: QWidget = QPushButton()
        self.yahtzeeBtn: QWidget = QPushButton()
        self.beanBagTossBtn: QWidget = QPushButton()
        self.bingoBtn: QWidget = QPushButton()
        self.bocceBallBtn: QWidget = QPushButton()
        self.unoBtn: QWidget = QPushButton()
        self.bowlingBtn: QWidget = QPushButton()

        self.widgetList: list = [
            self.residentLookupBtn, self.residentHistoryBtn, self.yahtzeeBtn,
            self.beanBagTossBtn, self.bingoBtn, self.bocceBallBtn,
            self.unoBtn, self.bowlingBtn, self.header
            ]

    def applyLayouts(self) -> None:                                 # -- Applies layouts to the applicaiton
        self.layout = QGridLayout()
        
        self.layout.addWidget(self.header, 0, 0, 1, 8, Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.residentLookupBtn, 1, 0, Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.residentHistoryBtn, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.yahtzeeBtn, 1, 2, Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.beanBagTossBtn, 1, 3, Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.bingoBtn, 1, 4, Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.bocceBallBtn, 1, 5, Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.unoBtn, 1, 6, Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.bowlingBtn, 1, 7, Qt.AlignmentFlag.AlignCenter)



        self.setLayout(self.layout)

    def setConnections(self) -> None:                               # -- Establishes connections for widgets to functions
        self.residentLookupBtn.clicked.connect(lambda: self.openApp(self.appDict["residentLookup"]))
        self.residentHistoryBtn.clicked.connect(lambda: self.openApp(self.appDict["residentHistory"]))
        self.yahtzeeBtn.clicked.connect(lambda: self.openApp(self.appDict["yahtzee"]))
        self.beanBagTossBtn.clicked.connect(lambda: self.openApp(self.appDict["beanBagToss"]))
        self.bingoBtn.clicked.connect(lambda: self.openApp(self.appDict["bingo"]))
        self.bocceBallBtn.clicked.connect(lambda: self.openApp(self.appDict["bocceBall"]))
        self.unoBtn.clicked.connect(lambda: self.openApp(self.appDict["uno"]))

    def applyStylsheets(self) -> None:
        self.header.setMaximumHeight(400)
        self.header.setMaximumWidth(500)
        pixmap: QPixmap = QPixmap(os.path.join("app_icons", "fec.png"))
        pixmap = pixmap.scaled(500, 500, Qt.AspectRatioMode.KeepAspectRatio)                            # -- Applies stylesheets to the application
        self.header.setPixmap(pixmap)

        for widg in self.widgetList[:-1:1]:
            widg.setMaximumHeight(150)
            widg.setMaximumWidth(200)
            widg.setMinimumHeight(150)
            widg.setMinimumWidth(200)

        self.header.setProperty("class", "header")
        self.residentLookupBtn.setProperty("class", "app")
        self.residentHistoryBtn.setProperty("class", "app")
        self.yahtzeeBtn.setProperty("class", "app")
        self.beanBagTossBtn.setProperty("class", "app")
        self.bingoBtn.setProperty("class", "app")
        self.bocceBallBtn.setProperty("class", "app")
        self.unoBtn.setProperty("class", "app")

        with open(os.path.join("stylesheets", "app_list_window.css")) as file:
            self.setStyleSheet(file.read())

    def applyBtnImg(self) -> None:                                  # -- Applies images to the different button options
        for _, _, file in os.walk("app_icons"):
            images: list = file

        for inx, item in enumerate(self.widgetList):
            if item != self.widgetList[-1]:
                item.setIcon(QIcon(os.path.join("app_icons", images[inx])))
                item.setIconSize(QSize(100, 100))

    def openApp(self, currentApp) -> None:                          # -- Opens individual application in current window.
        if currentApp:
            for item in self.widgetList:
                item.hide()
            self.layout.addWidget(currentApp)
            currentApp.show()


if __name__ == "__main__":
    app: QWidget = QApplication(sys.argv)
    appListWindow = AppListWindow()
    appListWindow.show()
    sys.exit(app.exec())