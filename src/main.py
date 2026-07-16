from data import game_data, game_pbp_data, schedule_data, pbp_data
from plots import show_wp_graph, show_excitement_chart

# Games with no play-by-play data: 1999_01_BAL_STL, 2000_03_SD_KC, 2000_06_BUF_MIA
SEASON = 2025
HOME_TEAM = "PHI"
AWAY_TEAM = "DAL"
GAME_TYPE = "REG"

game = game_data(SEASON, HOME_TEAM, AWAY_TEAM, GAME_TYPE)
plays = game_pbp_data(SEASON, game["game_id"])
show_wp_graph(game, plays)

all_games = schedule_data(SEASON)
all_plays = pbp_data(SEASON)
show_excitement_chart(all_games, all_plays)