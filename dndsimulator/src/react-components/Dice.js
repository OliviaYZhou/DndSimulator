import React from 'react';
import {withRouter} from 'react-router-dom';
import "../styles/Dice.css"
class Dice extends React.Component {

    state = {
        diceMax: this.props.properties[0],
        diceVal: this.props.properties[1],
        originalprops: this.props.properties[1]
    }

    static getDerivedStateFromProps(props, state){
        if (props.originalprops != state.originalprops){
            return{diceVal: props.properties[1], originalprops: props.originalprops}
        }
        return null
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
                    var finalVal = Math.floor(Math.random() * this.state.diceMax) + 1
                    this.props.updateDice(this.props.index, finalVal, this.state.diceMax)
                    // this.props.addHistory(this.state.diceMax, finalVal)
                }
            }
            , 100);
    }

    // rollAll(){
    //     var times = 0
    //     var interval = setInterval(() => 
    //         {
    //             this.rolling()
    //             if (++times == 10){
    //                 clearInterval(interval)
    //                 var finalVal = this.rolling()
    //                 this.props.addHistory(this.state.diceMax, finalVal)
    //             }
    //         }
    //         , 100);
    // }
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