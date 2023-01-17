import React, {Fragment, useRef} from 'react';
import {uid} from "react-uid";
import {withRouter} from 'react-router-dom';
import CharacterStatsCard from './CharacterStatsCard';
import DiceBoard from './DiceBoard';
import "../styles/DiceBoard.css"
import "../styles/CharacterWorkSpace.css"
import StatusEffectForm from './StatusEffectForm';

class CharacterWorkSpace extends React.Component {

    state = {
        showStatusForm: false
    }

    showStatusForm = () => {
        this.setState({showStatusForm : true})
    }
    closeStatusForm = () => {
        this.setState({showStatusForm : false})
    }

    render(){
        const renderStatusEffectForm = () => {
            if (this.state.showStatusForm){
                return <StatusEffectForm characterid={this.props.characterid} socket={this.props.socket} closeStatusForm={this.closeStatusForm} />
            }
            
        }
        return(
            <div className='CharacterWorkSpace'>
                <div className='flexbox'>
                    {/* {console.log("workspace board", this.props.boardIndex)} */}
                    <CharacterStatsCard socket={this.props.socket} characterid={this.props.characterid} showStatusForm={this.showStatusForm} />
                    {renderStatusEffectForm()}
                </div>
                <DiceBoard socket={this.props.socket} boardIndex={this.props.boardIndex}/>
            </div>
        )

    }
    

}

export default CharacterWorkSpace;