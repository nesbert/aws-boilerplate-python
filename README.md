# aws-boilerplate-python
Starter Python project for development with the goal of adding AWS support.

## Getting Started

### Installation

```sh
# create virtual environment
python -m venv venv

# activiate virtual environment
source venv/bin/activate

# install virtual environment packages
pip install --upgrade pip
pip install poetry
```

### Project Dependencies

Use `poetry` to manage project package dependencies.

```sh
# install all required package dependencies
poetry install

# add a dependency
poetry add requests

# add a development dependency
poetry add --dev black

# remove a dependency
poetry remove requests

# update dependencies to latest
poetry update
```

### Code Quailty

Requires `dev` dependinces to be installed.

#### Testing

```sh
# run all tests
pytest -v

# run test a single method
pytest tests/gorest/test_users.py::test_fetch_all -v

# run test based on an expression
pytest -k "all or main" -v
```

#### Coverage Reporting
```sh
# run coverage analysis
coverage run -m pytest -v

# view coverage reports
coverage report
coverage html
```

#### Linting & Style Guide

```sh
# lint project files
pylint ./src/* ./tests/*

# format code with black
black src/gorest/users.py # single file
black src/example/*.py # all files in directory
black src/**/*.py # all files in directory recursively
```

## Usage

Here are a few ways to use this application.

### CLI Examples

#### Project/Poetry CLI Scripts

Requires `venv` to be active `source venv/bin/activate`. The console scripts below may also be invoked through `poetry`.

```sh
#test lambda handlers locally (`pip install -e .`)
lambda-handler list_users_handler --verbose
lambda-handler read_user_handler --event '{ "id": 1610 }'

# use poetry to test lambda handlers locally
poetry run lambda-handler list_users_handler -e '{ "page": 2, "limit": 20 }' | jq .
```

## TODOs

- [x] Start project and get good (learn by doing)
- [x] Pick project struture (flat vs src)
- [x] Virtual environement (`venv`)
- [x] Porject package dependency managment (`poetry`)
- [x] CLI First design approach #CLIallthethings
- [ ] Developer Experience
    - [x] Add test framework (`pytest`, `coverage`)
    - [x] Add linting suppport (`pylint`)
    - [x] Add logging support
    - [x] Add Type Checking support
    - [x] Add VSCode support
    - [ ] Add VSCode Debugger support
    - [ ] Add `pre-commit` support (`black`, etc.)
    - [ ] Add configuration support (`yaml`)
- [ ] Package Examples
    - [ ] REST client example (`gorest`)
    - [ ] CRUD example
- [ ] AWS Support
    - [ ] AWS Lambda Example
    - [ ] AWS Lambda Layers Example
    - [ ] AWS CDK Example
    - [ ] AWS S3 Example
    - [ ] AWS API Gateway Example
    - [ ] AWS Step Function Example
    - [ ] AWS DynamoDB Example
