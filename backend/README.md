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

### Main App

In [`backend/`](backend/) directory contains the main `Django` app. The most important files are [`setings.py`](backend/settings.py) where we set the whole app settings and [`urls.py`](backend/urls.py), where we set the urls our app can handle.

### API

In [`api/`](api/) is where all the app magic occurs.

#### URLs

In [`urls.py`](api/urls.py) is where we set up the actual url's through we access our server. There are two main ones `process-file` and `get-data`. This are the two ones that we describe in the [frontends flow](../frontend/README.md#project-flow).

#### Views

In [`views.py`](api/views.py) we can see the actual "controllers" that handle the routes shown in [URLs](#urls). You can see more about each one of them viewing their `docstring`'s.

#### Models

Normally, in a basic `Django` app all models are in a `models.py` file. But I have decided to modularize them into the [`models/`](api/models/) directory. There are two models, `TableCol` and `GenericData`. The first one stores the column information of an uploaded file and the second one stores each cell in a file excluding the headers.

#### Serializers

Same as `models`, I have modularized the normal `serializers.py` into the [`serializers/`](api/serializers/) directory. Here we can encounter one standard `Serializer` called `GetDataSerializer` made to validate and serialize the `request.query_params` from `get-data` sent from the frontend and two `ModelSerializer` for the two models.

## Data Flow

The flow of data is as follows:

1. The file arrives to the backend through a `POST` request.

2. It's extension gets validated only accepting `.csv` and `.xlsx`.

3. According to it's extension we read it from memory using the `pandas` library, creating a `DataFrame` object.

4. We get the `force_casting` option from the `request`.

5. We inferd and convert the data using the `DataFrame` and the `force_casting` options, returning another `DataFrame` and a `errors` dictionary containing any errors that could have ocurred trying to force cast the data. See the data infererance's [README.md](api/scripts/README.md).

6. We assign a `file_id` to the file made from it's name and the current timestamp.

7. We save the converted `DataFrame` into the database using the `create_data` function in [`utils.py`](api/utils.py) which is an `atomic` transaction involving `TableCol` and `GenericData` models.

   1. We iterate over all columns in the `DataFrame`.
   2. For each column, we create it's model and save it into the database.
   3. We now iterate over each cell in the column.
   4. According to the column `dtype` we store the cell's value into different columns in the database. For example to store a `int` we use two columns, `uint_value` and `int_sign_value`. This behaiviour was designed to allow sorting from within the database.
   5. Finally, we create all `GenericData` in a bulk operation.

8. We return to the user the `file_id` and the force casting `errors`.

9. The user inmediatelly requests the data from the `file_id`. This operation occurs again every time the user requests another sorting or page.

10. We serialize and validate the `query_params` from the `request`.

11. We retrieve all the stored file's columns and then serialize them.

12. We begin a query to retrieve the data from all columns.

13. We then sort and slice the data, creating a `rows` object.

14. We then return the `rows` and `cols` objects to the frontend along with other information.
