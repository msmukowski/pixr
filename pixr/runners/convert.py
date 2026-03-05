from pathlib import Path
from typing import Optional

from PIL import Image

from pixr.formats import SUPPORTED_FORMATS
from pixr.runners import BaseRunner


class ConvertRunner(BaseRunner):
    """Runner for converting between image formats."""

    def run(self) -> None:
        """Convert image from one format to another."""
        input_path = self._validate_input_file()

        target_format = self.command.options.target_format
        if not target_format:
            raise ValueError("Target format is required for conversion")
        quality = self.command.options.quality

        output_path = self._determine_output_path(suffix="_converted", extension=f".{target_format}")

        original_size = input_path.stat().st_size

        self._convert_image(input_path, output_path, target_format, quality)

        converted_size = output_path.stat().st_size
        self._report_conversion_results(input_path, output_path, original_size, converted_size)

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
                pil_format = SUPPORTED_FORMATS[target_format]

                if target_format in ['jpeg', 'jpg', 'webp']:
                    save_kwargs['quality'] = quality
                    save_kwargs['optimize'] = True

                if target_format == 'webp':
                    save_kwargs['method'] = 6
                    if self._detect_source_format(input_path) in ['jpeg', 'jpg']:
                        if quality >= 90:
                            save_kwargs['lossless'] = True
                        else:
                            save_kwargs['quality'] = min(quality - 5, 80)

                img.save(output_path, format=pil_format, **save_kwargs)

        except Exception as e:
            raise RuntimeError(f"Failed to convert image: {e}")

    def _report_conversion_results(
        self, input_path: Path, output_path: Path, original_size: int, converted_size: int
    ) -> None:
        """Report conversion results including file size changes."""

        def format_size(size_bytes: int) -> str:
            """Format file size in human readable format."""
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size_bytes < 1024.0:
                    return f"{size_bytes:.1f} {unit}"
                size_bytes /= 1024.0
            return f"{size_bytes:.1f} TB"

        size_change = converted_size - original_size

        if self.command.options.verbose or abs(size_change) > original_size * 0.05:
            print(f"✓ Conversion complete: {input_path.name} → {output_path.name}")
            print(f"  Original:  {format_size(original_size)}")
            print(f"  Converted: {format_size(converted_size)}")

            if size_change < 0:
                reduction = abs(size_change)
                reduction_pct = ((original_size - converted_size) / original_size) * 100
                print(f"  📉 Reduced by {format_size(reduction)} ({reduction_pct:.1f}% smaller)")
            elif size_change > 0:
                increase_pct = ((converted_size - original_size) / original_size) * 100
                print(f"  📈 Increased by {format_size(size_change)} ({increase_pct:.1f}% larger)")
            else:
                print(f"  ➡️  Same file size")
        else:
            print(f"✓ Successfully converted {input_path} to {output_path}")
