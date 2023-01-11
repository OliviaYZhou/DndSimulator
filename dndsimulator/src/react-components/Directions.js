import React from 'react';
import "../styles/Directions.css"
class Directions extends React.Component {
    render() {
        return(
            <div id='directionsBlock'>
                <h2>Directions</h2>
                <ul className='directions-list'>
                    <li>Click button in red bar to add dice</li>
                    <li>Click dice to roll</li>
                    <li>Right click dice to delete</li>
                    <li>Right click "Dice" header to clear all dice</li>
                    <li>Right click "History" header to clear all history</li>
                    
                </ul>
            </div>
        )
    }
}

export default Directions