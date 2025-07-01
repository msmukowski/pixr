# Contributing to PIXR

First off, thank you for considering contributing to PIXR! Any contribution, from bug reports to new features, is greatly appreciated.

## Getting Started

To get started with development, you'll need to set up a local environment. This project uses `pipenv` to manage dependencies and virtual environments.

1.  **Clone the repository**:
    ```sh
    git clone https://github.com/msmukowski/pixr.git
    cd pixr
    ```

2.  **Install dependencies**:
    This command installs all production and development dependencies into a managed virtual environment.
    ```sh
    pipenv install --dev
    ```

3.  **Activate the virtual environment**:
    To work on the project, you need to activate the environment.
    ```sh
    pipenv shell
    ```

## Running Quality Checks

Before committing any code, please run the suite of quality checks to ensure your code is clean, typed, and tested.

-   **Linter (flake8)**:
    ```sh
    pipenv run flake8 pixr tests
    ```
-   **Type Checker (mypy)**:
    ```sh
    pipenv run mypy pixr
    ```
-   **Tests (pytest)**:
    ```sh
    pipenv run pytest
    ```

## Architectural Overview

The project follows a simple, decoupled architecture:

1.  **CLI (`pixr/__main__.py`)**: The entry point, using `click` to define command groups and sub-commands. It parses user input.
2.  **Command Object (`pixr/command/core.py`)**: A `pydantic` model that structures the validated data from the CLI.
3.  **Factory (`pixr/runner_factory.py`)**: A simple function that takes a `Command` object and dispatches it to the correct runner.
4.  **Runners (`pixr/runners/`)**: These are classes that inherit from `BaseRunner` and contain the actual image processing logic for a specific command.

## How to Add a New Command

1.  Create a new runner class in `pixr/runners/` (e.g., `rotate.py` with a `RotateRunner` class).
2.  In your new runner class, inherit from `BaseRunner` and implement the `run()` method.
3.  Add a new sub-command function in `pixr/__main__.py`.
4.  Update the factory in `pixr/runner_factory.py` to include your new command.
5.  Add integration tests for your new runner in the `tests/` directory.

Looking forward to your contributions! 