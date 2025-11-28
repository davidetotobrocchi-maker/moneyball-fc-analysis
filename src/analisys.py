import pandas as pd
from pathlib import Path

SHOTS_FILE = Path("data/shots_clean.csv")

def main():
    # Carico il dataset dei tiri pulito
    df = pd.read_csv(SHOTS_FILE)

    # Raggruppo per giocatore e calcolo le metriche principali
    stats = df.groupby("player.name").agg(
        shots=("player.name", "count"),
        goals=("is_goal", "sum"),
        xg=("shot.statsbomb_xg", "sum")
    ).reset_index()

    # Conversion rate e Goals Above Expectation
    stats["conversion_rate"] = stats["goals"] / stats["shots"]
    stats["gax"] = stats["goals"] - stats["xg"]

    # Ordino per GAx decrescente
    ranking = stats.sort_values("gax", ascending=False)

    # Salvo la classifica finale
    output_path = Path("data/player_gax_ranking.csv")
    ranking.to_csv(output_path, index=False)

    print("Analysis completed. Saved:", output_path)
    print("\nTop 10 players by GAx:")
    print(ranking.head(10))

if __name__ == "__main__":
    main()
