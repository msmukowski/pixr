from pixr.formats import SUPPORTED_FORMATS, TARGET_SIZE_FORMATS


def test_target_size_formats_are_subset_of_supported():
    """TARGET_SIZE_FORMATS must only contain formats present in SUPPORTED_FORMATS."""
    supported_pil_names = set(SUPPORTED_FORMATS.values())
    assert TARGET_SIZE_FORMATS.issubset(supported_pil_names)
