# widgets/memory_plot.py
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MemoryCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=3, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)

        self.fig.tight_layout()
        self.plot_empty()

    def plot_empty(self):
        self.ax.clear()
        self.ax.text(0.5, 0.5, "No data", ha="center", va="center")
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.draw()

    def plot_memory(self, flash_val, ram_val):
        self.ax.clear()

        labels = ["Flash", "RAM"]
        values = [flash_val, ram_val]

        bars = self.ax.bar(labels, values, color=["#60a5fa", "#34d399"])

        self.ax.set_ylabel("Bytes")
        self.ax.set_title("Memory Usage (Flash vs RAM)")

        
        for bar, v in zip(bars, values):
            height = bar.get_height()
            self.ax.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                f"{v:,}",
                ha="center",
                va="bottom",
                fontsize=9,
            )

        self.fig.tight_layout()
        self.draw()