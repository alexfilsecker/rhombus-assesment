import { Alert, AlertTitle, Button, CircularProgress } from "@mui/material";
import axios from "axios";
import { useEffect, useState, Dispatch, SetStateAction } from "react";
import { API_URL, MyAlert, Status } from "../App";
import FileInput from "./FileInput";
import ProcessOptions from "./ProcessOptions";
import PreviewTable from "./PreviewTable";
import { ForceCastValueMap } from "../utils/constants";

type UploadErrors = {
  [header: string]: string;
};

type UploadFileApiResponse = {
  file_id: string;
  errors: UploadErrors;
};

type FileUploadProps = {
  setFileId: Dispatch<SetStateAction<string | null>>;
  setAlertStatus: Dispatch<SetStateAction<MyAlert>>;
};

export type ForceCastTypes = keyof typeof ForceCastValueMap;

export type CastMap = {
  [header: string]: {
    type: ForceCastTypes;
    option?: string;
  };
};

const FileUpload = ({ setFileId, setAlertStatus }: FileUploadProps) => {
  const [uploadStatus, setUploadStatus] = useState<Status>("idle");
  const [uploadErrors, setUploadErrors] = useState<UploadErrors>({});

  const [file, setFile] = useState<File | null>(null);
  const [fileCells, setFileCells] = useState<string[][]>([]);

  const [forceCast, setForceCast] = useState<CastMap | null>(null);

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
    setUploadErrors({});
    setAlertStatus((prev) => ({ ...prev, open: false }));
  }, [uploadStatus, setAlertStatus]);

  const handleUpload = async () => {
    if (file === null) return;
    if (forceCast === null) return;

    const formData = new FormData();
    formData.append("file", file);
    Object.entries(forceCast).forEach(([header, value]) => {
      if (value.type !== "default") {
        let appending: string = value.type;
        if (value.option !== undefined) {
          appending = value.option;
          if (value.type === "datetime") {
            appending = `datetime(${value.option})`;
          }
        }
        formData.append(`cast-col-${header}`, appending);
      }
    });

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
      setUploadErrors(response.data.errors);
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
        <div className="flex flex-col gap-10">
          <PreviewTable fileCells={fileCells} />
          <ProcessOptions
            headers={fileCells[0]}
            forceCast={forceCast}
            setForceCast={setForceCast}
          />
          {uploadStatus !== "loading" ? (
            <Button
              variant="contained"
              onClick={handleUpload}
              className="w-min self-center"
            >
              PROCESS
            </Button>
          ) : (
            <CircularProgress className="self-center" />
          )}
        </div>
      )}
      <div className="flex flex-col gap-1 text-red-500">
        {Object.entries(uploadErrors).map(([header, error]) => (
          <Alert severity="error">
            <AlertTitle>Error in {header}</AlertTitle>
            {error}
          </Alert>
        ))}
      </div>
    </div>
  );
};

export default FileUpload;
