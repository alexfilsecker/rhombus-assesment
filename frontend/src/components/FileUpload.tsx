import { Button, CircularProgress } from "@mui/material";
import axios from "axios";
import { useEffect, useState, Dispatch, SetStateAction } from "react";
import { API_URL, MyAlert, Status } from "../App";
import FileInput from "./FileInput";
import ProcessOptions from "./ProcessOptions";
import PreviewTable from "./PreviewTable";

type UploadFileApiResponse = {
  file_id: string;
};

type FileUploadProps = {
  setFileId: Dispatch<SetStateAction<string | null>>;
  setAlertStatus: Dispatch<SetStateAction<MyAlert>>;
};

const FileUpload = ({ setFileId, setAlertStatus }: FileUploadProps) => {
  const [uploadStatus, setUploadStatus] = useState<Status>("idle");

  const [file, setFile] = useState<File | null>(null);
  const [fileCells, setFileCells] = useState<string[][]>([]);

  useEffect(() => {
    // On error or success, open the alert
    if (uploadStatus === "success" || uploadStatus === "error") {
      setAlertStatus({
        open: true,
        severity: uploadStatus,
        message:
          uploadStatus === "success"
            ? "File uploaded successfully"
            : "Error uploading file",
      });

      return;
    }

    // On every other state, close the alert
    setAlertStatus((prev) => ({ ...prev, open: false }));
  }, [uploadStatus, setAlertStatus]);

  const handleUpload = async () => {
    if (file === null) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      setUploadStatus("loading");
      const response = await axios.post<UploadFileApiResponse>(
        `${API_URL}/api/process-file`,
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );
      setUploadStatus("success");
      setFileId(response.data.file_id);
    } catch (e: unknown) {
      setUploadStatus("error");
      console.error(e);
    }
  };

  return (
    <div className="flex flex-col gap-4 w-full">
      <h2 className="text-center text-lg font-bold">
        Upload your .csv or .xslx file
      </h2>

      <FileInput
        setFile={setFile}
        setAlertStatus={setAlertStatus}
        file={file}
        setFileCells={setFileCells}
      />

      {fileCells.length > 0 && (
        <div className="flex flex-col">
          <PreviewTable fileCells={fileCells} />
          <ProcessOptions headers={fileCells[0]} />
          {uploadStatus !== "loading" ? (
            <Button variant="contained" onClick={handleUpload}>
              PROCESS
            </Button>
          ) : (
            <CircularProgress className="self-center" />
          )}
        </div>
      )}
    </div>
  );
};

export default FileUpload;
