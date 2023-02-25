import { useEffect, useState } from "react"
import StatsForm from "./StatsForm"
import "../../styles/PermanentEffectForm.css"

export default function PermanentEffectForm() {
    const [effectType, setEffectType] = useState("HP")

    // useEffect(() => {
    //     if (effectType == "Stats") {
    //     }
    // }, [effectType])
    const handleFocus = (event) => event.target.select()

    function defaultForm() {
        return (
            <div className="centered-flex column ">
                <label htmlFor="charid">Character ID:</label>
                <input
                    className=".default-inputbox centered-text"
                    type="text"
                    id="charid"
                    name="characterid"
                />
                <div className="centered-flex">
                    <label htmlFor="change-amount-id">Amount: </label>
                    <input
                        className="inputboxSmall roundedbox inline"
                        type="number"
                        defaultValue={0}
                        onFocus={handleFocus}
                        id="change-amount-id"
                        name="effect-amount"
                    />
                </div>

                <div className="centered-flex">
                    <input className="submit-button defaultButton strong-button" type="submit" />
                </div>
            </div>
        )
    }
    function renderForm() {
        switch (effectType) {
            case "Stats":
                return <StatsForm action="add_permanent_stats" />
            default:
                return defaultForm()
        }
    }
    return (
        <div>
            <iframe name="dummyframe" id="dummyframe" style={{ display: "none" }}></iframe>
            <form
                className="character-form"
                action={`/api/add_permanent_effect/`}
                target="dummyframe"
                method="post">
                <label htmlFor="effect-type">Change value of:</label>
                <select
                    className=".default-inputbox"
                    type="text"
                    id="effect-type"
                    name="effect-type"
                    onChange={(e) => setEffectType(e.target.value)}>
                    <option value="HP">HP</option>
                    <option value="Gold">Gold</option>
                    <option value="Exp">Exp</option>
                    <option value="Level">Level</option>
                    <option value="Stats">Stats</option>
                </select>
                {renderForm()}
            </form>
        </div>
    )
}
