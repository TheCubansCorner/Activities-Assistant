#! python3
#! player_selection.py -- Listboxes for selecting players for game applications

import os, sys

from PyQt6.QtWidgets import QApplication, QWidget, QListWidget, QAbstractItemView, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt

from database_queries import DatabaseQueries


class PlayerSelection(QWidget):
    def __init__(self, mainApp: QWidget = None) -> None:
        super().__init__()
        self.mainFrame: QWidget = mainApp
        self.residentList: list = DatabaseQueries().getAllResidents()

        self.init()
        self.loadListbox()
        self.widgetSettings()
        self.applyConnections()
        self.applyStyles()
        self.initLayouts()

    def init(self) -> None:
        self.residentListbox: QWidget = QListWidget()
        self.playersListbox: QWidget = QListWidget()
        self.submitPlayersBtn: QWidget = QPushButton("Submit")
        self.clearPlayersBtn: QWidget = QPushButton("Clear List")     

        self.widgetList: list = [self.residentListbox, self.playersListbox, self.submitPlayersBtn, self.clearPlayersBtn]

    def initLayouts(self) -> None:
        self.layout = QVBoxLayout()
        self.listboxLayout = QHBoxLayout()
        self.buttonLayout = QHBoxLayout()

        self.listboxLayout.addWidget(self.residentListbox)
        self.listboxLayout.addWidget(self.playersListbox)

        self.buttonLayout.addWidget(self.clearPlayersBtn)
        self.buttonLayout.addWidget(self.submitPlayersBtn)
    
        self.layout.addLayout(self.listboxLayout)
        self.layout.addLayout(self.buttonLayout)
        self.setLayout(self.layout)

    def widgetSettings(self) -> None:
        self.residentListbox.setAcceptDrops(True)
        self.playersListbox.setAcceptDrops(True)
        self.residentListbox.setDragEnabled(True)
        self.playersListbox.setDragEnabled(True)
        self.residentListbox.setDragDropMode(QAbstractItemView.DragDropMode.DragDrop)
        self.residentListbox.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.playersListbox.setDragDropMode(QAbstractItemView.DragDropMode.DragDrop)
        self.playersListbox.setDefaultDropAction(Qt.DropAction.MoveAction)

    def applyConnections(self) -> None:
        self.clearPlayersBtn.clicked.connect(self.resetPlayerList)
        self.submitPlayersBtn.clicked.connect(self.submitPlayerList)

    def applyStyles(self) -> None:
        pass

    def loadListbox(self) -> None:
        for res in self.residentList:
            self.residentListbox.addItem(f"{res[1]} {res[3]}")

    def submitPlayerList(self) -> None:
        self.playerList = [self.playersListbox.item(x).text().split()[0] for x in range(self.playersListbox.count())]
        
        if len(self.playerList) < 3:
            return
        
        try:
            if self.mainFrame.appTitle == "bowling":
                self.mainFrame.scoreboardTable.setRowCount(len(self.playerList) + 1)
                self.mainFrame.playerList = self.playerList
                self.mainFrame.showAll()
                self.mainFrame.buildTable()
                self.hide()
                
                return
        except:
            pass
        
        if self.playerList:
            self.mainFrame.playerList = self.playerList
            self.resetPlayerList()
            self.mainFrame.scoreboardTable.setRowCount(len(self.playerList) + 1)
            self.mainFrame.createTable()

            for inx, resident in enumerate(self.playerList):
                self.mainFrame.currentPlayerScore[(inx + 1)] = 0

            self.hide()
            #self.destroy()
            #self.close()

            for widg in self.mainFrame.widgetList:
                widg.show()
                       
    def resetPlayerList(self) -> None:
        self.residentListbox.clear()
        self.playersListbox.clear()
        self.loadListbox()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    playerSelection: QWidget = PlayerSelection()
    playerSelection.show()
    sys.exit(app.exec())
