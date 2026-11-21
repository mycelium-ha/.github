# mycelium-ha/.github

Central organization profile, community health files, and reusable GitHub Actions workflows for all repositories in [mycelium-ha](https://github.com/mycelium-ha).

## Reusable Validation Workflow

Call the shared Home Assistant validation workflow (`hassfest`, Marketplace/HACS validation, and `ruff`) from any integration repository:

    name: Validate

    on:
      push:
        branches: [main]
      pull_request:
      schedule:
        - cron: "0 0 * * *"
      workflow_dispatch:

    jobs:
      validate:
        uses: mycelium-ha/.github/.github/workflows/ha-validate.yml@main
        with:
          hacs_category: integration
