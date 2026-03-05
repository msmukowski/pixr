from pathlib import Path

import pytest
from click.testing import CliRunner

from pixr.__main__ import cli


@pytest.fixture
def cli_runner():
    return CliRunner()


def test_target_size_success(cli_runner, image_file_factory):
    """
    Test that the target-size command can successfully reduce an image's size.
    """
    input_file: Path = image_file_factory("test_success.jpg", size=(1200, 800), color="blue")
    output_file = input_file.with_name("test_success_targeted.jpg")
    target_size_kb = 50
    target_size_str = f"{target_size_kb}KB"

    result = cli_runner.invoke(cli, ["target-size", str(input_file), "--max-size", target_size_str])

    assert result.exit_code == 0, result.output
    assert output_file.exists()
    assert "Target size achieved" in result.output

    output_size_bytes = output_file.stat().st_size
    assert output_size_bytes <= target_size_kb * 1024


def test_target_size_partial_success_quality_floor(cli_runner, image_file_factory):
    """
    Test that the runner produces the best possible result when the target
    cannot be met without violating the default quality floor (50).
    """
    input_file: Path = image_file_factory("test_partial.jpg", size=(2400, 1800), color="red")
    output_file = input_file.with_name("test_partial_targeted.jpg")
    target_size_kb = 10
    target_size_str = f"{target_size_kb}KB"

    result = cli_runner.invoke(cli, ["target-size", str(input_file), "--max-size", target_size_str])

    assert result.exit_code == 0, result.output
    assert output_file.exists()
    assert "Could not meet target" in result.output
    assert "while maintaining min quality" in result.output

    output_size_bytes = output_file.stat().st_size
    assert output_size_bytes > target_size_kb * 1024


def test_target_size_wild_mode(cli_runner, image_file_factory):
    """
    Test that --wild mode ignores the quality floor to meet the target.
    """
    input_file: Path = image_file_factory("test_wild.jpg", size=(800, 600), color="green")
    output_file = input_file.with_name("test_wild_targeted.jpg")
    target_size_kb = 10
    target_size_str = f"{target_size_kb}KB"

    result = cli_runner.invoke(cli, ["target-size", str(input_file), "--max-size", target_size_str, "--wild"])

    assert result.exit_code == 0, result.output
    assert output_file.exists()
    assert "Target size achieved" in result.output

    output_size_bytes = output_file.stat().st_size
    assert output_size_bytes <= target_size_kb * 1024


def test_target_size_unsupported_format(cli_runner, image_file_factory):
    """
    Test that the command fails gracefully for unsupported file types.
    """
    input_file: Path = image_file_factory("test_unsupported.tiff", size=(100, 100), fmt="TIFF")

    result = cli_runner.invoke(cli, ["target-size", str(input_file), "--max-size", "10KB"])

    assert result.exit_code != 0
    assert "Input file format 'TIFF' is not supported" in (result.output + str(result.exception))
