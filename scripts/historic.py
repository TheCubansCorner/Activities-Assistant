#! python3, PyQt6
#! historic.py -- Application for reviewing the resident database as well as the historic database

import os, sys

from PyQt6.QtWidgets import (
    QWidget, QApplication
    )


class HistoricData(QWidget):
    def __init__(self, mainApp: QWidget = None):    # -- initiates the module/main variables
        super().__init__()
        self.mainFrame = mainApp

        self.initUI()
        self.initConfigWidgets()
        self.initStyleSheets()
        self.initConfigConnections()
        self.initLayouts()

    def initUI(self) -> None:                       # -- Initiates Widgets
        self.widgetList = []

    def initConfigWidgets(self) -> None:            # -- Configures widget settings
        pass

    def initStyleSheets(self) -> None:              # -- Initiates the stylesheets for the application
        pass

    def initConfigConnections(self) -> None:        # -- Configures connections between widgets and functions
        pass

    def initLayouts(self) -> None:                  # -- Applies widgets to the layouts/applies layouts to app
        pass

    def backToMain(self) -> None:                   # -- Returns to main application page
        pass

    def showAll(self) -> None:                      # -- Shows all widgets
        for widg in self.widgetList:
            widg.show()

    def hideAll(self) -> None:                      # -- Hides all widgets
        for widg in self.widgetList:                
            widg.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    historicData = HistoricData()
    historicData.show()
    sys.exit(app.exec())