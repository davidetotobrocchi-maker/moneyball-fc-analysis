import json
import pandas as pd
from pathlib import Path

EVENTS_DIR = Path("data/events")
OUTPUT_FILE = Path("data/shots_clean.csv")

def load_event_file(path):
    # Carico un singolo file events (JSON) e lo trasformo in DataFrame
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return pd.json_normalize(data)


def extract_shots(df, match_id):
    # Seleziono solo gli eventi di tipo "Shot"
    shots = df[df["type.name"] == "Shot"].copy()
    shots["match_id"] = match_id

    # Tengo solo le colonne che servono davvero
    cols = [
        "player.name",
        "team.name",
        "shot.outcome.name",
        "shot.statsbomb_xg",
        "shot.body_part.name",
        "shot.type.name",
        "location",
        "match_id"
    ]

    return shots[cols]


def main():
    all_shots = []

    # Scorro tutti i file della cartella eventi
    for file in EVENTS_DIR.glob("*.json"):
        match_id = int(file.stem)
        print(f"Processing match {match_id}...")

        df = load_event_file(file)
        shots = extract_shots(df, match_id)
        all_shots.append(shots)

    # Unisco tutto in un unico DataFrame
    final_df = pd.concat(all_shots, ignore_index=True)

    # Aggiungo colonna per indicare se è un gol
    final_df["is_goal"] = final_df["shot.outcome.name"] == "Goal"

    # Mi assicuro che la cartella esista
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Salvo il file
    final_df.to_csv(OUTPUT_FILE, index=False)

    print(f"\nSaved to: {OUTPUT_FILE}")
    print(f"Total shots extracted: {len(final_df)}")


if __name__ == "__main__":
    main()
