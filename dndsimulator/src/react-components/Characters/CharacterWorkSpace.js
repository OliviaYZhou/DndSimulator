import React, { Fragment, useRef } from "react"
import { useEffect, useState } from "react"
import { uid } from "react-uid"
import { withRouter } from "react-router-dom"
import CharacterStatsCard from "./CharacterStatsCard"
import "../../styles/CharacterWorkSpace.css"
import StatusEffectForm from "./StatusEffectForm"
import InventoryForm from "./InventoryForm"

// import CharacterAdd from './CharacterAdd';
// import DiceBoard from './DiceBoard';
// import "../styles/DiceBoard.css"

export default function CharacterWorkSpace(props) {
    const [showInventoryForm, setShowInventoryForm] = useState(false)
    function renderInventoryForm() {
        if (showInventoryForm) {
            return (
                <InventoryForm
                    characterid={props.characterid}
                    closeForm={() => setShowInventoryForm(false)}
                />
            )
        }
    }
    return (
        <div className="CharacterWorkSpace">
            <div className="column ch-column">
                <CharacterStatsCard
                    socket={props.socket}
                    characterid={props.characterid}
                    showStatusForm={() => setShowInventoryForm(true)}
                />
                {renderInventoryForm()}
            </div>
        </div>
    )
}
// class CharacterWorkSpace extends React.Component {

//     state = {
//         showStatusForm: false,
//         showInventoryForm: false,
//         showDiceBoard: true
//     }

//     showStatusForm = () => {
//         this.setState({showStatusForm : true})
//     }
//     closeStatusForm = () => {
//         this.setState({showStatusForm : false})
//     }
//     showDiceBoard = () => {
//         this.setState({showDiceBoard: true})
//     }

//     closeDiceBoard = () => {
//         console.log("close ")
//         this.setState({showDiceBoard: false})
//     }

//     render(){
//         const renderStatusEffectForm = () => {
//             if (this.state.showStatusForm){
//                 return <StatusEffectForm characterid={this.props.characterid} socket={this.props.socket} closeStatusForm={this.closeStatusForm} />
//             }
//         }
//         const renderInventoryForm = () => {
//             if (this.state.showStatusForm){
//                 return <StatusEffectForm characterid={this.props.characterid} socket={this.props.socket} closeStatusForm={this.closeStatusForm} />
//             }
//         }
//         // const renderDiceBoard = () =>{
//         //     if (this.state.showDiceBoard){
//         //         return <DiceBoard socket={this.props.socket} boardIndex={this.props.boardIndex} closeDiceBoard={this.closeDiceBoard}/>
//         //     }
//         //     else{
//         //         return <button onClick={() => this.showDiceBoard()}>DiceBoard+</button>
//         //     }
//         // }
//         return(
//             <div className='CharacterWorkSpace'>
//                 <div className='column ch-column'>
//                     {/* {console.log("workspace board", this.props.boardIndex)} */}
//                     <CharacterStatsCard socket={this.props.socket} characterid={this.props.characterid} showStatusForm={this.showStatusForm} />
//                     {renderStatusEffectForm()}
//                     {/* {renderDiceBoard()} */}
//                 </div>

//             </div>
//         )

//     }

// }

// // export default CharacterWorkSpace;
