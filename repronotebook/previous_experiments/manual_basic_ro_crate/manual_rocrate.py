
import json
from datetime import date
from pathlib import Path

def generate_ro_crate(folder_path: str, author: str):

    # converts folder path into an absolute path
    folder = Path(folder_path).resolve()
    print('folder:', folder)

    # create the new RO-crate folder 
    crate_folder = folder.with_name(f"{folder.name}-ro-crate")
    print('crate folder:', crate_folder)
    crate_folder.mkdir(exist_ok=True)

    # Copy files into RO-Crate folder
    for item in folder.iterdir():
        if item.is_file():
            target = crate_folder / item.name
            target.write_bytes(item.read_bytes())

    # look for a notebook file in the RO-crate folder
    notebook_file = next((f.name for f in crate_folder.glob("*.ipynb")), None)

    # Build RO-Crate Metadata
    metadata = {
        "@context": "https://w3id.org/ro/crate/1.1/context",
        "@graph": [
            {
                "@id": "ro-crate-metadata.json",
                "@type": "CreativeWork",
                "about": { "@id": "./" }
            },
            {
                "@id": "./",
                "@type": "Dataset",
                "name": folder.name,
                "datePublished": str(date.today()),
                "author": { "@id": "#author" },
                "hasPart": [{"@id": f.name} for f in crate_folder.iterdir() if f.is_file() and f.name != "ro-crate-metadata.json"]
            },
            {
                "@id": "#author",
                "@type": "Person",
                "name": author
            }
        ]
    }

    # add notebook as code
    if notebook_file:
        metadata["@graph"].append({
            "@id": notebook_file,
            "@type": "SoftwareSourceCode",
            "name": notebook_file,
            "programmingLanguage": {
                "@id": "https://w3id.org/ro/terms#Python",
                "name": "Python"
            }
        })

    metadata_path = crate_folder / "ro-crate-metadata.json"
    metadata_path.write_text(json.dumps(metadata, indent=2))
    print(f"✅ RO-Crate created at {crate_folder}")
