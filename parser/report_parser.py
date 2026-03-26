import os
import re


def to_int(val):
    if not val:
        return None
    try:
        return int(str(val).replace(",", "").strip())
    except Exception:
        return None


def extract(pattern, text, default=None, flags=0):
    m = re.search(pattern, text, flags)
    return m.group(1).strip() if m else default


def parse_report_file(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    model_name = (
        extract(r"Model name\s*-\s*(.+)", text) or
        extract(r"model_name\s*:\s*(.+)", text) or
        os.path.basename(file_path)
    )

    target = (
        extract(r"target/series\s*:\s*(.+)", text) or
        extract(r"--target\s+([A-Za-z0-9_]+)", text) or
        "Unknown"
    )

    macc = to_int(
        extract(r"macc\s*:\s*([\d,]+)", text) or
        extract(r"model: macc=([\d,]+)", text)
    )

    weights = to_int(
        extract(r"weights \(ro\)\s*:\s*([\d,]+)", text) or
        extract(r"weights=([\d,]+)", text)
    )

    activations = to_int(
        extract(r"activations \(rw\)\s*:\s*([\d,]+)", text) or
        extract(r"activations=([\d,]+)", text)
    )

    flash_ro = to_int(extract(r"TOTAL\s+([\d,]+)\s+[\d,]+", text))
    ram_rw = to_int(extract(r"TOTAL\s+[\d,]+\s+([\d,]+)", text))

    analysis = []
    analysis.append(f"Model: {model_name}")
    analysis.append(f"Target: {target}")
    if macc is not None:
        analysis.append(f"MACC: {macc:,}")
    if weights is not None:
        analysis.append(f"Weights: {weights:,}")
    if activations is not None:
        analysis.append(f"Activations: {activations:,}")
    if flash_ro is not None and ram_rw is not None:
        analysis.append(f"Estimated memory -> Flash: {flash_ro:,} bytes, RAM: {ram_rw:,} bytes")

    if activations and weights:
        if activations > weights:
            analysis.append("Runtime memory demand is higher than model storage.")
        else:
            analysis.append("Model storage demand is higher than runtime activation demand.")

    return {
        "file_name": os.path.basename(file_path),
        "model_name": model_name,
        "target": target,
        "macc": macc,
        "weights": weights,
        "activations": activations,
        "flash_ro": flash_ro,
        "ram_rw": ram_rw,
        "analysis": "\n".join(analysis),
    }