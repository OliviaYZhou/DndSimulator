import React, { useState } from "react"
import DiceBoard from "./DiceBoard"
import "../../styles/DiceArea.css"

function DiceArea(props) {
    const [diceList, setDiceList] = useState([
        ["tentacle_guy", true],
        ["orc_guy", true],
        ["Enemy", true],
    ])

    let clearDice = (boardIndex) => {
        this.state.socket.emit("clear_dice", { boardIndex: boardIndex })
    }

    function addDiceBoard(boardKey) {
        var diceListCopy = [...diceList]
        // server call
    }
    let showDiceBoard = (boardIndex) => {
        var diceListCopy = [...diceList]
        diceListCopy[boardIndex][1] = true

        setDiceList(diceListCopy)
    }

    let closeDiceBoard = (boardIndex) => {
        console.log("close ")
        var diceListCopy = [...diceList]
        console.log("dicecopy", diceListCopy)
        console.log("boardIndex", boardIndex)
        diceListCopy[boardIndex][1] = false

        setDiceList(diceListCopy)
    }

    const renderDiceBoard = (characterid, boardIndex) => {
        console.log(diceList)
        if (diceList == undefined) {
            return null
        }
        if (diceList[0] == undefined) {
            return null
        }
        if (diceList[boardIndex][1] == true) {
            return (
                <li>
                    <DiceBoard socket={props.socket} boardIndex={boardIndex} closeDiceBoard={closeDiceBoard} characterid={characterid} />
                </li>
            )
        } else {
            return (
                <button className="bigHeader clear-dice-button hoverable highlightable" onClick={() => showDiceBoard(boardIndex)}>
                    {characterid}
                </button>
            )
        }
    }
    return (
        <div className="dice-area">
            <ul className="characterDiceBoardList scrollable-x">
                {diceList != undefined ? diceList.map((characterid, boardIndex) => renderDiceBoard(characterid, boardIndex)) : null}
            </ul>
        </div>
    )
}

export default DiceArea
