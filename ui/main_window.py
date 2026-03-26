from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QFileDialog, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QGridLayout, QListWidget, QTextEdit, QMessageBox, QFrame,
    QScrollArea, QTabWidget, QComboBox, QSpinBox, QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import Qt
import os
import json

from parser.report_parser import parse_report_file
from widgets.metric_card import MetricCard
from widgets.badge import StatusBadge
        # flash usage card
from widgets.waveform_plot import WaveformCanvas
from widgets.overview_table import OverviewTable
from widgets.section_box import SectionBox
from widgets.memory_plot import MemoryCanvas
from utils.helpers import format_int

# default dataset directory; can be overridden in the UI
DEFAULT_BASE_DATA_DIR = r".\preprocessed data"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Driver Behaviour Analysis Dashboard")
        self.resize(1680, 980)
        self.reports = []

        # current dataset directory (can be changed via "Set Dataset Directory")
        self.base_data_dir = DEFAULT_BASE_DATA_DIR

        self.setStyleSheet("""
            QMainWindow, QWidget {
                background: #f8fafc;
                color: #0f172a;
                font-family: Segoe UI;
            }

            QFrame#sidebar {
                background: #ffffff;
                border-right: 1px solid #e2e8f0;
            }

            QFrame#sectionBox {
                background: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 18px;
            }

            QLabel#sectionTitle {
                font-size: 16px;
                font-weight: 700;
                color: #0f172a;
            }

            QFrame#metricCard {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #ffffff, stop:1 #f8fbff);
                border: 1px solid #dbeafe;
                border-radius: 16px;
            }

            QLabel#metricTitle {
                font-size: 12px;
                color: #64748b;
                font-weight: 600;
            }

            QLabel#metricValue {
                font-size: 20px;
                font-weight: 800;
                color: #0f172a;
            }

            QLabel#metricSubtitle {
                font-size: 11px;
                color: #94a3b8;
            }

            QPushButton {
                background: #2563eb;
                color: white;
                border: none;
                border-radius: 12px;
                padding: 11px 16px;
                font-size: 14px;
                font-weight: 700;
            }

            QPushButton:hover {
                background: #1d4ed8;
            }

            QListWidget, QTextEdit, QTableWidget {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 14px;
                padding: 6px;
            }

            QListWidget::item {
                padding: 10px;
                border-radius: 10px;
                margin: 4px;
            }

            QListWidget::item:selected {
                background: #dbeafe;
                color: #1d4ed8;
                font-weight: 700;
            }

            QHeaderView::section {
                background: #f1f5f9;
                color: #334155;
                font-weight: 700;
                border: none;
                padding: 10px;
            }

            QTabWidget::pane {
                border: none;
                background: transparent;
            }

            QTabBar::tab {
                background: #e2e8f0;
                color: #334155;
                padding: 10px 16px;
                border-radius: 10px;
                margin-right: 6px;
                font-weight: 600;
            }

            QTabBar::tab:selected {
                background: #2563eb;
                color: white;
            }
        """)

        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.build_sidebar(root)
        self.build_main_area(root)
        self.set_empty_state()

    # ------------------------------------------------------------------ #
    # Sidebar
    # ------------------------------------------------------------------ #
    def build_sidebar(self, root):
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(300)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        app_title = QLabel("Report Dashboard")
        app_title.setStyleSheet("font-size: 22px; font-weight: 800; color: #0f172a;")
        layout.addWidget(app_title)

        app_sub = QLabel("Upload reports and visualize hardware + signal analysis")
        app_sub.setWordWrap(True)
        app_sub.setStyleSheet("font-size: 12px; color: #64748b;")
        layout.addWidget(app_sub)

        self.upload_btn = QPushButton("Upload Report(s)")
        self.upload_btn.clicked.connect(self.load_reports)
        layout.addWidget(self.upload_btn)

        self.dir_btn = QPushButton("Set Dataset Directory")
        self.dir_btn.clicked.connect(self.set_dataset_dir)
        layout.addWidget(self.dir_btn)

        self.report_list = QListWidget()
        self.report_list.currentRowChanged.connect(self.display_report)
        layout.addWidget(self.report_list)

        layout.addStretch()
        root.addWidget(sidebar)

    # ------------------------------------------------------------------ #
    # Main area with tabs
    # ------------------------------------------------------------------ #
    def build_main_area(self, root):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)

        container = QWidget()
        scroll.setWidget(container)

        self.main_layout = QVBoxLayout(container)
        self.main_layout.setContentsMargins(22, 22, 22, 22)
        self.main_layout.setSpacing(18)

        top_row = QHBoxLayout()

        title_wrap = QVBoxLayout()
        page_title = QLabel("Run Analysis")
        page_title.setStyleSheet("font-size: 30px; font-weight: 800; color: #0f172a;")
        title_wrap.addWidget(page_title)

        page_sub = QLabel("Hardware usage, parsed report overview, and waveform behaviour analysis")
        page_sub.setStyleSheet("font-size: 13px; color: #64748b;")
        title_wrap.addWidget(page_sub)

        top_row.addLayout(title_wrap)
        top_row.addStretch()

        self.badge_row = QHBoxLayout()
        self.badge_row.addWidget(StatusBadge("Model not verified on target", "warning"))
        self.badge_row.addWidget(StatusBadge("Validation with random data", "info"))
        badge_wrap = QWidget()
        badge_wrap.setLayout(self.badge_row)
        top_row.addWidget(badge_wrap)

        self.main_layout.addLayout(top_row)

        self.metric_grid = QGridLayout()
        self.metric_grid.setSpacing(14)
        self.main_layout.addLayout(self.metric_grid)

        self.tabs = QTabWidget()
        self.main_layout.addWidget(self.tabs)

        self.build_overview_tab()
        self.build_confusion_tab()
        self.build_wave_tab()
        self.build_analysis_tab()
        self.build_memory_tab()

        root.addWidget(scroll)

    def build_overview_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(16)

        self.context_table = OverviewTable()
        context_box = SectionBox("Context")
        context_box.add_widget(self.context_table)

        self.result_table = OverviewTable()
        result_box = SectionBox("Result Overview")
        result_box.add_widget(self.result_table)

        layout.addWidget(context_box)
        layout.addWidget(result_box)

        self.tabs.addTab(tab, "Overview")

    # ------------------------------------------------------------------ #
    # Confusion Matrix tab
    # ------------------------------------------------------------------ #
    def build_confusion_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(16)

        self.upload_json_btn = QPushButton("Upload JSON with Confusion Matrix")
        self.upload_json_btn.clicked.connect(self.load_confusion_json)
        layout.addWidget(self.upload_json_btn)

        self.confusion_table = QTableWidget()
        self.confusion_table.setRowCount(0)
        self.confusion_table.setColumnCount(0)

        confusion_box = SectionBox("Confusion Matrix")
        confusion_box.add_widget(self.confusion_table)
        layout.addWidget(confusion_box)

        self.tabs.addTab(tab, "Confusion Matrix")

    def load_confusion_json(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select JSON File",
            "",
            "JSON Files (*.json);;All Files (*.*)"
        )

        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to read JSON file:\n{e}")
            return

        if "confusion_matrix" not in data:
            QMessageBox.warning(
                self,
                "Invalid JSON",
                "JSON does not contain key 'confusion_matrix'."
            )
            return

        matrix = data["confusion_matrix"]
        labels = data.get("labels", None)

        if not isinstance(matrix, list) or not matrix or not isinstance(matrix[0], list):
            QMessageBox.warning(
                self,
                "Invalid JSON",
                "Key 'confusion_matrix' must be a 2D list (list of lists)."
            )
            return

        self.populate_confusion_table(matrix, labels)

        QMessageBox.information(
            self,
            "Confusion Matrix Loaded",
            f"Confusion matrix loaded from:\n{file_path}"
        )

    def populate_confusion_table(self, matrix, labels=None):
        rows = len(matrix)
        cols = len(matrix[0])

        for r in matrix:
            if len(r) != cols:
                QMessageBox.warning(
                    self,
                    "Invalid Matrix",
                    "All rows in confusion_matrix must have the same length."
                )
                return

        self.confusion_table.clear()
        self.confusion_table.setRowCount(rows)
        self.confusion_table.setColumnCount(cols)

        if labels and len(labels) == rows and len(labels) == cols:
            self.confusion_table.setHorizontalHeaderLabels(labels)
            self.confusion_table.setVerticalHeaderLabels(labels)
        else:
            self.confusion_table.setHorizontalHeaderLabels([str(i) for i in range(cols)])
            self.confusion_table.setVerticalHeaderLabels([str(i) for i in range(rows)])

        for i in range(rows):
            for j in range(cols):
                value = matrix[i][j]
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.confusion_table.setItem(i, j, item)

    # ------------------------------------------------------------------ #
    # Wave tab + handlers
    # ------------------------------------------------------------------ #
    def on_dataset_changed(self, index: int):
        set_index = self.dataset_combo.itemData(index)
        if not set_index:
            self.wave_canvas.plot_default()
            self.wave_status.setText("Waveform: no set selected")
            return

        # use the current base_data_dir
        try:
            self.wave_canvas.load_epochs_from_set(set_index, self.base_data_dir)

            # Determine max epochs from loaded data
            max_epochs = 0
            if self.wave_canvas.epochs_eeg:
                max_epochs = max(max_epochs, len(self.wave_canvas.epochs_eeg))
            if self.wave_canvas.epochs_emg:
                max_epochs = max(max_epochs, len(self.wave_canvas.epochs_emg))
            if self.wave_canvas.epochs_ecg:
                max_epochs = max(max_epochs, len(self.wave_canvas.epochs_ecg))
            if self.wave_canvas.epochs_gsr:
                max_epochs = max(max_epochs, len(self.wave_canvas.epochs_gsr))

            if max_epochs > 0:
                self.epoch_spin.blockSignals(True)
                self.epoch_spin.setMinimum(0)
                self.epoch_spin.setMaximum(max(0, max_epochs - 1))
                self.epoch_spin.setValue(0)
                self.epoch_spin.blockSignals(False)

                self.wave_canvas.plot_epoch(0)
                self.wave_status.setText(
                    f"Waveform: set={set_index}, epoch=0 (1/{max_epochs})"
                )
            else:
                self.wave_canvas.plot_default()
                self.wave_status.setText("Waveform: failed to load set")

        except Exception as e:
            print(f"[MainWindow] Error loading set {set_index}: {e}")
            self.wave_canvas.plot_default()
            self.wave_status.setText("Waveform: error loading set")

    def on_epoch_changed(self, value: int):
        if not any([self.wave_canvas.epochs_eeg, self.wave_canvas.epochs_emg, 
                   self.wave_canvas.epochs_ecg, self.wave_canvas.epochs_gsr]):
            return

        epoch_index = value

        # Check max epochs
        max_epochs = 0
        if self.wave_canvas.epochs_eeg:
            max_epochs = max(max_epochs, len(self.wave_canvas.epochs_eeg))
        if self.wave_canvas.epochs_emg:
            max_epochs = max(max_epochs, len(self.wave_canvas.epochs_emg))
        if self.wave_canvas.epochs_ecg:
            max_epochs = max(max_epochs, len(self.wave_canvas.epochs_ecg))
        if self.wave_canvas.epochs_gsr:
            max_epochs = max(max_epochs, len(self.wave_canvas.epochs_gsr))

        if epoch_index < 0 or epoch_index >= max_epochs:
            return

        self.wave_canvas.plot_epoch(epoch_index)

        set_index = self.dataset_combo.itemData(self.dataset_combo.currentIndex())
        self.wave_status.setText(
            f"Waveform: set={set_index}, epoch={epoch_index} ({epoch_index+1}/{max_epochs})"
        )

    def build_wave_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(12)

        control_row = QHBoxLayout()

        self.dataset_combo = QComboBox()
        for i in range(1, 31):
            self.dataset_combo.addItem(f"Set {i}", i)

        self.dataset_combo.currentIndexChanged.connect(self.on_dataset_changed)
        control_row.addWidget(QLabel("Dataset:"))
        control_row.addWidget(self.dataset_combo)

        self.epoch_spin = QSpinBox()
        self.epoch_spin.setMinimum(0)
        self.epoch_spin.setMaximum(0)
        self.epoch_spin.valueChanged.connect(self.on_epoch_changed)
        control_row.addWidget(QLabel("Epoch:"))
        control_row.addWidget(self.epoch_spin)

        self.wave_status = QLabel("Waveform: no data")
        self.wave_status.setStyleSheet("font-size:12px;color:#64748b")
        control_row.addWidget(self.wave_status)

        control_row.addStretch()
        layout.addLayout(control_row)

        self.wave_canvas = WaveformCanvas(width=10, height=7)
        wave_box = SectionBox("Waveform Analysis")
        wave_box.add_widget(self.wave_canvas)

        layout.addWidget(wave_box)
        self.tabs.addTab(tab, "Wave Analysis")

    # ------------------------------------------------------------------ #
    # Analysis tab
    # ------------------------------------------------------------------ #
    def build_analysis_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        self.analysis_box = QTextEdit()
        self.analysis_box.setReadOnly(True)

        analysis_section = SectionBox("Auto Analysis")
        analysis_section.add_widget(self.analysis_box)

        layout.addWidget(analysis_section)
        self.tabs.addTab(tab, "Analysis")

    # ------------------------------------------------------------------ #
    # Memory Usage tab (Flash & RAM graph + cards)
    # ------------------------------------------------------------------ #
    def build_memory_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(16)

        summary_label = QLabel("Visual comparison of Flash and RAM usage")
        summary_label.setStyleSheet("font-size: 13px; color: #64748b;")
        layout.addWidget(summary_label)

        # Graph
        self.memory_canvas = MemoryCanvas(width=6, height=3)
        mem_box = SectionBox("Memory Usage (Flash vs RAM)")
        mem_box.add_widget(self.memory_canvas)
        layout.addWidget(mem_box)

        # Flash usage card
        flash_box = SectionBox("Flash Usage")
        flash_layout = QVBoxLayout()
        self.flash_label = QLabel("N/A")
        self.flash_label.setStyleSheet("font-size: 18px; font-weight: 800; color: #0f172a;")
        self.flash_detail = QLabel("Estimated FLASH: N/A")
        self.flash_detail.setStyleSheet("font-size: 12px; color: #64748b;")
        flash_layout.addWidget(self.flash_label)
        flash_layout.addWidget(self.flash_detail)
        flash_inner = QWidget()
        flash_inner.setLayout(flash_layout)
        flash_box.add_widget(flash_inner)

        # RAM usage card
        ram_box = SectionBox("RAM Usage")
        ram_layout = QVBoxLayout()
        self.ram_label = QLabel("N/A")
        self.ram_label.setStyleSheet("font-size: 18px; font-weight: 800; color: #0f172a;")
        self.ram_detail = QLabel("Estimated RAM: N/A")
        self.ram_detail.setStyleSheet("font-size: 12px; color: #64748b;")
        ram_layout.addWidget(self.ram_label)
        ram_layout.addWidget(self.ram_detail)
        ram_inner = QWidget()
        ram_inner.setLayout(ram_layout)
        ram_box.add_widget(ram_inner)

        layout.addWidget(flash_box)
        layout.addWidget(ram_box)
        layout.addStretch()

        self.tabs.addTab(tab, "Memory Usage")

    # ------------------------------------------------------------------ #
    # Memory tab helpers
    # ------------------------------------------------------------------ #
    def reset_memory_tab(self):
        # Reset labels
        if hasattr(self, "flash_label"):
            self.flash_label.setText("N/A")
        if hasattr(self, "flash_detail"):
            self.flash_detail.setText("Estimated FLASH: N/A")
        if hasattr(self, "ram_label"):
            self.ram_label.setText("N/A")
        if hasattr(self, "ram_detail"):
            self.ram_detail.setText("Estimated RAM: N/A")

        # Reset graph
        if hasattr(self, "memory_canvas"):
            self.memory_canvas.plot_empty()

    def update_memory_tab_from_report(self, report):
        flash_val = report.get("flash_ro")
        ram_val = report.get("ram_rw")

        if hasattr(self, "flash_label"):
            self.flash_label.setText(
                "N/A" if flash_val is None else format_int(flash_val)
            )
        if hasattr(self, "flash_detail"):
            self.flash_detail.setText(
                "Estimated FLASH: N/A"
                if flash_val is None
                else f"Estimated FLASH: {format_int(flash_val)} bytes"
            )

        if hasattr(self, "ram_label"):
            self.ram_label.setText(
                "N/A" if ram_val is None else format_int(ram_val)
            )
        if hasattr(self, "ram_detail"):
            self.ram_detail.setText(
                "Estimated RAM: N/A"
                if ram_val is None
                else f"Estimated RAM: {format_int(ram_val)} bytes"
            )

        if hasattr(self, "memory_canvas"):
            self.memory_canvas.plot_memory(flash_val or 0, ram_val or 0)

    # ------------------------------------------------------------------ #
    # Metrics helpers / empty state
    # ------------------------------------------------------------------ #
    def clear_metric_grid(self):
        while self.metric_grid.count():
            item = self.metric_grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def add_metric(self, row, col, title, value, subtitle=""):
        self.metric_grid.addWidget(MetricCard(title, value, subtitle), row, col)

    def set_empty_state(self):
        self.clear_metric_grid()

        self.add_metric(0, 0, "Model Name", "No file")
        self.add_metric(0, 1, "Target Platform", "N/A")
        self.add_metric(0, 2, "Flash Usage", "N/A")
        self.add_metric(0, 3, "RAM Usage", "N/A")

        self.context_table.load_data([("Status", "Upload one or more report files")])
        self.result_table.load_data([("Result", "No parsed report yet")])

        self.reset_memory_tab()

        self.wave_canvas.plot_default()
        self.wave_status.setText("Waveform: no data")

        self.analysis_box.setPlainText("No report loaded.")

    # ------------------------------------------------------------------ #
    # Dataset directory selector (fixed)
    # ------------------------------------------------------------------ #
    def set_dataset_dir(self):
        """
        Let the user choose a new base directory for datasets (.set files)
        and refresh the dataset combo box.
        """
        dir_path = QFileDialog.getExistingDirectory(
            self,
            "Select Dataset Directory",
            self.base_data_dir  # start from current
        )

        if not dir_path:
            return  # user cancelled

        # update instance variable
        self.base_data_dir = dir_path

        # reload current dataset if any
        current_index = self.dataset_combo.currentIndex()
        if current_index >= 0:
            self.on_dataset_changed(current_index)

        QMessageBox.information(
            self,
            "Dataset Directory Updated",
            f"Dataset directory set to:\n{dir_path}"
        )

    # ------------------------------------------------------------------ #
    # File loading / report selection
    # ------------------------------------------------------------------ #
    def load_reports(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select report files",
            "",
            "Text Files (*.txt);;All Files (*)"
        )
        if not files:
            return

        for path in files:
            try:
                report = parse_report_file(path)
                self.reports.append(report)
                self.report_list.addItem(report["file_name"])
            except Exception as e:
                QMessageBox.warning(
                    self,
                    "Parse Error",
                    f"Could not parse file:\n{path}\n\n{e}"
                )

        if self.report_list.count() > 0 and self.report_list.currentRow() == -1:
            self.report_list.setCurrentRow(0)

    def display_report(self, index):
        if index < 0 or index >= len(self.reports):
            self.set_empty_state()
            return

        report = self.reports[index]
        self.clear_metric_grid()

        self.add_metric(
            0, 0, "Model Name",
            report.get("model_name", "N/A"),
            "Parsed from uploaded report"
        )
        self.add_metric(
            0, 1, "Target Platform",
            report.get("target", "N/A"),
            "Deployment target"
        )
        self.add_metric(
            0, 2, "MACC",
            format_int(report.get("macc")),
            "Operations complexity"
        )
        self.add_metric(
            0, 3, "Weights",
            format_int(report.get("weights")),
            "Model storage"
        )

        self.add_metric(
            1, 0, "Activations",
            format_int(report.get("activations")), "Runtime memory"
        )
        self.add_metric(
            1, 1, "Flash Usage",
            format_int(report.get("flash_ro")), "Estimated FLASH"
        )
        self.add_metric(
            1, 2, "RAM Usage",
            format_int(report.get("ram_rw")), "Estimated RAM"
        )
        self.add_metric(
            1, 3, "Model Status",
            "Parsed", "Ready for inspection"
        )

        context_rows = [
            ("Model Name", report.get("model_name", "N/A")),
            ("Target Platform", report.get("target", "N/A")),
            ("Optimization Mode", "1x5"),
            ("Input Size", "1x63x500x1"),
            ("Output Size", "1x5"),
            ("Advanced Settings", "Future parser support"),
        ]
        self.context_table.load_data(context_rows)

        result_rows = [
            ("Operations (MACC)", format_int(report.get("macc"))),
            ("Flash Usage", f"{format_int(report.get('flash_ro'))} bytes"),
            ("RAM Usage", f"{format_int(report.get('ram_rw'))} bytes"),
            ("Inference Time", "1.98ms"),
            ("Compatibility", "Needs validation"),
            ("Runtime Info", "GCC 13.3.1 / STM32 runtime"),
        ]
        self.result_table.load_data(result_rows)

        self.update_memory_tab_from_report(report)

        self.wave_canvas.plot_default()
        self.wave_status.setText("Waveform: select dataset and epoch in Wave tab")

        self.analysis_box.setPlainText(
            report.get("analysis", "No analysis available.")
        )