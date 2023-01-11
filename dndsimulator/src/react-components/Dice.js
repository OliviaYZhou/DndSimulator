import React from 'react';
import {withRouter} from 'react-router-dom';
import socketIOClient from "socket.io-client"
import "../styles/Dice.css"

// let socket = socketIOClient("http://localhost:5000/");
class Dice extends React.Component {

    state = {
        diceMax: this.props.properties[0],
        diceVal: this.props.properties[1],
        isRolling: this.props.properties[2],
        index: this.props.index
    }

    static getDerivedStateFromProps(props, state){
        if (props.properties[1] != state.diceVal){
            return{diceVal: props.properties[1]}
        }
        if (props.properties[2] != state.isRolling){

            return{isRolling: props.properties[2]}
        }
        return null
    }

    rolled_dice_handler(){
        console.log("left click")
        this.props.socket.emit("i_clicked_roll", {index: this.state.index, maxRoll: this.state.diceMax})
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
                    this.rolled_dice_handler()
                }}
                onContextMenu={(e)=>{
                    e.preventDefault()
                    this.props.deleteDice(this.state.index)
                }}
                >
        
                    <div className='dice-body' style={{backgroundColor: this.state.isRolling ?  "rgb(134, 125, 253)": "rgb(236, 239, 255)"}}> 
                        <span className='dice-value'>{this.state.diceVal}</span>
                        
                    </div>
                    <div className='dice-type'> d{this.state.diceMax} </div>

                
                
            </div>
        );
        
    }
}
export default withRouter(Dice);