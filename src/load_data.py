import json
import requests
from pathlib import Path

# === CONFIGURAZIONE ===
MATCHES_FILE = "data/matches/27.json"
BASE_URL = "https://raw.githubusercontent.com/statsbomb/open-data/master/data"

# Directory locali
DIR_EVENTS = Path("data/events")
DIR_LINEUPS = Path("data/lineups")

DIR_EVENTS.mkdir(parents=True, exist_ok=True)
DIR_LINEUPS.mkdir(parents=True, exist_ok=True)

# === 1. Carica il file matches ===
with open(MATCHES_FILE, "r", encoding="utf-8") as f:
    matches = json.load(f)

match_ids = [m["match_id"] for m in matches]
print(f"Trovati {len(match_ids)} match_id.")

# === 2. Funzione per scaricare file ===
def download_file(category: str, match_id: int):

    # Mappa categorie → cartelle locali e remote
    remote_dirs = {
        "events": "events",
        "lineups": "lineups"
    }

    local_dirs = {
        "events": DIR_EVENTS,
        "lineups": DIR_LINEUPS
    }

    local_dir = local_dirs[category]
    remote_dir = remote_dirs[category]

    out_file = local_dir / f"{match_id}.json"

    # Skip se già esiste
    if out_file.exists():
        print(f"[SKIP] {category}/{match_id}.json già presente.")
        return

    # URL remoto
    url = f"{BASE_URL}/{remote_dir}/{match_id}.json"
    print(f"[DOWNLOAD] {url}")

    r = requests.get(url)

    if r.status_code == 200:
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(r.text)
        print(f"[OK] Salvato {category}/{match_id}.json")
    else:
        print(f"[ERRORE] {category}/{match_id}.json non trovato ({r.status_code})")


# === 3. Scarica events + lineups per ogni match ===
for mid in match_ids:
    download_file("events", mid)
    download_file("lineups", mid)

print("\nDownload completato.")

