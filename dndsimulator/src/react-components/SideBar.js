import React, { Fragment, useState, useEffect } from "react"
import "../styles/SideBar.css"
import CharacterAdd from "./Characters/CharacterAdd"
import PermanentEffectForm from "./Characters/PermanentEffectForm"
import DiceAdd from "./Dice/DiceAdd"
function SideBar(props) {
    const [currentTime, setCurrentTime] = useState(6.5)
    const [currentHour, setCurrentHour] = useState(6)
    const [currentMinute, setCurrentMinute] = useState(30)
    const [currentSession, setCurrentSession] = useState(props.currentTurn)
    const [showAddDiceBoardModule, setShowAddDiceBoardModule] = useState(false)
    const [showAddDiceModule, setShowAddDiceModule] = useState(false)
    const [showAddCharacterModule, setShowAddCharacterModule] = useState(false)
    const [showPermanentEffectModule, setShowPermanentEffectModule] = useState(false)
    const [showTimePassModule, setShowTimePassModule] = useState(false)
    function onTimeInput(event, hourMinute = "hour") {
        var input = event.target.value

        if (input == "") {
            if (hourMinute === "hour") {
                setCurrentHour("")
                console.log("cur time", currentHour, currentMinute)
            } else {
                setCurrentMinute("")
                console.log("cur time 2", currentHour, currentMinute)
            }
        } else {
            if (hourMinute === "hour") {
                setCurrentHour(Math.floor(parseFloat(input)))
                console.log("cur time 3", currentHour, currentMinute)
            } else {
                setCurrentMinute(Math.floor(parseInt(input)))
                console.log("cur time 4", currentHour, currentMinute)
            }
        }
    }
    function formatTime(num) {
        return Math.floor(parseFloat(num)).toLocaleString("en-US", {
            minimumIntegerDigits: 2,
            maximumSignificantDigits: 2,
            maximumFractionDigits: 0,
            useGrouping: false,
        })
    }
    function incrementTime(hours, days = 0) {
        hours = parseFloat(hours)

        var addedMinutes = (hours % 1) * 60
        var wholeHours = Math.floor(hours)
        var totalMinutes = addedMinutes + parseInt(currentMinute)
        if (totalMinutes >= 60) {
            wholeHours += 1
            totalMinutes = totalMinutes % 60
        }
        setCurrentHour(parseInt(currentHour) + wholeHours)
        setCurrentMinute(totalMinutes)
    }

    function renderAddDiceModule() {
        if (showAddDiceModule) {
            return <DiceAdd show={setShowAddDiceModule} />
        } else {
            return null
        }
    }
    // // request server post new diceboard
    // function postDiceBoard(boardId) {
    //     this.props.socket.emit("add_dice_board", { boardId: boardId })
    // }
    function renderAddDiceBoardModule() {
        if (showAddDiceBoardModule) {
            return (
                <div className="sidebar-popup thirdSidebarChild">
                    <button
                        className="closeButton"
                        onClick={() => setShowAddDiceBoardModule(false)}>
                        x
                    </button>{" "}
                    <iframe name="dummyframe" id="dummyframe" style={{ display: "none" }}></iframe>
                    <form
                        className="centered-flex column padded-form"
                        action={`/api/add_new_diceboard/`}
                        target="dummyframe"
                        method="post">
                        <label htmlFor="input-diceboard-name">DiceBoard Name: </label>
                        <input
                            className="default-inputbox"
                            id="input-diceboard-name"
                            name="boardId"
                        />

                        <input
                            className="submit-button defaultButton strong-button"
                            type="submit"
                        />
                    </form>
                </div>
            )
        }
    }
    function renderAddCharacterModule() {
        if (showAddCharacterModule) {
            return (
                <div className="sidebar-popup secondSidebarChild">
                    <button
                        className="closeButton"
                        onClick={() => setShowAddCharacterModule(false)}>
                        x
                    </button>
                    <CharacterAdd />
                </div>
            )
        } else {
            return null
        }
    }

    function renderPermanentEffectModule() {
        if (showPermanentEffectModule) {
            return (
                <div className="sidebar-popup sixthSidebarChild">
                    <button
                        className="closeButton"
                        onClick={() => setShowPermanentEffectModule(false)}>
                        x
                    </button>
                    <PermanentEffectForm />
                </div>
            )
        } else {
            return null
        }
    }
    function renderTimePassModule() {
        if (showTimePassModule) {
            var passXHours = 0
            return (
                <div className="sidebar-popup seventhSidebarChild">
                    <button className="closeButton" onClick={() => setShowTimePassModule(false)}>
                        x
                    </button>
                    <label> Pass </label>
                    <input
                        className="inputboxSmall"
                        type="number"
                        onInput={(e) => {
                            passXHours = e.target.value
                        }}
                    />
                    <label> hours</label>

                    <button
                        className="submit-button"
                        onClick={() => {
                            incrementTime(passXHours)
                            console.log(currentHour, currentMinute)
                        }}>
                        Submit
                    </button>
                </div>
            )
        } else {
            return null
        }
    }

    return (
        <div className="floaty">
            <div id="side-bar">
                <div className="vertical-grid">
                    <div className="time-grid">
                        <div>Session: {currentSession}</div>
                        <div>
                            Time:{""}
                            <input
                                className="invisible-input editable"
                                value={formatTime(currentHour)}
                                type="number"
                                onInput={(e) => onTimeInput(e, "hour")}
                            />
                            :
                            <input
                                className="invisible-input editable"
                                value={formatTime(currentMinute)}
                                type="number"
                                onInput={(e) => onTimeInput(e, "minute")}
                            />
                            {/* {Math.floor(currentTime)}:{(currentTime % 1) * 60} */}
                        </div>
                    </div>
                    <button className="hoverable" onClick={() => setShowAddCharacterModule(true)}>
                        Add Character
                    </button>
                    <button className="hoverable" onClick={() => setShowAddDiceBoardModule(true)}>
                        Add DiceBoard
                    </button>
                    <button className="hoverable" onClick={() => setShowAddDiceModule(true)}>
                        Add Dice
                    </button>
                    <button className="hoverable">Add Status Effect</button>
                    <button
                        className="hoverable"
                        onClick={() => setShowPermanentEffectModule(true)}>
                        Add Permanent Effect
                    </button>
                    <button className="hoverable" onClick={() => setShowTimePassModule(true)}>
                        Time Pass
                    </button>
                    <button
                        className="hoverable"
                        onClick={() => {
                            setCurrentSession(currentSession + 1)
                        }}>
                        Next Session
                    </button>
                </div>
            </div>
            <div className="sidebar-popup-wrapper">
                {renderAddCharacterModule()}
                {renderAddDiceBoardModule()}
                {renderAddDiceModule()}
                {renderPermanentEffectModule()}
                {renderTimePassModule()}
            </div>
        </div>
    )
}

export default SideBar
