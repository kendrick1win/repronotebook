# Repronotebook

A command-line tool for validating and ensuring reproducibility of Jupyter notebooks, with RO-Crate generation capabilities for research data management.

## Description

Repronotebook is a Python tool that helps validate and ensure the reproducibility of Jupyter notebooks. It performs several key checks:

1. Verifies that the required kernel is installed
2. Executes the notebook to ensure it runs without errors
3. Generates a `requirements.txt` file to capture dependencies
4. **NEW**: Generates RO-Crates for research data management and reproducibility

## Installation

**Note: This is currently a development project and not yet published to PyPI (Python Package Index).**

### Development Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd repronotebook
   ```

2. **Set up a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install in development mode:**
   ```bash
   pip install -e .
   ```

### What is this software?

This is a **Command Line Interface (CLI)** tool, not a web application. It runs in your terminal/command prompt like other developer tools (git, npm, etc.). Unlike web apps that run in browsers, CLI tools:

- **Run locally** on your computer via terminal commands
- **Process files directly** from your file system  
- **No web server needed** - everything runs on your machine
- **Perfect for automation** and integration with other developer workflows

### Future PyPI Installation (when published)

Once published to PyPI (Python's package repository), installation will be simple:
```bash
pip install repronotebook
```

## Usage

**Important:** All commands assume you're in the project directory with your virtual environment activated:
```bash
cd repronotebook
source .venv/bin/activate  # You should see (.venv) in your prompt
```

### Basic Notebook Validation

**Current development usage:**
```bash
python -m repronotebook.checks_pipeline.cli path/to/your/notebook.ipynb
```

**Future usage (when published to PyPI):**
```bash
repronotebook path/to/your/notebook.ipynb
```

### Example Commands

**Complete validation and RO-Crate generation:**
```bash
python -m repronotebook.checks_pipeline.cli notebook.ipynb --author "Your Name" --generate-rocrate
```

**Full pipeline with Zenodo upload:**
```bash
export ZENODO_TOKEN="your-api-token"
python -m repronotebook.checks_pipeline.cli notebook.ipynb --author "Your Name" --generate-rocrate --upload
```

### RO-Crate Generation

RO-Crate generation is now integrated into the CLI and supports two methods:

#### CLI RO-Crate Generation (Recommended)
```bash
# Generate RO-Crate using library method
python -m repronotebook.checks_pipeline.cli notebook.ipynb --generate-rocrate --author "Your Name"

# Combined with validation pipeline
python -m repronotebook.checks_pipeline.cli notebook.ipynb --generate-rocrate --use-conda --fail-on-style --author "Your Name"

# Generate and upload to Zenodo
export ZENODO_TOKEN="your-zenodo-api-token"
python -m repronotebook.checks_pipeline.cli notebook.ipynb --generate-rocrate --upload --author "Your Name"
```

### Zenodo Upload Integration

Upload your RO-Crates directly to Zenodo for long-term preservation and DOI assignment:

#### Setup Zenodo API Access
1. Create a Zenodo account at [zenodo.org](https://zenodo.org)
2. Generate an API token: Account → Applications → Personal access tokens
3. Set the token as an environment variable:
   ```bash
   export ZENODO_TOKEN="your-zenodo-api-token"
   ```

#### Upload Commands
```bash
# Complete workflow: validate → generate RO-Crate → upload to Zenodo
python -m repronotebook.checks_pipeline.cli notebook.ipynb --generate-rocrate --upload --author "Your Name"

# Full validation pipeline with upload
python -m repronotebook.checks_pipeline.cli notebook.ipynb --generate-rocrate --upload --use-conda --fail-on-style --author "Your Name"
```

#### Upload Process
- **Automatic ZIP creation**: RO-Crate is compressed for upload
- **Metadata generation**: Zenodo-compatible metadata with title, description, and keywords
- **Draft upload**: Files uploaded as draft for manual review before publishing
- **DOI assignment**: Permanent DOI assigned upon publication

#### Programmatic RO-Crate Generation
```python
from repronotebook.ro_crate_library.library_rocrate import generate_ro_crate_with_library

# Library method (recommended)
generate_ro_crate_with_library("path/to/folder", "Author Name")
```

### Command Line Options

- `notebook_path`: Path to the Jupyter notebook file or directory (required)
- `--author`: Specify the author name (default: "Unknown")
- `--fail-on-style`: Abort execution if style issues are detected
- `--use-conda`: Execute notebook in an isolated Conda environment
- `--remove-conda-env`: Delete Conda environment after execution
- `--generate-rocrate`: Generate RO-Crate for the notebook using library method
- `--upload`: Upload RO-Crate to Zenodo (requires ZENODO_TOKEN environment variable)
- `--validate`: Validate RO-Crate (coming soon)

## Features

- **Style Validation**: Uses flakenb to check PEP8 compliance and code style
- **Dependency Management**: Automatically generates `requirements.txt` and `environment.yml` based on notebook imports
- **Conda Environment Execution**: Runs notebooks in isolated Conda environments for reproducibility
- **Multi-notebook Processing**: Process individual notebooks or entire directories
- **Rich Output**: Provides clear, colorized feedback about the validation process
- **RO-Crate Generation**: Creates research data packages with proper metadata for reproducibility
  - Library-based generation using the `rocrate-py` library
  - Automatic author attribution and date stamping
  - Support for Jupyter notebooks as SoftwareSourceCode entities
- **Zenodo Integration**: Direct upload to Zenodo for long-term preservation
  - Automatic ZIP compression and metadata generation
  - Draft upload workflow for manual review
  - DOI assignment for permanent citation

## Requirements

- Python 3.x
- Conda (optional, for isolated environment execution)
- Required Python packages:
  - click
  - pipreqs
  - nbconvert
  - nbformat
  - rich
  - rocrate (for RO-Crate generation)
  - requests (for Zenodo API integration)
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
