import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter, Switch, Route } from "react-router-dom";
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

import Dice from "./react-components/Dice.js";
import DiceBoard from "./react-components/DiceBoard.js";
ReactDOM.render(
  <BrowserRouter>
    <Switch>
      <Route exact path="/" render={() => <DiceBoard />} />
      {/* <Route exact path="/book/view" render={() => <BookViewer />} /> */}

    </Switch>
  </BrowserRouter>,
  document.getElementById("root")
);

// const root = ReactDOM.createRoot(document.getElementById('root'));
// root.render(
//   <App />
//   // <React.StrictMode>
   
//   // </React.StrictMode>
// );

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
