from typing import Optional


class PixrError(Exception):
    """Base exception for all pixr errors."""

    ...


class PercentageRangeError(PixrError):
    """Custom error that is raised when the given percentage is not in allowed range"""

    def __init__(self, value: int, message: Optional[str] = None) -> None:
        self.value = value
        self._standard_message = f"The percentage value: '{self.value}' is outside the allowed range of 0-100!"
        self.message = message if message else self._standard_message
        super().__init__(self.message)


class TooManyCommandArguments(PixrError):
    """Custom error that is raised when the number of command arguments is larger than one."""

    ...


class NoSuchArgument(PixrError):
    """Custom error that is raised when the input argument doesn't exist"""

    ...


class InputFileError(PixrError):
    """Custom error for runner-specific input file errors."""

    ...


class ConversionError(PixrError):
    """Custom error for runner-specific conversion errors."""

    ...
