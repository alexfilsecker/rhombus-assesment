import { useState } from "react";
import FileUpload from "./components/FileUpload";
import TableData from "./components/TableData";

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

export type ApiResponse = {
  file_id: string;
  cols: { [key: string]: TableColData };
  rows: Row[];
};

const App = (): JSX.Element => {
  const [tableData, setTableData] = useState<ApiResponse | null>(null);

  return (
    <div className="w-screen min-h-screen px-32 pt-10">
      <div className="flex flex-col gap-10 items-center">
        <h1 className="text-5xl font-extrabold">Rhombus AI Assessment</h1>
        <FileUpload setTableData={setTableData} />
        {tableData !== null && <TableData tableData={tableData} />}
      </div>
    </div>
  );
};

export default App;
