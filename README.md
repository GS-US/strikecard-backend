# strikecard-backend (Operation Starfish 2.0)

Please read the [Project Overview](https://docs.google.com/document/d/1LDu3ReX-nmWdjed0XrI0YyilTRRPuWOKmF6_7TBK39M/edit?usp=sharing).

## Contributing

Please ensure you [Install Locally](#local-installation) to gain the benefits of our [Pre-Commit Hooks](#pre-commit).
Pull requests are checked using [Continuous Integration (CI)](#continuous-integration-ci), which mirrors Pre-Commit.

Create a branch for any feature or issue that you're working on, and submit a pull request back to main when you're done.
If you do not have permissions to create a branch, please reach out to the repo owner.

## Local Installation

See [`starfish/INSTALL.md`](./starfish/INSTALL.md) for more information about installing and deploying locally.

## Automation

### Configuration

Defined in the following files.

- [`pyproject.toml`](./pyproject.toml)
    - `black`
    - `isort`
    - `flake8`
- [`.markdownlint.json`](./markdownlint.json) and [`.markdownlint-cli2.jsonc`](./markdownlint-cli2.jsonc)
    - `markdownlint`
- [`.yamllint.yaml`](./.yamllint.yaml)
    - `yamllint`

### Pre-Commit

Defined in [`.pre-commit-config.yaml`](.pre-commit-config.yaml).

Runs the following repo hooks:

- Black (formatting)
- isort (formatting)
- flake8 (linting)
- markdownlint (linting)
- yamllint (linting)

### Continuous Integration (CI)

Defined in [`.github/`](.github/).

Runs the following actions dependent on what files are modified.

- Black (format linting)
- isort (format linting)
- flake8 (linting)
- markdownlint (linting)
- yamllint (linting)

Intended to mirror [pre-commit](#pre-commit) effects.

Checks and deploys the docs for any changes to files in `./docs/`.

## Documentation

Available at <https://gs-us.github.io/strikecard-backend/>.

### Docs Configuration

Defined in [`mkdocs.yml`](./mkdocs.yml). Controls navigation layout in the rendered docs.

### Docs Content

Defined in [`docs/`](docs/).

#### Blog, News, and Notes

Please give a date-based name with a title like `yyyy-mm-dd-title.md` and put in
[`docs/blog/posts/`](docs/blog/posts/).
