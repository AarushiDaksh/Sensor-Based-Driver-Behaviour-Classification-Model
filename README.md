# Sensor-Based Driver Behaviour Classification Model

A multimodal machine learning project for **driver behaviour classification** using physiological and sensor-based signals such as **EEG, ECG, EMG, and GSR**.  
This project combines **signal preprocessing, feature learning, fusion modelling, classification, and dashboard-based analysis** to detect and understand driver behavioural states.

---

## Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Objectives](#objectives)
- [Key Features](#key-features)
- [System Workflow](#system-workflow)
- [Dataset and Signals Used](#dataset-and-signals-used)
- [Model Architecture](#model-architecture)
- [Fusion Model](#fusion-model)
- [Classification Performance](#classification-performance)
- [Confusion Matrix Analysis](#confusion-matrix-analysis)
- [Dashboard Overview](#dashboard-overview)
- [How We Built the Dashboard](#how-we-built-the-dashboard)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [How to Run the Dashboard](#how-to-run-the-dashboard)
- [Use Cases](#use-cases)
- [Future Improvements](#future-improvements)
- [Conclusion](#conclusion)

---

## Overview

Driver behaviour plays a major role in road safety. Fatigue, stress, distraction, and delayed reactions can directly affect driving performance and increase accident risk.

In this project, we developed a **Sensor-Based Driver Behaviour Classification Model** that uses multiple physiological signals to identify behavioural patterns of drivers. We also built a **Driver Behaviour Analysis Dashboard** to visualize model performance, signal waveforms, memory usage, and deployment insights in a clear and interactive way.

This project focuses on both:

1. **Building an accurate classification model**
2. **Creating a dashboard for analysis, monitoring, and presentation**

---

## Problem Statement

Traditional driver monitoring systems often rely only on camera-based tracking or vehicle movement analysis. These approaches may miss internal physiological changes such as stress, fatigue, or cognitive overload.

To solve this, we worked on a system that uses **multimodal biosignals**:

- **EEG** – brain activity
- **ECG** – heart activity
- **EMG** – muscle activity
- **GSR** – skin conductance / stress response

The goal was to classify driver behaviour more effectively by combining these signals into a **fusion-based machine learning model**.

---

## Objectives

- Collect and process multimodal driver-related physiological data
- Extract meaningful patterns from EEG, ECG, EMG, and GSR signals
- Build a **fusion model** for better behaviour classification
- Evaluate performance using a **confusion matrix**
- Achieve reliable classification accuracy
- Build an interactive dashboard for result interpretation and deployment analysis

---

## Key Features

- Multimodal driver behaviour classification
- Fusion of EEG, ECG, EMG, and GSR signals
- Achieved around **85% classification accuracy**
- Confusion matrix-based evaluation
- Signal waveform visualization
- Embedded deployment analysis support
- Interactive desktop dashboard built with **PyQt5**
- Model metadata, RAM/Flash usage, and analysis panels

---

## System Workflow

The overall workflow of the project is shown below:

| Step | Description |
|------|-------------|
| 1 | Collect multimodal physiological data |
| 2 | Preprocess EEG, ECG, EMG, and GSR signals |
| 3 | Prepare labelled data for training |
| 4 | Train the classification / fusion model |
| 5 | Evaluate using accuracy and confusion matrix |
| 6 | Export model results and metadata |
| 7 | Visualize everything in the dashboard |

---

## Dataset and Signals Used

The model uses multiple physiological signals to understand driver state.

| Signal | Full Form | Purpose in Project |
|--------|-----------|-------------------|
| EEG | Electroencephalography | Captures brain activity and mental state |
| ECG | Electrocardiography | Measures heart activity and stress response |
| EMG | Electromyography | Captures muscle activity and physical response |
| GSR | Galvanic Skin Response | Indicates emotional arousal / stress level |

### Why multimodal signals?
A single signal may not fully represent driver behaviour.  
By combining multiple signals, the model can capture:

- mental workload
- physical reaction
- stress level
- neurological response

This improves robustness and classification performance.

---

## Model Architecture

The project uses a classification pipeline designed to learn patterns from physiological signals and identify driver behaviour states.

### Main steps:
- Signal acquisition
- Signal preprocessing
- Feature extraction / deep feature learning
- Fusion of multimodal inputs
- Classification
- Evaluation

Depending on implementation, the model may use:
- deep learning layers for pattern extraction
- CNN-based feature learning
- dense layers for classification
- multimodal feature fusion before final prediction

---

## Fusion Model

One of the most important parts of this project is the **fusion model**.

Instead of training on only one signal type, we combined information from multiple sensor streams to improve prediction quality.

### Why fusion?
Each signal provides different information:

- EEG gives brain-state information
- ECG gives heart/stress information
- EMG gives muscular response
- GSR gives skin conductance and arousal information

A fusion model learns from all these together, which helps the system make better behavioural decisions than a single-sensor model.

### Fusion approach used
| Component | Role |
|----------|------|
| EEG branch | Learns neurological patterns |
| ECG branch | Learns heart-related changes |
| EMG branch | Learns muscular activity patterns |
| GSR branch | Learns stress/arousal trends |
| Fusion layer | Combines features from all branches |
| Final classifier | Predicts driver behaviour class |

This fusion-based approach contributed to the overall performance of the system.

---

## Classification Performance

The model achieved approximately:

| Metric | Value |
|--------|-------|
| Accuracy | **85%** |
| Evaluation Method | Confusion Matrix |
| Input Type | Multimodal Sensor Fusion |
| Output | Driver Behaviour Class |

> The 85% result shows that the fusion model was able to learn meaningful behaviour-related patterns from the combined sensor signals.

---

## Confusion Matrix Analysis

A **confusion matrix** was used to evaluate the classification model.

It helps us understand:
- how many samples were classified correctly
- which classes were confused with each other
- where the model performs well
- where further improvement is needed

### Why confusion matrix is important?
Accuracy alone does not show complete model behaviour.  
A confusion matrix gives class-wise performance and helps identify misclassification trends.

### Interpretation
| Outcome | Meaning |
|---------|---------|
| High diagonal values | Correct predictions |
| Low off-diagonal values | Fewer classification mistakes |
| Off-diagonal errors | Confusion between behaviour classes |

In our project, the confusion matrix showed that the model was able to classify most driver behaviour states correctly, supporting the achieved **~85% classification accuracy**.

---

## Dashboard Overview

We built a **Driver Behaviour Analysis Dashboard** to make the project easier to understand, analyze, and present.

The dashboard provides a unified interface for:

- model metadata
- classification accuracy
- confusion matrix visualization
- RAM and Flash usage
- waveform display
- textual analysis
- deployment-oriented observations

### Dashboard modules

| Module | Description |
|--------|-------------|
| Model Info | Displays model name, target platform, weights, MACC, and metadata |
| Performance Panel | Shows accuracy and confusion matrix |
| Memory Analysis | Displays Flash and RAM consumption |
| Waveform Section | Visualizes EEG, ECG, EMG, and GSR signals |
| Analysis Panel | Provides observations and result summaries |
| File Loader | Loads report/evaluation files dynamically |

---

## How We Built the Dashboard

The dashboard was developed as a **desktop application in Python** using **PyQt5** and **Matplotlib**.

### Development approach

| Step | What We Did |
|------|-------------|
| UI Design | Created a clean multi-section dashboard layout |
| Data Parsing | Read model/evaluation/report files |
| Visualization | Used charts and waveform plots for signals |
| Performance Display | Added confusion matrix and accuracy presentation |
| System Metrics | Showed memory usage such as RAM and Flash |
| Interactivity | Allowed report loading and dynamic UI updates |

### Dashboard design logic
We wanted the dashboard to do more than just show numbers.  
So we designed it to support:

- **easy interpretation**
- **project demonstration**
- **model validation**
- **embedded deployment understanding**

### Main libraries used in dashboard
| Library | Purpose |
|--------|---------|
| PyQt5 | GUI development |
| Matplotlib | Graphs and waveform plotting |
| NumPy / JSON / Parsers | Data loading and report handling |
| Custom widgets | Cards, badges, tables, and section boxes |

### What the dashboard helps us do
- inspect the model quickly
- understand accuracy visually
- analyze class confusion
- display waveform behaviour
- present the project in a more professional way

---

## Tech Stack

### Machine Learning / Data Side
| Category | Tools / Concepts |
|----------|------------------|
| Language | Python |
| Data Handling | NumPy, JSON |
| ML / DL | CNN / Fusion Model / Classification Pipeline |
| Signal Processing | EEG, ECG, EMG, GSR preprocessing |
| Evaluation | Accuracy, Confusion Matrix |

### Dashboard Side
| Category | Tools |
|----------|------|
| GUI Framework | PyQt5 |
| Plotting | Matplotlib |
| Architecture | Modular desktop dashboard |
| Output | Interactive model analysis interface |

---

## Project Structure

```bash
Sensor-Based-Driver-Behaviour-Classification-Model/
│
├── main.py
├── parser/
│   └── report_parser.py
├── ui/
│   └── main_window.py
├── widgets/
│   ├── metric_card.py
│   ├── badge.py
│   ├── gauge_widget.py
│   ├── waveform_plot.py
│   ├── overview_table.py
│   └── section_box.py
├── utils/
│   └── helpers.py
├── reports/
├── assets/
└── README.md
