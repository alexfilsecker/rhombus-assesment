import { useState } from "react";
import FileUpload from "./components/FileUpload";
import TableData from "./components/TableData";
import Snackie from "./components/Snackie";
import PreviewTable from "./components/PreviewTable";
import ProcessOptions from "./components/ProcessOptions";

export const API_URL = "http://localhost:8000";

export type Status = "idle" | "loading" | "success" | "error";

export type MyAlert = {
  open: boolean;
  severity: "success" | "error";
  message: string;
};

const App = (): JSX.Element => {
  const [fileId, setFileId] = useState<string | null>(null);

  const [file, setFile] = useState<File | null>(null);

  const [headers, setHeaders] = useState<string[] | null>(null);

  const [alertStatus, setAlertStatus] = useState<MyAlert>({
    open: false,
    severity: "success",
    message: "",
  });

  return (
    <>
      <div className="w-screen min-h-screen px-10 pt-10">
        <div className="flex flex-col gap-10 items-center">
          <h1 className="text-5xl font-extrabold">Rhombus AI Assessment</h1>
          <FileUpload
            setFileId={setFileId}
            setAlertStatus={setAlertStatus}
            file={file}
            setFile={setFile}
          />
          {headers !== null && <ProcessOptions headers={headers} />}
          {file !== null && fileId === null && (
            <PreviewTable file={file} setHeaders={setHeaders} />
          )}
          {fileId !== null && (
            <TableData fileId={fileId} setAlertStatus={setAlertStatus} />
          )}
        </div>
      </div>
      <Snackie alertStatus={alertStatus} setAlertStatus={setAlertStatus} />
    </>
  );
};

export default App;
