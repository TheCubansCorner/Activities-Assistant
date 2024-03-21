#! python3
#! topThree.py -- Displays top three residents

import os, sys


from PyQt6.QtWidgets import QLabel, QApplication, QWidget, QFormLayout


class TopThreeDisplay(QWidget):
    def __init__(self, mainApp: QWidget = None, playerDict: dict = None) -> None:       # -- Initiates Module
        super().__init__()
        self.mainFrame: QWidget = mainApp
        self.playerDict: dict = playerDict
        self.topThree: list = []

        self.initUI()
        self.applyStyles()
        self.applyConnections()
        self.applyWidgetSettings()
        self.findTopThree()
        self.applyLayouts()
        
    def initUI(self) -> None:                                                           # -- Initiates WIdgets
        self.firstPlaceName: QWidget = QLabel("Name: ")
        self.firstPlaceScore: QWidget = QLabel("Score: ")
        self.secondPlaceName: QWidget  = QLabel("Name: ")
        self.secondPlaceScore: QWidget = QLabel("Score: ")
        self.thirdPlaceName: QWidget = QLabel("Name: ")
        self.thirdPlaceScore: QWidget = QLabel("Score: ")

    def applyStyles(self) -> None:                                                      # -- Applies Stylesheets
        pass

    def applyConnections(self) -> None:                                                 # -- Establishes conneciton between widgets and functions
        pass

    def applyWidgetSettings(self) -> None:                                              # -- Applies various widget settings (alignment, max size, etc)
        pass

    def applyLayouts(self) -> None:                                                     # -- Applies widgets to layout/sets primary layout
        self.layout = QFormLayout()
        
        self.layout.addRow(self.firstPlaceName, self.firstPlaceScore)
        self.layout.addRow(self.secondPlaceName, self.secondPlaceScore)
        self.layout.addRow(self.thirdPlaceName, self.thirdPlaceScore)


        self.setLayout(self.layout)

    def findTopThree(self) -> None:                                                     # -- Creates a list of top three residents
        if len(self.topThree) < 3:  
            try:
                highest = max(self.playerDict, key = self.playerDict.get) 
                print(highest)
                # remove the max score from the dictionary
                self.topThree.append((highest, self.playerDict[highest]))
                self.playerDict.pop(highest)
                self.findTopThree()
            except:
                pass
        else:
            self.displayTopThree()
            return
    
    def displayTopThree(self) -> None:                                                  # -- Updates display with top three informaiton
        self.firstPlaceName.setText(self.mainFrame.playerList[self.topThree[0][0] - 1])
        self.firstPlaceScore.setText(str(self.topThree[0][1]))

        self.secondPlaceName.setText(self.mainFrame.playerList[self.topThree[1][0] - 1])
        self.secondPlaceScore.setText(str(self.topThree[1][1]))

        self.thirdPlaceName.setText(self.mainFrame.playerList[self.topThree[2][0] - 1])
        self.thirdPlaceScore.setText(str(self.topThree[2][1]))

        self.topThree: list = []


if __name__ == "__main__":
    resident_dict = {
        "Tom" : 32,
        "Frank" : 54,
        "Bill" : 23,
        "Joe" : 10,
        "Steve" : 88,
        "walter" : 90,
        "Frank" : 120
        }
    app = QApplication(sys.argv)
    topThreeDisplay = TopThreeDisplay(playerDict=resident_dict)
    topThreeDisplay.show()
    sys.exit(app.exec())
