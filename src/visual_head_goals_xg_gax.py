import json
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

LINEUPS_DIR = Path("data/lineups")
SHOTS_FILE = Path("data/shots_clean.csv")


# ---------------------------------------------------
# 1. Estrarre tutti i giocatori che giocano CF
# ---------------------------------------------------
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
                positions = player.get("positions", [])

                extracted = []

                for pos in positions:
                    if isinstance(pos, dict):
                        if "name" in pos:
                            extracted.append(pos["name"])
                        elif "position" in pos:
                            extracted.append(pos["position"])

                if any(p in cf_positions for p in extracted):
                    center_forwards.add(name)

    return center_forwards


# ---------------------------------------------------
# 2. Grafico combinato:
#    Gol di testa + xG di testa + GAx di testa
# ---------------------------------------------------
def plot_cf_head_goals_xg_gax():

    # ---- CARICA CF ----
    cf_players = load_center_forward_players()
    print(f"Trovati {len(cf_players)} attaccanti centrali.")

    # ---- CARICA TIRI ----
    df = pd.read_csv(SHOTS_FILE)

    # ---- FILTRA SOLO TESTA + SOLO CF ----
    headers_cf = df[
        (df["shot.body_part.name"] == "Head") &
        (df["player.name"].isin(cf_players))
    ].copy()

    if headers_cf.empty:
        print("Nessun colpo di testa trovato per i CF.")
        return

    # ---- CALCOLA GOALS, XG, GAX ----
    grouped = headers_cf.groupby("player.name").agg(
        header_goals=("is_goal", "sum"),
        header_xg=("shot.statsbomb_xg", "sum"),
        shots=("player.name", "count")
    ).reset_index()

    grouped["header_gax"] = grouped["header_goals"] - grouped["header_xg"]

    # ---- TOP 10 ORDINATI PER GOAL ----
    top10 = grouped.sort_values("header_goals", ascending=False).head(10)

    # Etichetta: nome + (gol)
    top10["label"] = top10.apply(
        lambda r: f"{r['player.name']} ({int(r['header_goals'])})",
        axis=1
    )

    # ---- GRAFICO ----
    x = range(len(top10))
    bar_width = 0.25

    plt.figure(figsize=(14, 7))

    # I tre colori
    color_goals = "#1f77b4"
    color_xg = "#2ca02c"
    color_gax = "#ff7f0e"

    # Gol di testa
    bars_goals = plt.bar(
        [i - bar_width for i in x],
        top10["header_goals"],
        width=bar_width,
        color=color_goals,
        label="Gol di testa"
    )

    # xG di testa
    bars_xg = plt.bar(
        x,
        top10["header_xg"],
        width=bar_width,
        color=color_xg,
        label="xG di testa"
    )

    # GAx di testa
    bars_gax = plt.bar(
        [i + bar_width for i in x],
        top10["header_gax"],
        width=bar_width,
        color=color_gax,
        label="GAx di testa (Goals - xG)"
    )

    # Valori sopra ogni barra
    for bars in [bars_goals, bars_xg, bars_gax]:
        for bar in bars:
            h = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, h + 0.03, f"{h:.2f}",
                     ha="center", va="bottom", fontsize=8)

    # Layout grafico
    plt.xticks(x, top10["label"], rotation=45, ha="right")
    plt.ylabel("Valore")
    plt.title("Center Forward – Gol di Testa vs xG di Testa vs GAx di Testa", fontsize=15)
    plt.legend()

    plt.tight_layout()

    # ---- SALVATAGGIO ----
    Path("plots").mkdir(exist_ok=True)
    out = "plots/cf_header_goals_xg_gax.png"
    plt.savefig(out, dpi=300)

    print(f"Grafico salvato in: {out}")
    plt.show()

if __name__ == "__main__":
    plot_cf_head_goals_xg_gax()
