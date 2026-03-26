import os
import numpy as np
import mne

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class WaveformCanvas(FigureCanvas):
    """
    Qt-embedded Matplotlib canvas that displays epochs of multimodal
    biosignals (EEG/ECG/EMG/GSR) from EEGLAB .set files using MNE.

    Displays four panels: EEG, EMG, ECG, GSR for a selected set index.
    """

    def __init__(self, width=10, height=7, parent=None):
        self.fig = Figure(figsize=(width, height))
        # initial 4 stacked axes share the x-axis (time)
        self.axes = self.fig.subplots(4, 1, sharex=True)

        super().__init__(self.fig)
        self.setParent(parent)

        self.epochs_eeg = None
        self.epochs_emg = None
        self.epochs_ecg = None
        self.epochs_gsr = None
        self.times = None
        self.current_set = None

        self.plot_default()

    # ------------------------------------------------------------------ #
    # Load EEGLAB .set files for a set index
    # ------------------------------------------------------------------ #
    def load_epochs_from_set(self, set_index: int, base_dir: str):
        """
        Load epochs for EEG, EMG, ECG, GSR from .set files for the given set index.
        """
        eeg_path = os.path.join(base_dir, "EEG", f"EEG_{set_index}.set")
        emg_path = os.path.join(base_dir, "EMG", f"EMG_{set_index}.set")
        ecg_path = os.path.join(base_dir, "ECG", f"ECG_{set_index}.set")
        gsr_path = os.path.join(base_dir, "GSR", f"GSR_{set_index}.set")

        self.epochs_eeg = self._load_single_file(eeg_path, "EEG")
        self.epochs_emg = self._load_single_file(emg_path, "EMG")
        self.epochs_ecg = self._load_single_file(ecg_path, "ECG")
        self.epochs_gsr = self._load_single_file(gsr_path, "GSR")

        # Use times from EEG if available, else from others
        if self.epochs_eeg:
            self.times = self.epochs_eeg.times
        elif self.epochs_emg:
            self.times = self.epochs_emg.times
        elif self.epochs_ecg:
            self.times = self.epochs_ecg.times
        elif self.epochs_gsr:
            self.times = self.epochs_gsr.times
        else:
            self.times = None

        self.current_set = set_index

        if self.times is not None:
            self.plot_epoch(0)
        else:
            self.plot_default()

    def _load_single_file(self, filepath: str, signal_type: str):
        if not os.path.isfile(filepath):
            print(f"[WaveformCanvas] {signal_type} .set file not found: {filepath}")
            return None

        try:
            print(f"[WaveformCanvas] Loading {signal_type} epochs from: {filepath}")
            epochs = mne.io.read_epochs_eeglab(filepath, verbose=False)
            print(f"{signal_type}: {len(epochs)} epochs, channels: {epochs.ch_names}")
            return epochs
        except Exception as e:
            print(f"[WaveformCanvas] Error loading {signal_type} from {filepath}: {e}")
            return None

    # ------------------------------------------------------------------ #
    # Placeholder when nothing is loaded
    # ------------------------------------------------------------------ #
    def plot_default(self):
        # ensure we have 4 axes
        self.fig.clear()
        self.axes = self.fig.subplots(4, 1, sharex=True)

        for ax in self.axes:
            ax.clear()

        t = np.linspace(-0.5, 1.5, 500)
        dummy = np.zeros_like(t)
        for ax in self.axes:
            ax.plot(t, dummy, color="#9ca3af")
            ax.axvline(0, linestyle="--", color="#d1d5db")
            ax.grid(True, alpha=0.3)

        self.axes[0].set_title("No epochs loaded", fontsize=11)
        self.axes[1].set_title("Select a set to view EEG/ECG/EMG/GSR", fontsize=10)
        self.axes[2].set_title("", fontsize=10)
        self.axes[3].set_title("", fontsize=10)
        self.axes[-1].set_xlabel("Time (s)")

        self.fig.tight_layout()
        self.draw()

    # ------------------------------------------------------------------ #
    # Plot one epoch (4 panels)
    # ------------------------------------------------------------------ #
    def plot_epoch(self, epoch_index: int, classification_label: str = None):
        """
        Plot one epoch in four stacked panels (EEG / EMG / ECG / GSR),
        visually similar to the reference figure:

          - Shared time axis (bottom) in ms
          - Vertical dashed line at t = 0 (event)
          - Shaded baseline / pre-event / post-event regions
        """
        if not any([self.epochs_eeg, self.epochs_emg, self.epochs_ecg, self.epochs_gsr]):
            print("[WaveformCanvas] No epochs loaded; cannot plot epoch.")
            self.plot_default()
            return

        # Check if epoch_index is valid for at least one epochs
        max_epochs = 0
        if self.epochs_eeg:
            max_epochs = max(max_epochs, len(self.epochs_eeg))
        if self.epochs_emg:
            max_epochs = max(max_epochs, len(self.epochs_emg))
        if self.epochs_ecg:
            max_epochs = max(max_epochs, len(self.epochs_ecg))
        if self.epochs_gsr:
            max_epochs = max(max_epochs, len(self.epochs_gsr))

        if epoch_index < 0 or epoch_index >= max_epochs:
            print(
                f"[WaveformCanvas] epoch_index {epoch_index} out of range (0..{max_epochs - 1})"
            )
            return

        # ------------------------------------------------------------------
        # Prepare figure
        # ------------------------------------------------------------------
        self.fig.clear()
        self.axes = self.fig.subplots(4, 1, sharex=True)

        # ------------------------------------------------------------------
        # Visual configuration: regions & colours
        # ------------------------------------------------------------------
        if self.times is not None:
            t_min, t_max = self.times[0], self.times[-1]
            times_ms = self.times * 1000.0
        else:
            t_min, t_max = -0.5, 1.5
            times_ms = np.linspace(t_min, t_max, 500) * 1000.0

        baseline_start, baseline_end = t_min, -0.25
        pre_start, pre_end = 0, 0.25
        post_start, post_end = 0.25, t_max

        baseline_color = "#f3f4f6"  # light gray
        pre_color = "#fee2e2"       # light red
        post_color = "#dcfce7"      # light green

        zero_line_color = "red"
        zero_line_style = "--"

        # ------------------------------------------------------------------
        # Helper to shade regions & draw t=0 line on one axis
        # ------------------------------------------------------------------
        def _add_background(ax):
            # ax.axvspan(baseline_start*1000.0, baseline_end*1000.0,
            #            color=baseline_color, alpha=0.5, zorder=-10)
            ax.axvspan(pre_start*1000.0, pre_end*1000.0,
                       color=pre_color, alpha=0.4, zorder=-10)
            ax.axvspan(post_start*1000.0, post_end*1000.0,
                       color=post_color, alpha=0.3, zorder=-10)
            # vertical event line at t=0
            ax.axvline(0, linestyle=zero_line_style, color=zero_line_color, linewidth=1.5)

        # ------------------------------------------------------------------
        # Helper to plot a signal type on a given axis
        # ------------------------------------------------------------------
        def _plot_signal(ax, epochs, signal_type, color, y_label):
            ax.clear()
            _add_background(ax)

            if epochs is None or epoch_index >= len(epochs):
                ax.plot(times_ms, np.zeros_like(times_ms), color="#e5e7eb")
                ax.set_title(f"{signal_type} (no data)", fontsize=10)
                ax.set_ylabel(y_label, fontsize=9)
                ax.grid(True, alpha=0.2)
                return

            ep = epochs[epoch_index]
            data = ep.get_data()[0]  # (n_channels, n_times)

            # Pick the first channel of the appropriate type
            if signal_type == "EEG":
                picks = mne.pick_types(epochs.info, eeg=True, emg=False, ecg=False, misc=False)
            elif signal_type == "EMG":
                emg_candidates = [
                    name for name in epochs.ch_names
                    if "EMG" in name.upper()
                ]
                picks = mne.pick_channels(epochs.ch_names, include=emg_candidates)
            elif signal_type == "ECG":
                ecg_candidates = [
                    name for name in epochs.ch_names
                    if "ECG" in name.upper()
                ]
                picks = mne.pick_channels(epochs.ch_names, include=ecg_candidates)
            elif signal_type == "GSR":
                gsr_candidates = [
                    name for name in epochs.ch_names
                    if "GSR" in name.upper() or "EDA" in name.upper()
                ]
                picks = mne.pick_channels(epochs.ch_names, include=gsr_candidates)
            else:
                picks = []

            if len(picks) == 0:
                ax.plot(times_ms, np.zeros_like(times_ms), color="#e5e7eb")
                ax.set_title(f"{signal_type} (no channels)", fontsize=10)
            else:
                ch_idx = picks[0]
                ch_name = epochs.ch_names[ch_idx]
                ax.plot(times_ms, data[ch_idx], label=ch_name, color=color)
                ax.set_title(f"{signal_type} (epoch {epoch_index + 1})", fontsize=10)
                ax.legend(fontsize=8, loc="upper right")

            ax.set_ylabel(y_label, fontsize=9)
            ax.grid(True, alpha=0.3)

        # ------------------------------------------------------------------
        # Plot each signal type in its own panel
        # ------------------------------------------------------------------
        _plot_signal(
            self.axes[0],
            self.epochs_eeg,
            "EEG",
            "#1d4ed8",
            "EEG (µV)"
        )

        _plot_signal(
            self.axes[1],
            self.epochs_emg,
            "EMG",
            "#16a34a",
            "EMG (mV)"
        )

        _plot_signal(
            self.axes[2],
            self.epochs_ecg,
            "ECG",
            "#dc2626",
            "ECG (mV)"
        )

        _plot_signal(
            self.axes[3],
            self.epochs_gsr,
            "GSR",
            "#7c3aed",
            "GSR (µS)"
        )

        # ------------------------------------------------------------------
        # Shared X label & figure title
        # ------------------------------------------------------------------
        self.axes[-1].set_xlabel("Time (ms)", fontsize=10)

        # Optional classification title at top
        if classification_label:
            self.fig.suptitle(
                f"Classification: {classification_label}",
                fontsize=14,
                fontweight="bold",
                color="#1f2937"
            )

        self.fig.tight_layout(rect=[0, 0, 1, 0.95])  # leave space for suptitle
        self.draw()

    def plot_epochs_range(self, start_epoch: int, end_epoch: int):
        """
        Plot multiple epochs (start_epoch..end_epoch inclusive) stacked vertically,
        showing EEG channels only. This does not affect plot_epoch() behaviour.

        Example: plot_epochs_range(10, 15) plots epochs 10..15 (0-based).
        """
        if self.epochs_eeg is None:
            print("[WaveformCanvas] No EEG epochs loaded; cannot plot epochs range.")
            self.plot_default()
            return

        n_epochs = len(self.epochs_eeg)
        if start_epoch < 0 or end_epoch >= n_epochs or start_epoch > end_epoch:
            print(
                f"[WaveformCanvas] Invalid epoch range {start_epoch}..{end_epoch} "
                f"(valid 0..{n_epochs - 1})"
            )
            return

        picks_eeg = mne.pick_types(self.epochs_eeg.info, eeg=True, emg=False, ecg=False, misc=False)
        if len(picks_eeg) == 0:
            print("[WaveformCanvas] No EEG channels; cannot plot range.")
            return

        # Rebuild figure with one row per epoch
        self.fig.clear()
        axes = self.fig.subplots(end_epoch - start_epoch + 1, 1, sharex=True)
        if not isinstance(axes, np.ndarray):
            axes = np.array([axes])
        self.axes = axes

        for row, epoch_idx in enumerate(range(start_epoch, end_epoch + 1)):
            ep = self.epochs_eeg[epoch_idx]
            data = ep.get_data()[0]   # (n_channels, n_times)
            times = ep.times
            ax = axes[row]
            ax.clear()

            offset = 0.0
            step = 10e-6
            for ch_idx in picks_eeg:
                ch_name = self.epochs_eeg.ch_names[ch_idx]
                ax.plot(times, data[ch_idx] + offset, label=ch_name)
                offset += step

            ax.axvline(0, linestyle="--", color="red")
            ax.grid(True, alpha=0.3)
            ax.set_ylabel(f"Epoch {epoch_idx}", fontsize=8)
            if row == 0:
                ax.set_title(
                    f"EEG – Epochs {start_epoch}..{end_epoch}",
                    fontsize=10
                )
            if row == 0 and len(picks_eeg) <= 8:
                ax.legend(fontsize=7, loc="upper right")

        axes[-1].set_xlabel("Time (s)")
        self.fig.tight_layout()
        self.draw()