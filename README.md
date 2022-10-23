# Platform

[![CircleCI](https://circleci.com/gh/pennlabs/platform.svg?style=shield)](https://circleci.com/gh/pennlabs/platform)
[![Coverage Status](https://codecov.io/gh/pennlabs/platform/branch/master/graph/badge.svg)](https://codecov.io/gh/pennlabs/platform)

The <strong> Labs Platform </strong> is the back-end interface to the ecosystem that facilitates the organization's:

1. Accounts Engine
2. Cross-Product Resources
3. Organizational Information

## Installation

0. Configure environment variables (e.g. `.env`) containing:

```bash
DATABASE_URL=mysql://USER:PASSWORD@HOST:PORT/NAME
SECRET_KEY=secret
DJANGO_SETTINGS_MODULE=Platform.settings.production
SENTRY_URL=https://pub@sentry.example.com/product
```

1. Run using docker: `docker run -d pennlabs/platform`

## Documentation

Routes are defined in `/pennlabs/urls.py` and subsequent app folders in the form of `*/urls.py`. Account/authorization related scripts are located in `accounts/` and Penn Labs related scripts are located in `org/`.

Documentation about individual endpoints is available through the `documentation/` route when the Django app is running.

## Installation
You will need to start both the backend and the frontend to do Platform development.

### Backend

Running the backend requires [Python 3](https://www.python.org/downloads/).

To run the server, `cd` to the folder where you cloned `platform`. Then run:
- `cd backend`

Setting up `psycopg2` (this is necessary if you want to be able to modify
dependencies, you can revisit later if not)

- Mac
  - `$ brew install postgresql`
  - `$ brew install openssl`
  - `$ brew unlink openssl && brew link openssl --force`
  - `$ echo 'export PATH="/usr/local/opt/openssl@3/bin:$PATH"' >> ~/.zshrc`
  - `$ export LDFLAGS="-L/usr/local/opt/openssl@3/lib"`
  - `$ export CPPFLAGS="-I/usr/local/opt/openssl@3/include"`
- Windows
  - `$ apt-get install gcc python3-dev libpq-dev`

Now, you can run 

- `$ pipenv install` to install Python dependencies. This may take a few
  minutes. Optionally include the `--dev` argument if you are installing locally
  for development. If you skipped installing `psycopg2` earlier, you might see
  an error with locking -- this is expected!
- `$ pipenv shell`
- `$ ./manage.py migrate` OR `$ python3 manage.py migrate`
- `$ ./manage.py populate_users` OR `$ python3 manage.py populate_users` (in development,
  to populate the database with dummy data)
- `$ ./manage.py runserver` OR `$ python3 manage.py runserver`

### Frontend

Running the frontend requires [Node.js](https://nodejs.org/en/) and [Yarn](https://yarnpkg.com/getting-started/install).

1. Enter the `frontend` directory with a **new terminal window**. Don't kill your backend server!
2. Install dependencies using `yarn install` in the project directory.
3. Run application using `yarn dev`.
4. Access application at [http://localhost:3000](http://localhost:3000).

### Development

Click `Login` to log in as a test user. The `./manage.py populate_users` command creates a test user for you with username `bfranklin` and password `test`. Go to `/api/admin` to login to this account.
