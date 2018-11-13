# Labs Platform
The Penn Lab's Platform API for accessing Users, Products, Members, Updates and more. 

## Dependencies
1. Django REST Framework (Python 3.7)

## Usage
0. Configure environment variables (e.g. `.env`) containing:
```
DATABASE_URL=mysql://USER:PASSWORD@HOST:PORT/NAME
SECRET_KEY=secret
DJANGO_SETTINGS_MODULE=pennlabs.settings.production
```
1. Install requirements using `pip install -r requirements.txt`.
2. Run server using `python manage.py runserver`.

## Documentation
Routes are defined in `/pennlabs/urls.py` and subsequent app folders in the form of `*/urls.py`. Account/authorization related scripts are located in `accounts/` and Penn Labs related routes are located in `org/`.

## Current Maintainers
- [Arun Kirubarajan](https://github.com/kirubarajan)
- [Armaan Tobaccowalla](https://github.com/ArmaanT)
