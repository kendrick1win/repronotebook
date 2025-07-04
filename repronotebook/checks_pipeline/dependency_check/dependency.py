from pathlib import Path
import nbformat
import re
import yaml

def extract_imports_from_notebook(notebook_path: str) -> list[str]:
    """Extract a list of unique top-level imported packages from the notebook."""
    with open(notebook_path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    imports = set()
    for cell in nb.cells:
        if cell.cell_type != "code":
            continue
        for line in cell.source.split("\n"):
            line = line.strip()
            if line.startswith("import ") or line.startswith("from "):
                line = line.split("#")[0]  # remove inline comments
                line = line.replace(",", " ")  # handle comma-separated imports
                words = line.split()
                if "import" in words:
                    try:
                        idx = words.index("import")
                        base = words[idx + 1]
                        base = base.split(".")[0]
                        imports.add(base)
                    except IndexError:
                        continue  # skip malformed lines
    return sorted(imports)

def extract_package_name(line: str, keep_version: bool = False) -> str:
    """Extract base package name from a line with optional version."""
    line = line.split(";")[0].strip()  # Remove markers like `; python_version < "3.8"`
    if keep_version:
        return line
    match = re.match(r"([a-zA-Z0-9_\-\.]+)", line)
    return match.group(1) if match else ""

def read_dependencies(file_path: Path, keep_version: bool = False) -> list[str]:
    """Read dependencies from a requirements.txt or environment.yml."""
    if not file_path.exists():
        return []

    deps = []
    try:
        if file_path.suffix in [".yml", ".yaml"]:
            with open(file_path, "r") as f:
                env = yaml.safe_load(f)
            for dep in env.get("dependencies", []):
                if isinstance(dep, str):
                    pkg = extract_package_name(dep, keep_version)
                    if pkg:
                        deps.append(pkg)
                elif isinstance(dep, dict) and "pip" in dep:
                    for pip_dep in dep["pip"]:
                        pkg = extract_package_name(pip_dep, keep_version)
                        if pkg:
                            deps.append(pkg)
        else:
            with open(file_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    pkg = extract_package_name(line, keep_version)
                    if pkg:
                        deps.append(pkg)

        return sorted(set(deps))
    except Exception as e:
        print(f"[red]❌ Error reading dependency file:[/] {e}")
        return []

def check_existing_dependency_file(file_path: Path, notebook_imports: list[str]) -> tuple[bool, list[str]]:
    """Check if all notebook imports are already in the dependency file."""
    existing_deps = read_dependencies(file_path)
    missing = [imp for imp in notebook_imports if imp not in existing_deps]
    all_present = len(missing) == 0
    return all_present, missing

def generate_requirements(notebook_path: str, output_dir: Path, overwrite: bool = True) -> bool:
    """Generate a requirements.txt based on notebook imports."""
    try:
        imports = extract_imports_from_notebook(notebook_path)
        filename = "requirements.txt" if overwrite else "auto-requirements.txt"
        req_path = output_dir / filename
        with open(req_path, "w") as f:
            for package in imports:
                f.write(package + "\n")
        return True
    except Exception as e:
        print(f"[red]❌ Error generating requirements.txt:[/] {e}")
        return False

def generate_environment_yml(notebook_path: str, output_dir: Path, overwrite: bool = False) -> bool:
    """Generate a basic environment.yml from notebook imports."""
    try:
        imports = extract_imports_from_notebook(notebook_path)
        filename = "environment.yml" if overwrite else "auto-environment.yml"
        env_path = output_dir / filename
        env_dict = {
            "name": "repronotebook-env",
            "channels": ["defaults"],
            "dependencies": sorted(imports),
        }
        with open(env_path, "w") as f:
            f.write(f"name: {env_dict['name']}\n")
            f.write("channels:\n")
            for channel in env_dict["channels"]:
                f.write(f"  - {channel}\n")
            f.write("dependencies:\n")
            for dep in env_dict["dependencies"]:
                f.write(f"  - {dep}\n")
        return True
    except Exception as e:
        print(f"[red]❌ Error generating environment.yml:[/] {e}")
        return False
