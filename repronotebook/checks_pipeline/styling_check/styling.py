# repronotebook/checks_pipeline/styling_check

import subprocess
from pathlib import Path

def run_flakenb(notebook_path: str) -> list[str]:
    """Run flakenb on a notebook and return a list of style violations."""
    try:
        result = subprocess.run(
            ["flakenb", notebook_path],
            capture_output=True,
            text=True,
            check=False  # We want to capture errors, not crash
        )

        if result.returncode != 0 and result.stdout:
            return result.stdout.strip().splitlines()
        return []
    except FileNotFoundError:
        print("[red]❌ flakenb is not installed. Please install it with `pip install flakenb`[/]")
        return []
    except Exception as e:
        print(f"[red]❌ flakenb failed:[/] {e}")
        return []
