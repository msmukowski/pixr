import pytest

from gif_sizer.command.core import CmdArgument, CmdOptions, Command
from gif_sizer.runner_factory import RunnerFactory
from gif_sizer.runners.rescale import RescaleRunner
from gif_sizer.runners.resize import ResizeRunner


@pytest.mark.parametrize(
    "command, expected_runner",
    [
        (
            Command(
                CmdArgument(**{"resize": "resize"}),
                CmdOptions(**{"percentage": 50, "verbose": False}),
            ),
            ResizeRunner,
        ),
        (
            Command(
                CmdArgument(**{"rescale": "rescale"}),
                CmdOptions(**{"percentage": 50, "verbose": False}),
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
                CmdArgument(**{"resize": "test"}),
                CmdOptions(**{"percentage": 50, "verbose": False}),
            ),
            ValueError,
            "Unhandled creation command argument: 'test'!",
        ),
    ],
)
def test_runner_factory_value_error(command, expected_error, expected_msg):
    with pytest.raises(expected_error, match=expected_msg):
        RunnerFactory.create_runner(command)
