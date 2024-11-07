import {
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  SelectChangeEvent,
} from "@mui/material";
import { useState } from "react";

type ProcessOptionsProps = {
  headers: string[];
};

type CastMap = {
  [key: string]: string;
};

const ProcessOptions = ({ headers }: ProcessOptionsProps): JSX.Element => {
  const [forceCast, setForceCast] = useState<CastMap>(
    headers.reduce<CastMap>((acc, header) => {
      acc[header] = "default";
      return acc;
    }, {})
  );

  const handleChange = (header: string) => {
    const inner = (event: SelectChangeEvent) => {
      setForceCast((prev) => ({ ...prev, [header]: event.target.value }));
    };
    return inner;
  };

  return (
    <div className="flex flex-col gap-10">
      <div className="text-2xl font-bold">Processing Options</div>
      <div className="flex w-full gap-10">
        {headers.map((header) => {
          const id = `select-${header}`;
          return (
            <div className="min-w-44">
              <FormControl key={header} fullWidth>
                <InputLabel id={id}>{header}</InputLabel>
                <Select
                  labelId={id}
                  label={header}
                  value={forceCast[header]}
                  onChange={handleChange(header)}
                >
                  <MenuItem value="default">Default</MenuItem>
                  <MenuItem value="number">Number</MenuItem>
                </Select>
              </FormControl>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default ProcessOptions;
