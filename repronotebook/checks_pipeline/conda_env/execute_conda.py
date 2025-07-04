# repronotebook/checks_pipeline/conda_env/execute_conda.py

import subprocess
from pathlib import Path
from rich import print

def env_exists(env_name: str) -> bool:
    """Check if the Conda environment already exists."""
    try:
        result = subprocess.run(
            ["conda", "env", "list"],
            capture_output=True,
            text=True,
            check=True
        )
        return any(env_name in line.split() for line in result.stdout.splitlines())
    except Exception as e:
        print(f"[red]❌ Failed to check Conda environments:[/] {e}")
        return False


def create_conda_env(env_yml_path: Path, env_name: str) -> bool:
    """Create a Conda environment from an environment.yml file."""
    if env_exists(env_name):
        print(f"[blue]ℹ️ Conda environment '{env_name}' already exists. Reusing it.[/]")
        return True

    try:
        result = subprocess.run(
            ["conda", "env", "create", "-f", str(env_yml_path), "-n", env_name],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"[green]✅ Created Conda environment: {env_name}[/]")
            return True
        else:
            print(f"[red]❌ Failed to create Conda environment:[/]")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"[red]❌ Error during conda env creation:[/] {e}")
        return False


def run_notebook_in_env(notebook_path: Path, env_name: str) -> bool:
    """Execute a notebook inside a Conda environment."""
    try:
        result = subprocess.run(
            [
                "conda", "run", "-n", env_name,
                "jupyter", "nbconvert", "--to", "notebook",
                "--execute", "--inplace", str(notebook_path)
            ],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("[green]✅ Notebook executed successfully inside Conda env[/]")
            return True
        else:
            print("[red]❌ Notebook execution failed[/]")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"[red]❌ Error executing notebook in Conda environment:[/] {e}")
        return False

def remove_conda_env(env_name: str) -> bool:
    """Remove the specified Conda environment."""
    try:
        result = subprocess.run(
            ["conda", "env", "remove", "-n", env_name, "--yes"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"[green]🧹 Removed Conda environment: {env_name}[/]")
            return True
        else:
            print(f"[red]❌ Failed to remove Conda environment: {env_name}[/]")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"[red]❌ Error while removing Conda environment:[/] {e}")
        return False
