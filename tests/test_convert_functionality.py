import pytest

from pixr.command.core import CmdOptions, Command
from pixr.runner_factory import RunnerFactory
from pixr.runners.convert import ConvertRunner


class TestConvertFunctionality:
    """Test the new convert functionality."""

    def test_cmd_options_with_convert_parameters(self):
        """Test CmdOptions with conversion-specific parameters."""
        options = CmdOptions(
            verbose=False, percentage=50, file_path="/path/to/input.png", target_format="webp", quality=90
        )
        assert options.target_format == "webp"
        assert options.quality == 90

    def test_cmd_options_validates_quality_range(self):
        """Test that quality validation works correctly."""
        options = CmdOptions(
            verbose=False, percentage=50, file_path="/path/to/input.png", target_format="webp", quality=85
        )
        assert options.quality == 85

        with pytest.raises(ValueError, match="Quality must be between 1-100"):
            CmdOptions(verbose=False, percentage=50, file_path="/path/to/input.png", target_format="webp", quality=0)

        with pytest.raises(ValueError, match="Quality must be between 1-100"):
            CmdOptions(verbose=False, percentage=50, file_path="/path/to/input.png", target_format="webp", quality=101)

    def test_cmd_options_validates_target_format(self):
        """Test that target format validation works correctly."""
        options = CmdOptions(verbose=False, percentage=50, file_path="/path/to/input.png", target_format="webp")
        assert options.target_format == "webp"

        with pytest.raises(ValueError, match="Unsupported target format"):
            CmdOptions(verbose=False, percentage=50, file_path="/path/to/input.png", target_format="invalid")

    def test_runner_factory_creates_convert_runner(self):
        """Test that RunnerFactory creates ConvertRunner for 'convert' command."""
        command = Command(
            "convert", CmdOptions(verbose=False, percentage=50, file_path="/path/to/input.png", target_format="webp")
        )

        runner = RunnerFactory.create_runner(command)
        assert isinstance(runner, ConvertRunner)

    def test_convert_command_from_cli(self):
        """Test creating a convert command from CLI-like input."""
        command = Command.from_cli(
            "convert",
            {
                "verbose": False,
                "percentage": 50,
                "file_path": "/path/to/input.png",
                "target_format": "webp",
                "quality": 90,
            },
        )

        assert command.argument == "convert"
        assert command.options.target_format == "webp"
        assert command.options.quality == 90
