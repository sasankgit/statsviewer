from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from logic import calculate_scores
from charts import ChartCanvas

class StatsApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stats App")

        layout = QVBoxLayout()

        # Input fields
        self.physical_input = QLineEdit()
        self.education_input = QLineEdit()
        self.development_input = QLineEdit()
        self.graphics_input = QLineEdit()

        self.physical_input.setPlaceholderText("Physical (0-100)")
        self.education_input.setPlaceholderText("Education (0-100)")
        self.development_input.setPlaceholderText("Development (0-100)")
        self.graphics_input.setPlaceholderText("Graphics (0-100)")

        layout.addWidget(QLabel("Enter your stats:"))
        layout.addWidget(self.physical_input)
        layout.addWidget(self.education_input)
        layout.addWidget(self.development_input)
        layout.addWidget(self.graphics_input)

        # Button
        self.calc_btn = QPushButton("Calculate Stats")
        layout.addWidget(self.calc_btn)

        # Result label
        self.result_label = QLabel("Results will appear here")
        layout.addWidget(self.result_label)

        self.setLayout(layout)

        # Connect button
        self.calc_btn.clicked.connect(self.show_results)

    def show_results(self):
        stats = {
            "Physical": int(self.physical_input.text() or 0),
            "Education": int(self.education_input.text() or 0),
            "Development": int(self.development_input.text() or 0),
            "Graphics": int(self.graphics_input.text() or 0),
        }

        averages = calculate_scores(stats)
        self.result_label.setText(str(averages))

        # Add chart
        chart = ChartCanvas(averages)
        self.layout().addWidget(chart)
