import React, { Fragment, useState, useEffect } from "react"
import "../../styles/CharacterAdd.css"
// ".../styles/CharacterAdd.css"
function CharacterAdd(props) {
    const [showAddCharacterForm, setAddCharacterForm] = useState(true)
    const [showAddStatsForm, setAddStatsForm] = useState(false)
    const [showAddCumulativeStatsForm, setAddCumulativeStatsForm] = useState(false)
    const [showDeleteCharacterForm, setDeleteCharacterForm] = useState(false)
    const [characterid, setCharacterId] = useState("")

    useEffect(() => {
        if (props.characterid != undefined) {
            setCharacterId(props.characterid)
        }
    }, [props.characterid])

    const handleFocus = (event) => event.target.select()

    function renderAddCharacterForm() {
        if (showAddCharacterForm) {
            return (
                <div className="add-basic-character add-character-block">
                    <button className="closeButton" onClick={() => setAddCharacterForm(false)}>
                        {" "}
                        x
                    </button>
                    <form className="character-form" action="/api/add_character/" target="dummyframe" method="post">
                        <label for="charName">Character name:</label>
                        <input type="text" id="charName" name="characterName" />
                        <br />
                        <label for="charid">Character ID:</label>
                        <input type="text" id="charid" name="characterid" />
                        <br />
                        <label for="chartype">Character Type:</label>
                        <select type="text" id="chartype" name="characterType">
                            <option value="basic">Basic</option>
                            <option value="npc">NPC</option>
                            <option value="enemy">Enemy</option>
                            <option value="player">Player</option>
                        </select>
                        <input type="submit"></input>
                    </form>
                </div>
            )
        } else {
            return (
                <button
                    onClick={() => {
                        setAddCharacterForm(true)
                    }}
                >
                    Add Basic Character
                </button>
            )
        }
    }
    function renderAddStatsForm() {
        if (showAddStatsForm) {
            return (
                <div className="add-character-stats add-character-block">
                    <button className="closeButton" onClick={() => setAddStatsForm(false)}>
                        x
                    </button>
                    <form className="character-form" action="/api/add_new_stats/" target="dummyframe" method="post">
                        <label for="charidstats">Character ID: </label>
                        <input type="text" id="charidstats" name="characterid" />
                        <br />
                        <label for="nHP">HP: </label>
                        <input
                            className="inputboxSmall roundedbox inline"
                            type="number"
                            min={0}
                            defaultValue={0}
                            onFocus={handleFocus}
                            id="nHP"
                            name="HP"
                        />
                        <br />
                        <label for="nlevel">Level: </label>
                        <input
                            className="inputboxSmall roundedbox inline"
                            type="number"
                            min={1}
                            defaultValue={1}
                            onFocus={handleFocus}
                            id="nlevel"
                            name="level"
                        />
                        <br />
                        {["STR", "DEX", "CON", "INT", "WIS", "CHA"].map((stat) => (
                            <Fragment>
                                <label for={stat}>{stat}: </label>
                                <input
                                    className="inputboxSmall roundedbox inline"
                                    type="number"
                                    min={0}
                                    defaultValue={0}
                                    onFocus={handleFocus}
                                    id={stat}
                                    name={stat}
                                />
                            </Fragment>
                        ))}
                        <input type="submit"></input>
                    </form>
                </div>
            )
        } else {
            return (
                <button
                    onClick={() => {
                        setAddStatsForm(true)
                    }}
                >
                    Add Stats
                </button>
            )
        }
    }
    function renderAddCumulativeStatsForm() {
        if (showAddCumulativeStatsForm) {
            return (
                <div className="add-cumulative-stats-form add-character-block">
                    <button className="closeButton" onClick={() => setAddCumulativeStatsForm(false)}>
                        {" "}
                        x
                    </button>
                    <form className="character-form" action="/api/add_new_cumulative_stats/" target="dummyframe" method="post">
                        <label for="charidc">Character ID:</label>
                        <input type="text" id="charidc" name="characterid" />
                        <br />
                        <label for="gold">Gold:</label>
                        <input type="number" id="gold" name="gold" min="0" defaultValue={0} onFocus={handleFocus} />
                        <br />
                        <label for="exp">EXP:</label>
                        <input type="number" id="exp" name="exp" min="0" defaultValue={0} onFocus={handleFocus} />
                        <br />
                        <input type="submit"></input>
                    </form>
                </div>
            )
        } else {
            return (
                <button
                    onClick={() => {
                        setAddCumulativeStatsForm(true)
                    }}
                >
                    Add Cumulative Stats
                </button>
            )
        }
    }

    function renderDeleteCharacterForm() {
        if (showDeleteCharacterForm) {
            return (
                <div className="delete-character-form add-character-block">
                    <button className="closeButton" onClick={() => setDeleteCharacterForm(false)}>
                        {" "}
                        x
                    </button>
                    <form className="character-form" action="/api/delete_character/" target="dummyframe" method="post">
                        <label for="charidc">Character ID:</label>
                        <input type="text" id="charidc" name="characterid" />
                        <br />
                        <input type="submit"></input>
                    </form>
                </div>
            )
        } else {
            return (
                <button
                    onClick={() => {
                        setDeleteCharacterForm(true)
                    }}
                >
                    Delete A Character
                </button>
            )
        }
    }

    return (
        <div className="character-add">
            <iframe name="dummyframe" id="dummyframe" style={{ display: "none" }}></iframe>
            {renderAddCharacterForm()}
            {renderAddStatsForm()}
            {renderAddCumulativeStatsForm()}
        </div>
    )
}
export default CharacterAdd
