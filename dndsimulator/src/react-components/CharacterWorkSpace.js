import React, {Fragment, useRef} from 'react';
import {uid} from "react-uid";
import {withRouter} from 'react-router-dom';
import CharacterStatsCard from './CharacterStatsCard';
import DiceBoard from './DiceBoard';
import "../styles/DiceBoard.css"
import "../styles/CharacterWorkSpace.css"

class CharacterWorkSpace extends React.Component {

    state = {
        characterid: this.props.characterid,
        socket: this.props.socket
    }

    render(){
        return(
            <div className='CharacterWorkSpace'>
                <CharacterStatsCard socket={this.state.socket} characterid={this.state.characterid}/>
                <DiceBoard socket={this.state.socket} />
            </div>
        )

    }
    

}

export default CharacterWorkSpace;