import matplotlib.pyplot as plt


def plot_epoch(times_ms, signal, epoch_idx, total_epochs, channel_name="EEG"):
    fig, ax = plt.subplots(figsize=(10, 3))

    ax.plot(times_ms, signal, linewidth=1.5)

    # Event trigger line
    ax.axvline(0, linestyle="--", color="red")

    ax.set_xlim(times_ms[0], times_ms[-1])

    ymin = signal.min() - 1
    ymax = signal.max() + 1
    ax.set_ylim(ymin, ymax)

    ax.set_title(f"{channel_name} Epoch {epoch_idx+1}/{total_epochs}")
    ax.set_xlabel("Time relative to event trigger (ms)")
    ax.set_ylabel("uV")

    ax.grid(True, alpha=0.3)

    fig.tight_layout()

    return fig