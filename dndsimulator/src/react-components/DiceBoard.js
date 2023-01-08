import React, {Fragment} from 'react';
import {uid} from "react-uid";
import {withRouter} from 'react-router-dom';
import Dice from "./Dice";
import "../styles/DiceBoard.css"
class DiceBoard extends React.Component {

    state = {
        diceList: [],
        customDice: '',
        diceHistory: []
    }
    componentDidMount() {
        // this.addDice(10)
        // this.addHistory(6, 5)
        // this.addHistory(10, 2)
        // console.log(this.state.diceHistory)
        // this.addHistory(11, 3)
        // console.log(this.state.diceHistory)
    }
    afunction(){}

    addHistory = (diceMax, diceroll) => {
        console.log(this.state.diceHistory)
        this.setState(() => ({
            diceHistory: [...this.state.diceHistory, `d${diceMax}: ${diceroll}`]
          }))
    }

    handleInputChange(event, fieldName) {
        const target = event.target;
        const value = target.value;

        this.setState({[fieldName]: value});
    }
    addDice(diceMax){
        this.setState(() => ({
            diceList: [...this.state.diceList, diceMax]
          }))
        // console.log(this.state.diceList)
    }

    render() {

        return (
            <div className='dice-module roundedbox'>
                <div className='row wrapper'>
                    <div className='add-dice'>
                        <div className='addDiceButtonColumn column roundedbox'>
                            <button className='addDiceButton'
                            onClick={() => {this.addDice(3)}}>
                            d3</button>
                            <button className='addDiceButton'
                            onClick={() => {this.addDice(4)}}>d4</button>
                            <button className='addDiceButton'
                            onClick={() => {this.addDice(6)}}>d6</button>
                            <button className='addDiceButton'
                            onClick={() => {this.addDice(10)}}>d10</button>
                            <button className='addDiceButton'
                            onClick={() => {this.addDice(20)}}>d20</button>
                            <button className='addDiceButton'
                            onClick={() => {this.addDice(100)}}>d100</button>
                            <div className='column customDice'>

                                <h3>Custom Dice</h3>
                                <div className='d-something row'>
                                    d <input
                                            className="customDiceInput"
                                            type="number"
                                            onChange={(e) => this.handleInputChange(e, "customDice")}
                                        />
                                </div>
                                
                                <button className='addCustomDiceButton'
                                onClick={() => {this.addDice(this.state.customDice)}}>Add Dice</button>

                            </div>
                            
                        </div>
                        
                    </div>

                    <div class='dice-board-wrapper roundedbox'>
                    
                        <h3>Dice</h3>
                        <ul id="dice-board">
                        {this.state.diceList.map((dicemax, index) => (
                            <li key={index}>
                                <Dice val={dicemax} addHistory={this.addHistory}/>
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