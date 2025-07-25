# repronotebook/checks_pipeline/cli.py
import click
from rich import print
from pathlib import Path
import os
from repronotebook.checks_pipeline.styling_check.styling import run_flakenb
from repronotebook.checks_pipeline.dependency_check.dependency import (
    extract_imports_from_notebook,
    check_existing_dependency_file,
    generate_requirements,
    generate_environment_yml
)
from repronotebook.checks_pipeline.conda_env.execute_conda import (
    create_conda_env,
    run_notebook_in_env,
    remove_conda_env
)
from repronotebook.manual_basic_ro_crate.manual_rocrate import generate_ro_crate
from repronotebook.ro_crate_library.library_rocrate import generate_ro_crate_with_library



@click.command()
@click.argument('notebook_path', type=click.Path(exists=True))
@click.option('--fail-on-style', is_flag=True, help='Abort if flakenb detects any style issues')
@click.option('--author', default='Unknown', help='Notebook author')
@click.option('--use-conda', is_flag=True, help='Use Conda environment for execution')
@click.option('--remove-conda-env', is_flag=True, help='Delete Conda env after execution')
@click.option('--generate-rocrate', is_flag=True, help='Generate RO-Crate for the notebook')
@click.option('--rocrate-method', type=click.Choice(['manual', 'library']), default='library', help='RO-Crate generation method')
@click.option('--upload', is_flag=True, help='Upload to Zenodo')
@click.option('--validate', is_flag=True, help='Validate RO-Crate')
def main(notebook_path, fail_on_style, author, use_conda, remove_conda_env, generate_rocrate, rocrate_method, upload, validate):
    # Collect all notebooks
    notebook_path = Path(notebook_path) # Convert to Path object
    notebooks = []
    if notebook_path.is_file() and notebook_path.suffix == ".ipynb":
        notebooks = [notebook_path]
    elif notebook_path.is_dir():
        notebooks = list(notebook_path.rglob("*.ipynb"))

    for nb in notebooks:
        nb = Path(nb).resolve()  # Convert to absolute path
        relative_name = nb.relative_to(Path.cwd())
        print(f"\n[bold cyan]🔍 Processing:[/] {relative_name}")
        # Style check
        print("[bold]🎨 Checking code style with flakenb...[/]")
        style_issues = run_flakenb(str(nb))
        if style_issues:
            print(f"[yellow]⚠️ {len(style_issues)} style issue(s) found in {nb.name}:[/]")
            for line in style_issues:
                print("  ", line)
            
            if fail_on_style:
                print("[red]❌ Aborting due to style issues (use --fail-on-style to disable this check).[/]")
                return  # or sys.exit(1)
            else:
                print("[green]✅ No PEP8 style issues detected[/]")
            
        # Extract imports from the notebook
        notebook_imports = extract_imports_from_notebook(str(nb))
            
        # Handle requirements.txt
        req_path = nb.parent / "requirements.txt"
        if req_path.exists():
            all_present, missing = check_existing_dependency_file(req_path, notebook_imports)
            if all_present:
                print("[green]✅ All notebook imports are already in requirements.txt[/]")
            else:
                print(f"[yellow]⚠️ requirements.txt exists but is missing: {missing}[/]")
        else:
            if generate_requirements(str(nb), nb.parent, overwrite=True):
                print("[green]✅ requirements.txt generated[/]")

        # Handle environment.yml
        env_path = nb.parent / "environment.yml"
        if env_path.exists():
            all_present, missing = check_existing_dependency_file(env_path, notebook_imports)
            if all_present:
                print("[green]✅ All notebook imports are already in environment.yml[/]")
            else:
                print(f"[yellow]⚠️ environment.yml exists but is missing: {missing}[/]")
        else:
            if generate_environment_yml(str(nb), nb.parent, overwrite=True):
                print("[green]✅ environment.yml generated[/]")
        
        # Handle running in a conda environment.
        if use_conda:
            print("[bold]📦 Running in Conda environment...[/]")
            env_path = nb.parent / "environment.yml"
            env_name = "repronotebook-run" 
            if env_path.exists():
                if create_conda_env(env_path, env_name):
                    run_notebook_in_env(nb, env_name)
            else:
                print("[red]❌ environment.yml not found. Cannot execute in Conda environment.[/]")
        if use_conda and remove_conda_env:
            remove_conda_env("repronotebook-run")
        
        # Generate RO-Crate if requested
        if generate_rocrate:
            print("[bold]📦 Generating RO-Crate...[/]")
            notebook_dir = nb.parent
            
            if rocrate_method == 'manual':
                generate_ro_crate(str(notebook_dir), author)
            else:  # library method
                generate_ro_crate_with_library(str(notebook_dir), author)




    # DONE: Generate requirements.txt and environment.yml
    # DONE: Run in conda environment
    # DONE: Generate RO-Crate
    # TODO: Convert notebook to HTML
    # TODO: Validate RO-Crate
    # TODO: Upload to Zenodo

if __name__ == "__main__":
    main()
