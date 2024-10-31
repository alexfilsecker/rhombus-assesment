import { Alert, Button, CircularProgress } from "@mui/material";
import axios from "axios";
import { ChangeEvent, useRef, useState } from "react";

const API_URL = "http://localhost:8000";

const FileUpload = () => {
  const [status, setStatus] = useState<
    "idle" | "loading" | "success" | "error"
  >("idle");

  const [file, setFile] = useState<File | null>(null);

  const inputRef = useRef<HTMLInputElement>(null);

  const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (files === null || files.length === 0) return;
    setFile(files[0]);
  };

  const handleUpload = async () => {
    if (file === null) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      setStatus("loading");
      const response = await axios.get(`${API_URL}/api/`);
      setStatus("success");
      console.log(response.data);
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
      {file !== null && status === "idle" && (
        <Button variant="contained" onClick={handleUpload}>
          PROCESS
        </Button>
      )}
      {status === "loading" && <CircularProgress />}
      {(status === "success" || status === "error") && (
        <Alert
          variant="filled"
          severity={status}
          onClose={() => setStatus("idle")}
        >
          {status === "success"
            ? "File Upload Successfull"
            : "File Upload Error"}
        </Alert>
      )}
    </div>
  );
};

export default FileUpload;
