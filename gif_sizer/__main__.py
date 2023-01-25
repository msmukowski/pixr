from typing import Any

import click

from .parser import parse_command


@click.command(help="Resize an animated GIF")
@click.argument("command")
@click.option(
    "--percentage",
    help="Specifies the percentage to which it should be reduced relative to the original GIF",
    is_flag=False,
    required=True,
    type=int,
)
@click.option(
    "--verbose", "-v", help="Enable verbose output", is_flag=True, default=False
)
def main(command: str, **kwargs: dict[str, Any]) -> None:
    parsed_command = parse_command(command, **kwargs)


if __name__ == "__main__":
    main()
