from __future__ import annotations

import pathlib

import jubilant as real_jubilant
import pytest

import jubilant_backports as jubilant
from jubilant_backports._juju import Juju29

from . import helpers


@pytest.fixture(scope='module', autouse=True)
def setup(juju: Juju29):
    juju.deploy(helpers.find_charm('testdb'), base='ubuntu@22.04')
    juju.wait(
        lambda status: status.apps['testdb'].units['testdb/0'].workload_status.current == 'unknown'
    )


def test_run_success(juju: Juju29):
    juju.config('testdb', {'testoption': 'foobar'})

    task = juju.run('testdb/0', 'do-thing', {'param1': 'value1'})
    assert task.success
    assert task.return_code == 0
    assert task.results == {
        'config': {'testoption': 'foobar'},
        'params': {'param1': 'value1'},
        'thingy': 'foo',
    }


def test_run_error(juju: Juju29):
    with pytest.raises((jubilant.TaskError, real_jubilant.TaskError)) as excinfo:
        juju.run('testdb/0', 'do-thing', {'error': 'ERR'})
    task = excinfo.value.task
    assert not task.success
    assert task.status == 'failed'  # type: ignore
    assert task.return_code == 0  # return_code is 0 even if action fails
    assert task.message == 'failed with error: ERR'  # type: ignore


def test_run_exception(juju: Juju29):
    with pytest.raises((jubilant.TaskError, real_jubilant.TaskError)) as excinfo:
        juju.run('testdb/0', 'do-thing', {'exception': 'EXC'})
    task = excinfo.value.task
    assert not task.success
    assert task.status == 'failed'  # type: ignore
    assert task.return_code != 0
    assert 'EXC' in task.stderr


def test_run_timeout(juju: Juju29):
    with pytest.raises(TimeoutError):
        juju.run('testdb/0', 'do-thing', wait=0.001)


def test_run_action_not_defined(juju: Juju29):
    with pytest.raises(ValueError):
        juju.run('testdb/0', 'action-not-defined')


def test_run_unit_not_found(juju: Juju29):
    with pytest.raises(ValueError):
        juju.run('testdb/42', 'do-thing')


def test_exec_success(juju: Juju29):
    task = juju.exec('echo foo', unit='testdb/0')
    assert task.success
    assert task.return_code == 0
    assert task.stdout == 'foo\n'
    assert task.stderr == ''

    task = juju.exec('echo', 'bar', 'baz', unit='testdb/0')
    assert task.success
    assert task.stdout == 'bar baz\n'


def test_exec_error(juju: Juju29):
    with pytest.raises((jubilant.TaskError, real_jubilant.TaskError)) as excinfo:
        juju.exec('sleep x', unit='testdb/0')
    task = excinfo.value.task
    assert not task.success
    assert task.stdout == ''
    assert 'invalid time' in task.stderr


def test_exec_timeout(juju: Juju29):
    with pytest.raises(TimeoutError):
        juju.exec('sleep 1', unit='testdb/0', wait=0.001)


def test_exec_unit_not_found(juju: Juju29):
    with pytest.raises(ValueError):
        juju.exec('echo foo', unit='testdb/42')


def test_exec_error_machine_on_k8s(juju: Juju29):
    with pytest.raises(jubilant.CLIError):
        juju.exec('echo foo', machine=0)


def test_ssh_and_scp(juju: Juju29):
    # The 'testdb' charm doesn't have any containers, so use 'snappass-test'.
    juju.deploy('snappass-test')
    juju.wait(lambda status: jubilant.all_active(status, 'snappass-test'))

    output = juju.ssh('snappass-test/0', 'ls', '/charm/containers')
    assert output.split() == ['redis', 'snappass']
    expected_pebble = 'pebble' if juju.cli_major_version >= 3 else 'pebble.socket'
    output = juju.ssh('snappass-test/0', 'ls', '/charm/container', container='snappass')
    assert expected_pebble in output.split()
    output = juju.ssh('snappass-test/0', 'ls', '/charm/container', container='redis')
    assert expected_pebble in output.split()

    juju.scp('snappass-test/0:agents/unit-snappass-test-0/charm/src/charm.py', 'charm.py')
    charm_src = pathlib.Path('charm.py').read_text()
    assert 'class Snappass' in charm_src

    juju.scp('snappass-test/0:/etc/passwd', 'passwd', container='redis')
    passwd = pathlib.Path('passwd').read_text()
    assert 'redis:' in passwd


def test_cli_input(juju: Juju29):
    stdout = juju.cli('ssh', '--container', 'charm', 'testdb/0', 'cat', stdin='foo')
    assert stdout == 'foo'
