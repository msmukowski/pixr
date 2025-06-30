from typing import Any

import click

from pixr.command.core import Command
from pixr.runner_factory import RunnerFactory


@click.command(help="Resize an animated GIF")
@click.argument("argument")
@click.option(
    "--percentage",
    help="Specifies the percentage to which it should be reduced relative to the original GIF",
    is_flag=False,
    required=True,
    type=int,
)
@click.option(
    "--file-path", "-p",
    help="Path to GIF to be processed.",
    is_flag=False,
    required=True,
    type=str,
)
@click.option(
    "--output-path", "-o",
    help="Path where the processed GIF will be saved.",
    is_flag=False,
    required=False,
    type=str,
)
@click.option(
    "--verbose", "-v", help="Enable verbose output", is_flag=True, default=False
)
def main(argument: str, **kwargs: dict[str, Any]) -> None:
    parsed_command = Command.from_cli(argument, kwargs)
    runner = RunnerFactory.create_runner(parsed_command)
    runner.run()


if __name__ == "__main__":
    main()
