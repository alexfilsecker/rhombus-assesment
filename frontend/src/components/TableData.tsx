import { ApiResponse } from "../App";
import { DataGrid, GridColDef } from "@mui/x-data-grid";

type TableDataProps = {
  tableData: ApiResponse;
};

const TableData = ({ tableData }: TableDataProps): JSX.Element => {
  console.log(tableData);

  const rows = tableData.rows.map((row) => ({
    id: row.row_index,
    row_index: row.row_index + 1,
    ...row.values,
  }));

  let columns: GridColDef<(typeof rows)[number]>[] = Object.values(
    tableData.cols
  )
    .sort((a, b) => a.col_index - b.col_index)
    .map((col) => ({
      field: col.col_name,
      headerName: `${col.col_name} (${col.col_type})`,
      description: col.human_col_type,
      width: 150,
    }));
  columns = [{ field: "row_index", headerName: "#" }, ...columns];

  return (
    <DataGrid
      columns={columns}
      rows={rows}
      className="w-full"
      density="compact"
      paginationMode="server"
      rowCount={200}
      sortingMode="server"
      onSortModelChange={(hola) => {
        console.log(hola);
      }}
    />
  );
};

export default TableData;
