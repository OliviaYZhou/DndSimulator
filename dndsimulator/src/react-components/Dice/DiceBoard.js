import React, { Fragment, useRef } from "react"
import { uid } from "react-uid"
import { withRouter } from "react-router-dom"
import Dice from "./Dice"
import "../../styles/DiceBoard.css"

class DiceBoard extends React.Component {
    state = {
        diceList: [], // [[dicemax, diceval, rolling]]
        customDice: "",
        diceHistory: [],
        isRolling: false,
        socket: this.props.socket,
        boardIndex: this.props.boardIndex,
        characterid: this.props.characterid,
    }
    componentDidMount() {
        console.log("mount board index", this.props.boardIndex)
        this.state.socket.emit("i_just_connected", { boardIndex: this.props.boardIndex })
        this.state.socket.on(`welcome/${this.props.boardIndex}`, (data) => this.load_board(data))

        this.state.socket.on(`get_dice/${this.props.boardIndex}`, (data) => {
            this.setDice(data)
        })
        this.state.socket.on(`everyone_start_roll/${this.props.boardIndex}`, (data) => {
            this.rollDice(data.index, data.predetermined_result)
        })
        // this.scaleFontSize("dice-history")
    }

    load_board(data) {
        this.setState({ diceList: data.diceList, diceHistory: data.diceHistory })
        this.state.socket.off(`welcome/${this.state.boardIndex}`)
    }

    deleteDice = (index) => {
        this.state.socket.emit("delete_dice", { index: index, boardIndex: this.state.boardIndex })
    }

    clearDice() {
        this.state.socket.emit("clear_dice", { boardIndex: this.state.boardIndex })
    }

    clearHistory() {
        this.state.socket.emit("clear_history", { boardIndex: this.state.boardIndex })
    }

    rolling = (index, diceMax) => {
        if (this.state.diceList.length <= index) {
            console.log("index out of bounds")
            return false
        }

        var ranVar = Math.floor(Math.random() * diceMax) + 1
        let items = [...this.state.diceList]
        var rolledDice = items[index]
        rolledDice[1] = ranVar
        items[index] = rolledDice

        this.setState({
            diceList: items,
        })
        return true
    }

    setRollingStatus = (index, on = true) => {
        console.log("rollingStatus", on)
        if (this.state.diceList.length <= index) {
            console.log("setRollingStatus index out of bounds")
            this.setState({ isRolling: on })
        } else {
            let items = [...this.state.diceList]
            var clickedDice = [...items[index]]
            clickedDice[2] = on
            items[index] = clickedDice

            this.setState({
                diceList: items,
                isRolling: on,
            })
        }
    }

    rollDice = (index, predetermined_result) => {
        console.log("index", index)
        console.log(this.state)
        if (this.state.diceList.length <= index) {
            console.log("rollDice index out of bounds")
            this.updateDice(index, predetermined_result, diceMax)
            return false
        }
        var diceMax = this.state.diceList[index][0]
        this.setRollingStatus(index, true)

        var times = 0
        var interval = setInterval(() => {
            const status = this.rolling(index, diceMax)
            if (status === false) {
                clearInterval(interval)
                this.setRollingStatus(index, false)
                return false
            }
            if (++times == 10) {
                clearInterval(interval)

                this.updateDice(index, predetermined_result, diceMax)
                this.setRollingStatus(index, false)
            }
        }, 100)
    }

    setDice(data) {
        console.log("from server", data)
        this.setState({ diceHistory: data.history, diceList: data.diceList })
    }

    handleInputChange(event, fieldName) {
        const target = event.target
        const value = target.value

        this.setState({ [fieldName]: value })
    }
    addDice(diceMax) {
        const newDiceJson = {
            dicemax: diceMax,
            boardIndex: this.state.boardIndex,
        }
        console.log(newDiceJson)

        this.state.socket.emit("dice_add", newDiceJson)
    }
    allowDrop(ev) {
        ev.preventDefault()
    }
    drag(ev, diceMax) {
        ev.dataTransfer.setData("diceMax", diceMax)
    }

    drop(ev) {
        ev.preventDefault()
        var diceMax = ev.dataTransfer.getData("diceMax")
        this.addDice(diceMax)
    }

    updateDice = (index, roll) => {
        const diceJson = {
            index: index,
            diceval: roll,
            boardIndex: this.state.boardIndex,
        }
        console.log(diceJson)
        this.state.socket.emit("dice_update", diceJson)
    }

    render() {
        return (
            <div className="dice-module-wrapper">
                <button
                    className="bigHeader clear-dice-button"
                    onClick={() => this.props.closeDiceBoard(this.props.boardIndex)}
                    onContextMenu={(e) => {
                        e.preventDefault()
                        this.clearDice()
                    }}>
                    {this.state.characterid}
                </button>
                <div className="dice-module roundedbox" style={{ backgroundColor: this.state.isRolling ? "rgb(201, 200, 200)" : "rgb(236, 236, 236)" }}>
                    {/* <div className='row wrapper'> */}
                    {/* <div className="add-dice ">
                        <div className="addDiceButtonColumn">
                            <div className="addDiceButtonGrid">
                                {[4, 6, 8, 10, 20, 100].map((val) => (
                                    <button draggable="true" className="addDiceButton defaultButton" onDragStart={(ev) => this.drag(ev, val)} onClick={() => this.addDice(val)}>
                                        d{val}
                                    </button>
                                ))}
                            </div>
                        </div>

                        <div className="column customDiceWrapper">
                            <span className="label">Custom</span>
                            <div className="d-something row">
                                d <input className="customDiceInput roundedbox" type="number" min="2" onChange={(e) => this.handleInputChange(e, "customDice")} />
                            </div>

                            <button
                                draggable={this.state.customDice > 0 ? true : false}
                                onDragStart={(ev) => {
                                    this.drag(ev, this.state.customDice)
                                }}
                                className="addCustomDiceButton defaultButton"
                                onClick={() => {
                                    this.addDice(this.state.customDice)
                                }}
                            >
                                Add Dice
                            </button>
                        </div>
                    </div> */}

                    {/* <div class='dice-board-wrapper roundedbox'> */}

                    <ul className="dice-board scrollable-y" onDrop={(ev) => this.drop(ev)} onDragOver={(ev) => this.allowDrop(ev)}>
                        {this.state.diceList.map((dice, index) => (
                            <li key={index} className="dicelistitem">
                                <Dice
                                    properties={dice}
                                    index={index}
                                    socket={this.state.socket}
                                    deleteDice={this.deleteDice}
                                    boardIndex={this.state.boardIndex}
                                    drag={this.drag}
                                />
                            </li>
                        ))}
                    </ul>

                    {/* </div> */}
                    <div className="dice-history">
                        <span
                            className="diceHistoryHeader hoverable"
                            onContextMenu={(e) => {
                                e.preventDefault()
                                this.clearHistory()
                            }}>
                            History
                        </span>
                        <ul className="dice-history-list scrollable-y">
                            {this.state.diceHistory.map((historyString, index) => (
                                <li key={index}>{historyString}</li>
                            ))}
                        </ul>
                    </div>
                    {/* </div> */}
                </div>
            </div>
        )
    }
}

export default withRouter(DiceBoard)

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

// getHistory(){
//     fetch("/diceboard").then(res =>{
//         return res.json()
//     })
//         .then((data) => {
//             this.setState({diceHistory: data.history})
//         })
// }
