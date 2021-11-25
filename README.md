# Platform

[![CircleCI](https://circleci.com/gh/pennlabs/platform.svg?style=shield)](https://circleci.com/gh/pennlabs/platform)
[![Coverage Status](https://codecov.io/gh/pennlabs/platform/branch/master/graph/badge.svg)](https://codecov.io/gh/pennlabs/platform)

The <strong> Labs Platform </strong> is the full-stack interface to the ecosystem that facilitates the organization's accounts engine and other cross-product resources.

## Installation

0. Configure environment variables (e.g. `.env`) containing:

```bash
DATABASE_URL=mysql://USER:PASSWORD@HOST:PORT/NAME
SECRET_KEY=secret
DJANGO_SETTINGS_MODULE=Platform.settings.production
SENTRY_URL=https://pub@sentry.example.com/product
```

1. Run using docker: `docker run -d pennlabs/platform` (is this still correct?)

## Documentation

Routes are defined in `/backend/accounts/urls.py`. Account/authorization related scripts are located in `accounts/management/commands`.

Documentation about individual endpoints is available through the `documentation/` route when the Django app is running.
