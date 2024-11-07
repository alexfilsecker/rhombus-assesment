import {
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  SelectChangeEvent,
} from "@mui/material";
import { Dispatch, SetStateAction, useEffect } from "react";
import { CastMap, ForceCastTypes } from "./FileUpload";
import { ForceCastValueMap } from "../utils/constants";

type ProcessOptionsProps = {
  headers: string[];
  forceCast: CastMap | null;
  setForceCast: Dispatch<SetStateAction<CastMap | null>>;
};

const ProcessOptions = ({
  headers,
  forceCast,
  setForceCast,
}: ProcessOptionsProps): JSX.Element => {
  const handleChange = (header: string) => {
    const inner = (event: SelectChangeEvent) => {
      const newCast = event.target.value as ForceCastTypes;
      setForceCast((prev) => ({ ...prev, [header]: newCast }));
    };
    return inner;
  };

  useEffect(() => {
    setForceCast(
      headers.reduce<CastMap>((acc, header) => {
        acc[header] = "default";
        return acc;
      }, {})
    );
  }, [headers, setForceCast]);

  return (
    <div className="flex flex-col gap-10 overflow-x-scroll">
      <div className="text-2xl font-bold">Processing Options</div>
      <div className="flex items-center w-full gap-2 h-32 ">
        {headers.map((header) => {
          const id = `select-${header}`;
          return (
            <FormControl fullWidth key={header} className="!min-w-44">
              <InputLabel id={id}>{header}</InputLabel>
              {forceCast !== null && (
                <Select
                  labelId={id}
                  label={header}
                  value={forceCast[header]}
                  onChange={handleChange(header)}
                >
                  {Object.entries(ForceCastValueMap).map(
                    ([type, humanReadable]) => (
                      <MenuItem value={type} key={type}>
                        {humanReadable}
                      </MenuItem>
                    )
                  )}
                </Select>
              )}
            </FormControl>
          );
        })}
      </div>
    </div>
  );
};

export default ProcessOptions;
