#! python3
#! main.py -- Main applicaiton window

import sys, os

from PyQt6.QtWidgets import QApplication, QMainWindow

from app_list_window import AppListWindow


class MainWindow(QMainWindow):
    def __init__(self, user: tuple = None) -> None:      # -- Initiates the main window of the application
        super().__init__()
        self.mainApp = AppListWindow(self, user)
        self.setCentralWidget(self.mainApp)
        self.showFullScreen()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    with open(os.path.join("stylesheets", "main-style.css"), "r") as file:
        app.setStyleSheet(file.read())

    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())
