import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, 
                             QVBoxLayout, QHBoxLayout)

class StatsApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stats App")

        # Layout
        layout = QVBoxLayout()

        # Example stat: Physical
        self.physical_input = QLineEdit()
        self.physical_input.setPlaceholderText("Enter Physical stat (0-100)")
        layout.addWidget(QLabel("Physical"))
        layout.addWidget(self.physical_input)

        # Button
        self.calc_btn = QPushButton("Calculate Stats")
        layout.addWidget(self.calc_btn)

        # Result label
        self.result_label = QLabel("Result will appear here")
        layout.addWidget(self.result_label)

        self.setLayout(layout)

        # Connect button
        self.calc_btn.clicked.connect(self.calculate_stats)

    def calculate_stats(self):
        physical = int(self.physical_input.text())
        self.result_label.setText(f"Your Physical score: {physical}")




app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("My Stats App")

layout = QVBoxLayout()
label = QLabel("Welcome to Stats App!")
layout.addWidget(label)

window.setLayout(layout)
window.show()

sys.exit(app.exec_())
