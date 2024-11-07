import { Alert, Snackbar } from "@mui/material";
import { Dispatch, SetStateAction } from "react";
import { MyAlert } from "../App";

type SnackieProps = {
  setAlertStatus: Dispatch<SetStateAction<MyAlert>>;
  alertStatus: MyAlert;
};

const Snackie = ({
  setAlertStatus,
  alertStatus,
}: SnackieProps): JSX.Element => {
  return (
    <Snackbar
      open={alertStatus.open}
      onClose={() => {
        setAlertStatus((prev) => ({ ...prev, open: false }));
      }}
      autoHideDuration={alertStatus.severity === "success" ? 1000 : null}
    >
      <Alert severity={alertStatus.severity}>{alertStatus.message}</Alert>
    </Snackbar>
  );
};

export default Snackie;
