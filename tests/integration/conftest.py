from __future__ import annotations

from typing import Generator, cast

import pytest

import jubilant_backports as jubilant
from jubilant_backports._juju import Juju29


def pytest_addoption(parser: pytest.OptionGroup):
    parser.addoption(
        '--keep-models',
        action='store_true',
        default=False,
        help='keep temporarily-created models',
    )


@pytest.fixture(scope='module')
def juju(request: pytest.FixtureRequest) -> Generator[Juju29]:
    """Module-scoped pytest fixture that wraps :meth:`jubilant.with_model`."""
    keep_models = cast(bool, request.config.getoption('--keep-models'))
    with jubilant.temp_model(keep=keep_models) as juju:
        yield juju
        if request.session.testsfailed:
            log = juju.debug_log(limit=1000)
            print(log, end='')
