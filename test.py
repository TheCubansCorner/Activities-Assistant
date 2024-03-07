import PyQt6.QtWidgets as qtw

class MainButt(qtw.QWidget):
    def __init__(self):
        super().__init__()
        x = qtw.QDateTimeEdit()
        self.layout = qtw.QHBoxLayout()
        self.layout.addWidget(x)
        self.setLayout(self.layout)
        self.show()

app = qtw.QApplication([])
x = MainButt()
app.exec()