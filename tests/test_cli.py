from click.testing import CliRunner

from matrix_interpolator.cli import main


def test_cli_happy_path(tmp_path):
    runner = CliRunner()
    inp = tmp_path / "in.csv"
    out = tmp_path / "out.csv"
    inp.write_text(
        """1,2,3
4,nan,6
7,8,9
"""
    )
    result = runner.invoke(main, [str(inp), str(out)])
    assert result.exit_code == 0
    lines = out.read_text().splitlines()
    assert any("5" in cell for cell in lines[1].split(","))


def test_cli_nonexistent_input():
    runner = CliRunner()
    result = runner.invoke(main, ["nope.csv", "out.csv"])
    assert result.exit_code != 0
