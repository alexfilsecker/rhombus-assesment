FROM python:3.12.7

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN if [ ! -f ./db.sqlite3 ]; then touch ./db.sqlite3; fi

RUN python manage.py migrate
