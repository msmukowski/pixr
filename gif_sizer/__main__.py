from typing import Any

import click

from gif_sizer.command.core import Command


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
    "--verbose", "-v", help="Enable verbose output", is_flag=True, default=False
)
def main(argument: str, **kwargs: dict[str, Any]) -> None:
    parsed_command = Command.from_cli(argument, kwargs)


if __name__ == "__main__":
    main()
