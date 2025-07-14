from __future__ import annotations

import pytest

import jubilant_backports as jubilant

from . import mocks


@pytest.mark.parametrize('juju_version', ['2.9.52', '3.6.8'])
def test_completed(juju_version: str, run: mocks.Run):
    out_json = """
{
  "mysql/0": {
    "id": "42",
    "log": [
      "2025-03-01 16:23:26 +1300 NZDT Log message",
      "2025-03-01 16:23:26 +1300 NZDT Another message"
    ],
    "results": {
      "password": "pass",
      "return-code": 0,
      "username": "user",
      "stdout": "OUT",
      "stderr": "ERR"
    },
    "status": "completed"
  }
}
"""
    run.handle(
        [
            'juju',
            'run-action' if juju_version[0] == '2' else 'run',
            '--format',
            'json',
            'mysql/0',
            'get-password',
        ],
        stdout=out_json,
    )
    juju = jubilant.Juju(cli_version=juju_version)

    task = juju.run('mysql/0', 'get-password')

    assert task == jubilant.Task(
        id='42',
        status='completed',
        results={'username': 'user', 'password': 'pass'},
        return_code=0,
        stdout='OUT',
        stderr='ERR',
        log=[
            '2025-03-01 16:23:26 +1300 NZDT Log message',
            '2025-03-01 16:23:26 +1300 NZDT Another message',
        ],
    )
    assert task.success
