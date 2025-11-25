import json
import pandas as pd
from pathlib import Path

EVENTS_DIR = Path("data/events")
OUTPUT_FILE = Path("data/shots_clean.csv")


def load_event_file(path: Path) -> pd.DataFrame:
    """Carica un singolo file events JSON e ritorna un DataFrame normalizzato."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return pd.json_normalize(data)


def extract_shots(df: pd.DataFrame, match_id: int) -> pd.DataFrame:
    """Filtra i tiri e seleziona le colonne utili."""
    shots = df[df["type.name"] == "Shot"].copy()
    shots["match_id"] = match_id

    columns_keep = [
        "player.name",
        "team.name",
        "shot.outcome.name",
        "shot.statsbomb_xg",
        "shot.body_part.name",
        "shot.type.name",
        "location",
        "match_id"
    ]

    # Alcune colonne potrebbero non esistere in tutti i file → safe filtering
    shots = shots.reindex(columns=columns_keep)

    return shots


def main():
    all_shots = []

    for file in EVENTS_DIR.glob("*.json"):
        match_id = int(file.stem)
        print(f"Processo {match_id}...")

        df = load_event_file(file)
        shots = extract_shots(df, match_id)

        all_shots.append(shots)

    # Concatena tutti i tiri
    final_df = pd.concat(all_shots, ignore_index=True)

    # Aggiunge colonna is_goal
    final_df["is_goal"] = final_df["shot.outcome.name"] == "Goal"

    # Salva output
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    final_df.to_csv(OUTPUT_FILE, index=False)

    print(f"\nFile salvato: {OUTPUT_FILE}")
    print(f"Tiri totali estratti: {len(final_df)}")


if __name__ == "__main__":
    main()
