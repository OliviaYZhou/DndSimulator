import React, {Fragment} from 'react';
import {withRouter} from 'react-router-dom';
import "../style/Dice.css"
class Dice extends React.Component {

    state = {
        diceMax: this.props,
        diceVal: `d${this.props}`
    }

    componentDidMount() {}

    rolling(){
        this.setState({
            diceVal: Math.floor(Math.random() * diceMax) + 1
        })
    }

    rollDice() {
        var times = 0
        var interval = setInterval(() => 
            {
                this.rolling()
                if (++times == 10){
                    clearInterval(interval)
                }
            }
            , 100);

    }
    render() {
        <div className='dice-card' 
        onClick={() => {
            this.rollDice()
        }}>
            <div className='dice-body'> 
                <h4>{this.state.diceVal}</h4> 
            </div>
            <div className='dice-type'> d{this.state.diceMax} </div>
        </div>
    }
}
export default withRouter(Dice);