import pytest

from gif_sizer.command.core import CmdArgument, CmdOptions, Command
from gif_sizer.runner_factory import RunnerFactory


@pytest.mark.parametrize(
    "command, expected_runner",
    [
        (
            Command(
                CmdArgument(**{"resize": "resize"}),
                CmdOptions(**{"percentage": 50, "verbose": False}),
            ),
            None,
        ),
        (
            Command(
                CmdArgument(**{"rescale": "rescale"}),
                CmdOptions(**{"percentage": 50, "verbose": False}),
            ),
            None,
        ),
    ],
)
def test_runner_factory(command, expected_runner):
    runner = RunnerFactory.create_runner(command)
    assert runner == expected_runner
