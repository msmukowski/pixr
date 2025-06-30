from pixr.runners import BaseRunner


class RescaleRunner(BaseRunner):
    def run(self) -> None:
        """Rescale image by percentage."""
        # TODO: Implement image rescaling logic
        input_path = self._validate_input_file()
        output_path = self._determine_output_path(suffix=f"_rescaled_{self.command.options.percentage}pct")

        print(f"Rescaling {input_path} by {self.command.options.percentage}% to {output_path}")
        print("TODO: Implement rescale logic")
