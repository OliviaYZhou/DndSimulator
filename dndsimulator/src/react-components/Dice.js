import React from 'react';
import {withRouter} from 'react-router-dom';
import "../styles/Dice.css"
class Dice extends React.Component {

    state = {
        diceMax: this.props.val,
        diceVal: `d${this.props.val}`
    }

    

    rolling() {
        var ranVar = Math.floor(Math.random() * this.state.diceMax) + 1
        this.setState({
            diceVal:ranVar
        })
        return ranVar
    }

    rollDice() {
        var times = 0
        var interval = setInterval(() => 
            {
                this.rolling()
                if (++times == 10){
                    clearInterval(interval)
                    var finalVal = this.rolling()
                    this.props.addHistory(this.state.diceMax, finalVal)
                }
            }
            , 100);
    }
    
    render() {
        return(
            <div className='dice-card hoverable' 
                onClick={() => {
                    this.rollDice()
                }}>
        
                    <div className='dice-body'> 
                        <span className='dice-value'>{this.state.diceVal}</span>
                        
                    </div>
                    <div className='dice-type'> d{this.state.diceMax} </div>

                
                
            </div>
        );
        
    }
}
export default withRouter(Dice);