import click
from typing import Optional

from pixr.command.core import Command
from pixr.runner_factory import RunnerFactory


@click.group()
def cli():
    """A versatile image processing tool."""
    pass


def run_command(argument: str, options: dict):
    command = Command.from_cli(argument, options)
    runner = RunnerFactory.create_runner(command)
    runner.run()


@cli.command(name="anonymize", help="Remove metadata from an image.")
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose output.")
@click.argument("file_path", type=click.Path(exists=True))
@click.argument("output_path", type=click.Path(), required=False)
def anonymize_command(verbose: bool, file_path: str, output_path: Optional[str]):
    """Anonymize an image by removing its metadata."""
    run_command("anonymize", locals())


@cli.command(name="rescale", help="Rescale an image by a percentage.")
@click.option("-p", "--percentage", type=int, required=True, help="The percentage to rescale the image by.")
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose output.")
@click.argument("file_path", type=click.Path(exists=True))
@click.argument("output_path", type=click.Path(), required=False)
def rescale_command(percentage: int, verbose: bool, file_path: str, output_path: Optional[str]):
    """Rescale an image to a new size based on a percentage."""
    run_command("rescale", locals())


@cli.command(name="convert", help="Convert an image to a different format.")
@click.option("-f", "--target-format", type=str, required=True, help="The target format (e.g., png, jpg, webp).")
@click.option("-q", "--quality", type=int, default=85, help="The quality of the converted image (1-100).")
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose output.")
@click.argument("file_path", type=click.Path(exists=True))
@click.argument("output_path", type=click.Path(), required=False)
def convert_command(target_format: str, quality: int, verbose: bool, file_path: str, output_path: Optional[str]):
    """Convert an image from one format to another."""
    run_command("convert", locals())


@cli.command(name="target-size", help="Resize an image to a target size.")
@click.option("-s", "--max-size", type=str, required=True, help="The maximum file size (e.g., 500KB, 2MB).")
@click.option("--wild", is_flag=True, help="Prioritize meeting the size target above all else.")
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose output.")
@click.argument("file_path", type=click.Path(exists=True))
@click.argument("output_path", type=click.Path(), required=False)
def target_size_command(max_size: str, wild: bool, verbose: bool, file_path: str, output_path: Optional[str]):
    """Resize an image to meet a target file size."""
    run_command("target-size", locals())


if __name__ == "__main__":
    cli()
