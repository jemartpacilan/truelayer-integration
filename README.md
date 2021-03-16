# TrueLayer Data API Integration - Account Transactions

A Python Flask application with TrueLayer API integration that enables to:
- authorize access for UK bank accounts and cards
- view all the transactions for each
- view all the data associated with each transaction

## Usage

### Requirements

You must have `docker`, `pyenv`, `python3`, `pip3`, and `pipenv` installed.

The app uses a `.env` file to set required environment variables.

Create a `.env` file in the root project directory and add the following configuration:

```text
CLIENT_ID=********
SECRET_ID=********
REDIRECT_URL=********
```
Sample .env file can be found in the root of the project (.env.sample)

### Run the app

You can directly install all the dependencies and run the app using this docker command:
```bash
$ docker-compose up
```
### Testing
The Makefile is responsible for running tests:

```bash
$ make test
```

### Reference
Git repo: https://github.com/TrueLayer/data-api-quickstart-sample
