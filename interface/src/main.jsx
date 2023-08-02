import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import App from "./App.jsx";
import Form from "./components/Form.jsx";
import "./global.css";
function Fail() {
  document.getElementById("root").style.height = "100vh";
  document.getElementById("root").style.width = "100vw";
  document.getElementById("root").style.overflow = "hidden";
  return (
    <img
      src="https://rare-gallery.com/mocahbig/394707-wallpaper-error-404-anime-4k-hd.jpg"
      style={{ width: "100vw", height: "100vh" }}
      alt="An image showing Error 404 - Page Not Found"
    />
  );
}
ReactDOM.createRoot(document.getElementById("root")).render(
  <Router basename="/">
    <Routes>
      <Route exact path="*" element={<Fail />} />
      <Route exact path="/" element={<App />} />
      <Route exact path="/Form/*" element={<Form />} />
    </Routes>
  </Router>
);
