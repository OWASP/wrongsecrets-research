# Git Notes Research

A Python script for researching the use of Git notes in popular GitHub repositories. This script pulls popular repositories based on stars, checks if they use Git notes, and collects information about these notes.

## Table of Contents

- [Git Notes Research](#git-notes-research)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Prerequisites](#prerequisites)
  - [Usage](#usage)
  - [Project Structure](#project-structure)
  - [Database](#database)
  - [Contributing](#contributing)
  - [License](#license)

## Overview

Git notes are a powerful but often underutilized feature of Git. This script aims to gather data on the use of Git notes in popular GitHub repositories, including information about the notes themselves, their content, and when they were last updated. All with the aim of understanding if Git Notes is still in use.

## Prerequisites

Before using this script, ensure you have the following prerequisites installed:

- Python 3.11
- duckdb
- py_ulid

You can install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

## Usage

To run the script, use the following command:

```bash
python git_notes_research.py
```

This will initiate the data collection process and populate the DuckDB database with the relevant information.

## Project Structure

The project is organized as follows:

``` markdown
git-notes-research/
│
├── git_notes_research.py      # Main script
├── modules/                   # Custom modules
│   ├── db.py                  # database interactions
│   └── git.py                 # Git interactions
│   └── setup.py               # Setup steps
├── requirements.txt           # Required Python packages
├── README.md                  # This README file
└── .gitignore                 # Gitignore file
```

## Database

This script uses DuckDB to store and query the collected data. The database structure is defined in the `db.py` module.

## Contributing

Contributions are welcome! If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your changes to your fork.
5. Submit a pull request to the main repository.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
