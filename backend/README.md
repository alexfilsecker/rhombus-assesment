# Rhombus AI Assessment: Backend

Made with `Django` and `rest_framework` in `Python` languaje. In this part of the project, the file processing is done. As an adition to the project requirements, I have developed data persistency using the default's `sqlite3` database in the `Django` framework.

## Deployment

As said in the root [`README`](../README.md#docker) you can run `Docker` from the [`root/`](..) directory or from the [`current`](.) directory with:

```bash
docker compose up
```

Wich will start either the front and back (if run from the [`parent`](..) directory) or just the backend (if run from [`this`](.) directory). Remember you can use `-d` flag to prevent your terminal to be arrested with logs.

### Dev it

If you have python installed on your local machine, you can run this project with the following commands:

```bash
python -m venv venv
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

This will begin the `Django` server which you can access through: [`http://localhost:8000`](http://localhost:8000)

## Project Structure

This project follows the `Django` folder structure. The entry point is always the [`manage.py`](manage.py) file.

### backend

[This](backend/) directory contains the main `Django` app. The most important files are [`setings.py`](backend/settings.py) where we set the whole app settings and [`urls.py`](backend/urls.py), where we set the urls our app can handle.

### api

[Here](api/) is where
