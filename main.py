#! python3
#! main.py -- Main applicaiton window

import sys, os

from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout

from scripts.login import Login
from scripts.resident_lookup import ResidentLookup


class MainWindow(QMainWindow):
    def __init__(self) -> None:      # -- Initiates the main window of the application
        super().__init__()
        self.apps: dict = {
            'login' : Login(), 'residentLookup' : ResidentLookup(self)
            }
        self.currentApp = None

        self.initUI()
        self.applyLayouts()
        self.show()
    
    def initUI(self) -> None:
        pass

    def applyLayouts(self) -> None:
        # Create Layout
        self.layout = QVBoxLayout()
        
        # Add widgets to layout

        # Add Layout to Application
        self.setLayout(self.layout)

    def setButtonConnections(self) -> None:
        pass

    def applyStylesheets(self) -> None:
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec())
