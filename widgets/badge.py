from PyQt5.QtWidgets import QLabel


class StatusBadge(QLabel):
    def __init__(self, text: str, kind: str = "warning"):
        super().__init__(text)

        color_map = {
            "warning": ("#fff7ed", "#c2410c", "#fdba74"),
            "success": ("#ecfdf5", "#15803d", "#86efac"),
            "info": ("#eff6ff", "#1d4ed8", "#93c5fd"),
            "danger": ("#fef2f2", "#b91c1c", "#fca5a5"),
        }

        bg, fg, border = color_map.get(kind, color_map["warning"])
        self.setStyleSheet(f"""
            QLabel {{
                background: {bg};
                color: {fg};
                border: 1px solid {border};
                border-radius: 11px;
                padding: 6px 12px;
                font-size: 12px;
                font-weight: 600;
            }}
        """)