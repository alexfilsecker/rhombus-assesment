# Rhombus AI Assessment

Hello! This is my version of a `.csv | .xlsx` file parser.
See the video explanation: [video](TODO)

## Components

The project consists of four parts:

- [**Frontend**](frontend/): Made with `Vite`, `React.js` framework in `Typescript`. See it's [`README.md`](frontend/README.md).
- [**Backend**](backend/): Made with `Django` and `rest_framework` in `Python`. See it's [`README.md`](backend/README.md).
- [**Data Inferance Scripts**](backend/api/scripts/): Built into the **Backend's** API. This scripts are responsible for inferance and convertion of the data. See it's [`README.md`](backend/api/scripts/README.md).
- [**Sample Generators**](samples/): A script for generating `.csv` files for testing the application.

## Deployment

No need to deploy! As an extra I have hosted this app in my portfolio, just visit [www.alexfilsecker.com/rhombus-assessment](https://alexfilsecker.com/rhombus-assessment)

If you still wish to deploy the app locally, I have provided two methods:

### Docker

If you have `docker-compose` installed, you can just run:

```bash
docker-compose up
```

This should start 3 containers: `rhombus-front`, `rhombus-back` and `rhombus-db`

### Just Dev it

To run this simple project with normal dev tools you need to run each project separately, see how to run the `Frontend` and `Backend` in it's own `README`'s
