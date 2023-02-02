import "../styles/Session.css"
function Session(props) {
    return (
        <div className="session-block scrollable-y">
            <h3> Turn {props.currentTurn} </h3>
            <h3>Setting: Stronghold Outpost</h3>
            <h4>Name: IceBreaker</h4>
            <p>Description: </p>
            <p>In the outpost farms, tentacle guy and bb start to get to know each other.</p>
            <p>Here they meet previously unheard of Elven Farmers who are making a living, and dealing with their own issues around the stronghold</p>
            Details: {">"}
        </div>
    )
}

export default Session
