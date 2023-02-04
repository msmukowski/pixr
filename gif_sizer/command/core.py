from dataclasses import dataclass
from functools import cached_property
from typing import Any, Optional

from pydantic import BaseModel, root_validator, validator

from gif_sizer.command.exceptions import (
    NoSuchArgument,
    PercentageRangeError,
    TooManyCommandArguments,
)


class CmdArgument(BaseModel):
    resize: Optional[str]
    rescale: Optional[str]

    class Config:
        keep_untouched = (cached_property,)

    @root_validator(pre=True)
    @classmethod
    def max_one_argument_check(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Make sure that only one argument was given"""
        argument_count = len(values.keys())

        if argument_count > 1:
            raise TooManyCommandArguments(
                "A maximum of one command argument is allowed!"
            )

        return values

    @root_validator(pre=True)
    @classmethod
    def field_affiliation_valid(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Make sure that only one argument was given"""
        valid_arguments = set(cls.__fields__.keys())
        mismatched_argument = set(values.keys()).difference(valid_arguments)

        if mismatched_argument:
            raise NoSuchArgument(
                f"No such argument: '{mismatched_argument}'! Should be one of: {valid_arguments}"
            )
        return values

    @cached_property
    def value(self):
        values = self.dict().values()
        [value] = list(filter(None, values))
        return value


class CmdOptions(BaseModel):
    verbose: bool
    percentage: int
    file_path: str

    @validator("percentage")
    @classmethod
    def percentage_valid(cls, value: int) -> int:
        """Validator to check whether the percentage value is valid"""

        def permissible_range(start: int, stop: int):
            return range(start + 1, stop + 1)

        if value not in permissible_range(0, 100):
            raise PercentageRangeError(value)

        return value


@dataclass
class Command:
    argument: CmdArgument
    options: CmdOptions

    @classmethod
    def from_cli(cls, argument: str, options: dict[str, Any]) -> "Command":
        cmd_argument = CmdArgument(**{argument: argument})
        cmd_options = CmdOptions(**options)

        return cls(cmd_argument, cmd_options)
