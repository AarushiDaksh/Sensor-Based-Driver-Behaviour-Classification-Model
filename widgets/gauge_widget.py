from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QColor, QFont
from PyQt5.QtCore import Qt, QRectF


class GaugeWidget(QWidget):
    def __init__(self, title="Gauge", value=0, max_value=100, unit="%"):
        super().__init__()
        self.title = title
        self.value = value
        self.max_value = max_value
        self.unit = unit
        self.setMinimumHeight(240)

    def set_value(self, value, max_value=None):
        self.value = value
        if max_value is not None:
            self.max_value = max_value
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect().adjusted(20, 20, -20, -20)

        painter.setPen(QColor("#0f172a"))
        painter.setFont(QFont("Arial", 12, QFont.Bold))
        painter.drawText(rect.adjusted(0, 0, 0, -rect.height() + 20), Qt.AlignCenter, self.title)

        gauge_rect = QRectF(rect.left() + 28, rect.top() + 45, rect.width() - 56, rect.height() - 95)

        bg_pen = QPen(QColor("#e5e7eb"), 20)
        painter.setPen(bg_pen)
        painter.drawArc(gauge_rect, 180 * 16, -180 * 16)

        ratio = 0 if self.max_value == 0 else max(0, min(self.value / self.max_value, 1))

        if ratio < 0.70:
            color = QColor("#16a34a")
        elif ratio < 0.90:
            color = QColor("#0ea5e9")
        else:
            color = QColor("#dc2626")

        progress_pen = QPen(color, 20)
        painter.setPen(progress_pen)
        painter.drawArc(gauge_rect, 180 * 16, int(-180 * ratio * 16))

        painter.setPen(QColor("#111827"))
        painter.setFont(QFont("Arial", 18, QFont.Bold))
        painter.drawText(rect.adjusted(0, 52, 0, 0), Qt.AlignCenter, f"{self.value:.1f}{self.unit}")

        painter.setPen(QColor("#64748b"))
        painter.setFont(QFont("Arial", 10))
        painter.drawText(rect.adjusted(0, 86, 0, 0), Qt.AlignCenter, f"Capacity: {self.max_value}{self.unit}")