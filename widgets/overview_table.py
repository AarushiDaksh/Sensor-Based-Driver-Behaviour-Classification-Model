from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView


class OverviewTable(QTableWidget):
    def __init__(self):
        super().__init__(0, 2)
        self.setHorizontalHeaderLabels(["Parameter", "Values/Description/Results"])
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setVisible(False)

    def load_data(self, rows):
        self.setRowCount(len(rows))
        for i, (key, value) in enumerate(rows):
            self.setItem(i, 0, QTableWidgetItem(str(key)))
            self.setItem(i, 1, QTableWidgetItem(str(value)))