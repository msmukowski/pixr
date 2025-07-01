from pathlib import Path

import pytest
from PIL import Image, ImageSequence

from pixr.command.core import CmdOptions, Command
from pixr.runners.rescale import RescaleRunner


def test_rescale_static_image(static_image_path: Path):
    """Test rescaling a static PNG image."""
    percentage = 50
    command = Command.from_cli(
        "rescale",
        {
            "file_path": str(static_image_path),
            "percentage": percentage,
            "verbose": False,
        },
    )
    
    runner = RescaleRunner(command)
    runner.run()

    output_path = static_image_path.parent / f"{static_image_path.stem}_rescaled_{percentage}pct.png"
    assert output_path.exists()

    with Image.open(output_path) as img:
        assert img.width == 50
        assert img.height == 40
        assert not getattr(img, 'is_animated', False)


def test_rescale_animated_gif(animated_gif_path: Path):
    """Test rescaling an animated GIF."""
    percentage = 25
    command = Command.from_cli(
        "rescale",
        {
            "file_path": str(animated_gif_path),
            "percentage": percentage,
            "verbose": False,
        },
    )
    
    runner = RescaleRunner(command)
    runner.run()

    output_path = animated_gif_path.parent / f"{animated_gif_path.stem}_rescaled_{percentage}pct.gif"
    assert output_path.exists()

    with Image.open(output_path) as img:
        assert img.width == 25
        assert img.height == 20
        assert getattr(img, 'is_animated', False)
        assert img.n_frames == 3

        frame_dims = [(frame.width, frame.height) for frame in ImageSequence.Iterator(img)]
        assert all(dim == (25, 20) for dim in frame_dims) 