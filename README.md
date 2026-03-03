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
2. **Load observations** — reads `data/downloads/<species>/full_calls.csv` (exported from iNaturalist using a query for RG observations of the species with sound and renamed to full_calls.csv)
3. **Download sounds** — fetches audio files from iNaturalist observation URLs
4. **Segment audio** — splits each recording into 3-second WAV clips
5. **Generate spectrograms** — saves a PNG spectrogram for each clip
6. **Score clips** — auto-classifies clips as `keep`, `discard`, or `review` using signal band amplitude or RIBBIT (for trill species)
7. **Manual review** — plays borderline clips for human keep/discard decisions
8. **Export confirmed** — copies all `keep` clips to `data/snippets/<species>/confirmed/`
