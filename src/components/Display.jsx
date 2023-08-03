import { useState } from "react";
import { Dialog } from "@headlessui/react";

function Display(props) {
  return (
    <Dialog
      open={props.state}
      onClose={() => props.setState(false)}
      className="dialog"
    >
      <Dialog.Panel>
        <Dialog.Title className="dialog-title">Analysis Result</Dialog.Title>
        <Dialog.Description className="dialog-description">
          {props.data.result}
        </Dialog.Description>
        <button className="button" onClick={() => props.setState(false)}>
          Ok
        </button>
      </Dialog.Panel>
    </Dialog>
  );
}
export default Display;
