import './App.css';
import Dice from "./react-components/Dice";
import React from 'react';
import CharacterStatsCard from './react-components/CharacterStatsCard';
import socketIOClient from "socket.io-client"
import {withRouter} from 'react-router-dom';
import CharacterWorkSpace from './react-components/CharacterWorkSpace';
import Directions from './react-components/Directions';

// let socket = socketIOClient("http://52.14.89.21/");
// let socket = socketIOClient("http://localhost:5000/");
const socket = io();

class App extends React.Component {
  state = {
    characterList: ["tentacle_guy", "orc_guy"]
  }
  render() {
    return (
      <div className="App">
          <ul className='characterWSList'>
          {this.state.characterList.map((characterid) => (
            <li>
                <CharacterWorkSpace characterid={characterid} socket={socket}/>
            </li>
          ))}
              
          </ul>

          <Directions/>
      </div>
    )
  }
  
}

export default (App);
