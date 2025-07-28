import os
from pathlib import Path
from pixr.anonymize import purify_image
from pixr.runners.base import BaseRunner


class AnonymizeRunner(BaseRunner):
    """Runner for anonymizing images by removing metadata."""

    def run(self) -> None:
        """Remove metadata from an image."""
        input_path = self._validate_input_file()
        output_path = self._determine_output_path(suffix="_anonymized")

        if purify_image(input_path, output_path):
            print(f"Successfully anonymized {input_path} -> {output_path}")
        else:
            print(f"Failed to anonymize {input_path}") 