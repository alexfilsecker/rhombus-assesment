import { Button } from "@mui/material";
import axios from "axios";
import { ChangeEvent, useRef, useState } from "react";

const API_URL = "http://localhost:8000";

const FileUpload = () => {
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

    const response = await axios.get(`${API_URL}/api`);
    console.log(response.data);
  };

  return (
    <div className="flex flex-col gap-2">
      <h2>Upload Your .csv or .xslx file</h2>
      <form className="flex flex-col gap-4 w-min">
        <input
          type="file"
          ref={inputRef}
          accept=".csv"
          onChange={handleChange}
          className="hidden"
        />
        <div className="flex gap-3 items-end">
          <Button
            onClick={() => {
              inputRef.current?.click();
            }}
            variant="outlined"
          >
            SELECT
          </Button>
          {file !== null && <p>{file.name}</p>}
        </div>
        {file !== null && (
          <Button variant="contained" onClick={handleUpload}>
            Upload
          </Button>
        )}
      </form>
    </div>
  );
};

export default FileUpload;
