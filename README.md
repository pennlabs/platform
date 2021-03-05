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
IS_DEV_LOGIN=True
```

1. Run using docker: `docker run -d pennlabs/platform`

## Documentation

Routes are defined in `/pennlabs/urls.py` and subsequent app folders in the form of `*/urls.py`. Account/authorization related scripts are located in `accounts/` and Penn Labs related scripts are located in `org/`.

Documentation about individual endpoints is available through the `documentation/` route when the Django app is running.
