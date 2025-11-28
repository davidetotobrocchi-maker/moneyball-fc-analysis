import json
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

LINEUPS_DIR = Path("data/lineups")
SHOTS_FILE = Path("data/shots_clean.csv")


# -----------------------------
# Prendo i giocatori che hanno giocato da attaccante centrale
# -----------------------------
def load_center_forwards():
    cf_roles = {"Centre Forward", "Center Forward", "Central Forward", "Forward", "Striker"}
    cf = set()

    for file in LINEUPS_DIR.glob("*.json"):
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        for team in data:
            for player in team.get("lineup", []):
                name = player.get("player_name")
                pos_list = []

                # Estraggo il nome della posizione (gli JSON non sono sempre identici)
                for p in player.get("positions", []):
                    if isinstance(p, dict):
                        if "name" in p:
                            pos_list.append(p["name"])
                        elif "position" in p:
                            pos_list.append(p["position"])

                # Se almeno una delle posizioni coincide, lo considero CF
                if any(pos in cf_roles for pos in pos_list):
                    cf.add(name)

    return cf


# -----------------------------
# Grafico: gol di testa, xG di testa, GAx di testa
# -----------------------------
def plot_cf_headers():

    cf_players = load_center_forwards()
    print("Center forwards trovati:", len(cf_players))

    df = pd.read_csv(SHOTS_FILE)

    # Tiri di testa dei soli CF
    headers = df[
        (df["shot.body_part.name"] == "Head") &
        (df["player.name"].isin(cf_players))
    ].copy()

    if headers.empty:
        print("Nessun colpo di testa per i CF.")
        return

    stats = headers.groupby("player.name").agg(
        goals=("is_goal", "sum"),
        xg=("shot.statsbomb_xg", "sum"),
        shots=("player.name", "count")
    ).reset_index()

    stats["gax"] = stats["goals"] - stats["xg"]

    # Ordino per gol di testa
    top10 = stats.sort_values("goals", ascending=False).head(10)

    # Label tipo: "Higuain (5)"
    top10["label"] = top10.apply(
        lambda r: f"{r['player.name']} ({int(r['goals'])})", axis=1
    )

    # -----------------------------
    # GRAFICO
    # -----------------------------
    x = range(len(top10))
    w = 0.25

    plt.figure(figsize=(12, 6))

    plt.bar([i - w for i in x], top10["goals"], width=w, label="Header Goals", color="#1f77b4")
    plt.bar(x, top10["xg"], width=w, label="Header xG", color="#2ca02c")
    plt.bar([i + w for i in x], top10["gax"], width=w, label="Header GAx", color="#ff7f0e")

    # Etichette numeriche sopra le barre
    for col, shift in [("goals", -w), ("xg", 0), ("gax", w)]:
        for i, val in enumerate(top10[col]):
            plt.text(i + shift, val + 0.03, f"{val:.2f}", ha="center", fontsize=8)

    plt.xticks(x, top10["label"], rotation=45, ha="right")
    plt.ylabel("Valore")
    plt.title("CF – Header Goals vs Header xG vs Header GAx")
    plt.legend()

    plt.tight_layout()

    Path("plots").mkdir(exist_ok=True)
    out_path = "plots/cf_header_goals_xg_gax.png"
    plt.savefig(out_path, dpi=300)

    print("Grafico salvato in:", out_path)
    plt.show()


if __name__ == "__main__":
    plot_cf_headers()
