import React, { Fragment, useState, useEffect } from "react"
import "../styles/SideBar.css"
import CharacterAdd from "./Characters/CharacterAdd"
import DiceAdd from "./Dice/DiceAdd"
function SideBar() {
    const [currentTime, setCurrentTime] = useState(6.5)
    const [currentTurn, setCurrentTurn] = useState(1)
    const [showAddDiceModule, setShowAddDiceModule] = useState(false)
    const [showAddCharacterModule, setShowAddCharacterModule] = useState(false)

    function incrementTime(hours, days = 0) {
        var tentativeTime = (currentTime + hours + days * 24) % 24
        setCurrentTime(tentativeTime)
    }

    function renderAddDiceModule() {
        if (showAddDiceModule) {
            return <DiceAdd show={setShowAddDiceModule} />
        } else {
            return null
        }
    }
    function renderAddCharacterModule() {
        if (showAddCharacterModule) {
            return (
                <div className="sidebar-popup secondSidebarChild">
                    <button className="closeButton" onClick={() => setShowAddCharacterModule(false)}>
                        x
                    </button>
                    <CharacterAdd />
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
                        <div>Turn: {currentTurn}</div>
                        <div>
                            Time: {Math.floor(currentTime)}:{(currentTime % 1) * 60}
                        </div>
                    </div>
                    <button onClick={() => setShowAddCharacterModule(true)}>Add Character</button>
                    <button>Add DiceBoard</button>
                    <button onClick={() => setShowAddDiceModule(true)}>Add Dice</button>
                    <button>Add Status Effect</button>
                    <button>Add Permanent Effect</button>
                    <button>Time Pass</button>
                    <button
                        onClick={() => {
                            setCurrentTurn(currentTurn + 1)
                        }}>
                        Next Turn
                    </button>
                </div>
            </div>
            <div className="sidebar-popup-wrapper">
                {renderAddCharacterModule()}
                {renderAddDiceModule()}
            </div>
        </div>
    )
}

export default SideBar
