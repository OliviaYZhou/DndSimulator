import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter, Switch, Route } from "react-router-dom";
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

import Dice from "./react-components/Dice.js";
import DiceBoard from "./react-components/DiceBoard.js";
import CharacterStatsCard from "./react-components/CharacterStatsCard";
import Directions from "./react-components/Directions";
import CharacterWorkSpace from "./react-components/CharacterWorkSpace";
ReactDOM.render(
  <BrowserRouter>
    <Switch>
      <Route exact path="/diceboard" render={() => <DiceBoard />} />
      <Route exact path="/charactercard" render={() => <CharacterStatsCard />} />
      <Route exact path="/" render={() => <App />} />
      <Route exact path="/direction" render={() => <Directions />} />
      <Route exact path="/workspace" render={() => <CharacterWorkSpace />} />
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
