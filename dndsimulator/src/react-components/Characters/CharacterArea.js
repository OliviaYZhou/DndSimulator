import React, { useState, useEffect } from "react"
import CharacterWorkSpace from "./CharacterWorkSpace"
import "../../styles/CharacterArea.css"
// import DiceBoard from './DiceBoard';
import CharacterAdd from "./CharacterAdd"

function CharacterArea(props) {
    const [characterList, setCharacterList] = useState(["tentacle_guy", "orc_guy", "tester2"])
    const [showAddCharacterForm, setAddCharacterForm] = useState(false)
    useEffect(() => {
        fetch(`/api/get_all_characters`)
            .then((res) => res.json())
            .then((data) => setCharacterList(data.character_master_list))

        props.socket.on("master_character_changes", (data) => {
            console.log("master_character_changes", data)
            setCharacterList(data.master_character_list)
        })
    }, [])

    return (
        <div className="character-area">
            <img src="/assets/Art/DNDTK_revised_characterboard.png" id="characterAreaBG" />
            {/* <div className="padded "> */}
            <ul className="characterWSList scrollable-y">
                {characterList.map((character, index) => (
                    <li>
                        <CharacterWorkSpace
                            characterid={character}
                            socket={props.socket}
                            boardIndex={index}
                        />
                    </li>
                ))}
            </ul>
            {/* </div> */}
        </div>
    )
}

export default CharacterArea
