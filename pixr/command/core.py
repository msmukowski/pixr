from dataclasses import dataclass
from typing import Any, Optional

from pydantic import BaseModel, field_validator

from pixr.command.exceptions import PercentageRangeError


class CmdOptions(BaseModel):
    verbose: bool
    percentage: Optional[int] = None
    file_path: str
    output_path: Optional[str] = None
    target_format: Optional[str] = None
    quality: int = 85
    max_size: Optional[str] = None
    wild: bool = False

    @field_validator("percentage")
    @classmethod
    def percentage_valid(cls, value: Optional[int]) -> Optional[int]:
        """Validator to check whether the percentage value is valid"""
        if value is None:
            return value

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
    argument: str
    options: CmdOptions

    @classmethod
    def from_cli(cls, argument: str, options: dict[str, Any]) -> "Command":
        cmd_options = CmdOptions(**options)
        return cls(argument, cmd_options)
