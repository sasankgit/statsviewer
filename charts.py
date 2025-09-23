from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class ChartCanvas(FigureCanvas):
    def __init__(self, stats, parent=None):
        fig = Figure(figsize=(5, 3))
        super().__init__(fig)
        self.axes = fig.add_subplot(111)
        self.plot(stats)

    def plot(self, stats):
        self.axes.clear()
        self.axes.bar(stats.keys(), stats.values(), color='skyblue')
        self.axes.set_title("Stat Scores")
        self.draw()
