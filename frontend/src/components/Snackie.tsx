import { Alert, Snackbar } from "@mui/material";
import { Dispatch, SetStateAction } from "react";

type SnackieProps = {
  openAlert: boolean;
  setOpenAlert: Dispatch<SetStateAction<boolean>>;
  alertSeverity: "success" | "error";
  alertMessage: string;
};

const Snackie = ({
  openAlert,
  setOpenAlert,
  alertSeverity,
  alertMessage,
}: SnackieProps): JSX.Element => {
  return (
    <Snackbar
      open={openAlert}
      onClose={() => {
        setOpenAlert(false);
      }}
      autoHideDuration={alertSeverity === "success" ? 1000 : null}
    >
      <Alert severity={alertSeverity}>{alertMessage}</Alert>
    </Snackbar>
  );
};

export default Snackie;
