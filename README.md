# GIF-Sizer

GIF-Sizer is an application that takes an animated GIF and resizes it to a certain size in dimensions or weight depending on the user's input configuration.

## Prerequisites

- Python 3.7+
- Pipenv

## Installing

1. Clone this repository: `git clone https://github.com/msmukowski/gif-sizer.git`
2. Install Pipenv: `pip install pipenv`
3. Navigate to the project directory: `cd gif-sizer`
4. Install the project dependencies with Pipenv: `pipenv install`

## Running the Application

1. Activate the virtual environment: `pipenv shell`
2. Run the application with the specified options and flags:
```python
python gif-sizer [OPTION...]
```

## Configuration

The user can specify the input file name, output directory, and size percentage to resize the GIF by providing options and flags when running the application (e.g. `python gif-sizer -i my-image.gif -d my-output-directory -s 50%`).

## Contributing

Please feel free to contribute to this project by submitting a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.