# Setup python

## Up and running

### Install python3 and pip and Setup virtualenv

- python3 --version -> Python 3.7.9
- which pip3 -> /usr/local/bin/pip3
- python3 -m venv ./venv
- source ./venv/bin/activate
- pip install -r requirements.txt

## Additional useful commands

### Deactivate virtualenv

- deactivate

### Install python packages from requirements.txt

- pip install -r requirements.txt

### Save installed python packages

- pip freeze > requirements.txt

### Why I don't know but I get suggested to run this command

pip install --upgrade pip
