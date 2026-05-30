# %%
# setup - species config and directories
from pathlib import Path

SPECIES_CONFIG = {
    "acris_blanchardi": {
        "trill": False,
        "signal_band": [2500, 4400],
        "noise_bands": [[1000, 2000], [4600, 6000]],
    },
    "anaxyrus_americanus": {
        "trill": True,
        "signal_band": [1100, 1900],
        "noise_bands": [[500, 1000], [2400, 6000]],
        "pulse_rate_range": [20,40],
        "score_keep": 0.098,
        "score_discard": 0.025,
    },
    "anaxyrus_cognatus": {
        "trill": True,
        "signal_band": [2000, 2500],
        "noise_bands": [[500, 1900], [2700, 6000]],
        "pulse_rate_range": [10, 20],
        "score_keep": 10.0,
        "score_discard": 0.1,
    },
    "anaxyrus_fowleri": {
        "trill": True,
        "signal_band": [1200, 2500],
        "noise_bands": [[500, 1000], [2700, 6000]],
        "pulse_rate_range": [34,69],
        "score_keep": 0.098,
        "score_discard": 0.013,
    },
    "anaxyrus_woodhousii": {
        "trill": True,
        "signal_band": [900, 2000],
        "noise_bands": [[200, 800], [2500, 6000]],
        "pulse_rate_range": [37,65],
        "score_keep": 0.098,
        "score_discard": 0.003,
    },
    "dryophytes_chrysoscelis": {
        "trill": False,
        "signal_band": [2500, 4500],
        "noise_bands": [[1000, 2000], [4600, 6000]],
        "pulse_rate_range": [15, 35],
        "score_keep": 0.65,
        "score_discard": 0.03,
    },
    "dryophytes_cinereus": {
        "trill": False,
        "signal_band": [900, 4000],
        "noise_bands": [[100, 800], [4500, 6000]],
        "pulse_rate_range": [15, 35],
        "score_keep": 0.65,
        "score_discard": 0.07,
    },
    "dryophytes_versicolor": {
        "trill": False,
        "signal_band": [800, 3500],
        "noise_bands": [[300, 7500], [4000, 6000]],
        "pulse_rate_range": [15, 35],
        "score_keep": 0.25,
        "score_discard": 0.07,
    },
    "gastrophryne_carolinensis": {
        "trill": False,
        "signal_band": [1000, 5000],
        "noise_bands": [[0, 900], [5500, 7000]],
        "pulse_rate_range": [15, 35],
        "score_keep": 0.25,
        "score_discard": 0.03,
    },
    "gastrophryne_olivacea": {
        "trill": False,
        "signal_band": [3500, 6500],
        "noise_bands": [[0, 2500], [7000, 9000]],
        "pulse_rate_range": [15, 35],
        "score_keep": 0.25,
        "score_discard": 0.03,
    },
    "lithobates_areolatus": {
        "trill": False,
        "signal_band": [200, 2200],
        "noise_bands": [[0, 150], [2300, 7000]],
        "pulse_rate_range": [15, 35],
        "score_keep": 0.25,
        "score_discard": 0.03,
    },
   "lithobates_blairi": {
        "trill": False,
        "signal_band": [500, 3900],
        "noise_bands": [[200, 450], [4000, 7000]],
        "pulse_rate_range": [15, 35],
        "score_keep": 0.25,
        "score_discard": 0.03,
    },
    "lithobates_catesbeianus": {
        "trill": False,
        "signal_band": [100, 2500],
        "noise_bands": [[0, 750], [2900, 7000]],
        "pulse_rate_range": [15, 35],
        "score_keep": 0.25,
        "score_discard": 0.03,
    },
   "lithobates_clamitans": {
        "trill": False,
        "signal_band": [500, 3900],
        "noise_bands": [[200, 450], [4000, 7000]],
        "pulse_rate_range": [15, 35],
        "score_keep": 0.25,
        "score_discard": 0.03,
    },
   "lithobates_palustris": {
        "trill": False,
        "signal_band": [600, 2500],
        "noise_bands": [[200, 550], [3000, 7000]],
        "pulse_rate_range": [15, 35],
        "score_keep": 0.25,
        "score_discard": 0.03,
    },
   "lithobates_pipiens": {
        "trill": False,
        "signal_band": [300, 3000],
        "noise_bands": [[0, 250], [3500, 5000]],
        "pulse_rate_range": [15, 35],
        "score_keep": 0.25,
        "score_discard": 0.003,
    },
   "lithobates_sphenocephalus": {
        "trill": False,
        "signal_band": [800, 1700],
        "noise_bands": [[300, 750], [1900, 5000]],
        "pulse_rate_range": [15, 35],
        "score_keep": 0.25,
        "score_discard": 0.03,
    },
   "lithobates_sylvaticus": {
        "trill": False,
        "signal_band": [500, 4000],
        "noise_bands": [[100, 450], [4200, 7000]],
        "pulse_rate_range": [15, 35],
        "score_keep": 0.70,
        "score_discard": 0.03,
    },
    "pseudacris_crucifer": {
        "trill": False,
        "signal_band": [2000, 4000],
        "noise_bands": [[300, 1500], [4500, 7000]],
        "pulse_rate_range": [15, 35],
        "score_keep": 0.25,
        "score_discard": 0.04,
    },
   "pseudacris_fouquettei": {
        "trill": True,
        "signal_band": [2200, 4000],
        "noise_bands": [[300, 2000], [4500, 7000]],
        "pulse_rate_range": [10, 35],
        "score_keep": 0.1,
        "score_discard": 0.014,
    },
    "pseudacris_feriarum": {
        "trill": True,
        "signal_band": [2000, 4000],
        "noise_bands": [[300, 1500], [4500, 7000]],
        "pulse_rate_range": [10, 35],
        "score_keep": 0.1,
        "score_discard": 0.014,
    },
    "pseudacris_maculata": {
        "trill": True,
        "signal_band": [2000, 4500],
        "noise_bands": [[300, 1500], [5000, 7000]],
        "pulse_rate_range": [15, 35],
        "score_keep": 0.1,
        "score_discard": 0.014,
    },
    "scaphiopus_holbrookii": {
        "trill": False,
        "signal_band": [500, 3000],
        "noise_bands": [[250, 450], [3500, 5000]],
        "pulse_rate_range": [15, 35],
        "score_keep": 0.25,
        "score_discard": 0.005,
    },
    "spea_bombifrons": {
        "trill": False,
        "signal_band": [600, 1600],
        "noise_bands": [[250, 550], [1700, 5000]],
        "pulse_rate_range": [15, 35],
        "score_keep": 0.25,
        "score_discard": 0.005,
    }
 }
# CURRENT_SPECIES needs to be set in order to build the correct folder structure
CURRENT_SPECIES = "dryophytes_chrysoscelis"

BASE_DIR = Path("data")
species = CURRENT_SPECIES
(BASE_DIR / "downloads" / species).mkdir(parents=True, exist_ok=True)
(BASE_DIR / "snippets" / species / "clips").mkdir(parents=True, exist_ok=True)
(BASE_DIR / "snippets" / species / "confirmed").mkdir(parents=True, exist_ok=True)
(BASE_DIR / "snippets" / species / "all_spectrograms").mkdir(parents=True, exist_ok=True)

# load observations
import pandas as pd


df = pd.read_csv(BASE_DIR / "downloads" / CURRENT_SPECIES / "full_calls.csv")
print(df.columns)

# %%
# download sounds
import requests
import time
from tqdm import tqdm

HEADERS = {"User-Agent": "frognet/0.1 (lfelliott@hotmail.com)"}

def download_sounds(df, species, delay=1.0):
    out_dir = BASE_DIR / "downloads" / species
    for _, row in tqdm(df.iterrows(), total=len(df)):
        url = row["sound_url"]
        if not isinstance(url, str):
            continue
        original_name = url.split("/")[-1].split("?")[0]
        fname = out_dir / f"{row['id']}_{original_name}"
        if fname.exists():
            continue
        try:
            r = requests.get(url, headers=HEADERS, timeout=30)
            r.raise_for_status()
            fname.write_bytes(r.content)
        except Exception as e:
            print(f"Failed {url}: {e}")
        time.sleep(delay)

download_sounds(df, CURRENT_SPECIES)

# %%
# segment audio into 3-second clips
from opensoundscape.audio import Audio

CLIP_DURATION = 3.0

def segment_audio(species):
    in_dir = BASE_DIR / "downloads" / species
    out_dir = BASE_DIR / "snippets" / species / "clips"
    mp3_files = [f for ext in ("*.mp3", "*.mpga", "*.m4a", "*.ogg", "*.flac", "*.wav")
                 for f in in_dir.glob(ext)]
    print(f"Found {len(mp3_files)} files to segment")
    for mp3_path in tqdm(mp3_files):
        obs_id = mp3_path.stem.split("_")[0]
        audio = Audio.from_file(mp3_path)
        duration = audio.duration
        offset = 0.0
        while offset + CLIP_DURATION <= duration:
            out_path = out_dir / f"{obs_id}_{int(offset)}s.wav"
            if not out_path.exists():
                clip = audio.trim(offset, offset + CLIP_DURATION)
                clip.save(out_path)
            offset += CLIP_DURATION

segment_audio(CURRENT_SPECIES)

# %%
# generate spectrograms for all clips
import matplotlib.pyplot as plt
from tqdm import tqdm
from opensoundscape.spectrogram import Spectrogram

def generate_spectrograms(species):
    config = SPECIES_CONFIG[species]
    clips_dir = BASE_DIR / "snippets" / species / "clips"
    spec_dir = BASE_DIR / "snippets" / species / "all_spectrograms"

    freq_min = config["signal_band"][0] - 500
    freq_max = config["signal_band"][1] + 500

    clips = sorted(clips_dir.glob("*.wav"))
    print(f"Generating spectrograms for {len(clips)} clips")

    for clip_path in tqdm(clips):
        out_path = spec_dir / (clip_path.stem + ".png")
        if out_path.exists():
            continue
        audio = Audio.from_file(clip_path)
        spec = Spectrogram.from_audio(audio)

        fig, ax = plt.subplots(figsize=(6, 3))
        ax.imshow(
            spec.spectrogram,
            aspect="auto",
            origin="lower",
            extent=[spec.times[0], spec.times[-1], spec.frequencies[0], spec.frequencies[-1]],
            cmap="inferno",
        )
        ax.set_ylim(freq_min, freq_max)
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Frequency (Hz)")
        ax.set_title(clip_path.stem)
        fig.tight_layout()
        fig.savefig(out_path, dpi=100)
        plt.close(fig)

    print("Done.")

generate_spectrograms(CURRENT_SPECIES)

# %%
# scoring
import numpy as np
from tqdm import tqdm
from opensoundscape.audio import Audio
from opensoundscape.ribbit import ribbit

def score_clips(species):
    config = SPECIES_CONFIG[species]
    score_keep = config["score_keep"]
    score_discard = config["score_discard"]
    clips_dir = BASE_DIR / "snippets" / species / "clips"
    scores_path = BASE_DIR / "snippets" / species / "scores.csv"

    if scores_path.exists():
        scores_df = pd.read_csv(scores_path)
    else:
        scores_df = pd.DataFrame(columns=["file", "score", "status", "reviewed"])

    already_scored = set(scores_df["file"].tolist())
    clips = [f for f in sorted(clips_dir.glob("*.wav")) if f.name not in already_scored]
    print(f"{len(clips)} new clips to score")

    new_rows = []
    for clip_path in tqdm(clips):
        audio = Audio.from_file(clip_path)
        spec = Spectrogram.from_audio(audio)

        if config["trill"]:
            result = ribbit(
                spec,
                pulse_rate_range=config["pulse_rate_range"],
                signal_band=config["signal_band"],
                noise_bands=config["noise_bands"],
                clip_duration=CLIP_DURATION,
                clip_overlap=0,
                final_clip="remainder",
                spec_clip_range=(-200, -20),
            )
            score = float(result["score"].iloc[0]) * 1000 if len(result) > 0 else 0.0
        else:
            amplitude = np.array(spec.net_amplitude(config["signal_band"], config["noise_bands"]))
            score = float(np.mean(amplitude))

        if score >= score_keep:
            status = "keep"
        elif score < score_discard:
            status = "discard"
        else:
            status = "review"
        new_rows.append({"file": clip_path.name, "score": score, "status": status, "reviewed": False})

    if new_rows:
        scores_df = pd.concat([scores_df, pd.DataFrame(new_rows)], ignore_index=True)
        scores_df.to_csv(scores_path, index=False)

    print(scores_df["score"].astype(float).describe(percentiles=[.25, .5, .75, .90, .95, .99]))
    print("\nStatus counts:")
    print(scores_df["status"].value_counts())

score_clips(CURRENT_SPECIES)

# %%
# manual review of borderline clips
import time
from IPython.display import display, Audio as IPAudio, Image as IPImage

def review_clips(species):
    scores_path = BASE_DIR / "snippets" / species / "scores.csv"
    clips_dir = BASE_DIR / "snippets" / species / "clips"
    spec_dir = BASE_DIR / "snippets" / species / "all_spectrograms"

    if not scores_path.exists():
        print("scores.csv not found — run the scoring cell first.")
        return

    scores_df = pd.read_csv(scores_path)
    scores_df["reviewed"] = scores_df["reviewed"].astype(bool)
    to_review = scores_df[(scores_df["status"] == "review") & (~scores_df["reviewed"])]
    total = len(to_review)
    print(f"{total} clips to review")

    for i, (idx, row) in enumerate(to_review.iterrows(), 1):
        clip_path = clips_dir / row["file"]
        spec_path = spec_dir / (Path(row["file"]).stem + ".png")

        display(IPAudio(filename=str(clip_path), autoplay=True))
        if spec_path.exists():
            display(IPImage(filename=str(spec_path)))
        time.sleep(0.2)

        while True:
            decision = input(f"[{i}/{total}] {row['file']} (score: {row['score']:.6f}) | 1=keep 0=discard q=quit: ").strip().lower()
            if decision in ("0", "1", "q"):
                break

        if decision == "q":
            break
        scores_df.at[idx, "status"] = "keep" if decision == "1" else "discard"
        scores_df.at[idx, "reviewed"] = True

    scores_df.to_csv(scores_path, index=False)
    print("Decisions saved.")

review_clips(CURRENT_SPECIES)

# %%
# export confirmed clips
import shutil

def export_confirmed(species):
    scores_path = BASE_DIR / "snippets" / species / "scores.csv"
    clips_dir = BASE_DIR / "snippets" / species / "clips"
    confirmed_dir = BASE_DIR / "snippets" / species / "confirmed"

    scores_df = pd.read_csv(scores_path)
    to_export = scores_df[scores_df["status"] == "keep"]
    print(f"Exporting {len(to_export)} confirmed clips")

    for _, row in to_export.iterrows():
        src = clips_dir / row["file"]
        dst = confirmed_dir / row["file"]
        if src.exists() and not dst.exists():
            shutil.copy2(src, dst)

    print("Done.")

export_confirmed(CURRENT_SPECIES)

# %%
# quick cell
_config = SPECIES_CONFIG[CURRENT_SPECIES]
_score_keep = _config["score_keep"]
_score_discard = _config["score_discard"]
scores_path = BASE_DIR / "snippets" / CURRENT_SPECIES / "scores.csv"
scores_df = pd.read_csv(scores_path)
scores_df["score"] = scores_df["score"].astype(float)

# only re-classify rows not manually reviewed
mask = ~scores_df["reviewed"]
scores_df.loc[mask & (scores_df["score"] >= _score_keep), "status"] = "keep"
scores_df.loc[mask & (scores_df["score"] < _score_discard), "status"] = "discard"
scores_df.loc[mask & (scores_df["score"] >= _score_discard) & (scores_df["score"] < _score_keep), "status"] = "review"

scores_df.to_csv(scores_path, index=False)
print(scores_df["status"].value_counts())
# %%
# quick diagnostic 2
_config = SPECIES_CONFIG[CURRENT_SPECIES]
_score_keep = _config["score_keep"]
_score_discard = _config["score_discard"]
print(f"score_keep={_score_keep}, score_discard={_score_discard}")

scores_df = pd.read_csv(BASE_DIR / "snippets" / CURRENT_SPECIES / "scores.csv")
scores_df["score"] = scores_df["score"].astype(float)
print(f"scores >= {_score_keep}: {(scores_df['score'] >= _score_keep).sum()}")
print(f"scores < {_score_discard}:  {(scores_df['score'] < _score_discard).sum()}")
print(f"scores in between: {((scores_df['score'] >= _score_discard) & (scores_df['score'] < _score_keep)).sum()}")
# %%
# quick diagnostic 3
scores_df = pd.read_csv(BASE_DIR / "snippets" / CURRENT_SPECIES / "scores.csv")                                                                                                      
print(scores_df["status"].value_counts())                                                                                                                                            
print(f"\nUnreviewed 'review' clips: {((scores_df['status'] == 'review') & (~scores_df['reviewed'])).sum()}")   
# %%
# quick diagnostic 4
scores_df = pd.read_csv(BASE_DIR / "snippets" / CURRENT_SPECIES / "scores.csv")                                                                                                      
print(scores_df["status"].value_counts())
# %%
# Check thresholds
scores_df = pd.read_csv(BASE_DIR / "snippets" / CURRENT_SPECIES / "scores.csv")                                                                                                      
scores_df["score"] = scores_df["score"].astype(float)                                                                                                                                
scores_df["reviewed"] = scores_df["reviewed"].astype(bool)                                                                                                                           
                                                                                                                                                                                       
# score distribution by final status
print(scores_df.groupby("status")["score"].describe(percentiles=[.25, .5, .75]))

# of the auto-kept (not manually reviewed), how many kept vs discarded
print("\nAuto-classified (not reviewed):")
print(scores_df[~scores_df["reviewed"]]["status"].value_counts())

# of the manually reviewed, how did they split
print("\nManually reviewed:")
print(scores_df[scores_df["reviewed"]]["status"].value_counts())

# score distributions of manually kept vs discarded
print("\nScore mean by manual decision:")
print(scores_df[scores_df["reviewed"]].groupby("status")["score"].mean())
# %%
# spot-check auto-kept clips
from IPython.display import display, Audio as IPAudio

scores_df = pd.read_csv(BASE_DIR / "snippets" / CURRENT_SPECIES / "scores.csv")
clips_dir = BASE_DIR / "snippets" / CURRENT_SPECIES / "clips"

auto_kept = scores_df[(scores_df["status"] == "keep") & (~scores_df["reviewed"].astype(bool))]
sample = auto_kept.sample(min(10, len(auto_kept)), random_state=42)

for _, row in sample.iterrows():
    print(f"{row['file']} (score: {row['score']:.6f})")
    display(IPAudio(filename=str(clips_dir / row["file"]), autoplay=False))
# %%
# review keep scores
import time                                                                                                                                                                         
from IPython.display import display, Audio as IPAudio, Image as IPImage
scores_df = pd.read_csv(BASE_DIR / "snippets" / CURRENT_SPECIES / "scores.csv")
scores_df["reviewed"] = scores_df["reviewed"].astype(bool)
clips_dir = BASE_DIR / "snippets" / CURRENT_SPECIES / "clips"
spec_dir = BASE_DIR / "snippets" / CURRENT_SPECIES / "all_spectrograms"

kept = scores_df[scores_df["status"] == "keep"]
sample = kept.sample(max(1, int(len(kept) * 1.0)), random_state=42)
total = len(sample)
print(f"Reviewing {total} of {len(kept)} keep clips (20%)")

for i, (idx, row) in enumerate(sample.iterrows(), 1):
    clip_path = clips_dir / row["file"]
    spec_path = spec_dir / (Path(row["file"]).stem + ".png")
    display(IPAudio(filename=str(clip_path), autoplay=True))
    if spec_path.exists():
        display(IPImage(filename=str(spec_path)))
    time.sleep(0.2)

    while True:
        decision = input(f"[{i}/{total}] {row['file']} (score: {row['score']:.6f}) | 1=keep 0=discard q=quit: ").strip().lower()
        if decision in ("0", "1", "q"):
            break

    if decision == "q":
        break
    scores_df.at[idx, "status"] = "keep" if decision == "1" else "discard"
    scores_df.at[idx, "reviewed"] = True

scores_df.to_csv(BASE_DIR / "snippets" / CURRENT_SPECIES / "scores.csv", index=False)
print("Decisions saved.")


# %%
# noise review — mark discarded clips across all species as frog-free or not
import random
import time
import pandas as pd
from pathlib import Path
from IPython.display import display, Audio as IPAudio, Image as IPImage

def review_noise_clips():
    candidates = []
    scores_dfs = {}

    for species in SPECIES_CONFIG:
        scores_path = BASE_DIR / "snippets" / species / "scores.csv"
        if not scores_path.exists():
            continue
        df = pd.read_csv(scores_path)
        df["reviewed"] = df["reviewed"].astype(bool)
        if "noise_ok" not in df.columns:
            df["noise_ok"] = pd.NA
        df["noise_ok"] = df["noise_ok"].astype(object)
        scores_dfs[species] = (scores_path, df)

        mask = (df["status"] == "discard") & df["reviewed"] & df["noise_ok"].isna()
        for idx, row in df[mask].iterrows():
            candidates.append((species, idx, row["file"]))

    random.shuffle(candidates)
    total = len(candidates)
    print(f"{total} discarded clips remaining to noise-review")

    for i, (species, idx, fname) in enumerate(candidates, 1):
        clips_dir = BASE_DIR / "snippets" / species / "clips"
        spec_dir = BASE_DIR / "snippets" / species / "all_spectrograms"
        clip_path = clips_dir / fname
        spec_path = spec_dir / (Path(fname).stem + ".png")

        print(f"\n[{i}/{total}] {species} — {fname}")
        display(IPAudio(filename=str(clip_path), autoplay=True))
        if spec_path.exists():
            display(IPImage(filename=str(spec_path)))
        time.sleep(0.2)

        while True:
            decision = input("Frog-free? 1=yes  0=no (has frogs)  q=quit: ").strip().lower()
            if decision in ("1", "0", "q"):
                break

        if decision == "q":
            break

        scores_path, df = scores_dfs[species]
        df.at[idx, "noise_ok"] = (decision == "1")
        df.to_csv(scores_path, index=False)

    approved = sum(
        (df["noise_ok"] == True).sum()
        for _, (_, df) in scores_dfs.items()
    )
    reviewed = sum(
        (~df["noise_ok"].isna()).sum()
        for _, (_, df) in scores_dfs.items()
    )
    print(f"\nDone. {reviewed} clips noise-reviewed so far, {approved} approved as frog-free.")

review_noise_clips()

# %%
# export frog-free noise clips to birdnet training folder
import shutil
import pandas as pd
from pathlib import Path

def export_noise_clips():
    noise_dir = BASE_DIR / "birdnet_training" / "noise"
    noise_dir.mkdir(parents=True, exist_ok=True)

    exported = 0
    for species in SPECIES_CONFIG:
        scores_path = BASE_DIR / "snippets" / species / "scores.csv"
        if not scores_path.exists():
            continue
        df = pd.read_csv(scores_path)
        if "noise_ok" not in df.columns:
            continue
        approved = df[df["noise_ok"] == True]
        clips_dir = BASE_DIR / "snippets" / species / "clips"
        for _, row in approved.iterrows():
            src = clips_dir / row["file"]
            dst = noise_dir / f"{species}__{row['file']}"
            if src.exists() and not dst.exists():
                shutil.copy2(src, dst)
                exported += 1

    total = len(list(noise_dir.glob("*.wav")))
    print(f"Exported {exported} new clips. Noise folder total: {total}")

export_noise_clips()

# %%
# confirmed clip counts per species
rows = []
for sp in SPECIES_CONFIG:
    confirmed_dir = BASE_DIR / "snippets" / sp / "confirmed"
    count = len(list(confirmed_dir.glob("*.wav"))) if confirmed_dir.exists() else 0
    rows.append({"species": sp, "confirmed_clips": count})

summary = pd.DataFrame(rows).set_index("species")
total = summary["confirmed_clips"].sum()
print(summary.to_string())
print(f"\nTotal: {total}")

# %%
# segment extra_nonfrog WAVs into 3s clips and initialize scores.csv
import pandas as pd
from pathlib import Path
from tqdm import tqdm
from opensoundscape.audio import Audio

BASE_DIR = Path("data")
EXTRA_SRC_DIR = Path("data/extra_nonfrog")
EXTRA_CLIPS_DIR = BASE_DIR / "snippets" / "extra_nonfrog" / "clips"
EXTRA_SPEC_DIR = BASE_DIR / "snippets" / "extra_nonfrog" / "all_spectrograms"
EXTRA_SCORES_PATH = BASE_DIR / "snippets" / "extra_nonfrog" / "scores.csv"
CLIP_DURATION = 3.0

EXTRA_CLIPS_DIR.mkdir(parents=True, exist_ok=True)
EXTRA_SPEC_DIR.mkdir(parents=True, exist_ok=True)

wav_files = sorted(EXTRA_SRC_DIR.glob("*.wav"))
print(f"Found {len(wav_files)} source files")

for wav_path in wav_files:
    stem = wav_path.stem
    audio = Audio.from_file(wav_path)
    offset = 0.0
    while offset + CLIP_DURATION <= audio.duration:
        out_path = EXTRA_CLIPS_DIR / f"{stem}_{int(offset)}s.wav"
        if not out_path.exists():
            audio.trim(offset, offset + CLIP_DURATION).save(out_path)
        offset += CLIP_DURATION

all_clips = sorted(f.name for f in EXTRA_CLIPS_DIR.glob("*.wav"))
print(f"{len(all_clips)} total clips")

existing_files = set()
if EXTRA_SCORES_PATH.exists():
    existing_df = pd.read_csv(EXTRA_SCORES_PATH)
    existing_files = set(existing_df["file"])
else:
    existing_df = pd.DataFrame(columns=["file", "noise_ok"])

new_rows = [{"file": f, "noise_ok": pd.NA} for f in all_clips if f not in existing_files]
if new_rows:
    pd.concat([existing_df, pd.DataFrame(new_rows)], ignore_index=True).to_csv(EXTRA_SCORES_PATH, index=False)
    print(f"Added {len(new_rows)} rows to scores.csv")
else:
    print("scores.csv already up to date")

# %%
# generate spectrograms for extra_nonfrog clips
import matplotlib.pyplot as plt
from tqdm import tqdm
from pathlib import Path
from opensoundscape.audio import Audio
from opensoundscape.spectrogram import Spectrogram

EXTRA_CLIPS_DIR = Path("data/snippets/extra_nonfrog/clips")
EXTRA_SPEC_DIR = Path("data/snippets/extra_nonfrog/all_spectrograms")

clips = sorted(EXTRA_CLIPS_DIR.glob("*.wav"))
print(f"Generating spectrograms for {len(clips)} clips")

for clip_path in tqdm(clips):
    out_path = EXTRA_SPEC_DIR / (clip_path.stem + ".png")
    if out_path.exists():
        continue
    audio = Audio.from_file(clip_path)
    spec = Spectrogram.from_audio(audio)
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.imshow(
        spec.spectrogram,
        aspect="auto",
        origin="lower",
        extent=[spec.times[0], spec.times[-1], spec.frequencies[0], spec.frequencies[-1]],
        cmap="inferno",
    )
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Frequency (Hz)")
    ax.set_title(clip_path.stem)
    fig.tight_layout()
    fig.savefig(out_path, dpi=100)
    plt.close(fig)

print("Done.")

# %%
# review extra_nonfrog clips for noise training
import time
import pandas as pd
from pathlib import Path
from IPython.display import display, Audio as IPAudio, Image as IPImage

EXTRA_CLIPS_DIR = Path("data/snippets/extra_nonfrog/clips")
EXTRA_SPEC_DIR = Path("data/snippets/extra_nonfrog/all_spectrograms")
EXTRA_SCORES_PATH = Path("data/snippets/extra_nonfrog/scores.csv")

df = pd.read_csv(EXTRA_SCORES_PATH)
df["noise_ok"] = df["noise_ok"].astype(object)
pending = df[df["noise_ok"].isna()]
total = len(pending)
print(f"{total} clips to review")

for i, (idx, row) in enumerate(pending.iterrows(), 1):
    clip_path = EXTRA_CLIPS_DIR / row["file"]
    spec_path = EXTRA_SPEC_DIR / (Path(row["file"]).stem + ".png")

    print(f"\n[{i}/{total}] {row['file']}")
    display(IPAudio(filename=str(clip_path), autoplay=True))
    if spec_path.exists():
        display(IPImage(filename=str(spec_path)))
    time.sleep(0.2)

    while True:
        decision = input("Add to noise? 1=yes  0=no  q=quit: ").strip().lower()
        if decision in ("1", "0", "q"):
            break

    if decision == "q":
        break

    df.at[idx, "noise_ok"] = (decision == "1")
    df.to_csv(EXTRA_SCORES_PATH, index=False)

approved = (df["noise_ok"] == True).sum()
reviewed = (~df["noise_ok"].isna()).sum()
print(f"\nDone. {reviewed} reviewed, {approved} approved for noise training.")

# %%
# export approved extra_nonfrog clips to birdnet training noise folder
import shutil
import pandas as pd
from pathlib import Path

EXTRA_CLIPS_DIR = Path("data/snippets/extra_nonfrog/clips")
EXTRA_SCORES_PATH = Path("data/snippets/extra_nonfrog/scores.csv")
NOISE_DIR = Path("data/birdnet_training/noise")
NOISE_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(EXTRA_SCORES_PATH)
exported = 0
for _, row in df[df["noise_ok"] == True].iterrows():
    src = EXTRA_CLIPS_DIR / row["file"]
    dst = NOISE_DIR / f"extra_nonfrog__{row['file']}"
    if src.exists() and not dst.exists():
        shutil.copy2(src, dst)
        exported += 1

total = len(list(NOISE_DIR.glob("*.wav")))
print(f"Exported {exported} new clips. Noise folder total: {total}")
# %%
