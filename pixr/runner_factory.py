from pixr.command.core import Command
from pixr.runners.anonymize import AnonymizeRunner
from pixr.runners.convert import ConvertRunner
from pixr.runners.rescale import RescaleRunner
from pixr.runners.target_size import TargetSizeRunner


class RunnerFactory:
    @staticmethod
    def create_runner(command: Command):
        argument = command.argument
        if argument == "target-size":
            return TargetSizeRunner(command)
        elif argument == "rescale":
            return RescaleRunner(command)
        elif argument == "convert":
            return ConvertRunner(command)
        elif argument == "anonymize":
            return AnonymizeRunner(command)

        raise ValueError(f"Unhandled creation command argument: '{argument}'!")
