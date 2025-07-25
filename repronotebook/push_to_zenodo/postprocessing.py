# repronotebook/ro_crate_library/postprocessing.py

from pathlib import Path
from datetime import date
import shutil
import json

def zip_ro_crate(crate_folder: Path, output_path: Path = None):
    if output_path is None:
        zip_path = crate_folder.with_suffix(".zip")
    else:
        zip_path = output_path
    
    # Create parent directory if it doesn't exist
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    
    shutil.make_archive(str(zip_path.with_suffix("")), 'zip', root_dir=crate_folder.parent, base_dir=crate_folder.name)
    print(f"📦 Zipped RO-Crate at: {zip_path}")
    return zip_path

def generate_zenodo_metadata(crate_folder: Path, title: str, description: str, author_name: str, output_path: Path = None):
    metadata = {
        "title": title,
        "upload_type": "dataset",
        "description": description,
        "creators": [{"name": author_name}],
        "keywords": ["jupyter", "reproducibility", "ro-crate"],
        "license": "CC-BY-4.0",
        "publication_date": str(date.today())
    }

    if output_path is None:
        metadata_path = crate_folder.with_name("zenodo_metadata.json")
    else:
        metadata_path = output_path
    
    # Create parent directory if it doesn't exist
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"📝 Zenodo metadata file created at: {metadata_path}")
    return metadata_path
