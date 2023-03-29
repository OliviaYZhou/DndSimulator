import { useEffect, useState } from "react"
import StatsForm from "./StatsForm"
import "../../styles/PermanentEffectForm.css"

export default function InventoryForm(props) {
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
                    defaultValue={props.characterid}
                />
                <label htmlFor="item-name-id">Item Name:</label>
                <input
                    className=".default-inputbox centered-text"
                    type="text"
                    id="item-name-id"
                    name="item-name"
                />
                <div className="centered-flex">
                    <label htmlFor="amount-id">Amount: </label>
                    <input
                        className="inputboxSmall roundedbox inline"
                        type="number"
                        defaultValue={1}
                        onFocus={handleFocus}
                        id="amount-id"
                        name="amount"
                    />
                </div>

                <div className="centered-flex">
                    <input className="submit-button defaultButton strong-button" type="submit" />
                </div>
            </div>
        )
    }
    return (
        <div style={{ position: "relative" }}>
            <iframe name="dummyframe" id="dummyframe" style={{ display: "none" }}></iframe>
            <button className="closeButton" onClick={() => props.closeForm()}>
                x
            </button>
            <form
                className="character-form"
                action={`/api/add_inventory_item/`}
                target="dummyframe"
                method="post">
                {defaultForm()}
            </form>{" "}
        </div>
    )
}
