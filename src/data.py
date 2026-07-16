import nflreadpy as nfl
import pandas as pd

def schedule_data(season: int) -> pd.DataFrame:
    games = nfl.load_schedules(season).to_pandas()
    game_cols = [
        "game_id", "season", "week", "game_type",
        "home_team", "away_team",
        "home_score", "away_score", "overtime",
        # "home_rest",  "away_rest",
        # "home_moneyline", "away_moneyline", "spread_line",
    ]
    return games[game_cols]

def pbp_data(season: int) -> pd.DataFrame:
    plays = nfl.load_pbp(season).to_pandas()
    play_cols = [
        "play_id", "game_id",
        "posteam_type", "drive", "yardline_100",
        "qtr", "quarter_seconds_remaining", "game_seconds_remaining",
        "down", "ydstogo", "goal_to_go",
        "total_home_score", "total_away_score",
        "ep", "epa", "total_home_epa", "total_away_epa",
        "home_wp", "away_wp", "wpa", "vegas_wpa",
        # "desc", "play_type", "sp",
    ]
    return plays[play_cols]

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