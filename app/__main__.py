import click

from app.entrypoint import run_api


@click.group()
def cli() -> None:
    pass


@click.command()
def serve() -> None:
    run_api()


if __name__ == "__main__":
    cli.add_command(serve)
    cli()
