import sys
import click
from tellmewhattodo.job.job import main as job_main
from streamlit.cli import main as server_main


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
        print("Debug mode is active")
    pass


@cli.command()
def check():
    """Run all configured extractors against the configured backend"""
    job_main()


@cli.command()
@click.pass_context
def server(ctx):
    """Show the extracted alerts in an interactive front-end"""
    debug = ctx.obj["DEBUG"]
    args = ["streamlit", "run"]
    if debug:
        args += ["--logger.level", "debug"]
    sys.argv = args + [
        "tellmewhattodo/app/app.py",
    ]
    sys.exit(server_main())


if __name__ == "__main__":
    cli()
