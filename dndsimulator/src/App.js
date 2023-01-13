import './App.css';
import Dice from "./react-components/Dice";
import React from 'react';
import CharacterStatsCard from './react-components/CharacterStatsCard';
import socketIOClient from "socket.io-client"
import {withRouter} from 'react-router-dom';

let socket = socketIOClient("http://localhost:5000/");

class App extends React.Component {
  state = {
    characterList: ["tester2"]
  }
  render() {
    return (
      <div className="App">
        Hello
          <ul className='characters'>
          {this.state.characterList.map((characterid) => (
            <li>
                <CharacterStatsCard characterid={characterid} socket={socket}/>
            </li>
          ))}
              
          </ul>
      </div>
    )
  }
  
}

export default (App);
