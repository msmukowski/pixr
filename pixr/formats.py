# CLI name -> PIL format string
SUPPORTED_FORMATS: dict[str, str] = {
    'png': 'PNG',
    'jpg': 'JPEG',
    'jpeg': 'JPEG',
    'webp': 'WEBP',
    'bmp': 'BMP',
    'tiff': 'TIFF',
    'gif': 'GIF',
}

# PIL format names that support target-size optimization
TARGET_SIZE_FORMATS: set[str] = {'PNG', 'JPEG', 'GIF', 'WEBP'}
