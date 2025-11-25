import json
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

LINEUPS_DIR = Path("data/lineups")
SHOTS_FILE = Path("data/shots_clean.csv")


def load_center_forward_players():
    """
    Estrae tutti i giocatori che, in almeno una partita,
    hanno la posizione 'Centre Forward' o equivalenti.
    Gestisce automaticamente tutte le varianti dei JSON StatsBomb.
    """

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
                player_name = player.get("player_name")
                positions = player.get("positions", [])

                extracted_positions = []

                for pos in positions:
                    # Le lineup StatsBomb possono usare "name" oppure "position"
                    if isinstance(pos, dict):
                        if "name" in pos:
                            extracted_positions.append(pos["name"])
                        elif "position" in pos:
                            extracted_positions.append(pos["position"])

                # Controllo se almeno una posizione è quella del CF
                if any(p in cf_positions for p in extracted_positions):
                    center_forwards.add(player_name)

    return center_forwards


def plot_top10_header_cf_gax():
    """Crea un grafico dei migliori CF per GAx (solo tiri di testa)."""

    # 1. Carico lista CF
    center_forwards = load_center_forward_players()
    print(f"Trovati {len(center_forwards)} center forwards.")

    # 2. Carico dataset tiri
    df = pd.read_csv(SHOTS_FILE)

    # 3. Filtra: solo tiri di testa + solo CF
    headers_cf = df[
        (df["shot.body_part.name"] == "Head") &
        (df["player.name"].isin(center_forwards))
    ].copy()

    if headers_cf.empty:
        print("Nessun colpo di testa per i center forward trovati!")
        return

    # 4. Group + GAx
    grouped = headers_cf.groupby("player.name").agg(
        goals=("is_goal", "sum"),
        xg=("shot.statsbomb_xg", "sum"),
        shots=("player.name", "count")
    ).reset_index()

    grouped["gax"] = grouped["goals"] - grouped["xg"]

    # 5. Ordina Top 10
    top10 = grouped.sort_values("gax", ascending=False).head(10)

    # Label nome + numero gol
    top10["label"] = top10.apply(
        lambda row: f"{row['player.name']} ({int(row['goals'])})", axis=1
    )

    # 6. Plot
    colors = plt.cm.tab10(range(len(top10)))

    plt.figure(figsize=(12, 6))
    plt.bar(top10["label"], top10["gax"], color=colors)

    plt.title("Top 10 Center Forward – Goals Above Expectation (Header Shots Only)", fontsize=14)
    plt.xlabel("Giocatore (Gol di Testa)", fontsize=12)
    plt.ylabel("GAx sui colpi di testa", fontsize=12)
    plt.xticks(rotation=45, ha="right")

    plt.tight_layout()

    # 7. Salvataggio
    Path("plots").mkdir(exist_ok=True)
    output_path = "plots/top10_header_cf_gax.png"
    plt.savefig(output_path, dpi=300)
    print(f"Grafico salvato in: {output_path}")

    plt.show()


if __name__ == "__main__":
    plot_top10_header_cf_gax()
