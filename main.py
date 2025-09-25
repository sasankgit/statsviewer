from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from charts import ChartCanvas  # assuming saved in chart_canvas.py
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Game Stats Radar Chart")

        # Chart
        self.chart = ChartCanvas()

        layout = QVBoxLayout()
        layout.addWidget(self.chart)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
