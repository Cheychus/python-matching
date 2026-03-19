import json
import requests
from pathlib import Path

from config import BASE_DIR, RAW_DIR


def download_ontologies():
    # Pfad zur JSON Datei
    json_path = BASE_DIR / "ontologies.json"

    # Zielordner
    download_dir = Path(RAW_DIR)
    download_dir.mkdir(exist_ok=True)

    # JSON laden
    with open(json_path, "r", encoding="utf-8") as f:
        ontologies = json.load(f)

    # Alle Ontologien durchgehen
    for ontology in ontologies:
        url: str = ontology["url"]
        extension = Path(url).suffix
        short_name = ontology["short_form"]

        file_path = download_dir / f"{short_name}{extension}"
        if file_path.exists():
            print(f"{file_path} already exists -> Skip.")
            continue
        print(f"Downloading {url} -> {file_path}")

        response = requests.get(url)
        response.raise_for_status()

        with open(file_path, "wb") as f:
            f.write(response.content)

    print("Download finished.")
