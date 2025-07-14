# Jubilant-backports

```{toctree}
:maxdepth: 2
:hidden: true

Tutorial <tutorial/getting-started>
how-to/index
reference/index
explanation/index
```

Jubilant-backports is a Python library that wraps the [Jubilant](https://canonical-jubilant.readthedocs-hosted.com/) library to add support for Juju 2.9.

You should consider using Jubilant-backports if your integration tests need to support Juju 2.9 as well as Juju 3, and your integration tests currently use [pytest-operator](https://github.com/charmed-kubernetes/pytest-operator) (and they probably do). Jubilant has an API you'll pick up quickly, and it avoids some of the pain points of [python-libjuju](https://github.com/juju/python-libjuju/), such as websocket failures and having to use `async`. Read our [design goals](explanation/design-goals).


The library provides:

- The main [](jubilant_backports.Juju) class, with methods such as [`deploy`](jubilant_backports.Juju.deploy) and [`integrate`](jubilant_backports.Juju.integrate)


## In this documentation

````{grid} 1 1 2 2
```{grid-item-card} [Tutorial](tutorial/getting-started)
**Start here**: a hands-on introduction to Jubilant-backports
```

```{grid-item-card} [How-to guides](how-to/index)
**Step-by-step guides** covering key operations and common tasks
```
````

````{grid} 1 1 2 2
:reverse:
```{grid-item-card} [Reference](reference/index)
**Technical information**
- [API reference](reference/jubilant-backports)
```

```{grid-item-card} [Explanation](explanation/index)
**Discussion and clarification** of key topics
```
````


## Releases

[Jubilant-backports releases](https://github.com/canonical/jubilant-backports/releases) are tracked on GitHub, and use [semantic versioning](https://semver.org/). To get notified when there's a new release, watch the [Jubilant-backports repository](https://github.com/canonical/jubilant-backports).


## Project and community

Jubilant-backports is free software and released under the [Apache license, version 2.0](https://www.apache.org/licenses/LICENSE-2.0).

The Jubilant-backports project is sponsored by [Canonical Ltd](https://www.canonical.com).

- [Code of conduct](https://ubuntu.com/community/ethos/code-of-conduct)
- [Contribute to the project](https://github.com/canonical/jubilant-backports?tab=readme-ov-file#contributing-and-developing)
- [Development](https://github.com/canonical/jubilant-backports?tab=readme-ov-file#contributing-and-developing): how to make changes to Jubilant-backports and run its tests
