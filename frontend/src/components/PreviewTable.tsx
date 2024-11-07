import {
  Button,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from "@mui/material";
import { useState } from "react";

type PreviewTableProps = {
  fileCells: string[][];
};

const MIN_PREVIEW = 5;

const PreviewTable = ({ fileCells }: PreviewTableProps): JSX.Element => {
  const [previewLength, setPreviewLength] = useState<number>(MIN_PREVIEW);

  const handleIncDec = (ammount: number) => {
    const inner = () => {
      const rows = fileCells.length - 1;
      setPreviewLength((prev) => {
        const newLenght = prev + ammount;
        if (newLenght > rows) return rows;
        if (newLenght < MIN_PREVIEW) return MIN_PREVIEW;
        return newLenght;
      });
    };

    return inner;
  };

  const headers = fileCells[0];
  const data = fileCells.slice(1, previewLength);

  if (fileCells.length === 0) {
    return <div></div>;
  }

  return (
    <div className="flex flex-col items-center gap-4">
      <div>
        Previewing {previewLength} of {fileCells.length - 1}
      </div>
      <TableContainer component={Paper}>
        <Table size="small">
          <TableHead>
            <TableRow>
              {headers.map((headerCell, headerIndex) => (
                <TableCell key={headerIndex}>{headerCell}</TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {data.map((row, rowIndex) => (
              <TableRow key={rowIndex}>
                {row.map((cell, cellIndex) => (
                  <TableCell key={cellIndex}>{cell}</TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      <div className="flex gap-2">
        <Button
          onClick={handleIncDec(-5)}
          disabled={previewLength === MIN_PREVIEW}
        >
          Less
        </Button>
        <Button
          onClick={handleIncDec(5)}
          variant="contained"
          disabled={previewLength === fileCells.length - 1}
        >
          More
        </Button>
      </div>
    </div>
  );
};

export default PreviewTable;
