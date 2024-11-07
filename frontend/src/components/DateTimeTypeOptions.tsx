import { TextField } from "@mui/material";
import { TypeOptionsProps } from "./NumberTypeOptions";
import { ChangeEvent } from "react";

const DateTimeTypeOptions = ({
  forceCast,
  header,
  setForceCast,
}: TypeOptionsProps): JSX.Element => {
  const castType = forceCast[header].type;
  if (forceCast === null) return <div></div>;
  if (castType !== "datetime") return <div></div>;

  const handleChange = (ev: ChangeEvent<HTMLInputElement>) => {
    setForceCast((prev) => {
      if (prev === null) return null;

      const value = ev.target.value.length === 0 ? undefined : ev.target.value;

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
    <TextField
      value={forceCast[header].option ?? ""}
      onChange={handleChange}
      label="Format"
    />
  );
};

export default DateTimeTypeOptions;
