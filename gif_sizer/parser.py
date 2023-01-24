import click

@click.command(help='Resize an animated GIF')
@click.argument('command')
@click.option('--verbose', '-v', help='Enable verbose output', is_flag=True)
@click.option('--downscale', type=bool, help='Downscale GIF format')
def parse_command(command, verbose, downscale) -> dict:
    if command == 'resize':
        return {
            'verbose': verbose,
            'dowscale': downscale,
        }
    
    raise NotImplementedError("Only one command is permitted: 'resize'")