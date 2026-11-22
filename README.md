# mycelium-ha/.github

Central organization profile, community health files, and reusable GitHub Actions workflows for all repositories in [mycelium-ha](https://github.com/mycelium-ha).

Community health files (`CONTRIBUTING.md`, `SECURITY.md`, `SUPPORT.md`, `CODE_OF_CONDUCT.md`, issue and PR templates) apply to every repository that does not ship its own copy.

## Reusable workflows

| Workflow | Purpose |
| --- | --- |
| [`ha-validate.yml`](.github/workflows/ha-validate.yml) | `hassfest`, Marketplace/HACS validation, `ruff`; opt-in translation parity, `mypy`, `pytest` and tests on the minimum supported Home Assistant |
| [`ha-beta.yml`](.github/workflows/ha-beta.yml) | Runs the test suite against the newest Home Assistant pre-release |
| [`ha-release.yml`](.github/workflows/ha-release.yml) | Checks that a pushed tag matches `manifest.json` `version` and publishes a GitHub release with generated notes |

The [integration template](https://github.com/mycelium-ha/integration-template) already calls all three.

### Validation

    name: Validate

    on:
      push:
        branches: [main]
      pull_request:
      schedule:
        - cron: "0 0 * * *"
      workflow_dispatch:

    permissions:
      contents: read

    concurrency:
      group: ${{ github.workflow }}-${{ github.ref }}
      cancel-in-progress: true

    jobs:
      validate:
        uses: mycelium-ha/.github/.github/workflows/ha-validate.yml@main
        with:
          hacs_category: integration
          run_mypy: true
          run_pytest: true
          pytest_args: --cov
          # min_ha_requirements_file: requirements_test_min_ha.txt

| Input | Default | Description |
| --- | --- | --- |
| `hacs_category` | `integration` | Marketplace/HACS category |
| `hacs_ignore` | `""` | HACS checks to ignore |
| `run_hassfest` | `true` | Run `hassfest` (integrations only) |
| `run_ruff` | `true` | `ruff check` and `ruff format --check`, version from `requirements_file` |
| `run_translations` | `true` | Run `scripts/check_translations.py` if present |
| `run_mypy` | `false` | Run `mypy` as configured in `pyproject.toml` |
| `run_pytest` | `false` | Run `pytest` |
| `pytest_args` | `""` | Extra pytest arguments |
| `python_version` | `3.14` | Python for mypy/pytest |
| `requirements_file` | `requirements_test.txt` | Test and tooling dependencies |
| `min_ha_requirements_file` | `""` | Requirements pinning the minimum supported Home Assistant; enables an extra test job |

### Home Assistant beta

    name: Home Assistant beta

    on:
      schedule:
        - cron: "41 4 * * 1"
      workflow_dispatch:

    permissions:
      contents: read

    jobs:
      beta:
        uses: mycelium-ha/.github/.github/workflows/ha-beta.yml@main

### Release

Bump `version` in `manifest.json`, merge, then push a matching tag (`git tag v1.2.3 && git push origin v1.2.3`).

    name: Release

    on:
      push:
        tags: ["v*"]

    permissions:
      contents: write

    jobs:
      release:
        uses: mycelium-ha/.github/.github/workflows/ha-release.yml@main

## Versioning

Callers currently reference `@main`. Once the workflows are stable, tag them (`v1`) and move callers to `@v1`, so a change here cannot break every repository at once.
