import React, {Fragment} from 'react';
import {uid} from "react-uid";
import {withRouter} from 'react-router-dom';
import Dice from "./Dice";
import "../styles/DiceBoard.css"
class DiceBoard extends React.Component {

    state = {
        diceList: [[6,5], [5,4]], // [[dicemax, diceval]]
        customDice: '',
        diceHistory: []
    }
    componentDidMount() {
        this.getHistory()
    }
    getHistory(){
        fetch("/diceboard").then(res =>{
            return res.json()
        })
            .then((data) => {
                this.setState({diceHistory: data.history})
            })
    }

    // addHistory = (diceMax, diceroll) => {
    //     console.log("dicemax", diceMax, diceroll)
    //     const diceJson = 
    //             {
    //                 dicemax: diceMax,
    //                 diceval: diceroll,
    //                 allhistory: this.state.diceHistory
    //             }
        

    //     fetch("/diceboard/newroll",
    //     {
    //         headers: {
    //             'Accept': 'application/json',
    //             'Content-Type': 'application/json'
    //         },
    //         method: "POST",
    //         body: JSON.stringify(diceJson)
    //     }).then(res =>res.json())
    //         .then((data) => {
    //             console.log("from server", data)
    //             this.setState({diceHistory: data})
    //         })


    //     // original

    //     // this.setState(() => ({
    //     //     diceHistory: [...this.state.diceHistory, `d${diceMax}: ${diceroll}`]
    //     //   }))
    // }

    handleInputChange(event, fieldName) {
        const target = event.target;
        const value = target.value;

        this.setState({[fieldName]: value});
    }
    addDice(diceMax){
        this.setState(() => ({
            diceList: [...this.state.diceList, [diceMax, `d${diceMax}`]]
          }))
        console.log(this.state.diceList)
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
        

        fetch("/diceboard/newroll",
        {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            method: "POST",
            body: JSON.stringify(diceJson)
        }).then(res =>res.json())
            .then((data) => {
                console.log("from server", data)
                this.setState({diceHistory: data.history,
                               diceList: data.diceList
                })
            })


        // this.setState({diceList: items})
    }

    render() {
        return (
            <div className='dice-module roundedbox'>
                <div className='row wrapper'>
                    <div className='add-dice roundedbox'>
                        <div className='addDiceButtonColumn column'>
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
                                            className="customDiceInput roundedbox"
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
                        {this.state.diceList.map((dice, index) => (
                            <li key={index}>
                                <Dice properties={dice} originalprops={dice[1]} index={index} updateDice={this.updateDice}
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