from rocrate.rocrate import ROCrate
from pathlib import Path
from datetime import date

def generate_ro_crate_with_library(folder_path: str, author_name: str):
    # set up input and output paths to folders
    folder = Path(folder_path).resolve()
    crate_folder = folder.with_name(f"{folder.name}-library-ro-crate")


    # Step 1: Create a new RO-Crate object
    crate = ROCrate()

    # Step 2: Add all files in the folder
    for file in folder.iterdir():
        if file.is_file():
            crate.add_file(str(file), dest_path=file.name)

    # Step 3: Add dataset root info
    crate.metadata.name = folder.name
    crate.metadata.datePublished = str(date.today())

    # Step 4: Add author info
    author = crate.add_person(
        {"id": "#author", "name": author_name}
    )
    crate.metadata.author = author

    # Step 5: Write the crate to disk
    crate.write(crate_folder)

    print(f"✅ RO-Crate generated using rocrate-py at: {crate_folder}")
