from __future__ import annotations

import pytest

import jubilant_backports as jubilant
from jubilant_backports._juju import Juju29

pytestmark = pytest.mark.machine


@pytest.fixture(scope='module', autouse=True)
def setup(juju: Juju29):
    juju.deploy('ubuntu')
    juju.wait(jubilant.all_active)


def test_exec(juju: Juju29):
    task = juju.exec('echo foo', machine=0)
    assert task.success
    assert task.return_code == 0
    assert task.stdout == 'foo\n'
    assert task.stderr == ''

    task = juju.exec('echo', 'bar', 'baz', machine=0)
    assert task.success
    assert task.stdout == 'bar baz\n'


def test_ssh(juju: Juju29):
    output = juju.ssh('ubuntu/0', 'echo', 'UNIT')
    assert output == 'UNIT\n'

    output = juju.ssh(0, 'echo', 'MACHINE')
    assert output == 'MACHINE\n'


def test_add_and_remove_unit(juju: Juju29):
    juju.add_unit('ubuntu')
    juju.wait(lambda status: jubilant.all_active(status) and len(status.apps['ubuntu'].units) == 2)

    juju.remove_unit('ubuntu/1')
    juju.wait(lambda status: jubilant.all_active(status) and len(status.apps['ubuntu'].units) == 1)
