# PIXR

PIXR is an image processing application that handles various image operations including resizing, type conversion, and more, supporting multiple image formats.

## Prerequisites

- Python 3.7+
- Pipenv

## Installing

1. Clone this repository: `git clone https://github.com/msmukowski/pixr.git`
2. Install Pipenv: `pip install pipenv`
3. Navigate to the project directory: `cd pixr`
4. Install the project dependencies with Pipenv: `pipenv install`

## Running the Application

1. Activate the virtual environment: `pipenv shell`
2. Run the application with the specified options and flags:
```python
python pixr [OPTION...]
```

## Configuration

The user can specify the input file name, output directory, and size percentage to resize the image by providing options and flags when running the application (e.g. `python pixr -i my-image.jpg -d my-output-directory -s 50%`).

## Contributing

Please feel free to contribute to this project by submitting a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.