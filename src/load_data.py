import json
import requests
from pathlib import Path

# File dei match della stagione scelta
MATCHES_FILE = "data/matches/27.json"

# Directory base StatsBomb
BASE_URL = "https://raw.githubusercontent.com/statsbomb/open-data/master/data"

# Cartelle locali per salvare i dati
DIR_EVENTS = Path("data/events")
DIR_LINEUPS = Path("data/lineups")

DIR_EVENTS.mkdir(parents=True, exist_ok=True)
DIR_LINEUPS.mkdir(parents=True, exist_ok=True)

# Carico i match e raccolgo tutti i match_id
with open(MATCHES_FILE, "r", encoding="utf-8") as f:
    matches = json.load(f)

match_ids = [m["match_id"] for m in matches]
print(f"Trovati {len(match_ids)} match_id.")


def download_file(category, match_id):
    """
    Scarica il file JSON corrispondente (events o lineups)
    se disponibile nell'open-data StatsBomb.
    """

    remote_folder = "events" if category == "events" else "lineups"
    local_folder = DIR_EVENTS if category == "events" else DIR_LINEUPS

    out_path = local_folder / f"{match_id}.json"

    # Evita di riscaricare file già presenti
    if out_path.exists():
        print(f"[SKIP] {category}/{match_id}.json già presente.")
        return

    url = f"{BASE_URL}/{remote_folder}/{match_id}.json"
    print(f"[DOWNLOAD] {url}")

    response = requests.get(url)

    if response.status_code == 200:
        out_path.write_text(response.text, encoding="utf-8")
        print(f"[OK] Salvato {category}/{match_id}.json")
    else:
        print(f"[ERRORE] {category}/{match_id}.json non trovato ({response.status_code})")


# Scarico per ciascun match sia events che lineups
for mid in match_ids:
    download_file("events", mid)
    download_file("lineups", mid)

print("\nDownload completato.")
