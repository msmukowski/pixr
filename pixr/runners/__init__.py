from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

from pixr.command.core import Command


class BaseRunner(ABC):
    """Abstract base class for all image processing runners."""

    def __init__(self, command: Command) -> None:
        self.command = command

    @abstractmethod
    def run(self) -> None:
        """Execute the runner's main operation."""
        pass

    def _validate_input_file(self) -> Path:
        """Validate that the input file exists and is readable."""
        file_path = Path(self.command.options.file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"Input file not found: {file_path}")

        if not file_path.is_file():
            raise ValueError(f"Path is not a file: {file_path}")

        return file_path

    def _determine_output_path(self, suffix: Optional[str] = None, extension: Optional[str] = None) -> Path:
        """Determine the output file path based on input path and options."""
        input_path = Path(self.command.options.file_path)

        output_path_option = getattr(self.command.options, 'output_path', None)

        if output_path_option:
            return Path(output_path_option)

        stem = input_path.stem
        if suffix:
            stem += suffix

        extension = extension or input_path.suffix

        return input_path.parent / f"{stem}{extension}"
