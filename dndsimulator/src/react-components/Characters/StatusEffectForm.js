import React, { Fragment, useRef } from "react"
import { uid } from "react-uid"
import { withRouter } from "react-router-dom"
import "../../styles/DiceBoard.css"
import "../../styles/StatusEffectForm.css"

class StatusEffectForm extends React.Component {
    state = {
        characterid: "",
        inputName: "",
        inputStats: { HP: 0, STR: 0, DEX: 0, CON: 0, INT: 0, WIS: 0, CHA: 0 },
        inputDuration: 1,
        inputDescription: "",
    }
    componentDidMount() {
        if (this.props.characterid) {
            this.setState({ characterid: this.props.characterid })
        }
    }

    handleInputChange(event, fieldName) {
        const target = event.target
        const value = target.value

        this.setState({ [fieldName]: value })
    }
    handleInputChange(event, fieldName) {
        const target = event.target
        const value = target.value

        this.setState({ [fieldName]: value })
    }
    handleStatChange(event, stat) {
        const target = event.target
        const value = target.value

        var statCopy = this.state.inputStats
        statCopy[stat] = value
        this.setState({ inputStats: statCopy })
    }
    submitStatus() {
        if (this.state.inputName == "") {
            alert("Add Effect Name")
            return
        }
        var statusEffectJson = {
            characterid: this.state.characterid,
            name: this.state.inputName,
            stats: this.state.inputStats,
            duration: this.state.inputDuration,
            description: this.state.inputDescription,
        }
        // this.props.socket.emit(`/status_effect/`, statusEffectJson)

        fetch(`/api/status_effect/`, {
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
            },
            method: "POST",
            body: JSON.stringify(statusEffectJson),
            credentials: "include",
        })
        // this.props.closeStatusForm()
        // send server call
    }
    render() {
        return (
            <div className="status-effect-form column">
                <div className="titleHeader"> Add Status Effect</div>
                <button
                    className="closeButton"
                    onClick={() => this.props.closeStatusForm()}
                    style={{ display: this.props.closeStatusForm ? "inline-block" : "none" }}>
                    {" "}
                    x
                </button>
                <div className="">
                    <div>
                        character id ={" "}
                        <i>
                            <input
                                className="inputboxMedium roundedbox"
                                type="text"
                                onChange={(e) => this.handleInputChange(e, "characterid")}
                                defaultValue={this.props.characterid}
                            />
                        </i>
                    </div>
                    <div>
                        Status Effect Name:{" "}
                        <input
                            className="inputboxMedium roundedbox"
                            type="text"
                            onChange={(e) => this.handleInputChange(e, "inputName")}
                        />
                    </div>
                    <div>
                        <b>Effected Stats</b>
                    </div>
                    {["HP", "STR", "DEX", "CON", "INT", "WIS", "CHA"].map((stat) => (
                        <span>
                            {stat}:{" "}
                            <input
                                className="inputboxSmall roundedbox inline"
                                type="number"
                                defaultValue={0}
                                onChange={(e) => this.handleStatChange(e, stat)}
                            />
                        </span>
                    ))}
                    <div>
                        Effect Duration:{" "}
                        <input
                            className="inputboxSmall roundedbox"
                            type="number"
                            min="1"
                            onChange={(e) => this.handleInputChange(e, "inputDuration")}
                        />
                    </div>
                    <div>
                        Description:{" "}
                        <textarea
                            rows={2}
                            id={"growable"}
                            onChange={(e) => {
                                this.handleInputChange(e, "inputDescription")
                            }}
                            value={this.state.inputDescription}
                        />
                    </div>
                    <button className="submitStatusButton" onClick={() => this.submitStatus()}>
                        Submit
                    </button>
                </div>
            </div>
        )
    }
}
export default withRouter(StatusEffectForm)
