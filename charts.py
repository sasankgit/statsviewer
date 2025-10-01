import os
import json
import re
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class ChartCanvas(FigureCanvas):
    def __init__(self, json_file=None, parent=None):
        # default to stats.json located next to this file if not provided
        if json_file is None:
            json_file = os.path.join(os.path.dirname(__file__), "stats.json")

        fig = Figure(figsize=(5, 5), facecolor="#1a1423")
        super().__init__(fig)
        if parent is not None:
            self.setParent(parent)
        self.axes = fig.add_subplot(111, polar=True)
        self.json_file = json_file
        self.raw_data = None  # keep raw structure if needed

        # Load stats from JSON (computes averages for entries with subskills)
        stats = self.load_stats()
        self.plot(stats)

    def _strip_json_comments(self, text: str) -> str:
        """Remove // and /* */ comments often present in non-strict JSON files."""
        # remove // comments
        text = re.sub(r'//.*?(?=\n|$)', '', text)
        # remove /* ... */ comments (multiline)
        text = re.sub(r'/\*.*?\*/', '', text, flags=re.S)
        return text

    def load_stats(self):
        """Load stats from JSON file, compute averages for any entry that has a
        dict with a 'subskills' mapping. Returns a flat dict {category: numeric_value}
        suitable for plotting. Keeps original JSON structure in self.raw_data.
        """
        if not os.path.exists(self.json_file):
            print(f"[ChartCanvas] stats file not found: {self.json_file}")
            data = {}
        else:
            try:
                with open(self.json_file, "r", encoding="utf-8") as f:
                    raw_text = f.read()
                try:
                    data = json.loads(raw_text)
                except Exception as e:
                    # Try stripping JS-style comments and re-parse
                    print(f"[ChartCanvas] JSON parse error: {e}. Trying to strip comments.")
                    stripped = self._strip_json_comments(raw_text)
                    try:
                        data = json.loads(stripped)
                    except Exception as e2:
                        print(f"[ChartCanvas] Failed to parse stats.json after stripping comments: {e2}")
                        data = {}
            except Exception as io_e:
                print(f"[ChartCanvas] Failed to read stats file: {io_e}")
                data = {}

        self.raw_data = data

        def numeric_value(v):
            # If v is a mapping with 'subskills', compute averaged numeric value.
            if isinstance(v, dict) and "subskills" in v and isinstance(v["subskills"], dict):
                subs = v["subskills"].values()
                nums = []
                for s in subs:
                    try:
                        nums.append(float(s))
                    except Exception:
                        continue
                if nums:
                    return round(sum(nums) / len(nums), 2)
                return 0.0
            # If plain number
            if isinstance(v, (int, float)):
                return float(v)
            # Try to coerce string to float
            try:
                return float(v)
            except Exception:
                return 0.0

        # Build flat mapping for plotting
        if isinstance(data, dict) and data:
            flat = {k: numeric_value(v) for k, v in data.items()}
        else:
            # fallback default categories
            flat = {
                "Hero Shooter": 0.0,
                "Colony Sim": 0.0,
                "Vehicular Combat": 0.0,
                "City Builder": 0.0,
                "Roguelike": 0.0,
                "Destruction": 0.0
            }

        # debug output
        print(f"[ChartCanvas] Using stats: {flat}")
        return flat

    def save_stats(self, stats):
        """Save updated stats to JSON file. If raw_data is present and an entry
        existed as a dict with subskills, do not overwrite that structure —
        instead, write back the raw structure but add/update an 'average' field
        for convenience. If raw_data is not available, write the flat mapping."""
        out = {}

        if isinstance(self.raw_data, dict) and self.raw_data:
            # start from raw and update/add 'average' fields for subskill entries
            out = dict(self.raw_data)  # shallow copy
            for k, v in stats.items():
                if k in out and isinstance(out[k], dict) and "subskills" in out[k]:
                    out[k] = dict(out[k])  # copy inner dict
                    out[k]["average"] = float(v)
                else:
                    # replace or set top-level numeric entries
                    out[k] = float(v)
        else:
            # write flat mapping directly
            out = {k: float(v) for k, v in stats.items()}

        try:
            with open(self.json_file, "w", encoding="utf-8") as f:
                json.dump(out, f, indent=4)
            print(f"[ChartCanvas] Saved stats to {self.json_file}")
        except Exception as e:
            print(f"[ChartCanvas] Failed to save stats: {e}")

    def plot(self, stats):
        self.axes.clear()

        # Data
        categories = list(stats.keys())
        values = [float(stats[k]) for k in categories]
        N = len(categories)
        if N == 0:
            return

        # close the loop
        values += values[:1]
        angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
        angles += angles[:1]

        # Radar chart style
        self.axes.set_theta_offset(np.pi / 2)
        self.axes.set_theta_direction(-1)
        self.axes.set_facecolor("#1a1423")
        self.axes.set_ylim(0, 100)

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