import pytest

from pixr.command.core import CmdOptions, Command
from pixr.runner_factory import RunnerFactory
from pixr.runners.rescale import RescaleRunner
from pixr.runners.resize import ResizeRunner


@pytest.mark.parametrize(
    "command, expected_runner",
    [
        (
            Command(
                "resize",
                CmdOptions(percentage=50, verbose=False, file_path="/test/path.jpg"),
            ),
            ResizeRunner,
        ),
        (
            Command(
                "rescale",
                CmdOptions(percentage=50, verbose=False, file_path="/test/path.jpg"),
            ),
            RescaleRunner,
        ),
    ],
)
def test_runner_factory(command, expected_runner):
    runner = RunnerFactory.create_runner(command)
    assert isinstance(runner, expected_runner)


@pytest.mark.parametrize(
    "command, expected_error, expected_msg",
    [
        (
            Command(
                "test",
                CmdOptions(percentage=50, verbose=False, file_path="/test/path.jpg"),
            ),
            ValueError,
            "Unhandled creation command argument: 'test'!",
        ),
    ],
)
def test_runner_factory_value_error(command, expected_error, expected_msg):
    with pytest.raises(expected_error, match=expected_msg):
        RunnerFactory.create_runner(command)
