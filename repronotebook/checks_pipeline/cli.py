# repronotebook/checks_pipeline/cli.py
import click
from rich import print
from pathlib import Path
import os
import json
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
from repronotebook.ro_crate_library.library_rocrate import generate_ro_crate_with_library
from repronotebook.push_to_zenodo.postprocessing import zip_ro_crate, generate_zenodo_metadata
from repronotebook.push_to_zenodo.zenodo_upload import upload_ro_crate_to_zenodo



@click.command()
@click.argument('notebook_path', type=click.Path(exists=True))
@click.option('--fail-on-style', is_flag=True, help='Abort if flakenb detects any style issues')
@click.option('--author', default='Unknown', help='Notebook author')
@click.option('--use-conda', is_flag=True, help='Use Conda environment for execution')
@click.option('--remove-conda-env', is_flag=True, help='Delete Conda env after execution')
@click.option('--generate-rocrate', is_flag=True, help='Generate RO-Crate for the notebook')
@click.option('--upload', is_flag=True, help='Upload to Zenodo')
@click.option('--validate', is_flag=True, help='Validate RO-Crate')
@click.option('--zenodo-token', help='Zenodo API token (overrides ZENODO_TOKEN env var)')
@click.option('--sandbox', is_flag=True, help='Use Zenodo sandbox for testing')
def main(notebook_path, fail_on_style, author, use_conda, remove_conda_env, generate_rocrate, upload, validate, zenodo_token, sandbox):
    # Collect all notebooks
    notebook_path = Path(notebook_path) # Convert to Path object
    notebooks = []
    if notebook_path.is_file() and notebook_path.suffix == ".ipynb":
        notebooks = [notebook_path]
    elif notebook_path.is_dir():
        notebooks = list(notebook_path.rglob("*.ipynb"))
    
    # Determine output root directory
    # If notebook is in subdirectory, use parent as output root
    if notebooks:
        first_notebook = notebooks[0]
        # Check if notebook is in a subdirectory (like test_pipeline/)
        if first_notebook.parent.name != first_notebook.parent.parent.name:
            output_root = first_notebook.parent.parent
        else:
            output_root = first_notebook.parent
        
        # Create organized output structure
        generated_dir = output_root / "generated"
        dependencies_dir = generated_dir / "dependencies"
        style_reports_dir = generated_dir / "style_reports"
        conda_execution_dir = generated_dir / "conda_execution"
        ro_crates_dir = generated_dir / "ro_crates"
        zenodo_dir = generated_dir / "zenodo"
        
        # Create directories
        for dir_path in [dependencies_dir, style_reports_dir, conda_execution_dir, ro_crates_dir, zenodo_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

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
            
        # Handle requirements.txt - generate in organized location
        req_path = dependencies_dir / "requirements.txt"
        notebook_req_path = nb.parent / "requirements.txt"  # Check if exists in notebook dir
        
        if notebook_req_path.exists():
            all_present, missing = check_existing_dependency_file(notebook_req_path, notebook_imports)
            if all_present:
                print("[green]✅ All notebook imports are already in requirements.txt[/]")
                # Copy to organized location
                import shutil
                shutil.copy2(notebook_req_path, req_path)
            else:
                print(f"[yellow]⚠️ requirements.txt exists but is missing: {missing}[/]")
        else:
            if generate_requirements(str(nb), dependencies_dir, overwrite=True):
                print(f"[green]✅ requirements.txt generated at: {req_path}[/]")

        # Handle environment.yml - generate in organized location
        env_path = dependencies_dir / "environment.yml"
        notebook_env_path = nb.parent / "environment.yml"  # Check if exists in notebook dir
        
        if notebook_env_path.exists():
            all_present, missing = check_existing_dependency_file(notebook_env_path, notebook_imports)
            if all_present:
                print("[green]✅ All notebook imports are already in environment.yml[/]")
                # Copy to organized location
                import shutil
                shutil.copy2(notebook_env_path, env_path)
            else:
                print(f"[yellow]⚠️ environment.yml exists but is missing: {missing}[/]")
        else:
            if generate_environment_yml(str(nb), dependencies_dir, overwrite=True):
                print(f"[green]✅ environment.yml generated at: {env_path}[/]")
        
        # Handle running in a conda environment.
        if use_conda:
            print("[bold]📦 Running in Conda environment...[/]")
            # Use environment.yml from organized location
            env_yml_path = dependencies_dir / "environment.yml"
            env_name = "repronotebook-run" 
            if env_yml_path.exists():
                if create_conda_env(env_yml_path, env_name):
                    # Log execution to organized location
                    execution_log = conda_execution_dir / "execution_log.txt"
                    with open(execution_log, 'w') as f:
                        f.write(f"Executed notebook: {nb.name}\n")
                        f.write(f"Environment: {env_name}\n")
                    run_notebook_in_env(nb, env_name)
            else:
                print("[red]❌ environment.yml not found. Cannot execute in Conda environment.[/]")
        if use_conda and remove_conda_env:
            remove_conda_env("repronotebook-run")
        
        # Generate RO-Crate if requested
        crate_folder = None
        if generate_rocrate:
            print("[bold]📦 Generating RO-Crate...[/]")
            
            # Generate RO-Crate in organized location
            crate_name = f"{nb.stem}-ro-crate"
            crate_folder = ro_crates_dir / crate_name
            
            # Create temporary directory structure for RO-Crate generation
            temp_nb_dir = ro_crates_dir / "temp_notebook_dir"
            temp_nb_dir.mkdir(exist_ok=True)
            
            # Copy notebook and dependencies to temp location
            import shutil
            shutil.copy2(nb, temp_nb_dir / nb.name)
            if (dependencies_dir / "requirements.txt").exists():
                shutil.copy2(dependencies_dir / "requirements.txt", temp_nb_dir / "requirements.txt")
            if (dependencies_dir / "environment.yml").exists():
                shutil.copy2(dependencies_dir / "environment.yml", temp_nb_dir / "environment.yml")
            
            # Generate RO-Crate
            generate_ro_crate_with_library(str(temp_nb_dir), author)
            
            # Move generated RO-Crate to final location
            generated_crate = temp_nb_dir.with_name(f"{temp_nb_dir.name}-library-ro-crate_v2")
            if generated_crate.exists():
                if crate_folder.exists():
                    shutil.rmtree(crate_folder)
                shutil.move(str(generated_crate), str(crate_folder))
            
            # Cleanup temp directory
            if temp_nb_dir.exists():
                shutil.rmtree(temp_nb_dir)
            
            print(f"[green]✅ RO-Crate generated at: {crate_folder}[/]")
        
        # Upload to Zenodo if requested
        if upload and crate_folder and crate_folder.exists():
            print("[bold]☁️ Uploading RO-Crate to Zenodo...[/]")
            try:
                # Create ZIP archive in organized location
                zip_filename = f"{nb.stem}-ro-crate.zip"
                zip_path = ro_crates_dir / zip_filename
                zip_path = zip_ro_crate(crate_folder, output_path=zip_path)
                
                # Generate Zenodo metadata in organized location (unique per notebook)
                title = f"RO-Crate for {nb.stem}"
                description = f"Reproducible research package containing Jupyter notebook '{nb.name}' with dependencies and environment specifications."
                zenodo_metadata_path = zenodo_dir / f"zenodo_metadata_{nb.stem}.json"
                zenodo_metadata_path = generate_zenodo_metadata(crate_folder, title, description, author, output_path=zenodo_metadata_path)
                
                # Read metadata for upload
                with open(zenodo_metadata_path, 'r') as f:
                    zenodo_metadata = json.load(f)
                
                # Upload to Zenodo
                result = upload_ro_crate_to_zenodo(
                    crate_zip_path=zip_path,
                    zenodo_metadata=zenodo_metadata,
                    access_token=zenodo_token,  # Pass CLI token
                    sandbox=sandbox,  # Use CLI flag
                    publish=False   # Manual review before publishing
                )
                
                # Save upload results (unique per notebook)
                upload_results_path = zenodo_dir / f"upload_results_{nb.stem}.json"
                with open(upload_results_path, 'w') as f:
                    json.dump(result, f, indent=2)
                
                print(f"[green]✅ Upload complete! Deposition ID: {result['deposition_id']}[/]")
                print(f"[green]✅ Results saved to: {upload_results_path}[/]")
                
            except Exception as e:
                print(f"[red]❌ Zenodo upload failed: {str(e)}[/]")
                print("[yellow]💡 Make sure ZENODO_TOKEN environment variable is set[/]")
        elif upload and not generate_rocrate:
            print("[red]❌ Cannot upload without RO-Crate. Use --generate-rocrate flag[/]")
        elif upload and not (crate_folder and crate_folder.exists()):
            print("[red]❌ RO-Crate folder not found for upload[/]")




    # DONE: Generate requirements.txt and environment.yml
    # DONE: Run in conda environment
    # DONE: Generate RO-Crate
    # TODO: Convert notebook to HTML
    # TODO: Validate RO-Crate
    # TODO: Upload to Zenodo

if __name__ == "__main__":
    main()
