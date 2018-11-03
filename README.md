# Labs Platform
The Penn Lab's Platform API for accessing Users, Products, Members, Updates and more. 

## Dependencies
1. Django REST Framework (Python 3.7)

## Usage
0. Configure environment variables (e.g. `.env`) containing:
```
DB_PASSWORD=password
SECRET_KEY=secret
PLATFORM_ENV=debug
```
1. Install requirements using `pip install -r requirements.txt`.
2. Run server using `python manage.py runserver`.

## Documentation
Routes are defined in `/pennlabs/urls.py` and subsequent app folders in the form of `*/urls.py`. Account/authorization related scripts are located in `accounts/` and all other database-driven routes are located in `api/`.

## Current Maintainers
- [Arun Kirubarajan](https://github.com/kirubarajan)
- [Armaan Tobaccowalla](https://github.com/ArmaanT)
