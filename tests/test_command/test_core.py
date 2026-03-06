import pytest

from pixr.command.core import CmdOptions, Command, CommandType
from pixr.command.exceptions import NoSuchArgument, PercentageRangeError

ACCEPTED_ARGUMENTS = ["rescale", "convert", "anonymize"]


@pytest.fixture(params=ACCEPTED_ARGUMENTS)
def argument(request) -> str:
    return request.param


@pytest.fixture(params=range(1, 101, 33))
def cmd_options(request) -> CmdOptions:
    return CmdOptions(verbose=False, percentage=request.param, file_path="/test/path.jpg")


class TestCommandCore:
    def test_from_cli(self, argument: str, cmd_options: CmdOptions):
        command = Command.from_cli(argument, cmd_options.model_dump())
        expected_cmd = Command(CommandType(argument), cmd_options)
        assert command.argument == expected_cmd.argument
        assert command == expected_cmd

    def test_from_cli_unknown_argument_raises(self):
        with pytest.raises(NoSuchArgument, match="Unknown command: 'nonexistent'"):
            Command.from_cli("nonexistent", {"verbose": False, "file_path": "/test/path.jpg"})

    @pytest.mark.parametrize("corrupted_percentage", [0, 101])
    def test_cmd_options_with_corrupted_percentage(self, corrupted_percentage: int):
        with pytest.raises(PercentageRangeError):
            CmdOptions(verbose=False, percentage=corrupted_percentage, file_path="/test/path.jpg")
