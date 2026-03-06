import pytest

from pixr.command.core import CmdOptions, Command, CommandType
from pixr.command.exceptions import NoSuchArgument
from pixr.runner_factory import RunnerFactory
from pixr.runners.rescale import RescaleRunner
from pixr.runners.target_size import TargetSizeRunner


@pytest.mark.parametrize(
    "command, expected_runner",
    [
        (
            Command(
                CommandType.TARGET_SIZE,
                CmdOptions(max_size="1MB", verbose=False, file_path="/test/path.jpg"),
            ),
            TargetSizeRunner,
        ),
        (
            Command(
                CommandType.RESCALE,
                CmdOptions(percentage=50, verbose=False, file_path="/test/path.jpg"),
            ),
            RescaleRunner,
        ),
    ],
)
def test_runner_factory(command, expected_runner):
    runner = RunnerFactory.create_runner(command)
    assert isinstance(runner, expected_runner)


def test_runner_factory_unknown_command():
    with pytest.raises(NoSuchArgument, match="Unknown command: 'test'"):
        Command.from_cli("test", {"percentage": 50, "verbose": False, "file_path": "/test/path.jpg"})
