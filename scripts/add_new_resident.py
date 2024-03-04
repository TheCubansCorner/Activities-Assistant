#! pthon3
#! add_new_resident.py -- Window for adding residents to the database

from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QComboBox, QPushButton
from PyQt6.QtWidgets import QLabel, QDateEdit, QVBoxLayout, QHBoxLayout

import sys, os



class AddNewResident(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.initUI()
        self.show()

    def initUI(self):
        # Create layouts 
        self.layout = QVBoxLayout()


        # Apply layout to main Widgit
        self.setLayout(self.layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    addResidentScreen: QWidget = AddNewResident()
    sys.exit(app.exec())