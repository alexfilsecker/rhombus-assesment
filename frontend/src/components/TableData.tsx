import {
  DataGrid,
  GridColDef,
  GridPaginationModel,
  GridSortModel,
} from "@mui/x-data-grid";
import axios from "axios";
import { Dispatch, Fragment, SetStateAction, useEffect, useState } from "react";
import { API_URL, Status } from "../App";
import { CircularProgress } from "@mui/material";

export type Row = {
  row_index: number;
  values: {
    [key: string]: number | string | boolean | null;
  };
};

export type TableColData = {
  col_index: number;
  col_name: string;
  col_type: string;
  human_col_type: string;
};

export type TableDataApiResponse = {
  cols: { [key: string]: TableColData };
  rows: Row[];
  page: number;
  pageSize: number;
  total_rows: number;
};

type FetchTableDataProps = {
  fileId: string;
  paginationModel: GridPaginationModel;
  sortingModel: GridSortModel;
};

type TableDataProps = {
  fileId: string;
  setOpenAlert: Dispatch<SetStateAction<boolean>>;
  setAlertSeverity: Dispatch<SetStateAction<"error" | "success">>;
  setAlertMessage: Dispatch<SetStateAction<string>>;
};

const TableData = ({
  fileId,
  setOpenAlert,
  setAlertSeverity,
  setAlertMessage,
}: TableDataProps): JSX.Element => {
  const [fetchStatus, setFetchStatus] = useState<Status>("success");

  const [fetchingController, setFetchingController] =
    useState<AbortController | null>(null);

  useEffect(() => {
    if (fetchStatus === "success" || fetchStatus === "error") {
      setOpenAlert(true);
      setAlertSeverity(fetchStatus);
      setAlertMessage(
        fetchStatus === "success"
          ? "Table data fetched successfully"
          : "Error fetching table data"
      );
    }
  }, [fetchStatus, setAlertMessage, setAlertSeverity, setOpenAlert]);

  const [tableData, setTableData] = useState<TableDataApiResponse | null>(null);
  const [paginationModel, setPaginationModel] = useState<GridPaginationModel>({
    page: 0,
    pageSize: 100,
  });
  const [sortingModel, setSortingModel] = useState<GridSortModel>([]);

  useEffect(() => {
    if (fileId === null) return;

    const fetchTableData = async ({
      fileId,
      paginationModel,
    }: FetchTableDataProps) => {
      const sortBy =
        sortingModel.length > 0 ? sortingModel[0].field : undefined;
      const asc =
        sortingModel.length > 0 ? sortingModel[0].sort === "asc" : undefined;

      try {
        setFetchStatus("loading");
        if (fetchingController !== null) {
          fetchingController.abort();
        }
        const controller = new AbortController();
        setFetchingController(controller);
        const response = await axios.get<TableDataApiResponse>(
          `${API_URL}/api/get-data`,
          {
            signal: controller.signal,
            params: {
              file_id: fileId,
              page: paginationModel.page,
              page_size: paginationModel.pageSize,
              sort_by: sortBy,
              asc,
            },
          }
        );

        setTableData(response.data);
        setFetchStatus("success");
        setFetchingController(null);
      } catch (e) {
        if (e instanceof axios.CanceledError) {
          return;
        }
        console.error(e);
        setTableData(null);
        setFetchStatus("error");
      }
    };

    fetchTableData({ fileId, paginationModel, sortingModel });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [fileId, paginationModel, sortingModel]);

  if (tableData === null) {
    return <Fragment />;
  }

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
      width: 200,
    }));
  columns = [{ field: "row_index", headerName: "#" }, ...columns];

  return (
    <div className="flex flex-col w-full gap-4">
      <div className="flex items-center h-20 gap-20">
        <div>File ID: {fileId}</div>
        {fetchStatus === "loading" && <CircularProgress />}
      </div>
      {tableData !== null && (
        <DataGrid
          className="w-full"
          density="compact"
          columns={columns}
          rows={rows}
          rowCount={tableData.total_rows}
          sortingMode="server"
          sortModel={sortingModel}
          onSortModelChange={(newSortingModel) => {
            setSortingModel(newSortingModel);
          }}
          paginationMode="server"
          paginationModel={paginationModel}
          onPaginationModelChange={(newPaginationModel) => {
            setPaginationModel(newPaginationModel);
          }}
          disableColumnFilter
        />
      )}
    </div>
  );
};

export default TableData;
