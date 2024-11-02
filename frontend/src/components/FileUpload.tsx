import { Alert, Button, CircularProgress, Collapse } from "@mui/material";
import axios from "axios";
import {
  ChangeEvent,
  useEffect,
  useRef,
  useState,
  Dispatch,
  SetStateAction,
} from "react";
import { ApiResponse } from "../App";

const API_URL = "http://localhost:8000";

type FileUploadProps = {
  setTableData: Dispatch<SetStateAction<ApiResponse | null>>;
};

const FileUpload = ({ setTableData }: FileUploadProps) => {
  const [status, setStatus] = useState<
    "idle" | "loading" | "success" | "error"
  >("idle");

  const [alertStatus, setAlertStatus] = useState<"success" | "error">("error");

  const [openAlert, setOpenAlert] = useState<boolean>(false);

  const [file, setFile] = useState<File | null>(null);

  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (status === "success" || status === "error") {
      setOpenAlert(true);
      setAlertStatus(status);
    } else {
      setOpenAlert(false);
    }
  }, [status]);

  const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (files === null || files.length === 0) return;
    setFile(files[0]);
    setOpenAlert(false);
  };

  const handleUpload = async () => {
    if (file === null) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      setStatus("loading");
      const response = await axios.post<ApiResponse>(
        `${API_URL}/api/process-file`,
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );
      setStatus("success");
      setTableData(response.data);
    } catch (e: unknown) {
      setStatus("error");
      console.error(e);
    }
  };

  return (
    <div className="flex flex-col gap-4 w-80">
      <h2 className="text-center text-lg font-bold">
        Upload your .csv or .xslx file
      </h2>
      <input
        type="file"
        ref={inputRef}
        accept=".csv"
        onChange={handleChange}
        className="hidden"
      />
      <div className="flex flex-col w-full gap-1 items-center">
        <Button
          onClick={() => {
            inputRef.current?.click();
          }}
          variant="outlined"
          className="w-min"
        >
          SELECT
        </Button>
        {file !== null && <p>{file.name}</p>}
      </div>
      {file !== null &&
        (status !== "loading" ? (
          <Button variant="contained" onClick={handleUpload}>
            PROCESS
          </Button>
        ) : (
          <CircularProgress className="self-center" />
        ))}
      <Collapse in={openAlert}>
        <Alert
          variant="filled"
          severity={alertStatus}
          onClose={() => {
            setStatus("idle");
          }}
        >
          {alertStatus === "success"
            ? "File Upload Successfull"
            : "File Upload Error"}
        </Alert>
      </Collapse>
    </div>
  );
};

export default FileUpload;
