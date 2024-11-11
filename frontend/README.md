# Rhombus AI Assessment: Frontend

Made with `Vite`, `React.js` framework in `Typescript` language. Additionally it uses `Material UI` pre made components and `TailwindCSS` for managing styles. Here I'll show you how I did it.

## Deploying

As said in the root [`README`](../README.md#docker) you can run `Docker` from the [`root/`](..) directory or from the [`current`](.) directory with:

```bash
docker compose up
```

Which will start either the front and back (if run from the [`parent`](..) directory) or just the frontend (if run from [`this`](.) directory). Remember you can use `-d` flag to prevent your terminal to be arrested with logs.

### Dev it

If you have `Node.js` installed in your machine, you can run:

```bash
npm install
npm run dev
```

Which will start the development with `Vite`. You can access the page through: [`http://localhost:3000/rhombus-assessment`](http://localhost:3000/rhombus-assessment)

## Project Flow

The frontend flow is at follows:

1. **File Selection**: The user selects a `.csv` or `.xlsx` file from within it's computer.

2. **File Previewing**: The page will show a preview of the first `5` lines (excluding headers) by default. the user can increase the previewing size with two buttons.

3. **Casting Options**: For each column, the user can select a casting option, which will make the backend attempt to transform that column into the specified type. The types available are:

   - **Signed Integer**: with additional option of `8`, `16`, `32` or `64` bits.
   - **Unsigned Integer**: with additional option of `8`, `16` or `32` bits. Notice that It does not reach `64` bits. That is explained in the **backends** [README](../backend/README.md)
   - **Floating Point**: with additional option of `32` or `64` bits.
   - **Category**
   - **Complex**: This will result in a `128` complex value.
   - **Text**: The default behavior. In pandas, a `object` value.
   - **Date and Time**: Then displayed as an ISO formatted date and time. You can specify it's format parser following the `datetime` library [documentation](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes)
   - **Time Delta**: Casted into a difference of time.

4. **Processing Button**: When pressed, sends a request to the backends api that processes the file by inferring types, converting data, storing it into a database and returns a `file_id`. The page then immediately requests the stored data using the same `file_id`. This behavior was designed to reutilize the sorting feature.

5. **Processing Errors Display**: Two errors could have happened when processing the file:

   1. **Unintentional Errors**: If any "unintentional" error where to happen (any `HTTP codes` different from `200`) a red `Snackbar` will appear in the bottom left corner of the screen saying that an error occurred.
   2. **Force Casting Errors**: If any of the casting options selected in step **3**, `Alerts` will appear for every column casting error.

6. **Viewing the Result**: After having fetched the table data, another table will appear on the bottom part of the page. This table has been made using [`MUI X Data Grid`](https://mui.com/x/react-data-grid/). This component allows for server side sorting and pagination, and that is exactly what I used. Whenever you sort or change the page, another request is done to the server. If it is successful, it changes the table's content and a green `Snackbar` appears on the bottom left corner.
