import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def plot_top10_gax(csv_path="data/player_gax_ranking.csv"):

    df = pd.read_csv(csv_path)

    top10 = df.sort_values("gax", ascending=False).head(10)

    top10["label"] = top10.apply(
        lambda row: f"{row['player.name']} ({int(row['goals'])})", axis=1
    )

    colors = plt.cm.tab10(range(10))

    plt.figure(figsize=(12, 6))
    plt.bar(top10["label"], top10["gax"], color=colors)

    plt.title("Top 10 Giocatori per Goals Above Expectation (GAx)", fontsize=14)
    plt.xlabel("Giocatore (Gol)", fontsize=12)
    plt.ylabel("GAx (Goals Above Expectation)", fontsize=12)

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    # CREA CARTELLA plots/ SE NON ESISTE
    Path("plots").mkdir(exist_ok=True)

    # SALVA L’IMMAGINE
    output_path = "plots/top10_gax.png"
    plt.savefig(output_path, dpi=300)

    print(f"Grafico salvato in: {output_path}")

    plt.show()


if __name__ == "__main__":
    plot_top10_gax()
