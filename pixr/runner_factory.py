from pixr.command.core import Command
from pixr.runners.convert import ConvertRunner
from pixr.runners.rescale import RescaleRunner
from pixr.runners.resize import ResizeRunner


class RunnerFactory:
    @staticmethod
    def create_runner(command: Command):
        argument = command.argument
        if argument == "resize":
            return ResizeRunner(command)
        elif argument == "rescale":
            return RescaleRunner(command)
        elif argument == "convert":
            return ConvertRunner(command)

        raise ValueError(f"Unhandled creation command argument: '{argument}'!")
