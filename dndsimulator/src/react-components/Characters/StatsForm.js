import "../../styles/CharacterAdd.css"

export default function StatsForm(props) {
    const handleFocus = (event) => event.target.select()
    return (
        <form
            className="character-form centered-flex column"
            action={`/api/${props.action}/`}
            target="dummyframe"
            method="post">
            <label htmlFor="charidstats">Character ID: </label>
            <input type="text" id="charidstats" name="characterid" />
            {/* <br /> */}
            <div
                className="hp-level-grid-row"
                style={{ display: props.extraRow ? "block" : "None" }}>
                <span className="gridplaceholder"></span>
                {/* <span> */}
                <label htmlFor="nHP">HP: </label>
                <input
                    className="inputboxSmall roundedbox inline"
                    type="number"
                    min={0}
                    defaultValue={0}
                    onFocus={handleFocus}
                    id="nHP"
                    name="HP"
                />

                <label htmlFor="nlevel">Level: </label>
                <input
                    className="inputboxSmall roundedbox inline"
                    type="number"
                    min={1}
                    defaultValue={1}
                    onFocus={handleFocus}
                    id="nlevel"
                    name="level"
                />

                <span className="gridplaceholder"></span>
            </div>

            <div className="stats-grid">
                {["STR", "DEX", "CON", "INT", "WIS", "CHA"].map((stat) => (
                    <span className="oneStat">
                        <label htmlFor={stat}>{stat}: </label>
                        <input
                            className="inputboxSmall inline"
                            type="number"
                            min={0}
                            defaultValue={0}
                            onFocus={handleFocus}
                            id={stat}
                            name={stat}
                        />
                    </span>
                ))}
            </div>

            <input className="submit-button" type="submit"></input>
        </form>
    )
}
