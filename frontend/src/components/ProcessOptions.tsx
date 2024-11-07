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
import NumberTypeOptions from "./NumberTypeOptions";
import DateTimeTypeOptions from "./DateTimeTypeOptions";

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
      setForceCast((prev) => ({ ...prev, [header]: { type: newCast } }));
    };
    return inner;
  };

  useEffect(() => {
    setForceCast(
      headers.reduce<CastMap>((acc, header) => {
        acc[header] = { type: "default" };
        return acc;
      }, {})
    );
  }, [headers, setForceCast]);

  return (
    <div className="flex flex-col gap-10 overflow-x-scroll">
      <div className="text-2xl font-bold">Processing Options</div>
      {forceCast !== null && (
        <div className="flex items-start w-full gap-2 ">
          {headers.map((header) => {
            const id = `select-${header}`;
            return (
              <div className="flex flex-col gap-3 min-w-44" key={header}>
                <FormControl fullWidth>
                  <InputLabel id={id}>{header}</InputLabel>
                  <Select
                    labelId={id}
                    label={header}
                    value={forceCast[header].type}
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
                </FormControl>
                {(forceCast[header].type === "int" ||
                  forceCast[header].type === "uint" ||
                  forceCast[header].type === "float") && (
                  <NumberTypeOptions
                    forceCast={forceCast}
                    setForceCast={setForceCast}
                    header={header}
                  />
                )}
                {forceCast[header].type === "datetime" && (
                  <DateTimeTypeOptions
                    forceCast={forceCast}
                    setForceCast={setForceCast}
                    header={header}
                  />
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default ProcessOptions;
