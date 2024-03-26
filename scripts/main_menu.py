#! python3 
#! main_menu.py -- Main menu that houses all external applications

import os, sys

from PyQt6.QtGui import QIcon
from PyQt6.QtCore  import Qt, QSize
from PyQt6.QtWidgets import (
    QApplication, QWidget, QMainWindow, QLabel, 
    QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout
)

from resident_lookup import ResidentLookup
from bingo import Bingo
from yahtzee import Yahtzee
from bocceball import BocceBall
from bean_bag_toss import BeanBagToss
from uno import Uno
from bowling import Bowling
from historic import HistoricData


class MainMenu(QMainWindow):
    def __init__(self, user: int = None):
        super().__init__()
        self.currentApp = None
        self.applicationDictionary: dict = {
            "lookup" : ("\tResident Lookup", ResidentLookup(self)),
            "historic" : ("\tHistoric Database", HistoricData(self)),
            "yahtzee" : ("\tYahtzee", Yahtzee(self)),
            "beanbag" : ("\tBean Bag Toss", BeanBagToss(self)),
            "bingo" : ("\tBingo", Bingo(self)),
            "bocce" : ("\tBocce Ball", BocceBall(self)),
            "uno" : ("\tUNO", Uno(self)),
            "bowling" : ("\tBowling", Bowling(self))
        }

        self.widgetDictionary: dict = {
            "buttons" : None,
            "labels" : None,
        }
        
        self.initSideMenuWidgets()
        self.sideMenuLayouts()
        self.initMainLayout()
        self.initStyleSheets()
        self.initConfigConnections()
        self.applyMenuBtnImg()
        self.initConfigWidgets()
        
        self.setCentralWidget(self.mainContainer)

    def initSideMenuWidgets(self) -> None:
        self.mainContainer = QWidget()                                              # - QWidgets
        self.colapsedMenu = QWidget()
        self.expandedMenu = QWidget()
        self.currentApplication = QWidget()

        self.expandBtn: QWidget = QPushButton()                                # - QPushButtons
        self.colapsedResidentLookupBtn: QWidget = QPushButton()
        self.colapsedHistoricLookupBtn: QWidget = QPushButton()
        self.colapsedYahtzeeBtn: QWidget = QPushButton()
        self.colapsedBeanBagTossBtn: QWidget = QPushButton()
        self.colapsedBingoBtn: QWidget = QPushButton()
        self.colapsedBocceBallBtn: QWidget = QPushButton()
        self.colapsedUnoBtn: QWidget = QPushButton()
        self.colapsedBowlingBtn: QWidget = QPushButton()
        self.colapsedExitBtn: QWidget = QPushButton("X")

        self.colapseBtn: QWidget = QPushButton()
        self.expandedResidentLookupBtn: QWidget = QPushButton("    Resident Lookup")
        self.expandedHistoricLookupBtn: QWidget = QPushButton("    Historic Database")
        self.expandedYahtzeeBtn: QWidget = QPushButton("    Yahtzee")
        self.expandedBeanBagTossBtn: QWidget = QPushButton("    Bean Bag Toss")
        self.expandedBingoBtn: QWidget = QPushButton("    Bingo")
        self.expandedBocceBallBtn: QWidget = QPushButton("    Bocce Ball")
        self.expandedUnoBtn: QWidget = QPushButton("    Uno")
        self.expandedBowlingBtn: QWidget = QPushButton("    Bowling")
        self.expandedExitBtn: QWidget = QPushButton("    X")

        self.colapsedWidgetList: list = [
            self.expandBtn, self.colapsedResidentLookupBtn, self.colapsedHistoricLookupBtn,
            self.colapsedYahtzeeBtn, self.colapsedBeanBagTossBtn, self.colapsedBingoBtn, 
            self.colapsedBocceBallBtn, self.colapsedUnoBtn, self.colapsedBowlingBtn, 
            self.colapsedExitBtn,
        ]

        self.expandedWidgetList: list = [
            self.colapseBtn, self.expandedResidentLookupBtn, self.expandedHistoricLookupBtn, 
            self.expandedYahtzeeBtn, self.expandedBeanBagTossBtn, self.expandedBingoBtn, 
            self.expandedBocceBallBtn, self.expandedUnoBtn, self.expandedBowlingBtn, 
            self.expandedExitBtn
        ]
        
    def initConfigWidgets(self) -> None:
        self.showFullScreen()
        self.setFixedSize(self.size())
        
        self.mainContainer.layout.setContentsMargins(0,0,0,0)

        self.currentApplication.setMaximumHeight(self.height())
        self.colapsedMenu.setMaximumWidth(50)
        self.expandedMenu.setMaximumWidth(200)

        self.expandedMenu.hide()

    def initConfigConnections(self) -> None:
        self.expandBtn.clicked.connect(self.expandSideMenu)
        self.colapsedResidentLookupBtn.clicked.connect(lambda: self.openApp(self.applicationDictionary["lookup"][1]))
        self.colapsedHistoricLookupBtn.clicked.connect(lambda: self.openApp(self.applicationDictionary["historic"][1]))
        self.colapsedYahtzeeBtn.clicked.connect(lambda: self.openApp(self.applicationDictionary["yahtzee"][1]))
        self.colapsedBeanBagTossBtn.clicked.connect(lambda: self.openApp(self.applicationDictionary["beanbag"][1]))
        self.colapsedBingoBtn.clicked.connect(lambda: self.openApp(self.applicationDictionary["bingo"][1]))
        self.colapsedBocceBallBtn.clicked.connect(lambda: self.openApp(self.applicationDictionary["bocce"][1]))
        self.colapsedUnoBtn.clicked.connect(lambda: self.openApp(self.applicationDictionary["uno"][1]))
        self.colapsedBowlingBtn.clicked.connect(lambda: self.openApp(self.applicationDictionary["bowling"][1]))
        self.colapsedExitBtn.clicked.connect(sys.exit)

        self.colapseBtn.clicked.connect(self.colapseSideMenu)
        self.expandedResidentLookupBtn.clicked.connect(lambda: self.openApp(self.applicationDictionary["lookup"][1]))
        self.expandedHistoricLookupBtn.clicked.connect(lambda: self.openApp(self.applicationDictionary["historic"][1]))
        self.expandedYahtzeeBtn.clicked.connect(lambda: self.openApp(self.applicationDictionary["yahtzee"][1]))
        self.expandedBeanBagTossBtn.clicked.connect(lambda: self.openApp(self.applicationDictionary["beanbag"][1]))
        self.expandedBingoBtn.clicked.connect(lambda: self.openApp(self.applicationDictionary["bingo"][1]))
        self.expandedBocceBallBtn.clicked.connect(lambda: self.openApp(self.applicationDictionary["bocce"][1]))
        self.expandedUnoBtn.clicked.connect(lambda: self.openApp(self.applicationDictionary["uno"][1]))
        self.expandedBowlingBtn.clicked.connect(lambda: self.openApp(self.applicationDictionary["bowling"][1]))
        self.expandedExitBtn.clicked.connect(sys.exit)

    def sideMenuLayouts(self) -> None:
        self.mainContainer.layout = QHBoxLayout()
        self.colapsedMenu.layout = QGridLayout()
        self.expandedMenu.layout = QGridLayout()
        self.currentApplication.layout = QVBoxLayout()
    
        self.colapsedMenu.layout.addWidget(self.expandBtn, 0, 0)                          # - colapsed Menu
        self.colapsedMenu.layout.addWidget(self.colapsedResidentLookupBtn, 1, 0)
        self.colapsedMenu.layout.addWidget(self.colapsedHistoricLookupBtn, 2, 0)
        self.colapsedMenu.layout.addWidget(self.colapsedYahtzeeBtn, 3, 0)
        self.colapsedMenu.layout.addWidget(self.colapsedBeanBagTossBtn, 4, 0)
        self.colapsedMenu.layout.addWidget(self.colapsedBingoBtn, 5, 0)
        self.colapsedMenu.layout.addWidget(self.colapsedBocceBallBtn, 6, 0)
        self.colapsedMenu.layout.addWidget(self.colapsedUnoBtn, 7, 0)
        self.colapsedMenu.layout.addWidget(self.colapsedBowlingBtn, 8, 0)
        self.colapsedMenu.layout.addWidget(self.colapsedExitBtn, 9, 0)

        self.expandedMenu.layout.addWidget(self.colapseBtn, 0, 0, Qt.AlignmentFlag.AlignLeft)
        self.expandedMenu.layout.addWidget(self.expandedResidentLookupBtn, 1, 0, Qt.AlignmentFlag.AlignLeft)
        self.expandedMenu.layout.addWidget(self.expandedHistoricLookupBtn, 2, 0, Qt.AlignmentFlag.AlignLeft)
        self.expandedMenu.layout.addWidget(self.expandedYahtzeeBtn, 3, 0, Qt.AlignmentFlag.AlignLeft)
        self.expandedMenu.layout.addWidget(self.expandedBeanBagTossBtn, 4, 0, Qt.AlignmentFlag.AlignLeft)
        self.expandedMenu.layout.addWidget(self.expandedBingoBtn, 5, 0, Qt.AlignmentFlag.AlignLeft)
        self.expandedMenu.layout.addWidget(self.expandedBocceBallBtn, 6, 0, Qt.AlignmentFlag.AlignLeft)
        self.expandedMenu.layout.addWidget(self.expandedUnoBtn, 7, 0, Qt.AlignmentFlag.AlignLeft)
        self.expandedMenu.layout.addWidget(self.expandedBowlingBtn, 8, 0, Qt.AlignmentFlag.AlignLeft)
        self.expandedMenu.layout.addWidget(self.expandedExitBtn, 9, 0, Qt.AlignmentFlag.AlignLeft)


        #self.currentApplication.layout.addWidget(self.currentApplicationLabel)      # - Active Application

        self.colapsedMenu.setLayout(self.colapsedMenu.layout)
        self.expandedMenu.setLayout(self.expandedMenu.layout)
        self.currentApplication.setLayout(self.currentApplication.layout)

    def initMainLayout(self) -> None:
        self.mainContainer.layout.addWidget(self.colapsedMenu)
        self.mainContainer.layout.addWidget(self.expandedMenu)
        self.mainContainer.layout.addWidget(self.currentApplication)

        self.mainContainer.setLayout(self.mainContainer.layout)
    
    def initStyleSheets(self) -> None:
        self.colapsedMenu.setProperty("class", "colapsed")
        self.expandedMenu.setProperty("class", "expanded")

        with open(os.path.join("stylesheets", "main_menu.css")) as file:
            self.colapsedMenu.setStyleSheet(file.read())

        with open(os.path.join("stylesheets", "main_menu.css")) as file:
            self.expandedMenu.setStyleSheet(file.read())

    def expandSideMenu(self) -> None:
        self.colapsedMenu.hide()
        self.expandedMenu.show()  

    def colapseSideMenu(self) -> None:
        self.colapsedMenu.show()
        self.expandedMenu.hide()

    def applyMenuBtnImg(self) -> None:                                  # -- Applies images to the different button options
        for _, _, file in os.walk("app_icons"):
            images: list = file

        for inx, item in enumerate(self.colapsedWidgetList[1:]):
            if item != self.colapsedWidgetList[-1]:
                item.setIcon(QIcon(os.path.join("app_icons", images[inx])))
                item.setIconSize(QSize(30, 30))

        for inx, item in enumerate(self.expandedWidgetList[1:]):
            if item != self.expandedWidgetList[-1]:
                item.setIcon(QIcon(os.path.join("app_icons", images[inx])))
                item.setIconSize(QSize(30, 30))

        self.colapseBtn.setIcon(QIcon(os.path.join("app_icons", "colapseMenu.png")))
        self.colapseBtn.setIconSize(QSize(30, 30))

        self.expandBtn.setIcon(QIcon(os.path.join("app_icons", "menu.png")))
        self.expandBtn.setIconSize(QSize(30, 30))

    def openApp(self, currentApp: QWidget = None) -> None:
        if self.currentApp:
            self.currentApplication.layout.removeWidget(currentApp)
            self.currentApp.close()

        self.currentApp = currentApp
        self.currentApplication.layout.addWidget(currentApp)
        currentApp.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainMenu = MainMenu()

    with open(os.path.join("stylesheets", "main-style.css")) as file:
        mainMenu.setStyleSheet(file.read())

    mainMenu.show()
    sys.exit(app.exec())
