import os
import random
import pandas as pd
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QApplication
import sys
from statistics import Statistics


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]
        self.selected_file = None
        self.selected_df = None

        self.button = QtWidgets.QPushButton("Click me!")
        self.file_button = QtWidgets.QPushButton("Select File...")
        self.visualize_button = QtWidgets.QPushButton("Visualize Data")
        self.display_button = QtWidgets.QPushButton("Display Data")
        self.text = QtWidgets.QLabel(
            "Hello World",
            alignment=QtCore.Qt.AlignmentFlag.AlignCenter,
        )

        self.layout = QtWidgets.QHBoxLayout(self)

        controls_group = QtWidgets.QGroupBox("Controls")
        controls_layout = QtWidgets.QVBoxLayout()
        controls_layout.addWidget(self.button)
        controls_layout.addWidget(self.file_button)
        controls_layout.addWidget(self.visualize_button)
        controls_layout.addWidget(self.display_button)
        controls_group.setLayout(controls_layout)

        left_widget = QtWidgets.QWidget()
        left_group = QtWidgets.QVBoxLayout(left_widget)
        left_group.addWidget(controls_group)

        display_group = QtWidgets.QGroupBox("Display")
        display_layout = QtWidgets.QVBoxLayout()
        display_layout.addWidget(self.text)
        display_group.setLayout(display_layout)

        self.layout.addWidget(left_widget)
        self.layout.addWidget(display_group)

        self.setStyleSheet("")

        self.button.clicked.connect(self.magic)
        self.file_button.clicked.connect(self.select_file)
        self.visualize_button.clicked.connect(self.visualize_data)
        self.display_button.clicked.connect(self.display_data)

    @QtCore.pyqtSlot()
    def magic(self):
        self.text.setText(random.choice(self.hello))

    @QtCore.pyqtSlot()
    def select_file(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Select File",
            QtCore.QDir.homePath(),
            "CSV Files (*.csv);;Excel Files (*.xlsx)",
        )
        if not filename:
            return

        self.selected_file = filename
        try:
            _, ext = os.path.splitext(filename)
            ext = ext.lower()
            if ext == ".csv":
                df = pd.read_csv(filename)
            elif ext in (".xls", ".xlsx"):
                df = pd.read_excel(filename)
            else:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Unsupported File",
                    "Please select a .csv or .xlsx file.",
                )
                return

            self.selected_df = df
            self.text.setText(f"Loaded {len(df)} rows from {os.path.basename(filename)}")
        except Exception as e:
            self.selected_df = None
            QtWidgets.QMessageBox.critical(self, "Error loading file", str(e))

    @QtCore.pyqtSlot()
    def visualize_data(self):
        if self.selected_df is None:
            QtWidgets.QMessageBox.warning(
                self,
                "No Data",
                "Please select a .csv or .xlsx file first.",
            )
            return

        try:
            stats = Statistics(self.selected_df)
            stats.setUp()
            stats.plot_histogram(column_name="depth", bins=30)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", str(e))

    @QtCore.pyqtSlot()
    def display_data(self):
        if self.selected_df is None:
            QtWidgets.QMessageBox.warning(
                self,
                "No Data",
                "Please select a .csv or .xlsx file first.",
            )
            return

        try:
            stats = Statistics(self.selected_df)
            stats.setUp()
            self.text.setText(stats.data.head().to_string())
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", str(e))


if __name__ == "__main__":
    app = QApplication([])

    try:
        with open("style.qss", "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("style.qss file not found, running with default theme.")

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
