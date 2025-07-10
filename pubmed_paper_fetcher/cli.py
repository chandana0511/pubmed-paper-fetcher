import typer
import pandas as pd
from typing import Optional
from pubmed_paper_fetcher.core import fetch_pubmed_ids, fetch_paper_details

app = typer.Typer()

@app.command()
def get_papers_list(
    query: str,
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug info"),
    file: Optional[str] = typer.Option(None, "--file", "-f", help="CSV output file")
) -> None:
    """
    Fetch PubMed papers matching the query, filter for non-academic authors, and output as CSV or to console.
    """
    try:
        if debug:
            typer.echo(f"Running query: {query}")

        ids = fetch_pubmed_ids(query, retmax=10)
        if debug:
            typer.echo(f"Found IDs: {ids}")

        results = [fetch_paper_details(pmid) for pmid in ids]
        df = pd.DataFrame(results)

        if file:
            df.to_csv(file, index=False)
            typer.echo(f"Saved to {file}")
        else:
            typer.echo(df.to_string(index=False))
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()