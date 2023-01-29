import React, { useState, useEffect } from 'react';
import CharacterWorkSpace from './CharacterWorkSpace';
import "../../styles/CharacterArea.css"
// import DiceBoard from './DiceBoard';
import CharacterAdd from './CharacterAdd';


function CharacterArea(props) {
  const [characterList, setCharacterList] = useState(["tentacle_guy", "orc_guy", "tester2"]);
  const [showAddCharacterForm, setAddCharacterForm] = useState(false)
  useEffect(() => {

    fetch(`/api/get_all_characters`).then(res =>res.json())
      .then((data) => setCharacterList(data.character_master_list))

    props.socket.on("master_character_changes", data=> {
      console.log("master_character_changes", data)
      setCharacterList(data.master_character_list)})
  }, [])
  

  function renderAddCharacterForm () {
    if (showAddCharacterForm){
      return (
        <div className='addCharacterFormWrapper'>
          <button className='closeButton' onClick={()=>setAddCharacterForm(false)}> x</button>
          <CharacterAdd/>
        </div>
        
        // <div>
        //   <button className='closeButton' onClick={()=>setAddCharacterForm(false)}> x</button>
        //   <form>
        //     <label for="name">First name:</label>
        //     <input type="text" id="charName" name="name"/><br/>
        //     <label for="charid">Character ID:</label>
        //     <input type="text" id="charid" name="charid"/><br/>
        //     <label for="chartype">Character Type:</label>
        //     <input type="text" id="chartype" name="chartype"/><br/>
        //     <input type="submit"></input>
        //   </form>
        // </div>
      )
    }
    else{
      return <button onClick={()=>{setAddCharacterForm(true)}}>Show Add Character Forms</button>
    }
  }
  return  (
  <div className='character-area'>
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