import React, { Fragment, useState, useEffect } from "react"
import "../../styles/CharacterAdd.css"
import StatsForm from "./StatsForm"
// ".../styles/CharacterAdd.css"
function CharacterAdd(props) {
    // const [showAddCharacterForm, setAddCharacterForm] = useState(false)
    // const [showAddStatsForm, setAddStatsForm] = useState(false)
    // const [showAddCumulativeStatsForm, setAddCumulativeStatsForm] = useState(false)
    // const [showDeleteCharacterForm, setDeleteCharacterForm] = useState(false)
    const [showFormName, setShowFormName] = useState("") // "character", "stats", "cumulative", "delete"
    // const [characterid, setCharacterId] = useState("")

    // useEffect(() => {
    //     if (props.characterid != undefined) {
    //         setCharacterId(props.characterid)
    //     }
    // }, [props.characterid])

    const handleFocus = (event) => event.target.select()

    function renderForm() {
        switch (showFormName) {
            case "character":
                return renderAddCharacterForm()
            case "stats":
                return renderAddStatsForm()
            case "cumulative":
                return renderAddCumulativeStatsForm()
            case "delete":
                return renderDeleteCharacterForm()
            default:
                return null
        }
    }
    function renderAddCharacterForm() {
        if (1) {
            return (
                <div className="add-basic-character add-character-block">
                    <button className="closeButton" onClick={() => setShowFormName("")}>
                        {" "}
                        x
                    </button>
                    <form
                        className="character-form"
                        action="/api/add_character/"
                        target="dummyframe"
                        method="post">
                        <div className="add-character-form-grid">
                            <label htmlFor="charName">Character name:</label>
                            <input
                                className=".default-inputbox"
                                type="text"
                                id="charName"
                                name="characterName"
                            />

                            <label htmlFor="charid">Character ID:</label>
                            <input
                                className=".default-inputbox"
                                type="text"
                                id="charid"
                                name="characterid"
                            />

                            <label htmlFor="chartype">Character Type:</label>
                            <select
                                className=".default-inputbox"
                                type="text"
                                id="chartype"
                                name="characterType">
                                <option value="basic">Basic</option>
                                <option value="npc">NPC</option>
                                <option value="enemy">Enemy</option>
                                <option value="player">Player</option>
                            </select>
                            <div className="centered-flex">
                                <input
                                    className="submit-button defaultButton strong-button"
                                    type="submit"></input>
                            </div>
                        </div>
                    </form>
                </div>
            )
        }
        // else {
        //     return (

        //     )
        // }
    }
    function renderAddStatsForm() {
        return (
            <div className="add-character-stats add-character-block">
                <button className="closeButton" onClick={() => setShowFormName("")}>
                    x
                </button>
                <StatsForm action="add_new_stats" extraRow={true} />{" "}
            </div>
        )

        // if (1) {
        //     return (
        //         <div className="add-character-stats add-character-block">
        //             <button className="closeButton" onClick={() => setShowFormName("")}>
        //                 x
        //             </button>
        //             <form className="character-form centered-flex column" action="/api/add_new_stats/" target="dummyframe" method="post">
        //                 <label htmlFor="charidstats">Character ID: </label>
        //                 <input type="text" id="charidstats" name="characterid" />
        //                 {/* <br /> */}
        //                 <div className="hp-level-grid-row">
        //                     <span className="gridplaceholder"></span>
        //                     {/* <span> */}
        //                     <label htmlFor="nHP">HP: </label>
        //                     <input
        //                         className="inputboxSmall roundedbox inline"
        //                         type="number"
        //                         min={0}
        //                         defaultValue={0}
        //                         onFocus={handleFocus}
        //                         id="nHP"
        //                         name="HP"
        //                     />
        //                     {/* </span> */}
        //                     {/* <span> */}
        //                     <label htmlFor="nlevel">Level: </label>
        //                     <input
        //                         className="inputboxSmall roundedbox inline"
        //                         type="number"
        //                         min={1}
        //                         defaultValue={1}
        //                         onFocus={handleFocus}
        //                         id="nlevel"
        //                         name="level"
        //                     />
        //                     {/* </span> */}
        //                     <span className="gridplaceholder"></span>
        //                 </div>

        //                 <div className="stats-grid">
        //                     {["STR", "DEX", "CON", "INT", "WIS", "CHA"].map((stat) => (
        //                         <span className="oneStat">
        //                             <label htmlFor={stat}>{stat}: </label>
        //                             <input
        //                                 className="inputboxSmall inline"
        //                                 type="number"
        //                                 min={0}
        //                                 defaultValue={0}
        //                                 onFocus={handleFocus}
        //                                 id={stat}
        //                                 name={stat}
        //                             />
        //                         </span>
        //                     ))}
        //                 </div>

        //                 <input className="submit-button" type="submit"></input>
        //             </form>
        //         </div>
        //     )
        // }
        // else {
        //     return (

        //     )
        // }
    }
    function renderAddCumulativeStatsForm() {
        if (1) {
            return (
                <div className="add-cumulative-stats-form add-character-block">
                    <button className="closeButton" onClick={() => setShowFormName("")}>
                        {" "}
                        x
                    </button>
                    <form
                        className="character-form"
                        action="/api/add_new_cumulative_stats/"
                        target="dummyframe"
                        method="post">
                        <label htmlFor="charidc">Character ID:</label>
                        <input type="text" id="charidc" name="characterid" />
                        <br />
                        <label htmlFor="gold">Gold:</label>
                        <input
                            type="number"
                            id="gold"
                            name="gold"
                            min="0"
                            defaultValue={0}
                            onFocus={handleFocus}
                        />
                        <br />
                        <label htmlFor="exp">EXP:</label>
                        <input
                            type="number"
                            id="exp"
                            name="exp"
                            min="0"
                            defaultValue={0}
                            onFocus={handleFocus}
                        />
                        <br />
                        <input type="submit"></input>
                    </form>
                </div>
            )
        }
        // else {
        //     return (

        //     )
        // }
    }

    function renderDeleteCharacterForm() {
        if (1) {
            return (
                <div className="delete-character-form add-character-block">
                    <button className="closeButton" onClick={() => setShowFormName("")}>
                        {" "}
                        x
                    </button>
                    <form
                        className="character-form"
                        action="/api/delete_character/"
                        target="dummyframe"
                        method="post">
                        <label htmlFor="charidc">Character ID:</label>
                        <input type="text" id="charidc" name="characterid" />
                        <br />
                        <input type="submit"></input>
                    </form>
                </div>
            )
        }
        // else {
        //     return (

        //     )
        // }
    }

    return (
        <div className="character-add">
            <iframe name="dummyframe" id="dummyframe" style={{ display: "none" }}></iframe>
            <div className="add-character-grid">
                <div className="add-character-navbar">
                    <button className="defaultButton" onClick={() => setShowFormName("character")}>
                        Add Basic Character
                    </button>
                    <button className="defaultButton" onClick={() => setShowFormName("stats")}>
                        Add Stats
                    </button>
                    <button className="defaultButton" onClick={() => setShowFormName("cumulative")}>
                        Add Cumulative Stats
                    </button>
                    {/* <button onClick={() => setDeleteCharacterForm(true)}>Delete A Character</button> */}
                </div>
                <div className="add-character-grid-space">{renderForm()}</div>
                {/* {renderAddCharacterForm()}
                {renderAddStatsForm()}
                {renderAddCumulativeStatsForm()} */}
            </div>
        </div>
    )
}
export default CharacterAdd
