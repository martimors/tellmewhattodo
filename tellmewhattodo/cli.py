from pathlib import Path
import sys
import click
from tellmewhattodo.job.job import main as job_main

from logging import getLogger, DEBUG

logger = getLogger(__name__)


@click.group()
@click.option(
    "--debug",
    is_flag=True,
    help="Logs more info to the console when debugging",
    default=False,
)
@click.pass_context
def cli(ctx, debug):
    ctx.ensure_object(dict)
    ctx.obj["DEBUG"] = debug
    if debug:
        logger.setLevel(DEBUG)
    pass


@cli.command()
def check():
    """Run all configured extractors against the configured backend"""
    logger.debug("Running tellmewhattodo check job")
    job_main()


@cli.command()
@click.pass_context
def server(ctx):
    """Show the extracted alerts in an interactive front-end"""
    debug = ctx.obj["DEBUG"]
    args = ["streamlit", "run"]
    path_to_app = str(Path(__file__).parent / "app/app.py")
    if debug:
        args += ["--logger.level", "debug"]
    sys.argv = args + [path_to_app]
    raise NotImplementedError()


if __name__ == "__main__":
    cli()
