from rocrate.rocrate import ROCrate
from pathlib import Path
from datetime import date
from rocrate.model.person import Person

def extract_readme_metadata(folder: Path):
    readme = folder / "README.md"
    if readme.exists():
        lines = readme.read_text().splitlines()
        title = lines[0].strip("# ").strip() if lines else folder.name
        description = "\n".join(lines[1:3]) if len(lines) > 1 else "No description provided."
        return title, description
    return folder.name, "No description available."

def extract_license(folder: Path):
    license_file = folder / "LICENSE"
    if license_file.exists():
        text = license_file.read_text().lower()
        if "mit license" in text:
            return "https://opensource.org/licenses/MIT"
        elif "apache license" in text:
            return "https://www.apache.org/licenses/LICENSE-2.0"
        elif "gnu general public license" in text:
            return "https://www.gnu.org/licenses/gpl-3.0.en.html"
    return "https://creativecommons.org/licenses/by/4.0/"  # fallback default


def generate_ro_crate_with_library(folder_path: str, author_name: str):
    # set up input and output paths to folders
    folder = Path(folder_path).resolve()
    crate_folder = folder.with_name(f"{folder.name}-library-ro-crate_v2")


    # Create a new RO-Crate object
    crate = ROCrate()

    # Add all files in the folder
    for file in folder.iterdir():
        if file.is_file():
            crate.add_file(str(file), dest_path=file.name)
    
    # Extract title/description/license metadata
    title, description = extract_readme_metadata(folder)
    license_url = extract_license(folder)

 

    # Add dataset root info
    root = crate.root_dataset
    root["name"] = title
    root["description"] = description
    root["datePublished"] = str(date.today())
    root["keywords"] = ["jupyter", "reproducibility", "RO-Crate", "notebook", "biomedical"]
    root["license"] = license_url

    # Add author info 
    author = Person(crate, "#author", properties={
        "name": author_name
    })
    crate.add(author)
    root["author"] = author

     # Mark any notebook as written in Python
    for entity in crate.get_entities():
        if entity.id.endswith(".ipynb"):
            entity["programmingLanguage"] = {
                "@id": "https://w3id.org/ro/terms#Python",
                "name": "Python",
                "alternateName": "py"
            }

    # Write the crate to disk
    crate.write_crate(crate_folder)

    print(f"✅ RO-Crate generated using rocrate-py at: {crate_folder}")
