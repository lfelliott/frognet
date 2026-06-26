# frognet

This project was initiated to attempt to replicate the results of BirdNET, but with frogs in Missouri. We've only coded the portion to obtain calls from iNaturalist, split them into 3 second samples and manually review them for use. That code resides in `frog_calls_begin.py` and is set up to run in individual cells in a Jupyter notebook. Cells at the end are for diagnostic purposes and will go away as the project nears completion.

## Setup

Requires Python 3.12+. Install dependencies with:

```bash
pip install .
```

Then launch Jupyter and open `frog_calls_begin.py` as a notebook (e.g. via the Jupytext extension or by converting it first).

## Workflow

Run the cells in order for each species:

1. **Setup** — configure `CURRENT_SPECIES` and create the `data/` directory structure
2. **Load observations** — reads `data/downloads/<species>/full_calls.csv` (exported from iNaturalist using a query for RG observations of the species with sound within Missouri, or surrounding states if Missouri doesn't have enough observation, and renamed to full_calls.csv)
3. **Download sounds** — fetches audio files from iNaturalist observation URLs
4. **Segment audio** — splits each recording into 3-second WAV clips
5. **Generate spectrograms** — saves a PNG spectrogram for each clip
6. **Score clips** — auto-classifies clips as `keep`, `discard`, or `review` using signal band amplitude or RIBBIT (for trill species)
7. **Manual review** — plays borderline clips for human keep/discard decisions
8. **Export confirmed** — copies all `keep` clips to `data/snippets/<species>/confirmed/`

## Frog Classifier

`data/frog_classifier.tflite` is a custom BirdNET classifier trained on the confirmed clips listed below. It recognizes 24 Missouri anuran species and is intended to be used as a drop-in replacement for BirdNET's default classifier when analyzing field recordings for frogs.

Companion files:
- `data/frog_classifier_Labels.txt` — species list in classifier order
- `data/frog_classifier_Params.csv` — BirdNET training parameters
- `data/frog_classifier_sample_counts.csv` — per-species confirmed clip counts used during training

To run the classifier on a folder of WAV files:

```bash
./run_frognet_model_on_files_in_folder data/field_recordings/<folder>
```

This calls `birdnet-analyze` with settings tuned for frog calls (100–7000 Hz, min confidence 0.1, combined CSV output). Results are written to the same folder as `BirdNET_CombinedTable.csv` and per-file `.csv` files.

## Spectrogram Tool

`spectrogram_best_detections.py` reads the `BirdNET_CombinedTable.csv` produced by the classifier and generates one spectrogram PNG per detected species — the clip with the highest confidence score. Each image is labeled with the source filename, species name, and confidence value.

```bash
python spectrogram_best_detections.py data/field_recordings/<folder>
```

PNGs are written to the same folder as the CSV.

## Training Data — Confirmed Clips per Species

10,651 confirmed 3-second clips across 24 species, all sourced from iNaturalist Research Grade observations.

| Species | Confirmed clips |
|---|---:|
| Acris blanchardi | 303 |
| Anaxyrus americanus | 552 |
| Anaxyrus cognatus | 117 |
| Anaxyrus fowleri | 383 |
| Anaxyrus woodhousii | 168 |
| Dryophytes chrysoscelis | 286 |
| Dryophytes cinereus | 203 |
| Dryophytes versicolor | 636 |
| Gastrophryne carolinensis | 245 |
| Gastrophryne olivacea | 841 |
| Lithobates areolatus | 210 |
| Lithobates blairi | 140 |
| Lithobates catesbeianus | 326 |
| Lithobates clamitans | 286 |
| Lithobates palustris | 148 |
| Lithobates pipiens | 193 |
| Lithobates sphenocephalus | 583 |
| Lithobates sylvaticus | 986 |
| Pseudacris crucifer | 848 |
| Pseudacris feriarum | 1,419 |
| Pseudacris fouquettei | 893 |
| Pseudacris maculata | 603 |
| Scaphiopus holbrookii | 215 |
| Spea bombifrons | 67 |
| **Total** | **10,651** |
