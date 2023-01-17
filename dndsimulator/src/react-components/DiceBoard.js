import React, {Fragment, useRef} from 'react';
import {uid} from "react-uid";
import {withRouter} from 'react-router-dom';
import Dice from "./Dice";
import Directions from "./Directions";
import "../styles/DiceBoard.css"
import socketIOClient from "socket.io-client"

// let socket = socketIOClient("http://localhost:5000/");


class DiceBoard extends React.Component {
    state = {
        diceList: [], // [[dicemax, diceval, rolling]]
        customDice: '',
        diceHistory: [],
        isRolling: false,
        socket: this.props.socket,
        boardIndex: this.props.boardIndex
        
    }
    componentDidMount() {
        console.log("mount board index", this.state.boardIndex)
        this.state.socket.emit("i_just_connected", {boardIndex: this.props.boardIndex})
        this.state.socket.on(`welcome`, data => this.load_board(data))
        
        this.state.socket.on(`get_dice/${this.state.boardIndex}`, data=> {this.setDice(data)});
        this.state.socket.on(`everyone_start_roll/${this.state.boardIndex}`, data=>{this.rollDice(data.index, data.predetermined_result)})
        // this.scaleFontSize("dice-history")
        
    }

    // scaleFontSize(element) {
    //     var container = document.getElementsByClassName(element);
    
    //     // Reset font-size to 100% to begin
    //     container.style.fontSize = "100%";
    
    //     // Check if the text is wider than its container,
    //     // if so then reduce font-size
    //     if (container.scrollWidth > container.clientWidth) {
    //         container.style.fontSize = "70%";
    //     }
    // }

    load_board(data){
        this.setState({diceList: data.diceList, diceHistory: data.diceHistory, boardIndex: data.boardIndex})
        this.state.socket.off("welcome")
    }


    deleteDice = (index) => {
        this.state.socket.emit("delete_dice", {index: index, boardIndex: this.state.boardIndex})
    }

    clearDice(){
        this.state.socket.emit("clear_dice", {boardIndex: this.state.boardIndex})
    }

    clearHistory(){
        this.state.socket.emit("clear_history", {boardIndex: this.state.boardIndex})
    }
    
    rolling(index, diceMax) {
        
        var ranVar = Math.floor(Math.random() * diceMax) + 1
        let items = [...this.state.diceList]
        var rolledDice = items[index]
        rolledDice[1] = ranVar
        items[index] = rolledDice

        this.setState({
            diceList: items
        })
    }

    setRollingStatus(index, on=true){
        let items = [...this.state.diceList]
        var clickedDice = [...items[index]]
        clickedDice[2] = on
        items[index] = clickedDice
        
        this.setState({
            diceList: items,
            isRolling: on
        })
    }

    rollDice(index, predetermined_result) {
        var diceMax = this.state.diceList[index][0]
        this.setRollingStatus(index, true)
        var times = 0
        var interval = setInterval(() => 
            {   

                this.rolling(index, diceMax)
                if (++times == 10){
                    clearInterval(interval)
                    
                    this.updateDice(index, predetermined_result, diceMax)
                    this.setRollingStatus(index, false)
                }
            }
            , 100);
    }

    setDice(data){
        console.log("from server", data)
        this.setState({diceHistory: data.history,
                       diceList: data.diceList
        })
        
      }

    // getHistory(){
    //     fetch("/diceboard").then(res =>{
    //         return res.json()
    //     })
    //         .then((data) => {
    //             this.setState({diceHistory: data.history})
    //         })
    // }

    handleInputChange(event, fieldName) {
        const target = event.target;
        const value = target.value;

        this.setState({[fieldName]: value});
    }
    addDice(diceMax){

        const newDiceJson = 
        {
            dicemax: diceMax,
            boardIndex: this.state.boardIndex
        }
        console.log(newDiceJson)

        this.state.socket.emit("dice_add", newDiceJson)
    }

    emitUpdate = (dataJson) => {
        this.state.socket.emit("dice_update", dataJson)
    }

    updateDice = (index, roll, dicemax) => {

        const diceJson = 
                {
                    index: index,
                    diceval: roll,
                    dicemax: dicemax,
                    allDice: this.state.diceList,
                    boardIndex: this.state.boardIndex
                }
        console.log(diceJson)
        this.emitUpdate(diceJson)
    }

    render() {
        
        return (
      
            <div className='dice-module roundedbox'>
                <div className='row wrapper'>
                    <div className='add-dice roundedbox'>
                        <div className='addDiceButtonColumn column'>
                            {/* <button className='addDiceButton defaultButton'
                            onClick={() => {this.addDice(3)}}>
                            d3</button>
                            <button className='addDiceButton defaultButton'
                            onClick={() => {this.addDice(4)}}>d4</button> */}
                            <button className='addDiceButton defaultButton'
                            onClick={() => {this.addDice(6)}}>d6</button>
                            <button className='addDiceButton defaultButton'
                            onClick={() => {this.addDice(8)}}>d8</button>
                            <button className='addDiceButton defaultButton'
                            onClick={() => {this.addDice(10)}}>d10</button>
                            <button className='addDiceButton defaultButton'
                            onClick={() => {this.addDice(20)}}>d20</button>
                            <button className='addDiceButton defaultButton lowestButton'
                            onClick={() => {this.addDice(100)}}>d100</button>
                            <div className='column customDiceWrapper'>

                                <span className='label'>Custom</span>
                                <div className='d-something row'>
                                    d <input
                                            className="customDiceInput roundedbox"
                                            type="number"
                                            onChange={(e) => this.handleInputChange(e, "customDice")}
                                        />
                                </div>
                                
                                <button className='addCustomDiceButton defaultButton'
                                onClick={() => {this.addDice(this.state.customDice)}}>Add Dice</button>

                            </div>
                            
                        </div>
                        
                    </div>

                    <div class='dice-board-wrapper roundedbox'>
                    
                        <span className='bigHeader hoverable' onContextMenu={(e)=>{
                            e.preventDefault()
                            this.clearDice()
                        }}>Dice</span>
                        <ul id="dice-board" style={{backgroundColor: this.state.isRolling ?  " rgb(253, 184, 244)": "rgb(251, 222, 247)"}}>
                            {this.state.diceList.map((dice, index) => (
                                <li key={index}>
                                    <Dice properties={dice} index={index} socket={this.state.socket} deleteDice={this.deleteDice} 
                                    boardIndex={this.state.boardIndex}
                                    />
                                </li>
                            ))}
       
                        </ul>
                
                    </div>
                    <div className='dice-history roundedbox'>
                        <span className='bigHeader hoverable' onContextMenu={(e)=>{
                            e.preventDefault()
                            this.clearHistory()
                        }}>History</span>
                        <ul className='dice-history-list'>
                            {this.state.diceHistory.map((historyString, index) => (
                                <li key={index}>
                                    {historyString}
                                </li>
                            ))}
                        </ul>
                    </div>
                </div>
            </div>
      
    
        )
    }

}

export default withRouter(DiceBoard);
