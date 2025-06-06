# repronotebook/execute.py
import subprocess
from pathlib import Path
import nbformat

def run_notebook(path: str) -> bool:
    executed_path = Path(path).with_name(Path(path).stem + "_executed.ipynb")
    try:
        subprocess.run([
            "jupyter", "nbconvert",
            "--to", "notebook",
            "--execute", path,
            "--output", str(executed_path)
        ], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def get_kernel_name(notebook_path: str) -> str:
    # 1. Opens the notebook file
    with open(notebook_path) as f:
        # 2. Parses the notebook JSON using nbformat
        nb = nbformat.read(f, as_version=4)
    # 3. Safely extracts the kernel name
    return nb.metadata.get("kernelspec", {}).get("name", None)

