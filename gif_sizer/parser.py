from typing import Any

from pydantic import BaseModel, ValidationError

ACCEPTED_COMMANDS = ("resize", "rescale")


class CmdOptions(BaseModel):
    verbose: bool
    percentage: int


def parse_command(command: str, **kwargs: dict[str, Any]) -> dict:
    cmd_options = CmdOptions(**kwargs)
    _validate_command(command)
    return


def _validate_command(command: str) -> None:
    if command not in ACCEPTED_COMMANDS:
        raise KeyError(
            f"Given command: '{command}' is not allowed! Allowed commands: {ACCEPTED_COMMANDS}."
        )
