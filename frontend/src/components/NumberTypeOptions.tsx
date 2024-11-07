import {
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  SelectChangeEvent,
} from "@mui/material";
import { NumberOptionsByValue } from "../utils/constants";
import { CastMap } from "./FileUpload";
import { Dispatch, SetStateAction } from "react";

export type TypeOptionsProps = {
  forceCast: CastMap;
  setForceCast: Dispatch<SetStateAction<CastMap | null>>;
  header: string;
};

const NumberTypeOptions = ({
  forceCast,
  setForceCast,
  header,
}: TypeOptionsProps): JSX.Element => {
  const castType = forceCast[header].type;
  if (forceCast === null) return <div></div>;
  if (castType !== "int" && castType !== "uint" && castType !== "float")
    return <div></div>;

  const values = NumberOptionsByValue[castType];

  const handleChange = (ev: SelectChangeEvent<string>) => {
    setForceCast((prev) => {
      if (prev === null) return null;

      const value = ev.target.value === "default" ? undefined : ev.target.value;

      return {
        ...prev,
        [header]: {
          ...prev[header],
          option: value,
        },
      };
    });
  };

  return (
    <FormControl>
      <InputLabel id={`${header}-id`}>Options</InputLabel>
      <Select
        labelId={`${header}-id`}
        label="Options"
        value={forceCast[header].option ?? "default"}
        onChange={handleChange}
      >
        <MenuItem value="default">Default</MenuItem>
        {Object.entries(values).map(([key, value]) => (
          <MenuItem key={key} value={key}>
            {value}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
};

export default NumberTypeOptions;
