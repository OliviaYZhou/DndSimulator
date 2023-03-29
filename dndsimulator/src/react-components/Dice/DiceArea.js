import React, { useEffect, useState } from "react"
import DiceBoard from "./DiceBoard"
import "../../styles/DiceArea.css"

function DiceArea(props) {
    const [diceList, setDiceList] = useState([
        ["tentacle_guy", true],
        ["orc_guy", true],
        ["Enemy", true],
        ["npc1", true],
        ["npc2", true],
    ])

    useEffect(() => {
        // initial load
        fetch(`/api/get_master_dice`)
            .then((res) => res.json())
            .then((data) => loadDiceBoards(data.dice_boards))

        // server commands you add ONE new diceboard
        props.socket.on("get_new_diceboard", (data) => {
            console.log("new diceboard", data)
            addBoardDiceList(data.boardId)
        })
    }, [])

    function loadDiceBoards(dice_boards) {
        console.log("load dice boards", dice_boards)
        var tempDiceList = [...diceList]
        dice_boards.forEach((item, index) => {
            var inlist = false
            for (const i in tempDiceList) {
                console.log(tempDiceList[i], item)
                if (tempDiceList[i][0] == item) {
                    inlist = true
                }
            }
            if (!inlist) {
                console.log("new item", item)
                tempDiceList.push([item, true])
            }
        })
        setDiceList(tempDiceList)
        console.log("loaded", tempDiceList)
    }

    function addBoardDiceList(boardId) {
        var diceListCopy = [...diceList]

        diceListCopy.push([boardId, true])
        setDiceList(diceListCopy)
    }

    let clearDice = (boardIndex) => {
        this.props.socket.emit("clear_dice", { boardIndex: boardIndex })
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

    const renderDiceBoard = (boardId, boardIndex) => {
        // console.log(diceList)
        if (diceList == undefined) {
            return null
        }
        if (diceList[0] == undefined) {
            return null
        }
        if (diceList[boardIndex][1] == true) {
            return (
                <li>
                    <DiceBoard
                        socket={props.socket}
                        boardIndex={boardIndex}
                        closeDiceBoard={closeDiceBoard}
                        boardId={boardId}
                    />
                </li>
            )
        } else {
            return (
                <button
                    className="bigHeader clear-dice-button hoverable highlightable"
                    onClick={() => showDiceBoard(boardIndex)}>
                    {boardId}
                </button>
            )
        }
    }
    return (
        <div className="dice-area scrollable-x scrollable-y">
            <ul className="characterDiceBoardList">
                {diceList != undefined
                    ? diceList.map((boardlist, boardIndex) => {
                          console.log(boardlist, boardIndex)
                          return renderDiceBoard(boardlist[0], boardIndex)
                      })
                    : null}
            </ul>
        </div>
    )
}

export default DiceArea
