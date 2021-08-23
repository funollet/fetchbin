# justfile
#
# https://github.com/casey/just

project := "fetchfile"


# Show available commands.
default:
  @just -l

# Run the app.
run:
  poetry run {{project}}

# Run linters and formatters.
fmt:
  poetry run isort src/
  poetry run autoflake --in-place --remove-unused-variables --remove-all-unused-imports --expand-star-imports
  poetry run black src/
  poetry run flake8 src/

# Run tests.
test:
  poetry run pytest -v
  poetry run mypy src

# Run security scanners.
scan:
  poetry run bandit .
  poetry run safety check


# First time project setup.
init:
  poetry init
  poetry add --dev isort autoflake black flake8 pytest bandit safety mypy shiv
  pre-commit install
  pre-commit install-hooks
  pre-commit autoupdate
  pre-commit -av


# Package using shiv.
shiv:
  poetry run shiv . -p '/usr/bin/env python3' -o dist/{{project}}.pyz -c {{project}}


# Package using pex.
pex:
  pex . -o dist/{{project}}.pex -c {{project}}


# Remove temporary files.
clean:
  -rm dist/{{project}}-*.tar.gz
  -rm dist/{{project}}.pex
  -rm dist/{{project}}.pyz
  -rm dist/{{project}}.whl
  -rm requirements.txt
