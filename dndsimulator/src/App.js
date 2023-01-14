import './App.css';
import Dice from "./react-components/Dice";
import React from 'react';
import CharacterStatsCard from './react-components/CharacterStatsCard';
import socketIOClient from "socket.io-client"
import {withRouter} from 'react-router-dom';
import CharacterWorkSpace from './react-components/CharacterWorkSpace';
import Directions from './react-components/Directions';

let socket = socketIOClient("http://52.14.89.21/");

class App extends React.Component {
  state = {
    characterList: ["tester2"]
  }
  render() {
    return (
      <div className="App">
        Hello
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
