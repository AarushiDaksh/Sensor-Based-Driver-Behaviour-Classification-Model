# Driver Behaviour Analysis Dashboard

The **Driver Behaviour Analysis Dashboard** is a Python desktop
application designed to inspect, validate, and visualize driver
behaviour classification models used in embedded systems.

It provides engineers with a unified interface to analyze model
metadata, memory usage, confusion matrices, and physiological signal
waveforms used in training driver behavior models.

------------------------------------------------------------------------

# Features

### Model Inspection

View model metadata such as: - Model name - Target platform - MACC
operations - Weights - Flash usage - RAM usage

### Memory Usage Visualization

Displays Flash and RAM usage using bar charts.

### Confusion Matrix Analysis

Upload evaluation JSON files and view classification performance.

### Biosignal Visualization

Supports visualization of: - EEG - ECG - EMG - GSR

### Auto Report Analysis

Displays textual analysis extracted from model reports.

------------------------------------------------------------------------

# Technology Stack

-   Python 3
-   PyQt5
-   Matplotlib
-   NumPy
-   Pandas
-   MNE

------------------------------------------------------------------------

# Project Structure

DriverDashboard │ ├── main.py ├── ui │ └── main_window.py ├── parser │
└── report_parser.py ├── widgets │ ├── metric_card.py │ ├── badge.py │
├── waveform_plot.py │ ├── memory_plot.py │ ├── overview_table.py │ └──
section_box.py ├── utils │ └── helpers.py └── preprocessed data ├── ECG
├── EEG ├── EMG └── GSR

------------------------------------------------------------------------

# Running the Application

Run the project using:

python main.py

------------------------------------------------------------------------

# Confusion Matrix JSON Example

{ "confusion_matrix": \[ \[50,2\], \[3,45\] \], "labels":
\["class0","class1"\] }

------------------------------------------------------------------------

# Installation

Install dependencies:

pip install -r requirements.txt

Example requirements.txt:

PyQt5 matplotlib numpy scipy pandas mne

------------------------------------------------------------------------

# License

This project is intended for research, educational, and embedded AI
development purposes.
