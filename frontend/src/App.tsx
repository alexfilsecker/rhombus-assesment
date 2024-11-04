import { useState } from "react";
import FileUpload from "./components/FileUpload";
import TableData from "./components/TableData";
import Snackie from "./components/Snackie";

export const API_URL = "http://localhost:8000";

export type Status = "idle" | "loading" | "success" | "error";

const App = (): JSX.Element => {
  const [fileId, setFileId] = useState<string | null>(null);

  const [alertSeverity, setAlertSeverity] = useState<"success" | "error">(
    "success"
  );
  const [openAlert, setOpenAlert] = useState<boolean>(false);
  const [alertMessage, setAlertMessage] = useState<string>("");

  return (
    <>
      <div className="w-screen min-h-screen px-10 pt-10">
        <div className="flex flex-col gap-10 items-center">
          <h1 className="text-5xl font-extrabold">Rhombus AI Assessment</h1>
          <FileUpload
            setFileId={setFileId}
            setAlertMessage={setAlertMessage}
            setAlertSeverity={setAlertSeverity}
            setOpenAlert={setOpenAlert}
          />
          {fileId !== null && (
            <TableData
              fileId={fileId}
              setAlertMessage={setAlertMessage}
              setAlertSeverity={setAlertSeverity}
              setOpenAlert={setOpenAlert}
            />
          )}
        </div>
      </div>
      <Snackie
        alertSeverity={alertSeverity}
        openAlert={openAlert}
        setOpenAlert={setOpenAlert}
        alertMessage={alertMessage}
      />
    </>
  );
};

export default App;
