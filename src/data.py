"""Loaders for the nflverse play-by-play and schedule data.

Every nflreadpy call goes through an on-disk parquet cache under `data/cache/`.
A season of play-by-play is a ~20 MB download, so without the cache each kernel
restart would re-fetch hundreds of megabytes.
"""

from pathlib import Path

import nflreadpy as nfl
import pandas as pd

# Anchored on the repo root, not the working directory, so the cache is shared
# whether this module is imported from a notebook at the root or from src/.
CACHE_DIR = Path(__file__).resolve().parent.parent / "data" / "cache"

# Play-by-play columns the project actually uses. The full nflverse table is 372
# columns wide; narrowing it here is what keeps the cached parquet small and the
# notebook's memory footprint reasonable across ten seasons.
PLAY_COLS = [
    # identity / situation
    "play_id", "game_id", "season", "week", "posteam", "defteam", "posteam_type",
    "drive", "fixed_drive", "fixed_drive_result", "yardline_100",
    "qtr", "quarter_seconds_remaining", "game_seconds_remaining", "half_seconds_remaining",
    "down", "ydstogo", "goal_to_go", "play_type", "desc",
    # score state
    "total_home_score", "total_away_score", "score_differential", "posteam_score",
    # value models
    "ep", "epa", "qb_epa", "total_home_epa", "total_away_epa", "success",
    "wp", "def_wp", "home_wp", "away_wp", "wpa", "vegas_wp", "vegas_wpa",
    # events
    "yards_gained", "touchdown", "interception", "fumble_lost", "penalty",
    "penalty_yards", "third_down_converted", "fourth_down_converted",
    "field_goal_result", "sack", "pass_attempt", "rush_attempt",
]

# Schedule columns. Everything from `spread_line` down is pre-game context the
# nflscrapR data used in Phase 1 simply did not have.
GAME_COLS = [
    "game_id", "season", "week", "game_type",
    "home_team", "away_team", "home_score", "away_score", "result", "total", "overtime",
    "gameday", "weekday", "gametime", "location", "stadium", "roof", "surface",
    "temp", "wind", "div_game", "home_rest", "away_rest",
    "spread_line", "total_line", "home_moneyline", "away_moneyline",
]


def _cached(kind: str, season: int, fetch, columns: list[str]) -> pd.DataFrame:
    """Return one season of `kind`, downloading and caching it on first use."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    path = CACHE_DIR / f"{kind}_{season}.parquet"

    if path.exists():
        return pd.read_parquet(path)

    frame = fetch(season).to_pandas()
    # nflverse occasionally adds or renames columns between releases; keep what
    # is actually there rather than raising a KeyError on the whole season.
    keep = [c for c in columns if c in frame.columns]
    missing = [c for c in columns if c not in frame.columns]
    if missing:
        print(f"  note: {kind} {season} is missing {missing}")
    frame = frame[keep]
    frame.to_parquet(path, index=False)
    return frame


def schedule_data(season: int) -> pd.DataFrame:
    """One season of games, with pre-game context (lines, rest, weather, venue)."""
    return _cached("schedules", season, nfl.load_schedules, GAME_COLS)


def pbp_data(season: int) -> pd.DataFrame:
    """One season of plays, narrowed to `PLAY_COLS`."""
    return _cached("pbp", season, nfl.load_pbp, PLAY_COLS)


def load_schedules_seasons(seasons: list[int], verbose: bool = True) -> pd.DataFrame:
    """Concatenate `schedule_data` across seasons."""
    frames = []
    for season in seasons:
        if verbose:
            print(f"schedules {season} ...", end=" ", flush=True)
        frame = schedule_data(season)
        if verbose:
            print(f"{len(frame):,} games")
        frames.append(frame)
    return pd.concat(frames, ignore_index=True)


def load_pbp_seasons(seasons: list[int], verbose: bool = True) -> pd.DataFrame:
    """Concatenate `pbp_data` across seasons."""
    frames = []
    for season in seasons:
        if verbose:
            print(f"pbp {season} ...", end=" ", flush=True)
        frame = pbp_data(season)
        if verbose:
            print(f"{len(frame):,} plays")
        frames.append(frame)
    return pd.concat(frames, ignore_index=True)


def game_data(season: int, home_team: str, away_team: str, game_type: str) -> pd.Series:
    games = schedule_data(season)

    game = games[
        (games["home_team"] == home_team) &
        (games["away_team"] == away_team) &
        (games["game_type"] == game_type)
    ]

    if game.empty:
        raise ValueError(f"No {game_type} {away_team} @ {home_team} game in {season}.")

    return game.iloc[0]


def game_pbp_data(season: int, game_id: str) -> pd.DataFrame:
    plays = pbp_data(season)
    return plays[plays["game_id"] == game_id]
