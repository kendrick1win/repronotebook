# repronotebook/ro_crate_library/postprocessing.py

from pathlib import Path
from datetime import date
import shutil
import json

def zip_ro_crate(crate_folder: Path):
    zip_path = crate_folder.with_suffix(".zip")
    shutil.make_archive(zip_path.stem, 'zip', root_dir=crate_folder)
    print(f"📦 Zipped RO-Crate at: {zip_path}")
    return zip_path

def generate_zenodo_metadata(crate_folder: Path, title: str, description: str, author_name: str):
    metadata = {
        "title": title,
        "upload_type": "dataset",
        "description": description,
        "creators": [{"name": author_name}],
        "keywords": ["jupyter", "reproducibility", "ro-crate"],
        "license": "CC-BY-4.0",
        "publication_date": str(date.today())
    }

    metadata_path = crate_folder.with_name("zenodo_metadata.json")
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"📝 Zenodo metadata file created at: {metadata_path}")
    return metadata_path
