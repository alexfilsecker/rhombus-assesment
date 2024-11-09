import {
  ChangeEvent,
  Dispatch,
  SetStateAction,
  useEffect,
  useRef,
} from "react";
import { MyAlert } from "../App";
import { Button } from "@mui/material";

import * as XLSX from "xlsx";

type FileInputProps = {
  setFile: Dispatch<SetStateAction<File | null>>;
  setAlertStatus: Dispatch<SetStateAction<MyAlert>>;
  file: File | null;
  setFileCells: Dispatch<SetStateAction<string[][]>>;
};

const FileInput = ({
  setFile,
  setAlertStatus,
  file,

  setFileCells,
}: FileInputProps): JSX.Element => {
  const inputRef = useRef<HTMLInputElement>(null);

  const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (files === null || files.length === 0) return;
    setFile(files[0]);
    setAlertStatus((prev) => ({ ...prev, open: false }));
  };

  useEffect(() => {
    if (file === null) return;
    const reader = new FileReader();

    const parseCSV = (content: string) => {
      return content.split("\n").map((row) => {
        return row.split(",");
      });
    };

    if (file.type === "text/csv") {
      reader.onload = (event) => {
        if (event.target === null) return;
        const content = event.target.result;
        if (typeof content !== "string") return;

        setFileCells(parseCSV(content));
      };
      reader.readAsText(file);
    } else if (
      file.type ===
      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    ) {
      reader.onload = (event) => {
        if (event.target === null) return;
        const content = event.target.result;
        if (typeof content !== "object" || content === null) return;

        const workbook = XLSX.read(event.target.result, { type: "binary" });
        const firstSheetName = workbook.SheetNames[0];
        const firstSheet = workbook.Sheets[firstSheetName];
        const sheetAsCSV = XLSX.utils.sheet_to_csv(firstSheet);
        setFileCells(parseCSV(sheetAsCSV));
      };
      reader.readAsArrayBuffer(file);
    } else {
      console.error(`file type '${file.type}' not suported`);
    }
  }, [file, setFileCells]);

  // useEffect(() => {
  //   if (!reset) return;
  //   if (inputRef.current === null) return;
  //   inputRef.current.value = "";
  //   inputRef.current.type = "text";
  //   inputRef.current.type = "file";
  //   setFile(null);
  // }, [reset, setReset, setFile]);

  return (
    <>
      <input
        type="file"
        ref={inputRef}
        accept=".csv, .xlsx"
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
    </>
  );
};

export default FileInput;
