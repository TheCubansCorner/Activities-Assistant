#! python3
#! main.py -- Main applicaiton window

import sys, os

from PyQt6.QtWidgets import QApplication, QMainWindow

from app_list_window import AppListWindow


class MainWindow(QMainWindow):
    def __init__(self) -> None:      # -- Initiates the main window of the application
        super().__init__()
        self.mainApp = AppListWindow(self)
        self.setCentralWidget(self.mainApp)
        self.showFullScreen()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())
