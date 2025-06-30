from pathlib import Path
from typing import Optional

from PIL import Image

from pixr.runners import BaseRunner


class ConvertRunner(BaseRunner):
    """Runner for converting between image formats."""

    SUPPORTED_FORMATS = {
        'png': 'PNG',
        'jpg': 'JPEG',
        'jpeg': 'JPEG',
        'webp': 'WEBP',
        'bmp': 'BMP',
        'tiff': 'TIFF',
        'gif': 'GIF',
    }

    def run(self) -> None:
        """Convert image from one format to another."""
        input_path = self._validate_input_file()

        target_format = self._get_target_format()
        quality = self._get_quality()

        output_path = self._determine_output_path(suffix=f"_converted", extension=f".{target_format.lower()}")

        self._convert_image(input_path, output_path, target_format, quality)

        if self.command.options.verbose:
            print(f"✓ Successfully converted {input_path} to {output_path}")

    def _get_target_format(self) -> str:
        """Get and validate the target format."""
        target_format = getattr(self.command.options, 'target_format', None)

        if not target_format:
            raise ValueError("Target format is required for conversion")

        if target_format.lower() not in self.SUPPORTED_FORMATS:
            supported = ', '.join(self.SUPPORTED_FORMATS.keys())
            raise ValueError(f"Unsupported target format '{target_format}'. Supported: {supported}")

        return target_format.lower()

    def _get_quality(self) -> Optional[int]:
        """Get quality setting for lossy formats."""
        return getattr(self.command.options, 'quality', 85)

    def _detect_source_format(self, image_path: Path) -> str:
        """Detect the format of the source image."""
        try:
            with Image.open(image_path) as img:
                return img.format.lower() if img.format else 'unknown'
        except Exception as e:
            raise ValueError(f"Cannot detect format of {image_path}: {e}")

    def _convert_image(self, input_path: Path, output_path: Path, target_format: str, quality: Optional[int]) -> None:
        """Perform the actual image conversion."""
        try:
            with Image.open(input_path) as img:
                if target_format in ['jpeg', 'jpg'] and img.mode in ['RGBA', 'LA']:
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'RGBA':
                        background.paste(img, mask=img.split()[-1])  # Use alpha channel as mask
                    else:
                        background.paste(img)
                    img = background

                save_kwargs = {}
                pil_format = self.SUPPORTED_FORMATS[target_format]

                if target_format in ['jpeg', 'jpg', 'webp']:
                    save_kwargs['quality'] = quality
                    save_kwargs['optimize'] = True

                if target_format == 'webp':
                    save_kwargs['method'] = 6

                img.save(output_path, format=pil_format, **save_kwargs)

        except Exception as e:
            raise RuntimeError(f"Failed to convert image: {e}")
