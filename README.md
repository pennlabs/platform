<a href="https://platform.pennlabs.org" target="_blank" rel="noopener noreferrer"><img width="300" src="https://i.imgur.com/E0Qldg5.png" alt="Platform Logo"></a>

The <strong> Labs Platform </strong> is the back-end interface to the ecosystem that facilitates the organization's:

1. Accounts Engine
2. Engagement Infrastructure
3. Cross-Product Resources
4. Organizational Information

## Installation
0. Configure environment variables (e.g. `.env`) containing:
```
DATABASE_URL=mysql://USER:PASSWORD@HOST:PORT/NAME
SECRET_KEY=secret
DJANGO_SETTINGS_MODULE=pennlabs.settings.production
SENTRY_URL=https://pub:private@sentry.example.com/product
```
1. Install requirements using `pip install -r requirements.txt`.
2. Run server using `python manage.py runserver`.

## Documentation
Routes are defined in `/pennlabs/urls.py` and subsequent app folders in the form of `*/urls.py`. Account/authorization related scripts are located in `accounts/` and Penn Labs related scripts are located in `org/`.

Documentation about individual endpoints is available through the `documentation/` route when the Django app is running.

## Current Maintainers
- [Arun Kirubarajan](https://github.com/kirubarajan)
- [Armaan Tobaccowalla](https://github.com/ArmaanT)
