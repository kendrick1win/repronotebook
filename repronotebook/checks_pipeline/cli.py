# repronotebook/checks_pipeline/cli.py
import click
from rich import print
from pathlib import Path
import os
from repronotebook.checks_pipeline.styling_check.styling import run_flakenb

@click.command()
@click.argument('notebook_path')
@click.option('--fail-on-style', is_flag=True, help='Abort if flakenb detects any style issues')
@click.option('--author', default='Unknown', help='Notebook author')
@click.option('--use-conda', is_flag=True, help='Use Conda environment for execution')
@click.option('--upload', is_flag=True, help='Upload to Zenodo')
@click.option('--validate', is_flag=True, help='Validate RO-Crate')
def main(notebook_path, fail_on_style, author, use_conda, upload, validate):
    # Collect all notebooks
    notebooks = []
    if notebook_path.is_file() and notebook_path.suffix == ".ipynb":
        notebooks = [notebook_path]
    elif notebook_path.is_dir():
        notebooks = list(notebook_path.rglob("*.ipynb"))

    for nb in notebooks:
        relative_name = nb.relative_to(Path.cwd())
        print(f"\n[bold cyan]🔍 Processing:[/] {relative_name}")


    # Style check
    print("[bold]🎨 Checking code style with flakenb...[/]")
    style_issues = run_flakenb(str(notebook_path))
    if style_issues:
        print(f"[yellow]⚠️ {len(style_issues)} style issue(s) found in {notebook_path.name}:[/]")
        for line in style_issues:
            print("  ", line)
        
        if fail_on_style:
            print("[red]❌ Aborting due to style issues (use --fail-on-style to disable this check).[/]")
            return  # or sys.exit(1)
    else:
        print("[green]✅ No PEP8 style issues detected[/]")
    
    # Placeholder for execution
    if use_conda:
        print("[bold]📦 Running in Conda environment...[/]")
        # TODO: use conda_env.py
    else:
        print("[bold]⚙️ Running in current environment...[/]")
        # TODO: use execute.py

    # TODO: Generate requirements.txt and environment.yml
    # TODO: Generate RO-Crate
    # TODO: Convert notebook to HTML
    # TODO: Validate RO-Crate
    # TODO: Upload to Zenodo

if __name__ == "__main__":
    main()
