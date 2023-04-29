import React, { Fragment, useRef } from "react"
import { uid } from "react-uid"
import { withRouter } from "react-router-dom"
import "../../styles/CharacterStatsCard.css"

class CharacterStatsCard extends React.Component {
    state = {
        characterid: this.props.characterid,
        character_type: "",
        name: "No Name",
        status_effects: { HP: 0, STR: 0, DEX: 0, CON: 0, INT: 0, WIS: 0, CHA: 0 },
        max_stats: { HP: 0, STR: 0, DEX: 0, CON: 0, INT: 0, WIS: 0, CHA: 0 },
        lost_hp: 0,
        current_stats: {}, // never directly set, always calculate this
        exp: 0,
        gold: 0,
        level: 0,
        toggleStatBreakdown: false,
        stat_breakdown: { HP: [], STR: [], DEX: [], CON: [], INT: [], WIS: [], CHA: [] },
        selectedStat: "",
        inventory: [], // item name: amount {"itemName": "bandage", "amount": 1}
        minimized: true,
    }

    componentDidMount() {
        // console.log("mount")
        this.load_card()
        this.props.socket.on(`get_character_changes/${this.state.characterid}`, (data) =>
            this.reload_card(data)
        )
    }
    load_card(data = {}) {
        fetch(`/api/character_connected/?characterid=${this.state.characterid}`, {
            headers: {
                "Content-Type": "application/json",
                Accept: "application/json",
            },
        })
            .then((res) => res.json())
            .then((data) => {
                // console.log("api server call", data)
                this.setState(data, () => this.setCurrentStats())
            })

        // console.log("curr", this.state.current_stats)

        // console.log("loading")
        // console.log("loadcard", data)
        // this.setState(data, () => this.setCurrentStats())
        // console.log("status", this.state.status_effects)

        // this.props.socket.off(`character_setup/${this.state.characterid}`)
    }
    reload_card(data) {
        this.setState(data, () => this.setCurrentStats())
    }
    componentDidUpdate(prevProps, prevState) {
        if (
            prevState.status_effects != this.state.status_effects ||
            prevState.max_stats != this.state.max_stats
        ) {
            this.setCurrentStats()
        }
    }

    handleClickStat(stat) {
        // this.props.socket.emit("get_stat_breakdown", {characterid: this.state.characterid, stat: stat})
        this.setState({ toggleStatBreakdown: true, selectedStat: stat })
    }

    openStatBreakdown(stat) {
        // console.log("clicked")
        this.setState({ selectedStat: stat })
        // console.log(this.state.selectedStat)
        this.setState({ toggleStatBreakdown: true })
    }
    closeStatBreakdown() {
        this.setState({ toggleStatBreakdown: false })
    }
    toggleMinimizeCard() {
        this.setState({ minimized: !this.state.minimized })
    }

    setCurrentStats() {
        // console.log("setCurrentStats", this.state.max_stats)
        var newCurrStats = {}
        for (const key in this.state.max_stats) {
            newCurrStats[key] = this.state.max_stats[key] + this.state.status_effects[key]
        }
        newCurrStats["currHP"] = newCurrStats["HP"] + newCurrStats["CON"] - this.state.lost_hp
        console.log("newCurrStats", newCurrStats)
        this.setState({ current_stats: newCurrStats })
    }
    addStatusEffect() {
        this.props.showStatusForm()
    }
    deleteCharacter() {
        var yn = window.confirm("Delete Character FOREVER??")
        if (!yn) {
            return false
        }
        fetch(`/api/delete_character/?characterid=${this.state.characterid}`, {
            headers: {
                "Content-Type": "application/json",
                Accept: "application/json",
            },
            method: "DELETE",
        })
    }
    deleteStatusEffect(effect_name) {
        var yn = window.confirm(`Delete Status Effect ${effect_name} FOREVER??`)
        if (!yn) {
            return false
        }
        fetch(
            `/api/delete_status_effect/?characterid=${this.state.characterid}&effect_name=${effect_name}`,
            {
                headers: {
                    "Content-Type": "application/json",
                    Accept: "application/json",
                },
                method: "DELETE",
            }
        )
    }
    deleteItem(itemName) {
        var yn = window.confirm(`Remove 1 of ${itemName}?`)
        if (!yn) {
            return false
        }
        fetch(
            `/api/delete_inventory_item/?characterid=${this.state.characterid}&item_name=${itemName}`,
            {
                headers: {
                    "Content-Type": "application/json",
                    Accept: "application/json",
                },
                method: "DELETE",
            }
        )
    }

    render() {
        const renderStatBreakdown = () => {
            if (this.state.toggleStatBreakdown && !this.state.minimized) {
                var effectJsonList = this.state.stat_breakdown[this.state.selectedStat] // [{name: name, amount: amount, description: description, duration: duration, duration_remaining: duration}]
                return (
                    <div className="statBreakdown">
                        <button className="closeButton" onClick={() => this.closeStatBreakdown()}>
                            {" "}
                            x
                        </button>
                        <ul className="status_effect_list scrollable-y">
                            {effectJsonList.map((effect) => (
                                <li className="status_effect">
                                    <span>
                                        {effect["AMOUNT"] >= 0 ? "+" : null}
                                        {effect["AMOUNT"]}
                                    </span>
                                    <span>{effect["NAME"]}</span>
                                    <span>
                                        ({effect["DURATION_REMAINING"]}/{effect["DURATION"]})
                                    </span>
                                    <div>
                                        <i>{effect["DESCRIPTION"]}</i>
                                    </div>
                                    <button
                                        className="closeButton showOnHover"
                                        onClick={() => this.deleteStatusEffect(effect["NAME"])}>
                                        X
                                    </button>
                                </li>
                            ))}
                        </ul>
                    </div>
                )
            }
        }
        return (
            <div
                className="characterCardBody"
                style={{ height: this.state.minimized ? "fit-content" : "400px" }}>
                <button className="plusButton" onClick={() => this.addStatusEffect()}>
                    +
                </button>
                <button
                    className="closeButton"
                    id="deleteCharacterButton"
                    style={{
                        display: this.state.minimized ? "none" : "inline-block",
                    }}
                    onClick={() => this.deleteCharacter()}>
                    .
                </button>
                <div
                    className="characterName hoverable highlightable"
                    onClick={() => {
                        this.toggleMinimizeCard()
                    }}>
                    <span className="nameHeader">{this.state.name}</span>
                </div>
                {this.state.minimized ? null : (
                    <div className="characterid">
                        {" "}
                        <i>{this.state.characterid}</i>
                    </div>
                )}

                <div className="hpMpRow row">
                    <div
                        className="hoverable"
                        onClick={() => {
                            this.openStatBreakdown("HP")
                        }}>
                        {" "}
                        HP: {this.state.current_stats["currHP"]}/
                        {this.state.current_stats["HP"] + this.state.current_stats["CON"]}{" "}
                    </div>
                </div>

                <div className="cumulativeStatsRow row">
                    <div className="row">
                        <div className="cumulativeStat">Level {this.state.level} </div>
                        <div className="cumulativeStat">Exp: {this.state.exp} </div>
                        <div className="cumulativeStat">{this.state.gold} Gold </div>
                        {/* {this.state.character_type == "PLAYER" ? 
                        <Fragment>
                            <div className='cumulativeStat'>Exp: {this.state.exp} </div>
                            <div className='cumulativeStat'>{this.state.gold} Gold </div>
                        </Fragment> 
                        : null} */}
                    </div>
                </div>
                <ul
                    className="inventoryList scrollable-y"
                    style={{
                        height: this.state.minimized ? "0px" : "120px",
                        padding: this.state.minimized ? "0px" : "0.5em",
                        /*1.5em 0.5em 0.5em 0.5em */
                        margin: this.state.minimized ? "5px" : "10px",
                    }}>
                    {/* <button className="plusButton">+</button> */}
                    {this.state.inventory.map((itemJson) => (
                        <li className="inventory-item">
                            <span style={{ marginRight: "5px" }}>{itemJson["amount"]} x </span>
                            <span>{itemJson["itemName"]}</span>
                            <button
                                className="closeButton showOnHover"
                                onClick={() => this.deleteItem(itemJson["itemName"])}>
                                -
                            </button>
                        </li>
                    ))}
                </ul>

                <div className="statrow row">
                    <div className="row">
                        {["STR", "DEX", "CON", "INT", "WIS", "CHA"].map((stat) => (
                            <div
                                className="eachStat hoverable"
                                onClick={() => {
                                    this.openStatBreakdown(stat)
                                }}>
                                <div>
                                    <b>{stat}</b>
                                </div>
                                <div>
                                    <b>{this.state.current_stats[stat]}</b>
                                </div>
                                <div className="statDetails">
                                    {this.state.minimized
                                        ? null
                                        : this.state.status_effects[stat] >= 0
                                        ? `(${this.state.max_stats[stat]}+${this.state.status_effects[stat]})`
                                        : `(${this.state.max_stats[stat]}${this.state.status_effects[stat]})`}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
                {renderStatBreakdown()}
            </div>
        )
    }
}

export default withRouter(CharacterStatsCard)
