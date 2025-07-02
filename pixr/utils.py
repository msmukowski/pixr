import re


def parse_size(size_str: str) -> int:
    """Converts size strings like '500KB', '2MB' into bytes."""
    size_str = size_str.strip().upper()
    units = {"B": 1, "KB": 1024, "MB": 1024**2}

    match = re.match(r"^(\d+\.?\d*)\s*([KM]?B)$", size_str)
    if not match:
        if size_str.isdigit():
            return int(size_str)
        raise ValueError(f"Invalid size format: '{size_str}'")

    value, unit = match.groups()
    return int(float(value) * units[unit])
