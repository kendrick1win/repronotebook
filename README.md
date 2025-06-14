# Repronotebook

A command-line tool for validating and ensuring reproducibility of Jupyter notebooks.

## Description

Repronotebook is a Python tool that helps validate and ensure the reproducibility of Jupyter notebooks. It performs several key checks:

1. Verifies that the required kernel is installed
2. Executes the notebook to ensure it runs without errors
3. Generates a `requirements.txt` file to capture dependencies

## Installation

```bash
pip install repronotebook
```

## Usage

Basic usage:
```bash
repronotebook path/to/your/notebook.ipynb
```

With options:
```bash
repronotebook path/to/your/notebook.ipynb --author "Your Name"
```

### Command Line Options

- `notebook_path`: Path to the Jupyter notebook file (required)
- `--author`: Specify the author name (default: "Unknown")
- `--upload`: Flag for future upload functionality (coming soon)

## Features

- **Kernel Validation**: Checks if the required kernel is installed and provides installation instructions if missing
- **Notebook Execution**: Runs the notebook to verify it executes without errors
- **Dependency Management**: Automatically generates a `requirements.txt` file based on the notebook's imports
- **Rich Output**: Provides clear, colorized feedback about the validation process

## Requirements

- Python 3.x
- Jupyter
- Required Python packages:
  - click
  - pipreqs
  - nbconvert
  - nbformat
  - rich

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

## License

[]

## Author

Kendrick Lwin
