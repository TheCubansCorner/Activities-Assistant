#! python3
#! team_selection.py -- used to select players and teams

import os, sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel, QListWidget,
    QAbstractItemView, QTableWidgetItem
    )

from database_queries import DatabaseQueries


class TeamSelection(QWidget):
    def __init__(self, mainApp: QWidget = None) -> None:    # -- initiates the module/main variables
        super().__init__()
        self.mainFrame: QWidget = mainApp
        self.numberOfTeams = None
        self.isListGenerated = False
        self.residentList = DatabaseQueries().getAllResidents()

        self.initUI()
        self.initConfigWidgets()
        self.initStyleSheets()
        self.initConfigConnections()
        self.initLayouts()

    def initUI(self) -> None:                               # -- Initiates Widgets
        self.headerLabel: QWidget = QLabel("How many teams? (1 - 4)")
        self.numTeamsLine: QWidget = QLineEdit()
        self.submitNumBtn: QWidget = QPushButton("Submit")

        self.widgitList = [self.headerLabel, self.numTeamsLine, self.submitNumBtn]

    def initConfigWidgets(self) -> None:                    # -- Configures widget settings
        self.headerLabel.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.numTeamsLine.setAlignment(Qt.AlignmentFlag.AlignTop)

    def initStyleSheets(self) -> None:                      # -- Initiates the stylesheets for the application
        pass
    
    def initConfigConnections(self) -> None:                # -- Configures connections between widgets and functions
        self.submitNumBtn.clicked.connect(self.submitNumTeams)

    def initLayouts(self) -> None:                          # -- Applies widgets to the layouts/applies layouts to app
        self.layout = QVBoxLayout()
        self.rowOneLayout = QHBoxLayout()
        self.rowTwoLayout = QHBoxLayout()
        self.rowThreeLayout = QHBoxLayout()

        self.rowOneLayout.addWidget(self.numTeamsLine, alignment = Qt.AlignmentFlag.AlignHCenter)
        self.rowOneLayout.addWidget(self.submitNumBtn)

        self.layout.addWidget(self.headerLabel, alignment = Qt.AlignmentFlag.AlignHCenter)
        self.layout.addLayout(self.rowOneLayout)
        self.layout.addLayout(self.rowTwoLayout)
        self.layout.addLayout(self.rowThreeLayout)

        self.setLayout(self.layout)

    def submitNumTeams(self) -> None:                       # -- Checks that the input is a number and 4 or less teams
        try:
            self.numberOfTeams: int = int(self.numTeamsLine.text()) + 1

            if self.numberOfTeams >= 6:
                return self.numTeamsLine.setText("")
            
        except ValueError:
            return self.numTeamsLine.setText("")
        
        self.buildTeamListboxs()

    def buildTeamListboxs(self) -> None:                    # -- Creates listbox widgets based on the number of teams
        if self.isListGenerated:
            return 
        elif self.numberOfTeams < 3:
            return self.numTeamsLine.setText("") 
        else:
            self.isListGenerated = True
        
        self.headers: str = ["Residents:", "Team 1", "Team 2", "Team 3", "Team 4"]
        self.listBoxWidgets: list = [QListWidget() for _ in range(self.numberOfTeams)]  # Creates lostbox widgets
        self.labelWidgets: list = [QLabel() for _ in range(self.numberOfTeams)] # Creates label widgets
        self.submitTeamsBtn: QWidget = QPushButton("Submit Team")
        
        self.hideAll()
        self.fillLabelsListbox()

    def fillLabelsListbox(self):                            # -- Applies header Qlabels to the QListView widget
        for inx, label in enumerate(self.labelWidgets):     # Fills labels with team text
            label.setText(self.headers[inx])

        for resident in self.residentList:
            self.listBoxWidgets[0].addItem(f"{resident[1]} {resident[3]}")

        self.addListboxs()
    
    def addListboxs(self) -> None:                          # -- Adds the listbox(s) to the layout
        for label in self.labelWidgets:
            label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            self.rowTwoLayout.addWidget(label)

        for listbox in self.listBoxWidgets:
            listbox.setDragDropMode(QAbstractItemView.DragDropMode.DragDrop)
            listbox.setDefaultDropAction(Qt.DropAction.MoveAction)
            self.rowThreeLayout.addWidget(listbox)

        self.submitTeamsBtn.clicked.connect(self.submitAllTeams)
        self.layout.addWidget(self.submitTeamsBtn)

    def submitAllTeams(self) -> None:                       # -- Submits all the teams to the main function
        self.finalTeamSelection: list = []
        for inx, listbox in enumerate(self.listBoxWidgets):
            team: list = []

            if inx == 0:
                continue

            team.append(self.headers[inx])

            for item in range(listbox.count()):
                team.append(f"{listbox.item(item).text().split()[0]} {listbox.item(item).text().split()[0][0]}.")   # item is first name and last name initial

            self.finalTeamSelection.append(team)

        self.mainFrame.teamList = self.finalTeamSelection
        self.mainFrame.scoreBoard.setColumnCount(len(self.finalTeamSelection))
        self.mainFrame.showAll()

        for inx, name in enumerate(self.finalTeamSelection):
            self.mainFrame.scoreBoard.setCellWidget(0, inx, QLabel(name[0], alignment = Qt.AlignmentFlag.AlignHCenter))
            self.mainFrame.scoreBoard.setItem(8, inx, QTableWidgetItem("0"))
        self.hide()
    
    def showAll(self) -> None:                              # -- Shows all widgets
        for widg in self.widgitList:
            widg.show()

    def hideAll(self) -> None:                              # -- Hides all widgets
        for widg in self.widgitList:
            widg.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    teamSelection = TeamSelection()
    teamSelection.show()
    sys.exit(app.exec())

    