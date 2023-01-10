import React, {Fragment} from 'react';
import {uid} from "react-uid";
import {withRouter} from 'react-router-dom';
import Dice from "./Dice";
import "../styles/DiceBoard.css"
import socketIOClient from "socket.io-client"

let socket = socketIOClient("http://localhost:5000/");

class DiceBoard extends React.Component {
    state = {
        diceList: [], // [[dicemax, diceval, rolling]]
        customDice: '',
        diceHistory: []
    // constructor(props) {
    //     super(props)
        
    //     }
        
    }
    componentDidMount() {
        // this.getHistory()
        socket.emit("i_just_connected")
        socket.on("welcome", data => this.load_board(data))
        
        socket.on("get_dice", data=> {this.setDice(data)});
        socket.on("everyone_start_roll", data=>{this.rollDice(data.index, data.predetermined_result)})
        
    }

    load_board(data){
        this.setState({diceList: data.diceList, diceHistory: data.diceHistory})
        socket.off("welcome")
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

    setRollingStatus(index){
        let items = [...this.state.diceList]
        var clickedDice = [...items[index]]
        clickedDice[2] = !(items[index][2])
        
        items[index] = clickedDice
        
        this.setState({
            diceList: items
        })
    }

    rollDice(index, predetermined_result) {
        var diceMax = this.state.diceList[index][0]
        this.setRollingStatus(index)
        var times = 0
        var interval = setInterval(() => 
            {
                this.rolling(index, diceMax)
                if (++times == 10){
                    clearInterval(interval)
                    
                    this.updateDice(index, predetermined_result, diceMax)
                    this.setRollingStatus(index)
                    // this.props.addHistory(this.state.diceMax, finalVal)
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

    // componentDidUpdate(){
    //     this.fetchData()
    // }
    getHistory(){
        fetch("/diceboard").then(res =>{
            return res.json()
        })
            .then((data) => {
                this.setState({diceHistory: data.history})
            })
    }

    handleInputChange(event, fieldName) {
        const target = event.target;
        const value = target.value;

        this.setState({[fieldName]: value});
    }
    addDice(diceMax){

        const newDiceJson = 
        {
            dicemax: diceMax,
            allDice: this.state.diceList,
            allhistory: this.state.diceHistory
        }

        socket.emit("dice_add", newDiceJson)


        // this.setState(() => ({
        //     diceList: [...this.state.diceList, [diceMax, `d${diceMax}`]]
        //   }))
        // console.log(this.state.diceList)
    }

    emitUpdate = (dataJson) => {
        socket.emit("dice_update", dataJson)
    }

    updateDice = (index, roll, dicemax) => {


        // let items = [...this.state.diceList]
        // var rolledDice = items[index]
        // rolledDice[1] = roll
        // items[index] = rolledDice

        const diceJson = 
                {
                    index: index,
                    diceval: roll,
                    dicemax: dicemax,
                    allDice: this.state.diceList,
                    allhistory: this.state.diceHistory
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
                            <button className='addDiceButton defaultButton'
                            onClick={() => {this.addDice(3)}}>
                            d3</button>
                            <button className='addDiceButton defaultButton'
                            onClick={() => {this.addDice(4)}}>d4</button>
                            <button className='addDiceButton defaultButton'
                            onClick={() => {this.addDice(6)}}>d6</button>
                            <button className='addDiceButton defaultButton'
                            onClick={() => {this.addDice(10)}}>d10</button>
                            <button className='addDiceButton defaultButton'
                            onClick={() => {this.addDice(20)}}>d20</button>
                            <button className='addDiceButton defaultButton'
                            onClick={() => {this.addDice(100)}}>d100</button>
                            <div className='column customDice'>

                                <h3>Custom Dice</h3>
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
                    
                        <h3>Dice</h3>
                        <ul id="dice-board">
                        {this.state.diceList.map((dice, index) => (
                            <li key={index}>
                                <Dice properties={dice} originalprops={dice[1]} index={index} socket={socket}
                                />
                            </li>
                        ))}
       
                        </ul>
                
                    </div>
                    <div className='dice-history roundedbox'>
                        <h2>Dice History</h2>
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
