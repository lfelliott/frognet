# %%
# setup - species config and directories
from pathlib import Path

SPECIES_CONFIG = {
#    "acris_blanchardi": {
#        "trill": False,
#        "signal_band": [2500, 4400],
#        "noise_bands": [[1000, 2000], [4600, 6000]],
#    },
#    "dryophytes_chrysoscelis": {
#        "trill": False,
#        "signal_band": [2500, 4500],
#        "noise_bands": [[1000, 2000], [4600, 6000]],
#        "pulse_rate_range": [15, 35],
#    },
    "dryophytes_versicolor": {
        "trill": False,
        "signal_band": [800, 3500],
        "noise_bands": [[300, 7500], [4000, 6000]],
        "pulse_rate_range": [15, 35],
        "score_keep": 0.25,
        "score_discard": 0.07,
    },
    "pseudacris_maculata": {
        "trill": True,
        "signal_band": [2000, 4500],
        "noise_bands": [[300, 1500], [5000, 7000]],
        "pulse_rate_range": [15, 35],
        "score_keep": 0.0001,
        "score_discard": 0.000014,
    },
   "pseudacris_fouquettei": {
        "trill": True,
        "signal_band": [2000, 4500],
        "noise_bands": [[300, 1500], [5000, 7000]],
        "pulse_rate_range": [15, 35],
        "score_keep": 0.0001,
        "score_discard": 0.000014,
    },
    "pseudacris_crucifer": {
        "trill": False,
        "signal_band": [2000, 4000],
        "noise_bands": [[300, 1500], [4500, 7000]],
        "pulse_rate_range": [15, 35],
        "score_keep": 0.25,
        "score_discard": 0.07,
    },
}
# CURRENT_SPECIES needs to be set in order to build the correct folder structure
CURRENT_SPECIES = "pseudacris_crucifer"

BASE_DIR = Path("data")
species = CURRENT_SPECIES
(BASE_DIR / "downloads" / species).mkdir(parents=True, exist_ok=True)
(BASE_DIR / "snippets" / species / "clips").mkdir(parents=True, exist_ok=True)
(BASE_DIR / "snippets" / species / "confirmed").mkdir(parents=True, exist_ok=True)
(BASE_DIR / "snippets" / species / "all_spectrograms").mkdir(parents=True, exist_ok=True)

# %%
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
    mp3_files = [f for ext in ("*.mp3", "*.m4a", "*.ogg", "*.flac", "*.wav")
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
            score = float(result["score"].iloc[0]) if len(result) > 0 else 0.0
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
