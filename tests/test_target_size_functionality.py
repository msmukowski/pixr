import subprocess
from pathlib import Path

import pytest


@pytest.fixture
def run_pixr():
    def _run_pixr(args):
        base_args = ["python", "-m", "pixr"]
        return subprocess.run(base_args + args, capture_output=True, text=True, check=True)

    return _run_pixr


def test_target_size_success(run_pixr, image_file_factory):
    """
    Test that the target-size command can successfully reduce an image's size.
    """
    input_file: Path = image_file_factory("test_success.jpg", size=(1200, 800), color="blue")
    output_file = input_file.with_name("test_success_targeted.jpg")
    target_size_kb = 50
    target_size_str = f"{target_size_kb}KB"

    result = run_pixr(["target-size", str(input_file), "--max-size", target_size_str])

    assert output_file.exists()
    assert "✓ Target size achieved" in result.stdout

    output_size_bytes = output_file.stat().st_size
    assert output_size_bytes <= target_size_kb * 1024

    output_file.unlink()


def test_target_size_partial_success_quality_floor(run_pixr, image_file_factory):
    """
    Test that the runner produces the best possible result when the target
    cannot be met without violating the default quality floor (50).
    """
    input_file: Path = image_file_factory("test_partial.jpg", size=(2400, 1800), color="red")
    output_file = input_file.with_name("test_partial_targeted.jpg")
    target_size_kb = 10
    target_size_str = f"{target_size_kb}KB"

    result = run_pixr(["target-size", str(input_file), "--max-size", target_size_str])

    assert output_file.exists()
    assert "ℹ️ Could not meet target" in result.stdout
    assert "while maintaining min quality" in result.stdout

    output_size_bytes = output_file.stat().st_size
    assert output_size_bytes > target_size_kb * 1024

    output_file.unlink()


def test_target_size_wild_mode(run_pixr, image_file_factory):
    """
    Test that --wild mode ignores the quality floor to meet the target.
    """
    input_file: Path = image_file_factory("test_wild.jpg", size=(800, 600), color="green")
    output_file = input_file.with_name("test_wild_targeted.jpg")
    target_size_kb = 10
    target_size_str = f"{target_size_kb}KB"

    result = run_pixr(["target-size", str(input_file), "--max-size", target_size_str, "--wild"])

    assert output_file.exists()
    assert "✓ Target size achieved" in result.stdout

    output_size_bytes = output_file.stat().st_size
    assert output_size_bytes <= target_size_kb * 1024

    output_file.unlink()


def test_target_size_unsupported_format(run_pixr, image_file_factory):
    """
    Test that the command fails gracefully for unsupported file types.
    """
    input_file: Path = image_file_factory("test_unsupported.tiff", size=(100, 100), fmt="TIFF")

    with pytest.raises(subprocess.CalledProcessError) as excinfo:
        run_pixr(["target-size", str(input_file), "--max-size", "10KB"])

    assert "Input file format 'TIFF' is not supported" in excinfo.value.stderr
