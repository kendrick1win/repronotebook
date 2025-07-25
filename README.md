# Repronotebook

A command-line tool for validating and ensuring reproducibility of Jupyter notebooks, with RO-Crate generation capabilities for research data management.

## Description

Repronotebook is a Python tool that helps validate and ensure the reproducibility of Jupyter notebooks. It performs several key checks:

1. Verifies that the required kernel is installed
2. Executes the notebook to ensure it runs without errors
3. Generates a `requirements.txt` file to capture dependencies
4. **NEW**: Generates RO-Crates for research data management and reproducibility

## Installation

```bash
pip install repronotebook
```

## Usage

### Basic Notebook Validation

Basic usage:
```bash
repronotebook path/to/your/notebook.ipynb
```

With options:
```bash
repronotebook path/to/your/notebook.ipynb --author "Your Name" --use-conda --fail-on-style
```

### RO-Crate Generation

The tool now supports two methods for generating RO-Crates:

#### Manual RO-Crate Generation
```python
from repronotebook.manual_basic_ro_crate.manual_rocrate import generate_ro_crate

generate_ro_crate("path/to/folder", "Author Name")
```

#### Library-based RO-Crate Generation
```python
from repronotebook.ro_crate_library.library_rocrate import generate_ro_crate_with_library

generate_ro_crate_with_library("path/to/folder", "Author Name")
```

### Command Line Options

- `notebook_path`: Path to the Jupyter notebook file or directory (required)
- `--author`: Specify the author name (default: "Unknown")
- `--fail-on-style`: Abort execution if style issues are detected
- `--use-conda`: Execute notebook in an isolated Conda environment
- `--remove-conda-env`: Delete Conda environment after execution
- `--upload`: Upload to Zenodo (coming soon)
- `--validate`: Validate RO-Crate (coming soon)

## Features

- **Style Validation**: Uses flakenb to check PEP8 compliance and code style
- **Dependency Management**: Automatically generates `requirements.txt` and `environment.yml` based on notebook imports
- **Conda Environment Execution**: Runs notebooks in isolated Conda environments for reproducibility
- **Multi-notebook Processing**: Process individual notebooks or entire directories
- **Rich Output**: Provides clear, colorized feedback about the validation process
- **RO-Crate Generation**: Creates research data packages with proper metadata for reproducibility
  - Manual generation with custom metadata structure
  - Library-based generation using the `rocrate-py` library
  - Automatic author attribution and date stamping
  - Support for Jupyter notebooks as SoftwareSourceCode entities

## Requirements

- Python 3.x
- Conda (optional, for isolated environment execution)
- Required Python packages:
  - click
  - pipreqs
  - nbconvert
  - nbformat
  - rich
  - rocrate (for library-based RO-Crate generation)
  - flakenb (for style checking)

## Development

To set up the development environment:

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install development dependencies:
   ```bash
   pip install -e .
   ```

## RO-Crate Support

This tool now includes comprehensive RO-Crate generation capabilities:

- **Manual Generation**: Creates RO-Crates with custom metadata structure, suitable for research projects that need specific metadata requirements
- **Library Generation**: Uses the `rocrate-py` library for standardized RO-Crate creation with full compliance to the RO-Crate specification
- **Notebook Integration**: Automatically identifies Jupyter notebooks and marks them as SoftwareSourceCode entities
- **Author Attribution**: Properly attributes authors and includes publication dates
- **File Management**: Copies all files from the source directory into the RO-Crate structure

## License

[]

## Author

Kendrick Lwin
