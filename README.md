# NFL Game Excitement Index

Term project for DSCI 521 - Data Analysis and Interpretation (Summer 2026), Group 3.

**Question:** can the entertainment value of an NFL game be measured, explained, and predicted before kickoff?

**Answer:** the first two, yes. The third, essentially no. Across six test seasons, thirteen pre-game features predict whether a game will be a thriller at ROC-AUC 0.542, and the closing point spread alone does just as well (0.546). Meanwhile a model of what *wins* games reaches AUC 0.811 on a season it never saw. NFL outcomes are legible, but NFL entertainment is not, or at least not in advance.

## Contents

| Path | Description |
|---|---|
| `DSCI_521_Group3_Final.ipynb` | Final report |
| `DSCI_521_Group3.ipynb` | Phase 1 scoping submission (originally Colab but now runs locally) |
| `src/data.py` | nflverse loaders, parquet cache under `data/cache/` |
| `src/plots.py` | `show_wp_graph`, `show_excitement_chart` |
| `src/main.py` | Standalone script entry point |

## Setup

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m ipykernel install --user --name dsci521-nfl
.venv/bin/jupyter lab      # select the "Python (dsci521-nfl)" kernel
```

Run the notebooks from the repository root — `src/` and the `data/` cache are resolved relative to it.

## Data

Play-by-play and schedules for **2016-2025** (regular season and playoffs) from
[nflverse](https://nflreadr.nflverse.com/) via the
[`nflreadpy`](https://nflreadpy.nflverse.com/) package: 2,761 games, 484,254 plays.

No data is committed. The first run of either notebook downloads what it needs into `data/` (git-ignored) and caches it; the final report goes from an empty cache to fully executed in about 30 seconds and ~64 MB. The Phase 1 notebook additionally caches two [nflscrapR](https://github.com/ryurko/nflscrapR-data) CSVs, which is the dataset that phase used.

Both notebooks are committed with their outputs so the report is readable without running anything. Every model is seeded so that results are deterministic.
