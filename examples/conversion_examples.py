#!/usr/bin/env python3
"""
PIXR Conversion Examples

This script demonstrates how to use the new image conversion functionality.
Run with `python examples/conversion_examples.py` to see the available CLI commands.
"""

USAGE_EXAMPLES = """
🎨 PIXR - Image Processing Tool
==================================================

📋 Available Commands:
  • resize   - Resize image to specific dimensions
  • rescale  - Resize image by percentage
  • convert  - Convert between image formats

🔄 Conversion Examples:
------------------------------

1. Convert PNG to WebP (basic):
   python pixr convert --file-path input.png --target-format webp

2. Convert PNG to WebP with high quality:
   python pixr convert --file-path input.png --target-format webp --quality 95

3. Convert JPEG to PNG (preserve transparency):
   python pixr convert --file-path photo.jpg --target-format png

4. Convert with custom output path:
   python pixr convert --file-path input.png --target-format webp --output-path /custom/path/output.webp

5. Convert with verbose output:
   python pixr convert --file-path input.png --target-format webp --verbose

📏 Resize/Rescale Examples:
------------------------------

6. Resize image by percentage:
   python pixr rescale --file-path image.jpg --percentage 50

7. Resize image to specific dimensions:
   python pixr resize --file-path image.jpg --percentage 75

✅ Supported Formats:
--------------------
   Input:  PNG, JPEG, GIF, BMP, TIFF, WebP
   Output: PNG, JPEG, WebP, BMP, TIFF, GIF

💡 Tips:
----------
   • Use --quality 1-100 for lossy formats (JPEG, WebP)
   • WebP offers better compression than PNG/JPEG
   • PNG supports transparency, JPEG does not
   • Use --verbose for detailed processing information
"""

API_EXAMPLES = """
🔧 Programmatic Usage:
==============================

```python
from pixr.command.core import Command, CmdArgument, CmdOptions
from pixr.runner_factory import RunnerFactory

# Convert PNG to WebP
command = Command(
    CmdArgument(convert='convert'),
    CmdOptions(
        verbose=True,
        percentage=50,  # Required but not used for convert
        file_path='input.png',
        target_format='webp',
        quality=90
    )
)

runner = RunnerFactory.create_runner(command)
runner.run()
```
"""

if __name__ == "__main__":
    print(USAGE_EXAMPLES)
    print(API_EXAMPLES)