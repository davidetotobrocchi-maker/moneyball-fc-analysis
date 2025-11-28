import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def plot_top10_gax(csv_path="data/player_gax_ranking.csv"):

    # Carico la classifica già preparata
    df = pd.read_csv(csv_path)

    # Prendo i primi 10 per GAx
    top10 = df.sort_values("gax", ascending=False).head(10)

    # Etichetta: Nome + numero gol tra parentesi
    top10["label"] = top10.apply(
        lambda r: f"{r['player.name']} ({int(r['goals'])})", axis=1
    )

    # Colori diversi giusto per renderlo più leggibile
    colors = plt.cm.tab10(range(len(top10)))

    plt.figure(figsize=(12, 6))
    plt.bar(top10["label"], top10["gax"], color=colors)

    plt.title("Top 10 giocatori per Goals Above Expectation (GAx)")
    plt.xlabel("Giocatore (Gol)")
    plt.ylabel("GAx")

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    # Creo la cartella plots se non c’è già
    Path("plots").mkdir(exist_ok=True)
    out_path = "plots/top10_gax.png"

    plt.savefig(out_path, dpi=300)
    print("Grafico salvato in:", out_path)

    plt.show()


if __name__ == "__main__":
    plot_top10_gax()
