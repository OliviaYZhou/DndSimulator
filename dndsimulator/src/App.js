import './App.css';
import React from 'react';
// import Dice from "./react-components/Dice";
// import CharacterStatsCard from './react-components/CharacterStatsCard';
import { io } from "socket.io-client"
import {withRouter} from 'react-router-dom';

import Directions from './react-components/Directions';
import CharacterArea from './react-components/Characters/CharacterArea';
import DiceArea from './react-components/Dice/DiceArea';

// let socket = socketIOClient("http://52.14.89.21/");
// let socket = socketIOClient("http://localhost:5000/");
const socket = io();

class App extends React.Component {
  state = {
    characterList: ["tentacle_guy", "orc_guy", "tester2"]
  }
  render() {
    return (
      <div className="App">
        <div className='main-grid'>
          <CharacterArea socket={socket}/>
          <div></div>
          <DiceArea socket={socket}/>
          <Directions/>
        </div>

      </div>
    )
  }
  
}

export default (App);
