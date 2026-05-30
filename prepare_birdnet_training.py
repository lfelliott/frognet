"""
Builds data/birdnet_training/ from confirmed species clips and reviewed noise clips.

Species clips: copied from data/snippets/<species>/confirmed/
Noise clips:   sampled from all noise_ok=True rows across species scores.csv files
               plus data/snippets/extra_nonfrog/scores.csv, capped at NOISE_TARGET.

Run this once before birdnet-train. Safe to re-run — skips files already copied.
"""

import random
import shutil
import pandas as pd
from pathlib import Path

SNIPPETS_DIR = Path("data/snippets")
TRAINING_DIR = Path("data/birdnet_training")
NOISE_TARGET = 400
NOISE_SEED = 42

# ── species clips ─────────────────────────────────────────────────────────────

species_dirs = sorted(
    d for d in SNIPPETS_DIR.iterdir()
    if d.is_dir() and d.name != "extra_nonfrog" and (d / "confirmed").exists()
)

print("Copying confirmed species clips...")
species_totals = {}
for species_dir in species_dirs:
    species = species_dir.name
    src_dir = species_dir / "confirmed"
    dst_dir = TRAINING_DIR / species
    dst_dir.mkdir(parents=True, exist_ok=True)

    clips = sorted(src_dir.glob("*.wav"))
    copied = 0
    for clip in clips:
        dst = dst_dir / clip.name
        if not dst.exists():
            shutil.copy2(clip, dst)
            copied += 1
    species_totals[species] = len(clips)
    print(f"  {species}: {len(clips)} clips ({copied} new)")

# ── noise clips ───────────────────────────────────────────────────────────────

print("\nCollecting approved noise clips...")
noise_pool = []

# species discards marked noise_ok
for scores_path in sorted(SNIPPETS_DIR.glob("*/scores.csv")):
    species = scores_path.parent.name
    if species == "extra_nonfrog":
        clips_dir = scores_path.parent / "clips"
        prefix = "extra_nonfrog"
    else:
        clips_dir = scores_path.parent / "clips"
        prefix = species

    df = pd.read_csv(scores_path)
    if "noise_ok" not in df.columns:
        continue
    approved = df[df["noise_ok"] == True]
    for _, row in approved.iterrows():
        src = clips_dir / row["file"]
        if src.exists():
            noise_pool.append((src, f"{prefix}__{row['file']}"))

print(f"  {len(noise_pool)} total approved noise clips")

random.seed(NOISE_SEED)
sample = random.sample(noise_pool, min(NOISE_TARGET, len(noise_pool)))
print(f"  Sampling {len(sample)} for training")

noise_dir = TRAINING_DIR / "noise"
noise_dir.mkdir(parents=True, exist_ok=True)

copied = 0
for src, dst_name in sample:
    dst = noise_dir / dst_name
    if not dst.exists():
        shutil.copy2(src, dst)
        copied += 1

# ── summary ───────────────────────────────────────────────────────────────────

print("\n── Training folder summary ──────────────────────────────────────────")
total_species_clips = sum(species_totals.values())
for species, count in sorted(species_totals.items()):
    print(f"  {species:<35} {count:>5}")
print(f"  {'noise':<35} {len(sample):>5}")
print(f"\n  Total species clips : {total_species_clips}")
print(f"  Total noise clips   : {len(list(noise_dir.glob('*.wav')))}")
print(f"  Classes             : {len(species_totals)} species + noise")
print("\nDone. Run birdnet-train to train the classifier.")
print("""
  birdnet-train data/birdnet_training/ \\
    --output data/frog_classifier \\
    --model_save_mode replace \\
    --hidden_units 256 --dropout 0.2 \\
    --mixup --label_smoothing \\
    --upsampling_ratio 0.8 --upsampling_mode repeat \\
    --fmin 100 --fmax 7000 \\
    --epochs 75 --val_split 0.2
""")
