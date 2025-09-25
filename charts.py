import os
import json
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class ChartCanvas(FigureCanvas):
    def __init__(self, json_file="stats.json", parent=None):
        fig = Figure(figsize=(5, 5), facecolor="#1a1423")
        super().__init__(fig)
        self.axes = fig.add_subplot(111, polar=True)
        self.json_file = json_file

        # Load stats from JSON
        stats = self.load_stats()
        self.plot(stats)

    def load_stats(self):
        """Load stats from JSON file, or fallback to defaults."""
        if os.path.exists(self.json_file):
            with open(self.json_file, "r") as f:
                return json.load(f)
        else:
            # Default values if file does not exist
            return {
                "Hero Shooter": 0,
                "Colony Sim": 0,
                "Vehicular Combat": 0,
                "City Builder": 0,
                "Roguelike": 0,
                "Destruction": 0
            }

    def save_stats(self, stats):
        """Save updated stats to JSON file."""
        with open(self.json_file, "w") as f:
            json.dump(stats, f, indent=4)

    def plot(self, stats):
        self.axes.clear()

        # Data
        categories = list(stats.keys())
        values = list(stats.values())
        N = len(categories)

        values += values[:1]
        angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
        angles += angles[:1]

        # Radar chart style
        self.axes.set_theta_offset(np.pi / 2)
        self.axes.set_theta_direction(-1)
        self.axes.set_facecolor("#1a1423")

        # Plot
        self.axes.plot(angles, values, color="#4c8bf5", linewidth=2)
        self.axes.fill(angles, values, color="#4c8bf5", alpha=0.25)

        # Labels
        self.axes.set_xticks(angles[:-1])
        self.axes.set_xticklabels(categories, fontsize=10, color="white")

        self.axes.set_yticklabels([])
        self.axes.spines["polar"].set_visible(False)
        self.axes.grid(color="white", linestyle="dotted", alpha=0.4)

        self.draw()
