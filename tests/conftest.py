import sys
from pathlib import Path

import pytest  # noqa
from PIL import Image, ImageSequence


def pytest_configure():
    package_path = Path(__file__).resolve().parents[1]
    sys.path.append(str(package_path))


@pytest.fixture
def static_image_path(tmp_path: Path) -> Path:
    """Create a dummy static image file and return its path."""
    file_path = tmp_path / "static.png"
    img = Image.new("RGB", (100, 80), color="red")
    img.save(file_path, "PNG")
    return file_path


@pytest.fixture
def animated_gif_path(tmp_path: Path) -> Path:
    """Create a dummy animated GIF file and return its path."""
    file_path = tmp_path / "animated.gif"
    frames = []
    for color in ["red", "green", "blue"]:
        frame = Image.new("RGB", (100, 80), color=color)
        frames.append(frame)
    
    frames[0].save(
        file_path,
        save_all=True,
        append_images=frames[1:],
        duration=100,
        loop=0
    )
    return file_path
