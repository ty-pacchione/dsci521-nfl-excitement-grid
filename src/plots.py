import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def show_wp_graph(game: pd.Series, plays: pd.DataFrame) -> None:
    season = game["season"]
    week = game["week"]
    game_type = game["game_type"]
    home_team = game["home_team"]
    away_team = game["away_team"]
    
    match game_type:
        case "REG":
            week = f"Week {week}"
        case "WC":
            week = "Wild Card Round"
        case "DIV":
            week = "Divisional Round"
        case "CON":
            week = "Conference Championship Round"
        case "SB":
            week = "Super Bowl"
        case _:
            raise ValueError(f"Unknown game type: {game_type}")

    plays = plays.sort_values(by=["qtr", "quarter_seconds_remaining"], ascending=[True, False])
    short_overtime = (season >= 2017) & (game_type == "REG") & (plays["qtr"] == 5)
    quarter_length = np.where(short_overtime, 600, 900)
    seconds_elapsed = (plays["qtr"] - 1) * 900 + (quarter_length - plays["quarter_seconds_remaining"])

    plt.figure(figsize=(15, 8))
    plt.plot(seconds_elapsed, plays["away_wp"], linewidth=2)
    plt.ylabel(f"{away_team} Win Probability")
    plt.title(f"{away_team} @ {home_team} ({season} {week})")

    last_quarter = int(max(plays["qtr"]))
    last_second = int(max(seconds_elapsed))

    plt.xlim(0, last_second)
    ticks = [x * 900 for x in range(last_quarter)] + [last_second]
    labels = ["Q1", "Q2", "Q3", "Q4", "OT", "2OT"][:last_quarter] + ["Final"]
    plt.xticks(ticks, labels)
    for i in range(last_quarter - 1):
        plt.axvline((i + 1) * 900, color="gray", linestyle="--", linewidth=1)

    plt.ylim(0, 1)
    plt.yticks(
        [0, 0.25, 0.5, 0.75, 1.0],
        ["0%", "25%", "50%", "75%", "100%"]
    )
    plt.axhline(0.5, color="gray", linestyle="--", linewidth=1)

    plt.grid(alpha=0.5)
    plt.show()

def show_excitement_chart(games: pd.DataFrame, plays: pd.DataFrame) -> None:
    season = games.iloc[0]["season"]

    excitement = (
        plays
        .assign(abs_wpa=plays["wpa"].abs())
        .groupby("game_id", as_index=False)
        .agg(total_abs_wpa=("abs_wpa", "sum"))
    )

    games_wexc = games.merge(excitement, on="game_id", how="left")
    games_wexc = games_wexc.sort_values(["week", "game_id"])
    games_wexc["week_index"] = games_wexc.groupby("week").cumcount()
    games_wexc["label"] = (games_wexc["away_team"] + '@' + games_wexc["home_team"])

    value_matrix = games_wexc.pivot(index="week_index", columns="week", values="total_abs_wpa")
    label_matrix = games_wexc.pivot(index="week_index", columns="week", values="label")

    fig, ax = plt.subplots(figsize=(15, 8))
    im = ax.imshow(value_matrix.values, cmap="RdYlBu_r", aspect="auto", vmin=0, vmax=12)

    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label("Total Absolute WPA")

    playoff_week_labels = ['WC', 'Div', 'Conf', 'SB']
    xtick_labels = [str(w) for w in value_matrix.columns]
    xtick_labels[-4:] = playoff_week_labels

    ax.set_xticks(range(len(value_matrix.columns)))
    ax.set_xticklabels(xtick_labels)
    ax.set_xlabel("Week")

    ax.set_yticks([])
    ax.set_ylabel("")

    for i in range(value_matrix.shape[0]):
        for j in range(value_matrix.shape[1]):
            val = value_matrix.values[i, j]
            if not np.isnan(val):
                ax.text(
                    j, i, label_matrix.values[i, j],
                    ha="center", va="center",
                    fontsize=6, color="black"
                )

    ax.set_title(f"Excitement Scores ({season} NFL Season)")
    plt.tight_layout()
    plt.show()