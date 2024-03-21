#! python3
#! main.py -- Main applicaiton window

import sys, os

from PyQt6.QtWidgets import QApplication, QMainWindow, QMenuBar
from PyQt6.QtGui import QAction

from app_list_window import AppListWindow


class MainWindow(QMainWindow):
    def __init__(self, user: tuple = None) -> None:      # -- Initiates the main window of the application
        super().__init__()
        self.mainApp = AppListWindow(self, user)

        self.menuOptions()
        self.setMenuBar(self.menuBar)
        self.setCentralWidget(self.mainApp)
        self.setWindowTitle("Activities")
        self.showFullScreen()
        self.setFixedSize(self.size())
        self.show()
    
    def closeProgram(self) -> None:
        sys.exit()

    def applyStylesheets(self) -> None:
        pass

    def menuOptions(self) -> None:
        menuAction = QAction("&Exit", self)
        menuAction.setStatusTip("Exit the Application")
        menuAction.setToolTip("Exit the Application")
        menuAction.triggered.connect(self.closeProgram)
        self.menuBar = QMenuBar()
        menu = self.menuBar
        fileMenu = menu.addMenu('&File')
        fileMenu.addAction(menuAction)
        self.menuBar.addMenu(fileMenu)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    with open(os.path.join("stylesheets", "main-style.css"), "r") as file:
        app.setStyleSheet(file.read())

    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())
