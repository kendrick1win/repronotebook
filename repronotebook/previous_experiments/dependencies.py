# repronotebook/dependencies.py
import subprocess
from pathlib import Path

def generate_requirements(notebook_dir: str) -> bool:
    try:
        # pipreqs is a tool that generates requirements.txt from a directory of Python code
        # pipreqs - Lists only what your code actually imports
        # --force is used to overwrite the existing requirements.txt file
        subprocess.run(["pipreqs", notebook_dir, "--force"], check=True)
        return Path("requirements.txt").exists()
    except subprocess.CalledProcessError:
        return False
