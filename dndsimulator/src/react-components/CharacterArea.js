import React, { useState } from 'react';
import CharacterWorkSpace from './CharacterWorkSpace';
import "../styles/CharacterArea.css"
import DiceBoard from './DiceBoard';

function CharacterArea(props) {
  const [characterList, setCharacterList] = useState(["tentacle_guy", "orc_guy", "tester2"]);
  const [showAddCharacterForm, setAddCharacterForm] = useState(false)
  function renderAddCharacterForm () {
    if (showAddCharacterForm){
      return (
        <div>
          <button className='closeButton' onClick={()=>setAddCharacterForm(false)}> x</button>
          <form>
            <label for="name">First name:</label>
            <input type="text" id="charName" name="name"/><br/>
            <label for="charid">Character ID:</label>
            <input type="text" id="charid" name="charid"/><br/>
            <label for="chartype">Character Type:</label>
            <input type="text" id="chartype" name="chartype"/><br/>
            <input type="submit"></input>
          </form>
        </div>
      )
    }
    else{
      return <button onClick={()=>{setAddCharacterForm(true)}}>Add Character</button>
    }
  }
  return  (
  <div>
      <ul className='characterWSList'>
        {characterList.map((character, index) => (
          <li>
              <CharacterWorkSpace characterid={character} socket={props.socket} boardIndex={index}/>

          </li>
        ))}
      </ul>
      
      {renderAddCharacterForm()}

      
  </div>)
}

export default CharacterArea;