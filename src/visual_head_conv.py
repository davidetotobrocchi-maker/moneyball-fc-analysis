import json
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from adjustText import adjust_text   # <--- serve per evitare sovrapposizioni

LINEUPS_DIR = Path("data/lineups")
SHOTS_FILE = Path("data/shots_clean.csv")


def load_center_forward_players():
    cf_positions = {
        "Centre Forward", "Center Forward", "Central Forward",
        "Forward", "Striker"
    }

    center_forwards = set()

    for file in LINEUPS_DIR.glob("*.json"):
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        for team in data:
            for player in team.get("lineup", []):
                name = player.get("player_name")
                pos_list = player.get("positions", [])
                extracted = []

                for pos in pos_list:
                    if isinstance(pos, dict):
                        if "name" in pos:
                            extracted.append(pos["name"])
                        elif "position" in pos:
                            extracted.append(pos["position"])

                if any(p in cf_positions for p in extracted):
                    center_forwards.add(name)

    return center_forwards


def plot_top10_header_scorers_cf():

    df = pd.read_csv(SHOTS_FILE)
    cf_players = load_center_forward_players()

    headers_cf = df[
        (df["shot.body_part.name"] == "Head") &
        (df["player.name"].isin(cf_players))
    ].copy()

    stats = headers_cf.groupby("player.name").agg(
        header_shots=("player.name", "count"),
        header_goals=("is_goal", "sum")
    ).reset_index()

    stats["conversion_rate"] = stats["header_goals"] / stats["header_shots"]

    top10 = stats.sort_values("header_goals", ascending=False).head(10)

    plt.figure(figsize=(14, 8))

    plt.scatter(
        top10["header_shots"],
        top10["conversion_rate"],
        s=top10["header_goals"] * 200,
        color="#1f77b4",
        alpha=0.75
    )

    texts = []
    for _, row in top10.iterrows():
        label = f"{row['player.name']} ({int(row['header_goals'])})"
        texts.append(
            plt.text(
                row["header_shots"],
                row["conversion_rate"],
                label,
                fontsize=11,
                ha="center",
                va="bottom",
                bbox=dict(facecolor="white", alpha=0.7, edgecolor="none", pad=1)
            )
        )

    # evita sovrapposizioni in maniera intelligente
    adjust_text(
        texts,
        arrowprops=dict(arrowstyle="-", color="gray", lw=0.8)
    )

    plt.title("Top 10 CF – Header Conversion Rate (Serie A 2015/2016)", fontsize=16)
    plt.xlabel("Header Attempts", fontsize=13)
    plt.ylabel("Conversion Rate (Goals / Attempts)", fontsize=13)
    plt.grid(alpha=0.3)

    plt.tight_layout()

    Path("plots").mkdir(exist_ok=True)
    out = "plots/top10_header_scorers_cf_scatter.png"
    plt.savefig(out, dpi=300)

    print(f"Grafico salvato in: {out}")
    plt.show()


if __name__ == "__main__":
    plot_top10_header_scorers_cf()
