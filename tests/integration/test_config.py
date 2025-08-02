from __future__ import annotations

import contextlib

import pytest

from jubilant_backports._juju import Juju29

from . import helpers


@pytest.fixture(scope='module', autouse=True)
def setup(juju: Juju29):
    juju.deploy(helpers.find_charm('testdb'), base='ubuntu@22.04')
    juju.wait(
        lambda status: status.apps['testdb'].units['testdb/0'].workload_status.current == 'unknown'
    )


def test_config(juju: Juju29):
    config = juju.config('testdb')
    assert config['testoption'] == ''

    juju.config('testdb', {'testoption': 'foobar'})
    config = juju.config('testdb')
    assert config['testoption'] == 'foobar'

    juju.config('testdb', reset=['testoption'])
    config = juju.config('testdb')
    assert config['testoption'] == ''


@contextlib.contextmanager
def fast_forward(juju: Juju29):
    """Context manager that temporarily speeds up update-status hooks."""
    juju.model_config({'update-status-hook-interval': '10s'})
    try:
        yield
    finally:
        juju.model_config(reset=['update-status-hook-interval'])


def test_model_config(juju: Juju29):
    assert juju.model_config()['update-status-hook-interval'] == '5m'
    with fast_forward(juju):
        assert juju.model_config()['update-status-hook-interval'] == '10s'
    assert juju.model_config()['update-status-hook-interval'] == '5m'


def test_trust(juju: Juju29):
    app_config = juju.config('testdb', app_config=True)
    assert app_config['trust'] is False

    # Test that the "trust" app_config value updates.
    juju.trust('testdb', scope='cluster')
    app_config = juju.config('testdb', app_config=True)
    assert app_config['trust'] is True

    juju.trust('testdb', remove=True, scope='cluster')
    app_config = juju.config('testdb', app_config=True)
    assert app_config['trust'] is False
