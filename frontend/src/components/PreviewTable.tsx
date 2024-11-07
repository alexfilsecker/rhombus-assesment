import {
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from "@mui/material";
import { useEffect, useState } from "react";

type PreviewTableProps = {
  file: File;
};

const PreviewTable = ({ file }: PreviewTableProps): JSX.Element => {
  const [fileCells, setFileCells] = useState<string[][]>([]);

  useEffect(() => {
    const reader = new FileReader();

    reader.onload = (event) => {
      if (event.target === null) return;
      const content = event.target.result;
      if (typeof content !== "string") return;
      const splited = content.split("\n").map((row) => {
        return row.split(",");
      });
      splited.slice(0, splited.length > 11 ? 11 : -1);

      setFileCells(splited);
    };

    reader.readAsText(file);
  });

  if (fileCells.length === 0) {
    return <div></div>;
  }

  return (
    <div className="flex flex-col">
      <div>PREVIEW</div>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              {fileCells[0].map((headerCell, headerIndex) => (
                <TableCell key={headerIndex}>{headerCell}</TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {fileCells.slice(1).map((row, rowIndex) => (
              <TableRow key={rowIndex}>
                {row.map((cell, cellIndex) => (
                  <TableCell key={cellIndex}>{cell}</TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
};

export default PreviewTable;
