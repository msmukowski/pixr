from gif_sizer.command.core import Command


class RunnerFactory:
    @staticmethod
    def create_runner(command: Command):
        argument = command.argument.value
        if argument == "resize":
            return
        elif argument == "rescale":
            return

        raise ValueError(f"Unhandled creation command argument: '{argument}'!")
