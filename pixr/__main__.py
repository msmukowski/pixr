from typing import Any

import click

from pixr.command.core import Command
from pixr.runner_factory import RunnerFactory


@click.command(help="Process images: target-size, rescale, convert between formats, or anonymize (remove metadata)")
@click.argument("argument", type=click.Choice(['target-size', 'rescale', 'convert', 'anonymize']))
@click.option(
    "--max-size",
    help="Specifies the maximum file size (e.g., '500KB', '2MB'). Used with 'target-size'.",
    is_flag=False,
    required=False,
    type=str,
)
@click.option(
    "--wild",
    help="Prioritize meeting the size target above all else (for 'target-size').",
    is_flag=True,
    default=False,
)
@click.option(
    "--percentage",
    help="Specifies the percentage to which it should be reduced (for rescale operation)",
    is_flag=False,
    required=False,
    type=int,
)
@click.option(
    "--file-path",
    "-p",
    help="Path to image to be processed.",
    is_flag=False,
    required=True,
    type=str,
)
@click.option(
    "--output-path",
    "-o",
    help="Path where the processed image will be saved.",
    is_flag=False,
    required=False,
    type=str,
)
@click.option(
    "--target-format",
    "-tf",
    help="Target image format for conversion (required for convert operation)",
    type=click.Choice(['png', 'jpg', 'jpeg', 'webp', 'bmp', 'tiff', 'gif']),
    required=False,
)
@click.option(
    "--quality",
    "-q",
    help="Output quality for lossy formats (1-100, default: 85)",
    type=click.IntRange(1, 100),
    default=85,
)
@click.option("--verbose", "-v", help="Enable verbose output", is_flag=True, default=False)
def main(argument: str, **kwargs: dict[str, Any]) -> None:
    if argument == 'rescale' and not kwargs.get('percentage'):
        raise click.ClickException("--percentage is required for rescale operation")

    if argument == 'target-size' and not kwargs.get('max_size'):
        raise click.ClickException("--max-size is required for target-size operation")

    if argument == 'convert' and not kwargs.get('target_format'):
        raise click.ClickException("--target-format is required for convert operation")

    if argument == 'convert' and not kwargs.get('percentage'):
        kwargs['percentage'] = 50

    try:
        parsed_command = Command.from_cli(argument, kwargs)
        runner = RunnerFactory.create_runner(parsed_command)
        runner.run()
    except Exception as e:
        if kwargs.get('verbose'):
            raise
        else:
            raise click.ClickException(str(e))


if __name__ == "__main__":
    main()
