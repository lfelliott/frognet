#!/usr/bin/env python3
"""
For a folder that has been analyzed with birdnet-analyze, reads the combined CSV
and produces one spectrogram PNG per detected species — the clip with the highest
confidence score.  The PNG is written to the same folder.
Usage:
    python spectrogram_best_detections.py data/field_recordings/3MWetlands0626
"""

import sys
import os
import csv
import pathlib
import numpy as np
import librosa
import librosa.display
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def species_key(row):
    return f"{row['Scientific name']}_{row['Common name']}"


def species_display(row):
    return f"{row['Scientific name'].capitalize()} {row['Common name']}"


def make_spectrogram(wav_path, start_s, end_s, species_name, confidence, out_path):
    y, sr = librosa.load(wav_path, sr=None, offset=start_s, duration=end_s - start_s, mono=True)

    n_fft = 2048
    hop_length = 512
    S = librosa.stft(y, n_fft=n_fft, hop_length=hop_length)
    S_db = librosa.amplitude_to_db(np.abs(S), ref=np.max)

    fig, ax = plt.subplots(figsize=(10, 4))
    FMIN_DISPLAY = 350
    FMAX_DISPLAY = 7000

    img = librosa.display.specshow(
        S_db,
        sr=sr,
        hop_length=hop_length,
        x_axis="time",
        y_axis="hz",
        fmin=FMIN_DISPLAY,
        fmax=FMAX_DISPLAY,
        ax=ax,
        cmap="magma",
    )
    ax.set_ylim(FMIN_DISPLAY, FMAX_DISPLAY)
    fig.colorbar(img, ax=ax, format="%+2.0f dB")

    filename = pathlib.Path(wav_path).name
    title = (
        f"{filename}  |  {species_name}  |  confidence: {confidence:.4f}\n"
        f"t = {start_s:.1f} – {end_s:.1f} s"
    )
    ax.set_title(title, fontsize=11)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Frequency (Hz)")

    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f"  Saved {out_path}")


def main(folder):
    folder = pathlib.Path(folder)
    csv_path = folder / "BirdNET_CombinedTable.csv"
    if not csv_path.exists():
        sys.exit(f"No BirdNET_CombinedTable.csv found in {folder}")

    # Read all rows and find best-confidence row per species
    best = {}
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = species_key(row)
            conf = float(row["Confidence"])
            if key not in best or conf > float(best[key]["Confidence"]):
                best[key] = row

    print(f"Found {len(best)} species in {csv_path.name}:")
    for key, row in best.items():
        print(f"  {species_display(row):40s}  conf={float(row['Confidence']):.4f}  "
              f"file={pathlib.Path(row['File']).name}  "
              f"t={row['Start (s)']}-{row['End (s)']}s")

    for key, row in best.items():
        wav_path = pathlib.Path(row["File"])
        # Support paths relative to script working directory
        if not wav_path.exists():
            wav_path = pathlib.Path(os.getcwd()) / row["File"]
        if not wav_path.exists():
            print(f"  WARNING: cannot find {row['File']}, skipping")
            continue

        start_s = float(row["Start (s)"])
        end_s = float(row["End (s)"])
        conf = float(row["Confidence"])
        sp_display = species_display(row)

        safe_key = key.replace(" ", "_")
        out_path = folder / f"spectrogram_{safe_key}.png"
        make_spectrogram(str(wav_path), start_s, end_s, sp_display, conf, str(out_path))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: spectrogram_best_detections.py <folder>")
    main(sys.argv[1])
