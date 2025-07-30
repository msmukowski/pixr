from pathlib import Path
from PIL import Image


def purify_image(input_path: Path, output_path: Path) -> bool:
    """
    Removes all metadata from an image by saving its pixels to a new file.

    Args:
        input_path: Path to the source image.
        output_path: Path to save the purified image.

    Returns:
        True if purification was successful, False otherwise.
    """
    if not input_path.is_file():
        print(f"Input file not found: {input_path}")
        return False

    try:
        with Image.open(input_path) as img:
            # Create a new image with the same mode and size, filled with the pixel data.
            # This effectively strips all metadata (like EXIF, XMP, etc.).
            purified_img = Image.new(img.mode, img.size)
            purified_img.putdata(list(img.getdata()))

            # Save the new image, ensuring no metadata is carried over.
            purified_img.save(output_path, format=img.format)

            return True

    except (IOError, OSError) as e:
        print(f"Could not process file {input_path}. It might not be a valid image. Error: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False
