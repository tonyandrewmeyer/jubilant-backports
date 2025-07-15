import pytest

import jubilant_backports as jubilant

from . import mocks


def mock_token_hex(n: int):
    assert n == 4
    return 'abcd1234'


def test_defaults(run: mocks.Run, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr('secrets.token_hex', mock_token_hex)
    run.handle(['juju', 'version', '--format', 'json'], stdout='"2.9.52"\n')
    run.handle(['juju', 'add-model', '--no-switch', 'jubilant-abcd1234'])
    run.handle(['juju', 'deploy', '--model', 'jubilant-abcd1234', 'app1'])
    run.handle(
        [
            'juju',
            'destroy-model',
            'jubilant-abcd1234',
            '--no-prompt',
            '--destroy-storage',
            '--force',
        ]
    )

    with jubilant.temp_model() as juju:
        assert juju.model == 'jubilant-abcd1234'
        assert len(run.calls) == 2
        assert run.calls[1].args[1] == 'add-model'

        juju.deploy('app1')

        assert len(run.calls) == 3
        assert run.calls[2].args[1] == 'deploy'

    assert juju.model is None
    assert len(run.calls) == 4
    assert run.calls[3].args[1] == 'destroy-model'


def test_other_args(run: mocks.Run, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr('secrets.token_hex', mock_token_hex)
    run.handle(['juju', 'version', '--format', 'json'], stdout='"2.9.52"\n')
    run.handle(['juju', 'add-model', '--no-switch', 'jubilant-abcd1234', '--controller', 'ctrl'])
    run.handle(['juju', 'deploy', '--model', 'jubilant-abcd1234', 'app1'])

    with jubilant.temp_model(keep=True, controller='ctrl') as juju:
        assert juju.model == 'jubilant-abcd1234'
        assert len(run.calls) == 2
        assert run.calls[1].args[1] == 'add-model'

        juju.deploy('app1')

        assert len(run.calls) == 3
        assert run.calls[2].args[1] == 'deploy'

    assert juju.model == 'jubilant-abcd1234'
    assert len(run.calls) == 3
