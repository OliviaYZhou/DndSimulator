import "./App.css"
import "./styles/CommonStyles.css"
import React, { Fragment } from "react"
// import Dice from "./react-components/Dice";
// import CharacterStatsCard from './react-components/CharacterStatsCard';
import { io } from "socket.io-client"
import { withRouter } from "react-router-dom"

import Directions from "./react-components/Directions"
import CharacterArea from "./react-components/Characters/CharacterArea"
import DiceArea from "./react-components/Dice/DiceArea"
import SideBar from "./react-components/SideBar"
import Session from "./react-components/Session"

// let socket = socketIOClient("http://52.14.89.21/");
// let socket = socketIOClient("http://localhost:5000/");
const socket = io()

class App extends React.Component {
    state = {
        characterList: ["tentacle_guy", "orc_guy", "tester2"],
    }
    render() {
        return (
            <body>
                <img src="/assets/Art/DNDTK_revised_background.png" id="background" />
                <img id="border" src="/assets/Art/DNDTK_revised_screenborder.png" />
                <img id="draco" src="/assets/Art/DNDTK_revised_dracowithsword.png" />
                <SideBar currentTurn={4} />
                <div id="App">
                    <div className="main-grid">
                        <CharacterArea socket={socket} />
                        <Session currentTurn={4} />
                        <DiceArea socket={socket} />
                        {/* <Directions /> */}
                    </div>
                </div>
            </body>
        )
    }
}

export default App
