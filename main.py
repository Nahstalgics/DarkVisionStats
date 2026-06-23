import numpy as np
import scipy as sp
import pandas as pd
import statsmodels as sm
import random
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QApplication, QWidget
import sys

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]
        self.selected_file = None

        self.button = QtWidgets.QPushButton("Click me!")
        self.file_button = QtWidgets.QPushButton("Select File...")
        self.text = QtWidgets.QLabel("Hello World",
                                     alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.file_button)

        self.setStyleSheet("")

        self.button.clicked.connect(self.magic)
        self.file_button.clicked.connect(self.select_file)

    @QtCore.pyqtSlot()
    def magic(self):
        self.text.setText(random.choice(self.hello))

    @QtCore.pyqtSlot()
    def select_file(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Select File",
            QtCore.QDir.homePath(),
            "CSV Files (*.csv);;Excel Files (*.xls *.xlsx)"
        )
        if filename:
            self.selected_file = filename
            self.text.setText(f"Selected: {filename}")

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    try:
        with open("style.qss", "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("style.qss file not found, running with default theme.")
    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
