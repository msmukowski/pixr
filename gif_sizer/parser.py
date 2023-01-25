import click
from typing import Any

ACCEPTED_COMMANDS = ("resize", "rescale")

def parse_command(command: str, **kwargs: dict[str, Any]) -> dict:
    _validate_command(command)
    return


def _validate_command(command: str) -> None:
    if not command in ACCEPTED_COMMANDS:
        raise KeyError(f"Given command: '{command}' is not allowed! Allowed commands: {ACCEPTED_COMMANDS}.")
    