import { Button, CircularProgress } from "@mui/material";
import axios from "axios";
import {
  ChangeEvent,
  useEffect,
  useRef,
  useState,
  Dispatch,
  SetStateAction,
} from "react";
import { API_URL, Status } from "../App";

type UploadFileApiResponse = {
  file_id: string;
};

type FileUploadProps = {
  setFileId: Dispatch<SetStateAction<string | null>>;
  setOpenAlert: Dispatch<SetStateAction<boolean>>;
  setAlertSeverity: Dispatch<SetStateAction<"error" | "success">>;
  setAlertMessage: Dispatch<SetStateAction<string>>;
  file: File | null;
  setFile: Dispatch<SetStateAction<File | null>>;
};

const FileUpload = ({
  setFileId,
  setOpenAlert,
  setAlertSeverity,
  setAlertMessage,
  file,
  setFile,
}: FileUploadProps) => {
  const [status, setStatus] = useState<Status>("idle");

  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (status === "success" || status === "error") {
      setOpenAlert(true);
      setAlertSeverity(status);
      setAlertMessage(
        status === "success"
          ? "File uploaded successfully"
          : "Error uploading file"
      );
      return;
    }

    setOpenAlert(false);
  }, [status, setOpenAlert, setAlertSeverity, setAlertMessage]);

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
      const response = await axios.post<UploadFileApiResponse>(
        `${API_URL}/api/process-file`,
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );
      setStatus("success");
      setFileId(response.data.file_id);
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
    </div>
  );
};

export default FileUpload;
