import subprocess

import pytest


@pytest.mark.parametrize(
    ("cmd",),
    [
        pytest.param(["walker"], id="without-help-option"),
        pytest.param(["walker", "--help"], id="with-help-option"),
    ],
)
def test_server_help(cmd: list[str]):
    ret = subprocess.run(cmd, capture_output=True)
    assert ret.returncode == 0
    ret_stdout = ret.stdout.decode()
    assert ret_stdout.startswith("Usage: walker [OPTIONS]")
    assert "--config PATH" in ret_stdout
    assert "--host TEXT" in ret_stdout
    assert "--port INTEGER" in ret_stdout
