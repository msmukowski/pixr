from click.testing import CliRunner

from pixr.__main__ import cli


def test_bad_quality_produces_clean_error():
    """Bad quality value should show a user-friendly error, not a traceback."""
    runner = CliRunner()
    result = runner.invoke(cli, ['convert', '/dev/null', '-f', 'png', '-q', '150'])

    assert result.exit_code != 0
    assert 'Quality must be between 1-100' in result.output
    assert 'Error' in result.output
    assert 'Traceback' not in result.output


def test_bad_percentage_produces_clean_error():
    """Bad percentage value should show a user-friendly error, not a traceback."""
    runner = CliRunner()
    result = runner.invoke(cli, ['rescale', '/dev/null', '-p', '200'])

    assert result.exit_code != 0
    assert 'outside the allowed range' in result.output
    assert 'Error' in result.output
    assert 'Traceback' not in result.output


def test_unsupported_format_produces_clean_error():
    """Unsupported target format should show a user-friendly error, not a traceback."""
    runner = CliRunner()
    result = runner.invoke(cli, ['convert', '/dev/null', '-f', 'xyz'])

    assert result.exit_code != 0
    assert 'Unsupported target format' in result.output
    assert 'Traceback' not in result.output
