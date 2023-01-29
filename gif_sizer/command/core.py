from dataclasses import dataclass
from functools import cached_property
from typing import Any, Optional

from pydantic import BaseModel, root_validator, validator

from gif_sizer.command.exceptions import PercentageRangeError, TooManyCommandArguments


class CmdArgument(BaseModel):
    resize: Optional[str]
    rescale: Optional[str]

    class Config:
        keep_untouched = (cached_property,)

    @root_validator(pre=True)
    @classmethod
    def max_one_argument_check(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Make sure that only one argument was given"""
        if len(values.keys()) > 1:
            raise TooManyCommandArguments(
                "A maximum of one command argument is allowed!"
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

    @validator("percentage")
    @classmethod
    def percentage_valid(cls, value: int) -> None:
        """Validator to check whether the percentage value is valid"""

        def range_inclusive(start: int, stop: int):
            return range(start, stop + 1)

        if value not in range_inclusive(0, 100):
            raise PercentageRangeError(value)


@dataclass
class Command:
    argument: CmdArgument
    options: CmdOptions

    @classmethod
    def from_cli(cls, argument: str, options: dict[str, Any]) -> "Command":
        cmd_argument = CmdArgument(**{argument: argument})
        cmd_options = CmdOptions(**options)

        return cls(cmd_argument, cmd_options)
