import React, {createRef} from 'react';
import {withRouter} from 'react-router-dom';
import socketIOClient from "socket.io-client"
import "../styles/Dice.css"

// let socket = socketIOClient("htref = React.createRef()
class Dice extends React.Component {
    constructor(props){
        super(props)
        this.state = {
            diceMax: this.props.properties[0],
            diceVal: this.props.properties[1],
            isRolling: this.props.properties[2],
            index: this.props.index,
            hei: 0,
        }
        this.ref = createRef()
        this.handleResize = this.handleResize.bind(this);
    }

    componentDidMount(){
        console.log(this.ref)
        window.addEventListener("resize", this.handleResize);
        this.setState({hei: this.ref.current.clientWidth})

    }
    handleResize(WindowSize, event) {
        this.setState({hei: this.ref.current.clientWidth})
    }
    
    getHeight(){

        if(this.state.hei !== 0){
            return `${this.state.hei}px`
        }
        else{
            return "50px"
        }
        
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
        this.props.socket.emit(`i_clicked_roll`, {index: this.state.index, maxRoll: this.state.diceMax, boardIndex: this.props.boardIndex})
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
            <div className='dice-card' draggable='true' 
                onDragStart={(ev)=>{
                    this.props.deleteDice(this.state.index)
                    this.props.drag(ev, this.state.diceMax)
                }}
                onClick={() => {
                    this.rolled_dice_handler()
                }}
                onContextMenu={(e)=>{
                    e.preventDefault()
                    this.props.deleteDice(this.state.index)
                }}
                >
        
                    <div className='dice-body' ref={this.ref} style={{backgroundColor: this.state.isRolling ?  "rgb(134, 125, 253)": "rgb(236, 239, 255)", height: this.getHeight()}}> 
                        <span className='dice-value'>{this.state.diceVal}</span>
                        
                    </div>
                    <div className='dice-type'> d{this.state.diceMax} </div>

                
                
            </div>
        );
        
    }
}
export default withRouter(Dice);