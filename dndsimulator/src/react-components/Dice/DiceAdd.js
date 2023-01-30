import "../../styles/DiceAdd.css"
import { useState } from "react"
function DiceAdd(props) {
    const [customDice, setCustomDice] = useState(false)
    function drag(ev, diceMax) {
        ev.dataTransfer.setData("diceMax", diceMax)
    }
    return (
        <div className="add-dice-module roundedbox">
            <button className="closeButton" onClick={() => props.show(false)}>
                x
            </button>
            <div className="add-dice-grid centered">
                <div className="column customDiceWrapper">
                    <span className="customDiceLabel">Custom</span>
                    <div className="d-something row">
                        d <input className="customDiceInput roundedbox" type="number" min="2" onInput={(e) => setCustomDice(e.target.value)} />
                    </div>

                    <button draggable={customDice > 0 ? true : false} onDragStart={(ev) => drag(ev, customDice)} className="addCustomDiceButton defaultButton">
                        Add Dice
                    </button>
                </div>
                {/*  */}
                {/* <div className="addDiceButtonColumn"> */}
                <div className="addDiceButtonGrid">
                    {[4, 6, 8, 10, 20, 100].map((val) => (
                        <button draggable="true" className="addDiceButton defaultButton" onDragStart={(ev) => drag(ev, val)}>
                            d{val}
                        </button>
                    ))}
                </div>
                {/* </div> */}
                {/*  */}
            </div>
        </div>
    )
}

export default DiceAdd
