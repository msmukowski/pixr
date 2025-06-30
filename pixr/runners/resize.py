from pixr.runners import BaseRunner


class ResizeRunner(BaseRunner):
    def run(self) -> None:
        """Resize image to specific dimensions."""
        # TODO: Implement image resizing logic
        input_path = self._validate_input_file()
        output_path = self._determine_output_path(suffix="_resized")

        print(f"Resizing {input_path} to {output_path}")
        print("TODO: Implement resize logic")
