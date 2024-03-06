#! python3
#! main.py -- Main applicaiton window

import sys, os

from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout

from scripts.login import Login


class MainWindow(QMainWindow):
    def __init__(self) -> None:      # -- Initiates the main window of the application
        super().__init__()
        self.apps: dict = {'login' : Login()}
        
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec())
