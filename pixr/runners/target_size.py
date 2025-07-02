import io
import re

from PIL import Image

from pixr.runners import BaseRunner


class TargetSizeRunner(BaseRunner):
    def _parse_size(self, size_str: str) -> int:
        """Converts size strings like '500KB', '2MB' into bytes."""
        size_str = size_str.strip().upper()
        units = {"B": 1, "KB": 1024, "MB": 1024**2}

        match = re.match(r"^(\d+\.?\d*)\s*([KM]?B)$", size_str)
        if not match:
            if size_str.isdigit():
                return int(size_str)
            raise ValueError(f"Invalid size format: '{self.command.options.max_size}'")

        value, unit = match.groups()
        return int(float(value) * units[unit])

    def run(self) -> None:
        """
        Adjusts an image's compression to meet a target file size.
        """
        input_path = self._validate_input_file()
        if self.command.options.max_size is None:
            raise ValueError("max_size must be provided for target-size command.")
        target_bytes = self._parse_size(self.command.options.max_size)
        wild_mode = self.command.options.wild

        with Image.open(input_path) as img:
            if getattr(img, "is_animated", False):
                raise NotImplementedError("Target size for animated images is not supported.")

            result = self._optimize_image(img, target_bytes, wild_mode, input_path.suffix)

            best_result_data = result["best_result_data"]
            best_quality = result["best_quality"]

            output_path = self._determine_output_path(suffix="_targeted", extension=".jpg")

            if best_result_data:
                with open(output_path, "wb") as f:
                    f.write(best_result_data)

                original_size_kb = input_path.stat().st_size / 1024
                final_size_bytes = len(best_result_data)
                final_size_kb = final_size_bytes / 1024

                if final_size_bytes > target_bytes:
                    print(
                        f"ℹ️ Could not meet target of {target_bytes / 1024:.0f}KB while maintaining min quality. "
                        f"Best result: {final_size_kb:.0f}KB (quality: {best_quality}). Output: {output_path}"
                    )
                else:
                    print(
                        f"✓ Target size achieved: {original_size_kb:.0f}KB → {final_size_kb:.0f}KB "
                        f"(quality: {best_quality}). Output: {output_path}"
                    )
            else:
                smallest_size_kb = result["smallest_size"] / 1024
                print(
                    f"❌ Could not meet target of {target_bytes / 1024:.0f}KB. "
                    f"Smallest possible size is {smallest_size_kb:.0f}KB."
                )

    def _optimize_image(self, img: Image.Image, target_bytes: int, wild_mode: bool, original_extension: str):
        """
        Performs a binary search to find the optimal quality setting.
        """
        low = 1
        high = 100
        min_quality = 1 if wild_mode else 50
        best_result_data = None
        best_quality = -1
        iterations = 0
        max_iterations = 10  # Safety break
        smallest_size_so_far = float('inf')
        smallest_size_data = None
        smallest_size_quality = -1
        quality_floor_hit = False

        # For formats that don't support 'quality', we can't do much.
        # We will effectively convert them to JPEG for the optimization.
        save_format = 'JPEG'

        # Pillow needs RGB for JPEG saving
        if img.mode != 'RGB':
            img = img.convert('RGB')

        while low <= high and iterations < max_iterations:
            iterations += 1
            mid_quality = (low + high) // 2

            if mid_quality < min_quality:
                quality_floor_hit = True
                break

            with io.BytesIO() as buffer:
                img.save(buffer, format=save_format, quality=mid_quality, optimize=True)
                current_size = buffer.tell()

                if current_size < smallest_size_so_far:
                    smallest_size_so_far = current_size
                    smallest_size_data = buffer.getvalue()
                    smallest_size_quality = mid_quality

                if current_size <= target_bytes:
                    best_result_data = buffer.getvalue()
                    best_quality = mid_quality
                    # Try for better quality
                    low = mid_quality + 1
                else:
                    # Need to lower quality
                    high = mid_quality - 1

        # If we never found a result under the target, the "best" result
        # is the one with the smallest file size we generated.
        if not best_result_data and smallest_size_data:
            best_result_data = smallest_size_data
            best_quality = smallest_size_quality

        return {
            "best_result_data": best_result_data,
            "best_quality": best_quality,
            "smallest_size": smallest_size_so_far,
            "quality_floor_hit": quality_floor_hit,
        }
