from pixr.command.core import Command, CommandType
from pixr.runners.anonymize import AnonymizeRunner
from pixr.runners.base import BaseRunner
from pixr.runners.convert import ConvertRunner
from pixr.runners.rescale import RescaleRunner
from pixr.runners.target_size import TargetSizeRunner


class RunnerFactory:
    _runners: dict[CommandType, type[BaseRunner]] = {
        CommandType.TARGET_SIZE: TargetSizeRunner,
        CommandType.RESCALE: RescaleRunner,
        CommandType.CONVERT: ConvertRunner,
        CommandType.ANONYMIZE: AnonymizeRunner,
    }

    @staticmethod
    def create_runner(command: Command):
        runner_cls = RunnerFactory._runners.get(command.argument)
        if not runner_cls:
            raise ValueError(f"Unhandled creation command argument: '{command.argument}'!")
        return runner_cls(command)
