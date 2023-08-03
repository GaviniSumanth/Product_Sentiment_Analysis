import { useState } from "react";
import urls from "../urls";
import Display from "./Display";
const styles = {
  form: {
    color: "white",
    fontWeight: "boldest",
    display: "flex",
    flexDirection: "column",
    gap: 10,
    width: "700px",
    margin: "0 auto",
    backgroundColor: "black",
    padding: "20px 30px",
    borderRadius: "30px",
  },
};
function Text(props) {
  return (
    <div className="field">
      <label htmlFor={props.identifier}>{props.label}</label>
      <br />
      <input
        type="text"
        style={{ width: "100%", padding: "5px 10px", margin: "8px 0 10px 0" }}
        name={props.identifier}
        placeholder={props.placeholder}
        required
      />
    </div>
  );
}
function Number(props) {
  return (
    <div className="field">
      <label htmlFor={props.identifier}>{props.label}</label>
      <br />
      <input
        type="number"
        name={props.identifier}
        min={props.min}
        max={props.max}
        required
      />
    </div>
  );
}
function Select(props) {
  return (
    <div className="field">
      <label htmlFor={props.identifier}>{props.label}</label>
      <br />
      <select name={props.identifier}>
        {props.options.map((value) => (
          <option key={value} value={value}>
            {value}
          </option>
        ))}
      </select>
    </div>
  );
}
function Radio(props) {
  return (
    <div className="field">
      <label htmlFor={props.identifier}>{props.label}</label>
      <br />
      {props.options.map((value) => (
        <label key={value}>
          <input type="radio" name={props.identifier} value={value} />
          {value}
          {!(value % 2) ? <br /> : null}
        </label>
      ))}
    </div>
  );
}
export default function Form() {
  let [state, setState] = useState(true);
  let [isOpen, setIsOpen] = useState(false);
  let [form, setForm] = useState(false);
  const submitForm = (e) => {
    const formData = new FormData(e.target);
    var data = {
      form: window.location.hash.split("?")[1].split("=")[1],
    };
    formData.forEach((value, key) => (data[key] = value));
    URL = urls.SUBMIT;
    console.log(JSON.stringify(data));
    fetch(URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((json) => {
        console.log("HERE:", json);
        setState(json);
        setIsOpen(true);
      });
  };
  URL = urls.FORM({
    form: window.location.hash.split("?")[1].split("=")[1],
  });
  fetch(URL, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((json) => {
      console.log("HERE:", json);
      if (form === false) setForm(json);
    });
  if (form) {
    return (
      <div className="formbg">
        <form
          method="POST"
          encType="multipart/form-data"
          style={styles.form}
          onSubmit={(e) => {
            e.preventDefault();
            submitForm(e);
          }}
        >
          {form.map((e) => {
            if (e.type === "text") {
              return (
                <Text identifier={e.identifier} label={e.label} key={e.label} />
              );
            } else if (e.type === "select") {
              return (
                <Select
                  identifier={e.identifier}
                  label={e.label}
                  key={e.label}
                  options={e.options}
                />
              );
            } else if (e.type === "radio") {
              return (
                <Radio
                  identifier={e.identifier}
                  label={e.label}
                  key={e.label}
                  options={e.options}
                />
              );
            } else if (e.type === "number") {
              return (
                <Number
                  identifier={e.identifier}
                  label={e.label}
                  key={e.label}
                  min={e.min}
                  max={e.max}
                />
              );
            }
          })}
          <input type="submit" value="Submit" />
          <Display data={state} state={isOpen} setState={setIsOpen} />
        </form>
      </div>
    );
  }
}
