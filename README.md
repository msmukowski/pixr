# PIXR

A modern, command-line tool for fast and efficient image processing.

PIXR provides a suite of tools for common image manipulation tasks, including format conversion, dimension rescaling, and file size optimization. It's designed to be simple, scriptable, and powerful.

## Key Features

- **Convert**: Change image formats between PNG, JPEG, WEBP, and more.
- **Rescale**: Change the pixel dimensions of an image by a percentage.
- **Target Size**: Optimize an image's file size to be at or below a specific threshold (e.g., "250KB").
- **GIF Support**: Correctly handles rescaling animated GIFs, preserving their animations.

## Usage

PIXR uses a command-group structure. The main commands are:

```sh
pixr --help
Usage: pixr [OPTIONS] COMMAND [ARGS]...

  A modern, command-line tool for fast and efficient image processing.

Options:
  --help  Show this message and exit.

Commands:
  convert      Convert an image from one format to another.
  rescale      Rescale an image's dimensions by a percentage.
  target-size  Optimize an image to be at or below a target file size.
```

### Examples

#### Convert an image to WEBP format

```sh
pixr convert --file-path image.png --target-format webp --quality 80
```

#### Rescale an animated GIF to 50% of its original dimensions

```sh
pixr rescale --file-path animation.gif --percentage 50 --output-path small_animation.gif
```

#### Optimize an image to be under 250 Kilobytes

```sh
pixr target-size --file-path photo.jpg --max-size 250KB
```

## Contributing

Contributions are welcome! This project uses `pipenv` for dependency management.

To set up for development:
1. Clone this repository: `git clone https://github.com/msmukowski/pixr.git`
2. Navigate to the project directory: `cd pixr`
3. Install dependencies: `pipenv install --dev`
4. Activate the virtual environment: `pipenv shell`

For more detailed guidelines, please see the `CONTRIBUTING.md` file (coming soon).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.