import pandas as pd
from pathlib import Path

SHOTS_FILE = Path("data/shots_clean.csv")

def main():
    df = pd.read_csv(SHOTS_FILE)

    # Raggruppa per giocatore
    grouped = df.groupby("player.name").agg(
        shots=("player.name", "count"),
        goals=("is_goal", "sum"),
        xg=("shot.statsbomb_xg", "sum")
    ).reset_index()

    # Conversion rate
    grouped["conversion_rate"] = grouped["goals"] / grouped["shots"]

    # GAx = Goals - xG
    grouped["gax"] = grouped["goals"] - grouped["xg"]

    # Ordina dal migliore (overperformer)
    ranking = grouped.sort_values("gax", ascending=False)

    # Salva l’output
    ranking.to_csv("data/player_gax_ranking.csv", index=False)

    print("Analisi completata. File salvato in data/player_gax_ranking.csv")
    print(ranking.head(10))

if __name__ == "__main__":
    main()
