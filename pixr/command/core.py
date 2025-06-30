from dataclasses import dataclass
from functools import cached_property
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, field_validator, model_validator

from pixr.command.exceptions import (
    NoSuchArgument,
    PercentageRangeError,
    TooManyCommandArguments,
)


class CmdArgument(BaseModel):
    resize: Optional[str] = None
    rescale: Optional[str] = None
    convert: Optional[str] = None

    model_config = ConfigDict(ignored_types=(cached_property,))

    @model_validator(mode='before')
    @classmethod
    def max_one_argument_check(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Make sure that only one argument was given"""
        non_none_values = {k: v for k, v in values.items() if v is not None}
        argument_count = len(non_none_values.keys())

        if argument_count > 1:
            raise TooManyCommandArguments("A maximum of one command argument is allowed!")

        return values

    @model_validator(mode='before')
    @classmethod
    def field_affiliation_valid(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Make sure that only valid arguments are provided"""
        valid_arguments = set(cls.model_fields.keys())
        mismatched_argument = set(values.keys()).difference(valid_arguments)

        if mismatched_argument:
            raise NoSuchArgument(f"No such argument: '{mismatched_argument}'! Should be one of: {valid_arguments}")
        return values

    @cached_property
    def value(self):
        values = self.model_dump().values()
        [value] = list(filter(None, values))
        return value


class CmdOptions(BaseModel):
    verbose: bool
    percentage: int
    file_path: str
    output_path: Optional[str] = None
    target_format: Optional[str] = None
    quality: int = 85

    @field_validator("percentage")
    @classmethod
    def percentage_valid(cls, value: int) -> int:
        """Validator to check whether the percentage value is valid"""

        def permissible_range(start: int, stop: int):
            return range(start + 1, stop + 1)

        if value not in permissible_range(0, 100):
            raise PercentageRangeError(value)

        return value

    @field_validator("quality")
    @classmethod
    def quality_valid(cls, value: int) -> int:
        """Validator to check whether the quality value is valid"""
        if not 1 <= value <= 100:
            raise ValueError(f"Quality must be between 1-100, got: {value}")
        return value

    @field_validator("target_format")
    @classmethod
    def target_format_valid(cls, value: Optional[str]) -> Optional[str]:
        """Validator to check whether the target format is supported"""
        if value is None:
            return value

        supported_formats = {'png', 'jpg', 'jpeg', 'webp', 'bmp', 'tiff', 'gif'}
        if value.lower() not in supported_formats:
            raise ValueError(f"Unsupported target format '{value}'. Supported: {', '.join(supported_formats)}")

        return value.lower()


@dataclass
class Command:
    argument: CmdArgument
    options: CmdOptions

    @classmethod
    def from_cli(cls, argument: str, options: dict[str, Any]) -> "Command":
        cmd_argument = CmdArgument(**{argument: argument})
        cmd_options = CmdOptions(**options)

        return cls(cmd_argument, cmd_options)
