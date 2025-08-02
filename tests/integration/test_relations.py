from __future__ import annotations

import jubilant as real_jubilant

import jubilant_backports as jubilant
from jubilant_backports._juju import Juju29

from . import helpers


def test_integrate_and_remove_relation(juju: Juju29):
    juju.deploy(helpers.find_charm('testdb'), base='ubuntu@22.04')
    juju.deploy(helpers.find_charm('testapp'), base='ubuntu@22.04')

    juju.integrate('testdb', 'testapp')
    status = juju.wait(jubilant.all_active)
    if juju.cli_major_version == 2:
        assert status.apps['testdb'].relations['db'][0] == 'testapp'
        assert status.apps['testapp'].relations['db'][0] == 'testdb'
    else:
        assert isinstance(status, real_jubilant.Status)
        assert status.apps['testdb'].relations['db'][0].related_app == 'testapp'
        assert status.apps['testapp'].relations['db'][0].related_app == 'testdb'
    assert status.apps['testdb'].app_status.message == 'relation created'
    assert status.apps['testapp'].app_status.message == 'relation changed: dbkey=dbvalue'

    juju.remove_relation('testdb', 'testapp')
    juju.wait(
        lambda status: (
            not status.apps['testdb'].relations and not status.apps['testapp'].relations
        )
    )
