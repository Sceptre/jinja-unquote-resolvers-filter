# Code of Conduct

This project adheres to the Contributor Covenant
[code of conduct](http://contributor-covenant.org/version/1/4/). By
participating, you are expected to uphold this code. Please report unacceptable
behaviour to the [Sceptre github discussion](https://github.com/Sceptre/sceptre/discussions).

# How to Contribute

## Dependency Management

[Poetry](https://pypi.org/project/poetry/) is the tool that is used for
dependency management, versioning and deployment management to pypi.
Please [install poetry](https://python-poetry.org/docs/#installation)
and execute commands from the poetry environment.

## Linting

As a pre-deployment step we syntatically validate files with
[pre-commit](https://pre-commit.com).

Please [install pre-commit](https://pre-commit.com/#install) then run
`pre-commit install` to setup the git hooks.  Once configured the pre-commit
linters will automatically run on every git commit.  Alternatively you
can manually execute the validations by running `pre-commit run --all-files`.

## Unit Tests

[Tox](https://pypi.org/project/tox/) is used to execute tests against multiple
python versions inside of poetry virtual environments.

```bash
$ poetry run tox
```

## Releasing

Poetry is used to manage versions and deployments. Follow the below steps to release a version to pypi.

* Update the CHANGELOG.md with changes (see the example in the CHANGELOG comments).
* Bump the package version (i.e. `poetry version minor`)
* Create a release PR and have it reviewed, approved and then merged
* Create a git tag (i.e `git tag -as x.y.z`)
* Push the tag which will trigger a CI job to deploy to PyPi.

# Get Started

1. Fork this repository
2. Clone your fork locally
3. Create a branch for local development
4. Install dependencies (i.e. poetry install)
5. Update the [pyproject.toml](pyproject.toml) file with information
   specific to the project. Refer to the [poetry documentation](https://python-poetry.org/docs/pyproject/)
   for a reference to the configurations.
6. Add source code and tests for the project.
7. When you're done making changes, check that your changes pass
   [linting](#Linting), [unit tests](#Unit-Tests) and have
   sufficient coverage.
8. Submit a pull request through the GitHub website.
