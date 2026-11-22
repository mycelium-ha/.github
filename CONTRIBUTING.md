# Contributing to mycelium-ha

Thanks for considering a contribution! You don't need to write Python to help.

## Other ways to help

- **Translations:** every integration keeps its texts in `custom_components/<domain>/translations/<language>.json`. Copy `en.json`, translate the values (keep the keys and `{placeholders}`), and open a pull request. GitHub's web editor is enough.
- **Testing devices:** if you own a device an integration supports, or one it could support, open an issue with the model and the diagnostics download. Reports like this decide what we build next.
- **Reporting bugs:** a clear bug report with diagnostics and debug logs is often half the fix.

## Development setup

Most repositories follow the [integration template](https://github.com/mycelium-ha/integration-template):

```bash
python3.14 -m venv .venv
source .venv/bin/activate
pip install -r requirements_test.txt
pip install pre-commit && pre-commit install
```

Run the checks locally before pushing:

```bash
ruff check . && ruff format --check .
mypy
python scripts/check_translations.py
pytest --cov
```

## Before opening a pull request

1. Open an issue first for larger changes or new features so we can align on the approach.
2. Keep pull requests focused on a single topic.
3. Ensure all automated checks pass:
   - `hassfest` validation
   - Home Assistant Marketplace / HACS validation
   - `ruff check` and `ruff format --check`
   - `mypy` and `pytest` (where the repository has them)
   - translation parity (`strings.json` and every file in `translations/`)
4. Add or update tests for changed behavior.
5. Update documentation (`README.md`, `strings.json`, translations) and `quality_scale.yaml` if behavior or configuration changes.

## Releases

Maintainers bump `version` in `manifest.json`, merge, and push a matching `vX.Y.Z` tag. The release workflow verifies the version and publishes the GitHub release.
