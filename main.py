#! python3
#! main.py -- initiates

import sys, os

from PyQt6.QtWidgets import QApplication

from scripts.login import Login


if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open(os.path.join("stylesheets", "main-style.css"), "r") as file:
        app.setStyleSheet(file.read())

    main = Login()
    main.show()
    sys.exit(app.exec())