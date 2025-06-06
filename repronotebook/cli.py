# repronotebook/cli.py
import click
from rich import print
from repronotebook.execute import run_notebook
from repronotebook.dependencies import generate_requirements
from pathlib import Path

@click.command()
@click.argument('notebook_path')
@click.option('--upload', is_flag=True)
@click.option('--author', default='Unknown')
def main(notebook_path, upload, author):
    notebook_path = Path(notebook_path).resolve()
    print(f"[bold cyan]🔍 Processing:[/] {notebook_path.name}")
    print(f"[bold cyan]👤 Author:[/] {author}")

    # Step 1: Execute Notebook
    print("[bold]⚙️ Running notebook...[/]")
    if run_notebook(str(notebook_path)):
        print("[green]✅ Notebook ran successfully[/]")
    else:
        print("[red]❌ Notebook execution failed[/]")
        return

    # Step 2: Generate requirements.txt
    print("[bold]📦 Generating requirements.txt...[/]")
    if generate_requirements(str(notebook_path.parent)):
        print("[green]✅ requirements.txt created[/]")
    else:
        print("[red]❌ Failed to generate requirements[/]")
        return

    print("[bold green]🎉 Notebook passed initial checks![/]")

if __name__ == '__main__':
    main()
