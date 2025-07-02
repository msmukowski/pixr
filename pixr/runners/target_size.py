from PIL import Image

from pixr.runners import BaseRunner
from pixr.strategies.factory import StrategyFactory
from pixr.utils import parse_size


class TargetSizeRunner(BaseRunner):
    def run(self) -> None:
        """
        Adjusts an image's compression to meet a target file size
        by delegating to a format-specific strategy.
        """
        input_path = self._validate_input_file()
        if self.command.options.max_size is None:
            raise ValueError("max_size must be provided for the target-size command.")
        target_bytes = parse_size(self.command.options.max_size)
        wild_mode = self.command.options.wild

        with Image.open(input_path) as img:
            allowed_formats = ['PNG', 'JPEG', 'GIF', 'WEBP']
            if img.format.upper() not in allowed_formats:
                raise ValueError(
                    f"Input file format '{img.format}' is not supported for target-size. "
                    f"Supported formats are: {', '.join(allowed_formats)}."
                )

            if getattr(img, "is_animated", False) and img.format.upper() != 'GIF':
                raise NotImplementedError("Target size for animated images (except GIF) is not supported.")

            strategy = StrategyFactory.get_strategy(img, target_bytes, wild_mode)
            result = strategy.optimize()

            best_result_data = result["best_result_data"]
            best_params = result["best_params"]

            output_extension = f".{img.format.lower()}"
            if img.format.upper() == 'JPEG':
                output_extension = ".jpg"

            output_path = self._determine_output_path(suffix="_targeted", extension=output_extension)

            if best_result_data:
                with open(output_path, "wb") as f:
                    f.write(best_result_data)

                original_size_kb = input_path.stat().st_size / 1024
                final_size_bytes = len(best_result_data)
                final_size_kb = final_size_bytes / 1024

                quality_info = ""
                if "quality" in best_params:
                    quality_info = f"(quality: {best_params['quality']})"
                elif "info" in best_params:
                    quality_info = f"({best_params['info']})"

                if final_size_bytes > target_bytes:
                    print(
                        f"ℹ️ Could not meet target of {target_bytes / 1024:.0f}KB while maintaining min quality. "
                        f"Best result: {final_size_kb:.0f}KB {quality_info}. Output: {output_path}"
                    )
                else:
                    print(
                        f"✓ Target size achieved: {original_size_kb:.0f}KB → {final_size_kb:.0f}KB "
                        f"{quality_info}. Output: {output_path}"
                    )
            else:
                smallest_size_kb = result["smallest_size"] / 1024
                print(
                    f"❌ Could not meet target of {target_bytes / 1024:.0f}KB. "
                    f"Smallest possible size is {smallest_size_kb:.0f}KB."
                )
