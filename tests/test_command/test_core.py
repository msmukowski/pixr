import pytest

from gif_sizer.command.core import CmdArgument, CmdOptions, Command
from gif_sizer.command.exceptions import (
    NoSuchArgument,
    PercentageRangeError,
    TooManyCommandArguments,
)

ACCEPTED_ARGUMENTS = ["resize", "rescale"]


@pytest.fixture(params=ACCEPTED_ARGUMENTS)
def cmd_argument(request) -> CmdArgument:
    argument = request.param
    return CmdArgument(**{argument: argument})


@pytest.fixture(params=range(0 + 1, 100 + 1, 33))
def cmd_options(request) -> CmdOptions:
    return CmdOptions(**{"verbose": False, "percentage": request.param})


class TestExpectedBehaviour:
    def test_from_cli(self, cmd_argument, cmd_options):
        command = Command(cmd_argument, cmd_options)
        assert command

    @pytest.mark.parametrize(
        "argument, expected_value",
        [
            (CmdArgument(resize="resize"), "resize"),
            (CmdArgument(resize="rescale"), "rescale"),
        ],
    )
    def test_cmd_argument_value(self, argument: CmdArgument, expected_value: str):
        assert argument.value == expected_value


class TestUnexpectedBehaviour:
    @pytest.fixture(params=ACCEPTED_ARGUMENTS)
    def cmd_argument_corrupted(self, request):
        argument = request.param
        corrupted_argument = argument[-1] + argument[:-1]
        return corrupted_argument

    @pytest.fixture(params=[0, 101], ids=["lower_bound", "upper_bound"])
    def corrupted_percentage(self, request) -> int:
        return request.param

    def test_cmd_argument_corrupted_input(self, cmd_argument_corrupted):
        with pytest.raises(NoSuchArgument):
            CmdArgument(**{cmd_argument_corrupted: cmd_argument_corrupted})

    def test_cmd_options_with_corrupted_percentage(self, corrupted_percentage):
        with pytest.raises(PercentageRangeError):
            CmdOptions(**{"verbose": False, "percentage": corrupted_percentage})

    def test_cmd_argument_too_many_arguments(self):
        with pytest.raises(TooManyCommandArguments):
            CmdArgument(resize="resize", rescale="rescale")
