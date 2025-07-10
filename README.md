# PubMed Paper Fetcher

## Overview

This project provides a command-line tool and Python module to fetch PubMed papers matching a query, filter for non-academic (pharma/biotech) authors, and output results as CSV or to the console.

## Code Structure

- `pubmed_paper_fetcher/core.py`: Core logic for fetching and parsing PubMed data.
- `pubmed_paper_fetcher/cli.py`: Command-line interface using Typer.
- `pyproject.toml`: Poetry configuration for dependencies and packaging.

## Heuristics

- **Non-academic authors** are identified by searching for keywords (e.g., "pharma", "biotech", "inc", etc.) in the affiliation string, and ensuring academic keywords (e.g., "university", "institute", etc.) are not present.
- **Corresponding author email** is extracted from the affiliation if present.

## Tools Used

- [Typer](https://typer.tiangolo.com/) for CLI.
- [Requests](https://docs.python-requests.org/) for HTTP requests.
- [Pandas](https://pandas.pydata.org/) for data handling.
- [Poetry](https://python-poetry.org/) for dependency management.

## Installation

```sh
git clone https://github.com/chandana0511/pubmed-paper-fetcher.git
pip install poetry
cd pubmed-paper-fetcher
poetry install
```

## Usage

```sh
poetry run get-papers-list "cancer immunotherapy" --file results.csv --debug
```

## Publishing

This module can be published to Test PyPI using Poetry.

## License

MIT