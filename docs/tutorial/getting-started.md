# Getting started with Jubilant-backports

```{important}
Using Jubilant-backports is almost identical to using Jubilant. Make sure you [get started with Jubilant](https://canonical-jubilant.readthedocs-hosted.com/tutorial/getting-started/) first!
```

In this tutorial, we'll learn how to install Jubilant-backports, substitute it for the regular Jubilant package, and write a simple charm integration test that will run against both Juju 2.9 and Juju 3.x.

The tutorial assumes that you have a basic understanding of Juju and have already installed it. [Learn how to install the Juju CLI.](https://documentation.ubuntu.com/juju/2.9/howto/manage-juju/index.html#install-juju)


## Install Jubilant-backports

Jubilant-backports is published to PyPI, so you can install and use it with your favorite Python package manager:

```
$ pip install jubilant-backports
# or
$ uv add jubilant-backports
```

Like the 2.x releases of [Ops](https://github.com/canonical/operator) framework used by charms, Jubilant-backports requires Python 3.8 or above.


## Check your setup

To check that Jubilant-backports is working, use it to add a Juju model and check its status:

```{tip}
You can run this check with the 2.9 Juju CLI or a 3.x Juju CLI, against a 2.9 Juju controller or a 3.x Juju controller.
```

```
$ uv run python
>>> import jubilant_backports as jubilant
>>> juju = jubilant.Juju()
>>> juju.add_model('test')
>>> juju.status()
Status(
  model=ModelStatus(
    name='test',
    type='caas',
    controller='my-k8s-localhost',
    cloud='microk8s',
    version='2.9.50',
    region='localhost',
    model_status=StatusInfo(current='available', since='15 Jul 2025 21:31:29+12:00'),
    sla='unsupported',
  ),
  machines={},
  apps={},
  controller=ControllerStatus(timestamp='21:31:37+12:00'),
)
```

Compare the status to what's displayed when using the Juju CLI directly:

```
$ juju status --model test
Model  Controller  Cloud/Region      Version  SLA          Timestamp
test   k8s         my-k8s/localhost  3.6.4    unsupported  12:35:05+13:00

Model "test" is empty.

$ juju status --model test
Model  Controller  Cloud/Region      Version  SLA          Timestamp
test   k8s         my-k8s/localhost  2.9.50   unsupported  21:14:30+12:00

Model "admin/test" is empty.
```

## Substitute `jubilant_backports` for `jubilant`

Jubilant-backports is a drop-in replacement for Jubilant. Only two steps are required:

1. Replace `jubilant` in your dependencies with `jubilant_backports` (note that Jubilant-backports depends on Jubilant, so you'll still have it as a transitive dependency).
2. Use `jubilant_backports` in your imports rather than `jubilant`. We recommend `import jubilant_backports as jubilant` (and `import jubilant_backports.statustypes as statustypes`) for minimal disruption.

The Jubilant-backports `Juju` class will check the version of the `juju` CLI when objects are created. If it's Juju 3.x or higher, then the class is a simple wrapper around the Jubilant `Juju` class. If it's Juju 2.9, then you continue to use the familiar Jubilant `Juju` API, and the class will transparently translate CLI commands as required. Similarly, when using [](jubilant_backports.Juju.status), the class will inspect the status to determine the version of the controller, and return either a [](jubilant_backports.Status) or a Jubilant `Status`, as appropriate.

Two extra attributes are available on the Jubilant-backports class, to inspect the version:

```python
>> import jubilant_backports as jubilant
>>> juju = jubilant.Juju()
>>> juju.cli_version
'2.9.52-ubuntu-amd64'
>>> juju.cli_major_version
2
```

It's also possible to pass in the CLI version (`Juju(cli_version='2.9.0')`), but this should not be required in normal circumstances.

## Write a charm integration test

We recommend using [pytest](https://docs.pytest.org/en/stable/) for writing tests. You can define a [pytest fixture](https://docs.pytest.org/en/stable/explanation/fixtures.html) to create a temporary Juju model for each test. The [](jubilant_backports.temp_model) context manager creates a randomly-named model on entry, and destroys the model on exit. (Use this context manager rather than the Jubilant one, to make sure you get the right `Juju` class for the version of Juju you are using.)

Here is a module-scoped fixture called `juju`, which you would normally define in [`conftest.py`](https://docs.pytest.org/en/stable/reference/fixtures.html#conftest-py-sharing-fixtures-across-multiple-files):

```python
import jubilant_backports as jubilant

@pytest.fixture(scope='module')
def juju():
    with jubilant.temp_model() as juju:
        yield juju
```

Integration tests in a test file would use the fixture, operating on the temporary model:

```python
import jubilant_backports as jubilant

def test_deploy(juju: jubilant.Juju):  # type: ignore
    juju.deploy('snappass-test')
    juju.wait(jubilant.all_active)

    # Or wait for just 'snappass-test' to be active (ignoring other apps):
    juju.wait(lambda status: jubilant.all_active(status, 'snappass-test'))
```

You may want to adjust the [scope](https://docs.pytest.org/en/stable/how-to/fixtures.html#fixture-scopes) of your `juju` fixture. For example, to create a new model for every test function (pytest's default behavior), omit the scope:

```python
@pytest.fixture
def juju():
    ...
```

(next_steps)=
## Next steps

You've now learned the basics of Jubilant-backports! To learn more:

- Look over the [`jubilant_backports` API reference](/reference/jubilant_backports)
- See [Jubilant-backports's own integration tests](https://github.com/canonical/jubilant-backports/tree/main/tests/integration) for more examples of using `Juju` methods
- See [Jubilant-backports's `conftest.py`](https://github.com/canonical/jubilant-backports/blob/main/tests/integration/conftest.py) with a `juju` fixture that has a `--keep-models` command-line argument, and prints the `juju debug-log` on test failure

If you have any problems or want to request new features, please [open an issue](https://github.com/canonical/jubilant-backports/issues/new).
