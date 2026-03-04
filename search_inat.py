#!/usr/bin/env python3
"""
Search iNaturalist for Pseudacris observations (excluding P. crucifer and P. maculata)
with sound recordings that mention "aggressive" or "territorial" in
notes or comments, from Missouri and surrounding states.

Results are saved to data/pseudacris_aggressive.csv.
"""

import csv
import time
from pathlib import Path

import requests

BASE_URL = "https://api.inaturalist.org/v1"
HEADERS = {"User-Agent": "frognet/0.1 (lfelliott@hotmail.com)"}

TAXON_NAME = "Pseudacris"
EXCLUDE_TAXA = {"Pseudacris maculata", "Pseudacris crucifer"}
PLACE_IDS = [3, 12, 25, 28, 35, 36]
KEYWORDS = ["aggressive", "territorial"]
BATCH_SIZE = 30  # IDs per request when fetching details

OUT_PATH = Path("data/pseudacris_aggressive.csv")


def get(url, params=None):
    """GET with automatic retry on 429 rate-limit responses."""
    while True:
        r = requests.get(url, params=params, headers=HEADERS, timeout=30)
        if r.status_code == 429:
            wait = int(r.headers.get("Retry-After", 60))
            print(f"  Rate limited — waiting {wait}s")
            time.sleep(wait)
            continue
        r.raise_for_status()
        return r


def fetch_all_observations():
    """
    Fetch all RG Pseudacris crucifer observations with sound from target states.
    Uses id_above pagination to support result sets beyond the 10k page limit.
    """
    params = {
        "taxon_name": TAXON_NAME,
        "quality_grade": "research,needs_id",
        "place_id": ",".join(str(p) for p in PLACE_IDS),
        "sounds": "true",
        "per_page": 200,
        "order_by": "id",
        "order": "asc",
    }

    results = []
    while True:
        if results:
            params["id_above"] = results[-1]["id"]
        data = get(f"{BASE_URL}/observations", params).json()
        batch = data["results"]
        if not batch:
            break
        results.extend(batch)
        print(f"  Fetched {len(results)} (batch: {len(batch)})")
        time.sleep(1)

    return results


def fetch_comments_for(observations):
    """
    Fetch full observation details (including comments) for a list of observations.
    Batches IDs into single requests per iNat recommended practices.
    Returns a dict of {obs_id: [comments]}.
    """
    ids = [obs["id"] for obs in observations]
    comments_by_id = {}

    for i in range(0, len(ids), BATCH_SIZE):
        batch = ids[i:i + BATCH_SIZE]
        params = {
            "id": ",".join(str(x) for x in batch),
            "per_page": len(batch),
        }
        data = get(f"{BASE_URL}/observations", params).json()
        for obs in data["results"]:
            comments_by_id[obs["id"]] = obs.get("comments", [])
        time.sleep(1)

    return comments_by_id


def has_keyword(text):
    if not text:
        return False
    lower = text.lower()
    return any(kw in lower for kw in KEYWORDS)


def main():
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    print("Fetching observations...")
    observations = fetch_all_observations()
    observations = [
        obs for obs in observations
        if obs.get("taxon", {}).get("name") not in EXCLUDE_TAXA
    ]
    print(f"Total observations after exclusions: {len(observations)}\n")

    # Check descriptions locally — no extra API calls needed
    desc_matches = {obs["id"] for obs in observations if has_keyword(obs.get("description"))}

    # Batch-fetch comments only for observations that have them
    with_comments = [obs for obs in observations if obs.get("comments_count", 0) > 0]
    comment_matches = set()
    if with_comments:
        print(f"Fetching comments for {len(with_comments)} observations (batched)...")
        comments_map = fetch_comments_for(with_comments)
        comment_matches = {
            obs_id
            for obs_id, comments in comments_map.items()
            if any(has_keyword(c.get("body")) for c in comments)
        }

    # Combine and report
    obs_by_id = {obs["id"]: obs for obs in observations}
    matched_ids = desc_matches | comment_matches

    matches = []
    for obs_id in sorted(matched_ids):
        obs = obs_by_id[obs_id]
        in_desc = obs_id in desc_matches
        in_comments = obs_id in comment_matches
        matched_in = "both" if (in_desc and in_comments) else ("description" if in_desc else "comments")

        sound_urls = [s["file_url"] for s in obs.get("sounds", [])]
        matches.append({
            "id": obs_id,
            "url": obs.get("uri", ""),
            "observed_on": obs.get("observed_on", ""),
            "place_guess": obs.get("place_guess", ""),
            "matched_in": matched_in,
            "description": (obs.get("description") or "").replace("\n", " "),
            "sound_url": sound_urls[0] if sound_urls else "",
        })
        print(f"  Match [{matched_in}]: {obs_id} — {obs.get('place_guess', '')}")

    print(f"\nFound {len(matches)} matching observations")

    if matches:
        with open(OUT_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=matches[0].keys())
            writer.writeheader()
            writer.writerows(matches)
        print(f"Saved to {OUT_PATH}")
    else:
        print("No matches found.")


if __name__ == "__main__":
    main()
