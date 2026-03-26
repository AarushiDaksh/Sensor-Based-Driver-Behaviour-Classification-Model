from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class BarChartCanvas(FigureCanvas):
    def __init__(self, width=5, height=4, dpi=100):
        self.figure = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(self.figure)

    def plot_memory_regions(self, memory_regions):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        if not memory_regions:
            ax.text(0.5, 0.5, "No memory region data found", ha="center", va="center")
            ax.set_axis_off()
            self.draw()
            return

        names = [row["name"] for row in memory_regions]
        values = [row["used_percent"] for row in memory_regions]

        ax.bar(names, values)
        ax.set_title("Memory Region Usage (%)")
        ax.set_ylabel("Used %")
        ax.set_ylim(0, 110)
        ax.tick_params(axis='x', rotation=35)

        self.figure.tight_layout()
        self.draw()

    def plot_epoch_breakdown(self, epoch_summary):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        total = epoch_summary.get("total_epochs")
        sw = epoch_summary.get("sw_epochs")
        hybrid = epoch_summary.get("hybrid_epochs")
        hw = epoch_summary.get("hw_epochs")

        if total is None and sw is None and hybrid is None and hw is None:
            ax.text(0.5, 0.5, "No epoch data found", ha="center", va="center")
            ax.set_axis_off()
            self.draw()
            return

        labels = ["SW", "Hybrid", "HW"]
        values = [
            sw or 0,
            hybrid or 0,
            hw or 0
        ]

        ax.bar(labels, values)
        ax.set_title("Epoch Type Breakdown")
        ax.set_ylabel("Count")

        self.figure.tight_layout()
        self.draw()