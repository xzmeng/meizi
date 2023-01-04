import click
from .download import main
from .wsgi import create_app
from pathlib import Path

DEFAULT_PORT = 1310
DEFAULT_DATA_DIR = Path.home() / '.meizi'
DEFAULT_MAX_WORKERS = 2


@click.group()
def cli():
    """MEIZ albums downloader and server."""
    pass


@cli.command()
@click.option('--max-workers', default=DEFAULT_MAX_WORKERS, show_default=True,
              help="The number of threads for downloading.")
@click.option('--data-dir', type=click.Path(path_type=Path), default=DEFAULT_DATA_DIR, show_default=True,
              help="The directory to save albums.")
def download(max_workers, data_dir):
    """Download albums."""
    main(max_workers, data_dir)


@cli.command()
@click.option('--data-dir', type=click.Path(path_type=Path), default=DEFAULT_DATA_DIR, show_default=True,
              help="The directory to read albums.")
@click.option('--port', default=DEFAULT_PORT, show_default=True, help="The port of the http server.")
def serve(data_dir, port: int):
    """Run a local http server."""
    app = create_app(data_dir.absolute())
    app.run(port=port)
