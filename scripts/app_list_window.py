#! python3
#! app_list_window.py -- Main Menu for accessing applications

import sys, os

from PyQt6.QtWidgets import QLabel, QPushButton, QWidget, QApplication, QVBoxLayout, QHBoxLayout, QMainWindow
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import QSize, Qt

from resident_lookup import ResidentLookup

class AppListWindow(QWidget):
    def __init__(self, mainApp: QMainWindow = None, user: tuple = None) -> None:        # -- Initiates the module
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
    
    def initUI(self) -> None:                                       # -- Creates WIdgets
        self.header: QWidget = QLabel()
        self.residentLookupBtn: QWidget = QPushButton("Resident Directory")                                              # -- QPushButtons
        self.residentHistoryBtn: QWidget = QPushButton("Resident History")
        self.yahtzeeBtn: QWidget = QPushButton("Yahtzee")
        self.beanBagTossBtn: QWidget = QPushButton("Cornhole")
        self.bingoBtn: QWidget = QPushButton("Bingo")
        self.bocceBallBtn: QWidget = QPushButton("Bocce Ball")
        self.unoBtn: QWidget = QPushButton("Uno")
        self.bowlingBtn: QWidget = QPushButton("Bowling")

        self.widgetList: list = [
            self.residentLookupBtn, self.residentHistoryBtn, self.yahtzeeBtn,
            self.beanBagTossBtn, self.bingoBtn, self.bocceBallBtn,
            self.unoBtn, self.bowlingBtn, self.header
            ]

    def applyLayouts(self) -> None:                                 # -- Applies layouts to the applicaiton
        self.layout = QVBoxLayout()
        self.headerLayout = QHBoxLayout()
        self.appButtonLayout = QHBoxLayout()
        self.combinedLayout = QVBoxLayout()
        for item in self.widgetList:     
            self.appButtonLayout.addWidget(item, alignment = Qt.AlignmentFlag.AlignTop)

        self.headerLayout.addWidget(self.header, alignment = Qt.AlignmentFlag.AlignTop)
        self.combinedLayout.addLayout(self.headerLayout)
        self.combinedLayout.addLayout(self.appButtonLayout)
        
        self.layout.addLayout(self.combinedLayout)


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