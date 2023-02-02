from gif_sizer.command.core import Command
from gif_sizer.runners.rescale import RescaleRunner
from gif_sizer.runners.resize import ResizeRunner


class RunnerFactory:
    @staticmethod
    def create_runner(command: Command):
        argument = command.argument.value
        if argument == "resize":
            return ResizeRunner(command)
        elif argument == "rescale":
            return RescaleRunner(command)

        raise ValueError(f"Unhandled creation command argument: '{argument}'!")
