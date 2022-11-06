## Runbook
This section is to collect thoughts/learnings from the codebase that have been hard-won, so we don't lose a record of it if and when the information proves useful again

### Dependency Installation on MacOS Ventura
There's a couple of issues at play here. The first is that the current `Pipfile` and `Pipfile.lock` are out of sync, most significantly with regard to Django--the `Pipfile` would generate a lockfile with Django 4, however, we are using Django 3 in the current lockfile and our tests. For now, use the current lockfile and use `--keep-outdated` when adding a new package with `pipenv`.

However, there seems to be an issue with the way that lockfiles are interacting with MacOS Ventura. In that case, we have to ignore the lockfile entirely, using `pipenv install --dev --python 3.8 --skip-lock` to install dependenices. From what I can tell, this is the only way to actually install the dependencies without it failing, but it means that some tests might fail due to issues with Django 4.

The long term solution is to make sure that the `Pipfile` and lockfile are in sync, either by forcing Django 3 or by updating our code to support Django 4.
