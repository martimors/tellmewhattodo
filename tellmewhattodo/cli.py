import sys
import click
from tellmewhattodo.job.job import main as job_main
from streamlit.cli import main as server_main


@click.group()
def cli():
    pass


@cli.command()
def check():
    """Run all configured extractors against the configured backend"""
    job_main()


@cli.command()
def server():
    """Show the extracted alerts in an interactive front-end"""
    sys.argv = ["streamlit", "run", "tellmewhattodo/app/app.py"]
    sys.exit(server_main())


if __name__ == "__main__":
    cli()
