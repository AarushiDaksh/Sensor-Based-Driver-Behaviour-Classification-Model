from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel


class SectionBox(QFrame):
    def __init__(self, title: str):
        super().__init__()
        self.setObjectName("sectionBox")

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(18, 18, 18, 18)
        self.layout.setSpacing(12)

        self.title_label = QLabel(title)
        self.title_label.setObjectName("sectionTitle")
        self.layout.addWidget(self.title_label)

    def add_widget(self, widget):
        self.layout.addWidget(widget)