# Rhombus AI Assessment

Hello! This is my version of a `.csv | .xlsx` file parser.
See the video explanation: [video](TODO)

## Components

The project consists of four parts:

- [**Frontend**](frontend/): Made with `Vite`, `React.js` framework in `Typescript` languaje. See it's [`README.md`](frontend/README.md).
- [**Backend**](backend/): Made with `Django` and `rest_framework` in `Python` languaje. See it's [`README.md`](backend/README.md).
- [**Data Inferance Scripts**](backend/api/scripts/): Built into the **Backend's** API. This scripts are responsible for inferance and convertion of the data. See it's [`README.md`](backend/api/scripts/README.md).
- [**Sample Generators**](samples/): A script for generating `.csv` files for testing the application. See it's [`README.md`](samples/README.md)

## Deployment

No need to deploy! As an extra I have hosted this app in my personal portfolio website, just visit [www.alexfilsecker.com/rhombus-assessment](https://www.alexfilsecker.com/rhombus-assessment/)

If you still wish to deploy the app locally, I have provided some other methods:

### Docker

If you have `docker` and `docker-compose` installed, you can just run:

```bash
git clone https://github.com/alexfilsecker/rhombus-assesment.git
cd rhombus-assessment
docker compose up
```

This should start 2 containers: `rhombus-front`, `rhombus-back`, and begin to display it's logs.

Alternatively, you can run each docker service separately as:

```bash
git clone https://github.com/alexfilsecker/rhombus-assesment.git
cd rhombus-assessment/frontend
docker compose up -d
cd ../backend
docker compose up -d
```

Notice the `-d` flag (`d` for `detached`), this will not arrest your terminal. If you want to see the logs you can run `docker logs` followed by `rhombus-front` or `rhombus back`

### Just dev it

To run this simple project with normal dev tools you need to run each project separately, see how to run the [`Frontend`](frontend/README.md) and [`Backend`](backend/README.md) in it's own `README`'s.
